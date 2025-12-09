from django.shortcuts import render, get_list_or_404, get_object_or_404  # type: ignore
from django.http import HttpResponse, HttpResponseRedirect # pyright: ignore[reportMissingModuleSource]
from django.http import Http404 # type: ignore
from django.db.models import F  # type: ignore
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView # type: ignore
from django.forms import inlineformset_factory
from .models import Question, Choice


# For creating new questions - shows 4 empty choice fields
ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    fields=['choice_text'],
    extra=4,
    can_delete=False,
)


ChoiceUpdateFormSet = inlineformset_factory(
    Question,
    Choice,
    fields=['choice_text'],
    extra=4,
    max_num=4,
    can_delete=False,
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
        return self.model.objects.order_by("-pub_date")


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
        return HttpResponseRedirect(reverse("polls:index"))


class QuestionCreateView(CreateView):
    model = Question
    fields = ['question_text']  # Which fields to show in the form
    template_name = "polls/create_question.html"
    success_url = reverse_lazy('polls:index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['choice_formset'] = ChoiceFormSet(self.request.POST)
        else:
            context['choice_formset'] = ChoiceFormSet()
        return context
    
    def form_valid(self, form):
        # Set publish date and save the question
        form.instance.pub_date = timezone.now()
        self.object = form.save()
        
        # Save the choices linked to this question
        choice_formset = ChoiceFormSet(self.request.POST, instance=self.object)
        choice_formset.save()
        
        return HttpResponseRedirect(self.success_url)
    
class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['question_text']
    template_name = "polls/update_question.html"
    success_url = reverse_lazy('polls:index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            context['choice_formset'] = ChoiceUpdateFormSet(self.request.POST, instance=self.object)
        else:
            context['choice_formset'] = ChoiceUpdateFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            
            choice_formset = ChoiceUpdateFormSet(self.request.POST, instance=self.object)
            if choice_formset.is_valid():
                for choice_form in choice_formset:
                    choice_text = choice_form.cleaned_data.get('choice_text')
                    if not choice_text:
                        continue
                    
                    choice = choice_form.save(commit=False)
                    choice.question = self.object
                    # Reset votes to 0 only for new choices or if choice text changed
                    if not choice.pk or 'choice_text' in choice_form.changed_data:
                        choice.votes = 0
                    choice.save()
        
        return HttpResponseRedirect(self.success_url)
    
class QuestionDeleteView(DeleteView):
    model = Question
    template_name = "polls/confirm_delete_question.html"
    success_url = reverse_lazy('polls:index')
