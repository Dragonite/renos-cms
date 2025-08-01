from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import (
    TestingAccountEnvironment, TestingAccount,
    SyntheticEventTarget, SyntheticEventType, SyntheticEvent
)
from .serializers import (
    TestingAccountSerializer, TestingAccountEnvironmentSerializer, TestingAccountEnvironmentWithAccountsSerializer,
    SyntheticEventTargetSerializer, SyntheticEventTypeSerializer, SyntheticEventSerializer
)


class TestingAccountEnvironmentModelTest(TestCase):
    def setUp(self):
        self.environment = TestingAccountEnvironment.objects.create(name="Development")

    def test_environment_str_method(self):
        self.assertEqual(str(self.environment), "Development")

    def test_environment_verbose_name_plural(self):
        self.assertEqual(
            TestingAccountEnvironment._meta.verbose_name_plural,
            "Testing Account Environments"
        )


class TestingAccountModelTest(TestCase):
    def setUp(self):
        self.environment = TestingAccountEnvironment.objects.create(name="Staging")
        self.account = TestingAccount.objects.create(
            label="Test Account 1",
            description="A test account for staging",
            username="testuser1",
            password="testpass123",
            environment=self.environment,
            is_active=True
        )

    def test_account_str_method(self):
        expected = "Test Account 1 (Staging)"
        self.assertEqual(str(self.account), expected)

    def test_account_default_is_active(self):
        account = TestingAccount.objects.create(
            label="Test Account 2",
            description="Another test account",
            username="testuser2",
            password="testpass456",
            environment=self.environment
        )
        self.assertTrue(account.is_active)

    def test_account_verbose_name_plural(self):
        self.assertEqual(
            TestingAccount._meta.verbose_name_plural,
            "Testing Accounts"
        )

    def test_environment_relationship(self):
        self.assertEqual(self.account.environment, self.environment)
        self.assertIn(self.account, self.environment.testing_accounts.all())


class TestingAccountSerializerTest(TestCase):
    def setUp(self):
        self.environment = TestingAccountEnvironment.objects.create(name="Production")
        self.account = TestingAccount.objects.create(
            label="Prod Account",
            description="Production test account",
            username="produser",
            password="prodpass123",
            environment=self.environment,
            is_active=True
        )

    def test_testing_account_serializer_fields(self):
        serializer = TestingAccountSerializer(instance=self.account)
        data = serializer.data
        
        self.assertEqual(data['label'], 'Prod Account')
        self.assertEqual(data['description'], 'Production test account')
        self.assertEqual(data['username'], 'produser')
        self.assertEqual(data['password'], 'prodpass123')
        self.assertEqual(data['environment']['id'], self.environment.id)
        self.assertEqual(data['environment']['name'], self.environment.name)
        self.assertTrue(data['is_active'])
        self.assertIn('id', data)

    def test_testing_account_serializer_validation(self):
        valid_data = {
            'label': 'Valid Account',
            'description': 'Valid description',
            'username': 'validuser',
            'password': 'validpass',
            'environment': self.environment.id,
            'is_active': True
        }
        serializer = TestingAccountSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_testing_account_serializer_missing_required_fields(self):
        incomplete_data = {
            'label': 'Incomplete Account'
        }
        serializer = TestingAccountSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)
        self.assertIn('username', serializer.errors)
        self.assertIn('password', serializer.errors)
        # Note: environment is read_only in the serializer, so it won't be in errors


class TestingAccountEnvironmentSerializerTest(TestCase):
    def setUp(self):
        self.environment = TestingAccountEnvironment.objects.create(name="QA Environment")
        
        self.account1 = TestingAccount.objects.create(
            label='QA Account 1',
            description='First QA account',
            username='qa1',
            password='qa1pass',
            environment=self.environment,
            is_active=True
        )
        
        self.account2 = TestingAccount.objects.create(
            label='QA Account 2',
            description='Second QA account',
            username='qa2',
            password='qa2pass',
            environment=self.environment,
            is_active=False
        )

    def test_environment_serializer_fields(self):
        serializer = TestingAccountEnvironmentWithAccountsSerializer(instance=self.environment)
        data = serializer.data
        
        self.assertEqual(data['name'], 'QA Environment')
        self.assertIn('id', data)
        self.assertIn('testing_accounts', data)
        self.assertEqual(len(data['testing_accounts']), 2)

    def test_environment_serializer_nested_accounts(self):
        serializer = TestingAccountEnvironmentWithAccountsSerializer(instance=self.environment)
        data = serializer.data
        
        accounts_data = data['testing_accounts']
        account_labels = [account['label'] for account in accounts_data]
        
        self.assertIn('QA Account 1', account_labels)
        self.assertIn('QA Account 2', account_labels)
        
        for account in accounts_data:
            self.assertIn('id', account)
            self.assertIn('label', account)
            self.assertIn('description', account)
            self.assertIn('username', account)
            self.assertIn('password', account)
            self.assertIn('environment', account)
            self.assertIn('is_active', account)

    def test_environment_serializer_validation(self):
        valid_data = {
            'name': 'Valid Environment'
        }
        serializer = TestingAccountEnvironmentWithAccountsSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_environment_serializer_missing_name(self):
        invalid_data = {}
        serializer = TestingAccountEnvironmentWithAccountsSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_environment_empty_accounts(self):
        empty_environment = TestingAccountEnvironment.objects.create(name="Empty Environment")
        serializer = TestingAccountEnvironmentWithAccountsSerializer(instance=empty_environment)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Empty Environment')
        self.assertEqual(len(data['testing_accounts']), 0)
        self.assertEqual(data['testing_accounts'], [])


class ActiveTestingAccountsAPITest(APITestCase):
    def setUp(self):
        self.env1 = TestingAccountEnvironment.objects.create(name="Development")
        self.env2 = TestingAccountEnvironment.objects.create(name="Staging")
        
        # Active accounts
        self.active_account1 = TestingAccount.objects.create(
            label='Active Dev Account',
            description='Active development account',
            username='devuser',
            password='devpass123',
            environment=self.env1,
            is_active=True
        )
        
        self.active_account2 = TestingAccount.objects.create(
            label='Active Staging Account',
            description='Active staging account',
            username='stageuser',
            password='stagepass123',
            environment=self.env2,
            is_active=True
        )
        
        # Inactive account (should not appear in API)
        self.inactive_account = TestingAccount.objects.create(
            label='Inactive Account',
            description='Inactive account',
            username='inactiveuser',
            password='inactive123',
            environment=self.env1,
            is_active=False
        )

    def test_active_testing_accounts_api_endpoint(self):
        url = reverse('active-testing-accounts')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_active_testing_accounts_api_filters_active_only(self):
        url = reverse('active-testing-accounts')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        account_labels = [account['label'] for account in response.data]
        self.assertIn('Active Dev Account', account_labels)
        self.assertIn('Active Staging Account', account_labels)
        self.assertNotIn('Inactive Account', account_labels)

    def test_active_testing_accounts_api_response_structure(self):
        url = reverse('active-testing-accounts')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for account in response.data:
            self.assertIn('id', account)
            self.assertIn('label', account)
            self.assertIn('description', account)
            self.assertIn('username', account)
            self.assertIn('password', account)
            self.assertIn('environment', account)
            self.assertIn('is_active', account)
            self.assertTrue(account['is_active'])

    def test_active_testing_accounts_api_includes_environment_data(self):
        url = reverse('active-testing-accounts')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        environment_ids = [account['environment']['id'] for account in response.data]
        self.assertIn(self.env1.id, environment_ids)
        self.assertIn(self.env2.id, environment_ids)

    def test_active_testing_accounts_api_empty_when_no_active_accounts(self):
        # Deactivate all accounts
        TestingAccount.objects.all().update(is_active=False)
        
        url = reverse('active-testing-accounts')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])


class SyntheticEventTargetModelTest(TestCase):
    def setUp(self):
        self.target = SyntheticEventTarget.objects.create(name="API Endpoint")

    def test_target_str_method(self):
        self.assertEqual(str(self.target), "API Endpoint")

    def test_target_verbose_name_plural(self):
        self.assertEqual(
            SyntheticEventTarget._meta.verbose_name_plural,
            "Synthetic Event Targets"
        )


class SyntheticEventTypeModelTest(TestCase):
    def setUp(self):
        self.event_type = SyntheticEventType.objects.create(
            name="Performance Test",
            description="Tests for performance monitoring"
        )

    def test_event_type_str_method(self):
        self.assertEqual(str(self.event_type), "Performance Test")

    def test_event_type_verbose_name_plural(self):
        self.assertEqual(
            SyntheticEventType._meta.verbose_name_plural,
            "Synthetic Event Types"
        )


class SyntheticEventModelTest(TestCase):
    def setUp(self):
        self.target = SyntheticEventTarget.objects.create(name="Login Page")
        self.event_type = SyntheticEventType.objects.create(
            name="Functional Test",
            description="Tests for functional verification"
        )
        self.event = SyntheticEvent.objects.create(
            name="Login Validation Test",
            description="Test to validate login functionality",
            target=self.target,
            event_type=self.event_type
        )

    def test_event_str_method(self):
        expected = "Login Validation Test (Functional Test)"
        self.assertEqual(str(self.event), expected)

    def test_event_verbose_name_plural(self):
        self.assertEqual(
            SyntheticEvent._meta.verbose_name_plural,
            "Synthetic Events"
        )

    def test_event_target_relationship(self):
        self.assertEqual(self.event.target, self.target)
        self.assertIn(self.event, self.target.synthetic_events.all())

    def test_event_type_relationship(self):
        self.assertEqual(self.event.event_type, self.event_type)
        self.assertIn(self.event, self.event_type.synthetic_events.all())


class SyntheticEventTargetSerializerTest(TestCase):
    def setUp(self):
        self.target = SyntheticEventTarget.objects.create(name="User Dashboard")

    def test_target_serializer_fields(self):
        serializer = SyntheticEventTargetSerializer(instance=self.target)
        data = serializer.data
        
        self.assertEqual(data['name'], 'User Dashboard')
        self.assertIn('id', data)

    def test_target_serializer_validation(self):
        valid_data = {
            'name': 'Valid Target'
        }
        serializer = SyntheticEventTargetSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_target_serializer_missing_name(self):
        invalid_data = {}
        serializer = SyntheticEventTargetSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)


class SyntheticEventTypeSerializerTest(TestCase):
    def setUp(self):
        self.event_type = SyntheticEventType.objects.create(
            name="Load Test",
            description="Tests for load performance"
        )

    def test_event_type_serializer_fields(self):
        serializer = SyntheticEventTypeSerializer(instance=self.event_type)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Load Test')
        self.assertEqual(data['description'], 'Tests for load performance')
        self.assertIn('id', data)

    def test_event_type_serializer_validation(self):
        valid_data = {
            'name': 'Valid Type',
            'description': 'Valid description'
        }
        serializer = SyntheticEventTypeSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_event_type_serializer_missing_required_fields(self):
        incomplete_data = {
            'name': 'Incomplete Type'
        }
        serializer = SyntheticEventTypeSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)


class SyntheticEventSerializerTest(TestCase):
    def setUp(self):
        self.target = SyntheticEventTarget.objects.create(name="Checkout Process")
        self.event_type = SyntheticEventType.objects.create(
            name="Integration Test",
            description="Tests for integration verification"
        )
        self.event = SyntheticEvent.objects.create(
            name="Checkout Flow Test",
            description="Test to validate checkout process",
            target=self.target,
            event_type=self.event_type
        )

    def test_event_serializer_fields(self):
        serializer = SyntheticEventSerializer(instance=self.event)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Checkout Flow Test')
        self.assertEqual(data['description'], 'Test to validate checkout process')
        self.assertEqual(data['target']['id'], self.target.id)
        self.assertEqual(data['target']['name'], self.target.name)
        self.assertEqual(data['event_type']['id'], self.event_type.id)
        self.assertEqual(data['event_type']['name'], self.event_type.name)
        self.assertIn('id', data)

    def test_event_serializer_validation(self):
        valid_data = {
            'name': 'Valid Event',
            'description': 'Valid description',
            'target': self.target.id,
            'event_type': self.event_type.id
        }
        serializer = SyntheticEventSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_event_serializer_missing_required_fields(self):
        incomplete_data = {
            'name': 'Incomplete Event'
        }
        serializer = SyntheticEventSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)
        # Note: target and event_type are read_only in the serializer, so they won't be in errors


class SyntheticEventsAPITest(APITestCase):
    def setUp(self):
        self.target1 = SyntheticEventTarget.objects.create(name="Homepage")
        self.target2 = SyntheticEventTarget.objects.create(name="Search Page")
        
        self.type1 = SyntheticEventType.objects.create(
            name="Smoke Test",
            description="Basic functionality tests"
        )
        self.type2 = SyntheticEventType.objects.create(
            name="Regression Test",
            description="Tests to catch regressions"
        )
        
        self.event1 = SyntheticEvent.objects.create(
            name="Homepage Load Test",
            description="Test homepage loading performance",
            target=self.target1,
            event_type=self.type1
        )
        
        self.event2 = SyntheticEvent.objects.create(
            name="Search Functionality Test",
            description="Test search feature functionality",
            target=self.target2,
            event_type=self.type2
        )
        
        self.event3 = SyntheticEvent.objects.create(
            name="Homepage Navigation Test",
            description="Test navigation from homepage",
            target=self.target1,
            event_type=self.type2
        )

    def test_synthetic_events_api_endpoint(self):
        url = reverse('synthetic-events')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_synthetic_events_api_response_structure(self):
        url = reverse('synthetic-events')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for event in response.data:
            self.assertIn('id', event)
            self.assertIn('name', event)
            self.assertIn('description', event)
            self.assertIn('target', event)
            self.assertIn('event_type', event)

    def test_synthetic_events_api_includes_all_events(self):
        url = reverse('synthetic-events')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        event_names = [event['name'] for event in response.data]
        self.assertIn('Homepage Load Test', event_names)
        self.assertIn('Search Functionality Test', event_names)
        self.assertIn('Homepage Navigation Test', event_names)

    def test_synthetic_events_api_includes_relationship_data(self):
        url = reverse('synthetic-events')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        target_ids = [event['target']['id'] for event in response.data]
        type_ids = [event['event_type']['id'] for event in response.data]
        
        self.assertIn(self.target1.id, target_ids)
        self.assertIn(self.target2.id, target_ids)
        self.assertIn(self.type1.id, type_ids)
        self.assertIn(self.type2.id, type_ids)

    def test_synthetic_events_api_empty_when_no_events(self):
        SyntheticEvent.objects.all().delete()
        
        url = reverse('synthetic-events')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])

    def test_target_can_have_multiple_events(self):
        # Verify that target1 has multiple events
        events_for_target1 = SyntheticEvent.objects.filter(target=self.target1)
        self.assertEqual(events_for_target1.count(), 2)
        
        url = reverse('synthetic-events')
        response = self.client.get(url)
        
        target1_events = [event for event in response.data if event['target']['id'] == self.target1.id]
        self.assertEqual(len(target1_events), 2)

    def test_event_type_can_have_multiple_events(self):
        # Verify that type2 has multiple events
        events_for_type2 = SyntheticEvent.objects.filter(event_type=self.type2)
        self.assertEqual(events_for_type2.count(), 2)
        
        url = reverse('synthetic-events')
        response = self.client.get(url)
        
        type2_events = [event for event in response.data if event['event_type']['id'] == self.type2.id]
        self.assertEqual(len(type2_events), 2)
