from django.views.generic import ListView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import LogbookEntry, Goal

class LogbookListView(LoginRequiredMixin, ListView):
    model = LogbookEntry
    template_name = 'logbook/logbook_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return LogbookEntry.objects.filter(user=self.request.user)

class LogbookCreateView(LoginRequiredMixin, CreateView):
    model = LogbookEntry
    template_name = 'logbook/logbook_form.html'
    fields = ['date', 'goals', 'time_registration', 'tasks_completed', 'problems_challenges', 'solutions_learnings', 'feedback_reflection', 'todo_next']
    success_url = reverse_lazy('logbook_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'logbook/login.html'
    success_url = reverse_lazy('logbook_summary')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'logbook/register.html'
    success_url = reverse_lazy('login')

class LogbookSummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'logbook/summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show_completed = self.request.GET.get('completed') == 'on'
        show_uncompleted = self.request.GET.get('uncompleted') == 'on'

        goals_dict = {}
        for term in ['long', 'mid', 'short']:
            goals = Goal.objects.filter(user=self.request.user, term=term)
            if show_completed and not show_uncompleted:
                goals = goals.filter(completed=True)
            elif show_uncompleted and not show_completed:
                goals = goals.filter(completed=False)
            elif not show_completed and not show_uncompleted:
                goals = goals.none()
            goals_dict[term] = goals

        context['goals_dict'] = goals_dict
        context['show_completed'] = show_completed
        context['show_uncompleted'] = show_uncompleted
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string('logbook/goals_container.html', context, request=request)
            return HttpResponse(html)
        return super().get(request, *args, **kwargs)

class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    template_name = 'logbook/goal_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user, term=self.kwargs['term'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['term'] = self.kwargs['term']
        context['active_term'] = self.kwargs['term']
        if self.kwargs['term'] == 'short':
            context['logbook_form'] = LogbookCreateView.as_view()(self.request).context_data['form']
            context['logbook_entries'] = LogbookEntry.objects.filter(user=self.request.user).order_by('-date')[:5]
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs['term'] == 'short':
            form = LogbookCreateView.as_view()(request).form
            if form.is_valid():
                logbook_entry = form.save(commit=False)
                logbook_entry.user = request.user
                logbook_entry.save()
                return self.get(request, *args, **kwargs)
        return self.get(request, *args, **kwargs)

class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    template_name = 'logbook/goal_form.html'
    fields = ['description']
    
    def get_success_url(self):
        return reverse_lazy('goal_list', kwargs={'term': self.kwargs['term']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.term = self.kwargs['term']
        return super().form_valid(form)

def toggle_goal_completion(request, goal_id):
    goal = Goal.objects.get(id=goal_id, user=request.user)
    goal.completed = not goal.completed
    goal.save()
    return redirect('goal_list', term=goal.term)

def goal_list(request, term):
    goals = Goal.objects.filter(user=request.user, term=term)
    long_term_goals = Goal.objects.filter(user=request.user, term='long')
    mid_term_goals = Goal.objects.filter(user=request.user, term='mid')
    short_term_goals = Goal.objects.filter(user=request.user, term='short')
    context = {
        'goals': goals,
        'long_term_goals': long_term_goals,
        'mid_term_goals': mid_term_goals,
        'short_term_goals': short_term_goals,
        'term': term,
        'active_term': term,
    }
    return render(request, 'logbook/goal_list.html', context)
