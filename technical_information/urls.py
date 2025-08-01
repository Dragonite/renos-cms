from django.urls import path
from .views import ActiveTestingAccountsListView

urlpatterns = [
    path('', ActiveTestingAccountsListView.as_view(), name='active-testing-accounts'),
]