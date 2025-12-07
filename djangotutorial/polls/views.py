from django.shortcuts import render, get_list_or_404, get_object_or_404  # type: ignore
from django.http import HttpResponse, HttpResponseRedirect # pyright: ignore[reportMissingModuleSource]
from django.http import Http404 # type: ignore
from django.db.models import F  # type: ignore
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView  # type: ignore
from django.forms import inlineformset_factory
from .models import Question, Choice


# Creates 4 choice input fields linked to a Question
ChoiceFormSet = inlineformset_factory(
    Question,          # Parent model
    Choice,            # Child model  
    fields=['choice_text'],  # Which field to show
    extra=4,           # Show 4 empty forms
)


# def index(request):
#     latest_question_list = get_list_or_404(
#         Question.objects.order_by("pub_date")[:5]
#     )
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)

class IndexView(ListView):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        return self.model.objects.order_by("-pub_date")[:5]


# def detail(request, question_id):
#     # return HttpResponse(f"You're looking at question {question_id}.")
#     question = get_object_or_404(Question, pk=question_id)
#     context = {
#         "question" : question,
#     }
#     return render(request, "polls/details.html", context)

class DetailView(DetailView):
    model = Question
    template_name = "polls/details.html"
    context_object_name = "question"

# def results(request, question_id):
#     # return HttpResponse(f"You're looking at the result of question {question_id}.")
#     ques = get_object_or_404(Question, pk=question_id)
#     context = {
#         "question" : ques,
#     }
#     return render(request, "polls/results.html", context)

class ResultsView(DetailView):
    model = Question
    template_name = "polls/results.html"
    context_object_name = "question"


def vote(request, question_id):
    # return HttpResponse(f"You're voting on question {question_id}.")
    ques = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = ques.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/details.html",
            {
                "question": ques,
                "error_message": "You didn't select a choice."
            }
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(ques.id,)))

def hello(request):
    return HttpResponse("Welcome to POLL app!<br>")


class QuestionCreateView(CreateView):
    model = Question
    fields = ['question_text']  # Which fields to show in the form
    template_name = "polls/create_question.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['choice_formset'] = ChoiceFormSet(self.request.POST)
        else:
            context['choice_formset'] = ChoiceFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        choice_formset = context['choice_formset']
        
        if choice_formset.is_valid():
            # Save the question first
            form.instance.pub_date = timezone.now()
            self.object = form.save()
            
            # Now save the choices with the question reference
            choice_formset.instance = self.object
            choice_formset.save()
            
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return self.render_to_response(self.get_context_data(form=form))
