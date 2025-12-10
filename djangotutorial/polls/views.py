from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import F
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.forms import inlineformset_factory
from django import forms
from .models import Question, Choice


# Custom widget attrs for styling inputs
input_attrs = {
    'class': 'w-full p-2 border-2 border-[#c04515] rounded text-base bg-white'
}


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        widgets = {
            'question_text': forms.TextInput(attrs=input_attrs)
        }

ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    fields=['choice_text'],
    extra=4,
    can_delete=False,
    widgets={'choice_text': forms.TextInput(attrs=input_attrs)}
)

ChoiceUpdateFormSet = inlineformset_factory(
    Question,
    Choice,
    fields=['choice_text'],
    extra=4,
    max_num=4,
    can_delete=False,
    widgets={'choice_text': forms.TextInput(attrs=input_attrs)}
)


class IndexView(ListView):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        return self.model.objects.order_by("-pub_date")


class DetailView(DetailView):
    model = Question
    template_name = "polls/details.html"
    context_object_name = "question"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/details.html", {
            "question": question,
            "error_message": "You didn't select a choice."
        })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:index"))


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
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
        form.instance.pub_date = timezone.now()
        self.object = form.save()
        
        choice_formset = ChoiceFormSet(self.request.POST, instance=self.object)
        choice_formset.save()
        
        return HttpResponseRedirect(self.success_url)


class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
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
                    if 'choice_text' in choice_form.changed_data:
                        choice.votes = 0
                    choice.save()
        
        return HttpResponseRedirect(self.success_url)


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = "polls/confirm_delete_question.html"
    success_url = reverse_lazy('polls:index')
