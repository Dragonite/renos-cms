from rest_framework import serializers
from .models import (
    TestingAccountEnvironment, TestingAccount,
    SyntheticEventTarget, SyntheticEventType, SyntheticEvent
)


class TestingAccountEnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestingAccountEnvironment
        fields = ['id', 'name']


class TestingAccountSerializer(serializers.ModelSerializer):
    environment = TestingAccountEnvironmentSerializer(read_only=True)
    
    class Meta:
        model = TestingAccount
        fields = ['id', 'label', 'description', 'username', 'password', 'environment', 'is_active']


class TestingAccountEnvironmentWithAccountsSerializer(serializers.ModelSerializer):
    testing_accounts = TestingAccountSerializer(many=True, read_only=True)
    
    class Meta:
        model = TestingAccountEnvironment
        fields = ['id', 'name', 'testing_accounts']


class SyntheticEventTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyntheticEventTarget
        fields = ['id', 'name']


class SyntheticEventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyntheticEventType
        fields = ['id', 'name', 'description']


class SyntheticEventSerializer(serializers.ModelSerializer):
    target = SyntheticEventTargetSerializer(read_only=True)
    event_type = SyntheticEventTypeSerializer(read_only=True)
    
    class Meta:
        model = SyntheticEvent
        fields = ['id', 'name', 'description', 'target', 'event_type']