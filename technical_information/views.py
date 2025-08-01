from rest_framework import generics
from .models import TestingAccount
from .serializers import TestingAccountSerializer


class ActiveTestingAccountsListView(generics.ListAPIView):
    queryset = TestingAccount.objects.filter(is_active=True).select_related('environment')
    serializer_class = TestingAccountSerializer
