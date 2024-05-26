from django.urls import path
from . import views


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page_view'),
    path('debug/', trigger_error),
]
