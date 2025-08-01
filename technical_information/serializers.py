from rest_framework import serializers
from .models import TestingAccountEnvironment, TestingAccount


class TestingAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestingAccount
        fields = ['id', 'label', 'description', 'username', 'password', 'environment', 'is_active']


class TestingAccountEnvironmentSerializer(serializers.ModelSerializer):
    testing_accounts = TestingAccountSerializer(many=True, read_only=True)
    
    class Meta:
        model = TestingAccountEnvironment
        fields = ['id', 'name', 'testing_accounts']