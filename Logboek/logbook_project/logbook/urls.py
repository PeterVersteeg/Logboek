from django.urls import path
from .views import (
    LogbookListView, LogbookCreateView, UserLoginView, UserLogoutView, 
    UserRegisterView, LogbookSummaryView, GoalListView, GoalCreateView, 
    toggle_goal_completion
)

urlpatterns = [
    path('', LogbookSummaryView.as_view(), name='logbook_summary'),
    path('entries/', LogbookListView.as_view(), name='logbook_list'),
    path('entries/new/', LogbookCreateView.as_view(), name='logbook_create'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('goals/<str:term>/', GoalListView.as_view(), name='goal_list'),
    path('goals/<str:term>/new/', GoalCreateView.as_view(), name='goal_create'),
    path('goals/toggle/<int:goal_id>/', toggle_goal_completion, name='toggle_goal_completion'),
]