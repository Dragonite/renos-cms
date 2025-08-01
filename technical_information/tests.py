from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import TestingAccountEnvironment, TestingAccount
from .serializers import TestingAccountSerializer, TestingAccountEnvironmentSerializer


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
        self.assertEqual(data['environment'], self.environment.id)
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
        self.assertIn('environment', serializer.errors)


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
        serializer = TestingAccountEnvironmentSerializer(instance=self.environment)
        data = serializer.data
        
        self.assertEqual(data['name'], 'QA Environment')
        self.assertIn('id', data)
        self.assertIn('testing_accounts', data)
        self.assertEqual(len(data['testing_accounts']), 2)

    def test_environment_serializer_nested_accounts(self):
        serializer = TestingAccountEnvironmentSerializer(instance=self.environment)
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
        serializer = TestingAccountEnvironmentSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_environment_serializer_missing_name(self):
        invalid_data = {}
        serializer = TestingAccountEnvironmentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_environment_empty_accounts(self):
        empty_environment = TestingAccountEnvironment.objects.create(name="Empty Environment")
        serializer = TestingAccountEnvironmentSerializer(instance=empty_environment)
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
        
        environment_ids = [account['environment'] for account in response.data]
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
