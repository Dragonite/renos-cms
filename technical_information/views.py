from rest_framework import generics
from .models import TestingAccount, SyntheticEvent
from .serializers import TestingAccountSerializer, SyntheticEventSerializer


class ActiveTestingAccountsListView(generics.ListAPIView):
    queryset = TestingAccount.objects.filter(is_active=True).select_related('environment')
    serializer_class = TestingAccountSerializer


class SyntheticEventsListView(generics.ListAPIView):
    queryset = SyntheticEvent.objects.select_related('event_type', 'target').all()
    serializer_class = SyntheticEventSerializer
