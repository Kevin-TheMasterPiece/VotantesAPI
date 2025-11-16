from django.urls import path
from .views import DashboardStatsView, PredictVoteView, VotanteListView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('predict/', PredictVoteView.as_view(), name='predict-vote'),
    path("dashboard/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("listavotantes/", VotanteListView.as_view(), name="votante-list"),
    path('login/', obtain_auth_token, name='api_token_auth'),
]
