
from django.urls import path
from .views import TodayMenuView, VoteCreateView, TodayMenuResultsView

urlpatterns = [
    path('menu/today/', TodayMenuView.as_view(), name='today_menu'),
    path('vote/', VoteCreateView.as_view(), name='vote-create'),
    path('results/', TodayMenuResultsView.as_view(), name='today-menu-results'),
]
