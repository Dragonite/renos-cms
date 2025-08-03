from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import ToolCategory, Tool, LinkCategory, ImportantLinks, Role, TeamMember
from .serializers import ToolSerializer, ToolCategorySerializer, ImportantLinksSerializer, LinkCategorySerializer, RoleSerializer, TeamMemberSerializer


class ToolSerializerTest(TestCase):
    def setUp(self):
        self.category = ToolCategory.objects.create(name="Development Tools")
        self.tool = Tool.objects.create(
            name='Test Tool',
            description='A test tool for development',
            link='https://example.com',
            category=self.category
            # image field left blank/null
        )

    def test_tool_serializer_fields(self):
        serializer = ToolSerializer(instance=self.tool)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Test Tool')
        self.assertEqual(data['description'], 'A test tool for development')
        self.assertEqual(data['link'], 'https://example.com')
        self.assertIn('id', data)
        self.assertIn('image', data)

    def test_tool_serializer_validation(self):
        valid_data = {
            'name': 'Valid Tool',
            'description': 'Valid description',
            'link': 'https://valid-url.com'
        }
        serializer = ToolSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_tool_serializer_invalid_url(self):
        invalid_data = {
            'name': 'Invalid Tool',
            'description': 'Invalid description',
            'link': 'not-a-valid-url'
        }
        serializer = ToolSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('link', serializer.errors)

    def test_tool_serializer_missing_required_fields(self):
        incomplete_data = {
            'name': 'Incomplete Tool'
        }
        serializer = ToolSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)
        self.assertIn('link', serializer.errors)


class ToolCategorySerializerTest(TestCase):
    def setUp(self):
        self.category = ToolCategory.objects.create(name="Web Development")
        
        self.tool1 = Tool.objects.create(
            name='Tool 1',
            description='First tool',
            link='https://tool1.com',
            category=self.category
            # image field left blank/null
        )
        
        self.tool2 = Tool.objects.create(
            name='Tool 2',
            description='Second tool',
            link='https://tool2.com',
            category=self.category
            # image field left blank/null
        )

    def test_tool_category_serializer_fields(self):
        serializer = ToolCategorySerializer(instance=self.category)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Web Development')
        self.assertIn('id', data)
        self.assertIn('tools', data)
        self.assertEqual(len(data['tools']), 2)

    def test_tool_category_serializer_nested_tools(self):
        serializer = ToolCategorySerializer(instance=self.category)
        data = serializer.data
        
        tools_data = data['tools']
        tool_names = [tool['name'] for tool in tools_data]
        
        self.assertIn('Tool 1', tool_names)
        self.assertIn('Tool 2', tool_names)
        
        for tool in tools_data:
            self.assertIn('id', tool)
            self.assertIn('name', tool)
            self.assertIn('description', tool)
            self.assertIn('image', tool)
            self.assertIn('link', tool)

    def test_tool_category_serializer_validation(self):
        valid_data = {
            'name': 'Valid Category'
        }
        serializer = ToolCategorySerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_tool_category_serializer_missing_name(self):
        invalid_data = {}
        serializer = ToolCategorySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_tool_category_empty_tools(self):
        empty_category = ToolCategory.objects.create(name="Empty Category")
        serializer = ToolCategorySerializer(instance=empty_category)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Empty Category')
        self.assertEqual(len(data['tools']), 0)
        self.assertEqual(data['tools'], [])


class ImportantLinksSerializerTest(TestCase):
    def setUp(self):
        self.category = LinkCategory.objects.create(name="Documentation")
        self.link_data = {
            'label': 'Django Docs',
            'link': 'https://docs.djangoproject.com',
            'category': self.category
        }
        self.important_link = ImportantLinks.objects.create(**self.link_data)

    def test_important_links_serializer_fields(self):
        serializer = ImportantLinksSerializer(instance=self.important_link)
        data = serializer.data
        
        self.assertEqual(data['label'], 'Django Docs')
        self.assertEqual(data['link'], 'https://docs.djangoproject.com')
        self.assertIn('id', data)

    def test_important_links_serializer_validation(self):
        valid_data = {
            'label': 'Valid Link',
            'link': 'https://valid-url.com'
        }
        serializer = ImportantLinksSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_important_links_serializer_invalid_url(self):
        invalid_data = {
            'label': 'Invalid Link',
            'link': 'not-a-valid-url'
        }
        serializer = ImportantLinksSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('link', serializer.errors)

    def test_important_links_serializer_missing_required_fields(self):
        incomplete_data = {
            'label': 'Incomplete Link'
        }
        serializer = ImportantLinksSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('link', serializer.errors)


class LinkCategorySerializerTest(TestCase):
    def setUp(self):
        self.category = LinkCategory.objects.create(name="Resources")
        
        self.link1 = ImportantLinks.objects.create(
            label='Resource 1',
            link='https://resource1.com',
            category=self.category
        )
        
        self.link2 = ImportantLinks.objects.create(
            label='Resource 2',
            link='https://resource2.com',
            category=self.category
        )

    def test_link_category_serializer_fields(self):
        serializer = LinkCategorySerializer(instance=self.category)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Resources')
        self.assertIn('id', data)
        self.assertIn('important_links', data)
        self.assertEqual(len(data['important_links']), 2)

    def test_link_category_serializer_nested_links(self):
        serializer = LinkCategorySerializer(instance=self.category)
        data = serializer.data
        
        links_data = data['important_links']
        link_labels = [link['label'] for link in links_data]
        
        self.assertIn('Resource 1', link_labels)
        self.assertIn('Resource 2', link_labels)
        
        for link in links_data:
            self.assertIn('id', link)
            self.assertIn('label', link)
            self.assertIn('link', link)

    def test_link_category_serializer_validation(self):
        valid_data = {
            'name': 'Valid Category'
        }
        serializer = LinkCategorySerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_link_category_serializer_missing_name(self):
        invalid_data = {}
        serializer = LinkCategorySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_link_category_empty_links(self):
        empty_category = LinkCategory.objects.create(name="Empty Link Category")
        serializer = LinkCategorySerializer(instance=empty_category)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Empty Link Category')
        self.assertEqual(len(data['important_links']), 0)
        self.assertEqual(data['important_links'], [])


class ImportantLinksAPITest(APITestCase):
    def setUp(self):
        self.category1 = LinkCategory.objects.create(name="Documentation")
        self.category2 = LinkCategory.objects.create(name="Tools")
        
        ImportantLinks.objects.create(
            label='Django Docs',
            link='https://docs.djangoproject.com',
            category=self.category1
        )
        
        ImportantLinks.objects.create(
            label='DRF Docs',
            link='https://www.django-rest-framework.org',
            category=self.category1
        )
        
        ImportantLinks.objects.create(
            label='VS Code',
            link='https://code.visualstudio.com',
            category=self.category2
        )

    def test_important_links_api_endpoint(self):
        url = reverse('important-links')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Documentation', response.data)
        self.assertIn('Tools', response.data)

    def test_important_links_api_response_format(self):
        url = reverse('important-links')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        documentation_links = response.data['Documentation']
        tools_links = response.data['Tools']
        
        self.assertEqual(len(documentation_links), 2)
        self.assertEqual(len(tools_links), 1)
        
        doc_labels = [link['label'] for link in documentation_links]
        self.assertIn('Django Docs', doc_labels)
        self.assertIn('DRF Docs', doc_labels)
        
        tools_labels = [link['label'] for link in tools_links]
        self.assertIn('VS Code', tools_labels)

    def test_important_links_api_link_structure(self):
        url = reverse('important-links')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for category_name, links in response.data.items():
            for link in links:
                self.assertIn('id', link)
                self.assertIn('label', link)
                self.assertIn('link', link)
                self.assertTrue(link['link'].startswith('http'))

    def test_important_links_api_empty_category(self):
        empty_category = LinkCategory.objects.create(name="Empty Category")
        
        url = reverse('important-links')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Empty Category', response.data)
        self.assertEqual(response.data['Empty Category'], [])


class RoleModelTest(TestCase):
    def test_role_creation(self):
        role = Role.objects.create(name="Developer")
        self.assertEqual(role.name, "Developer")
        self.assertEqual(str(role), "Developer")

    def test_role_unique_name(self):
        Role.objects.create(name="Manager")
        with self.assertRaises(Exception):
            Role.objects.create(name="Manager")


class TeamMemberModelTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name="Designer")

    def test_team_member_creation(self):
        team_member = TeamMember.objects.create(
            name="John Doe",
            email="john@example.com",
            contact_number="123-456-7890",
            role=self.role
            # image field left blank/null
        )
        self.assertEqual(team_member.name, "John Doe")
        self.assertEqual(team_member.email, "john@example.com")
        self.assertEqual(team_member.contact_number, "123-456-7890")
        self.assertEqual(team_member.role, self.role)
        self.assertEqual(str(team_member), "John Doe")

    def test_team_member_role_relationship(self):
        team_member = TeamMember.objects.create(
            name="Jane Smith",
            email="jane@example.com",
            contact_number="098-765-4321",
            role=self.role
            # image field left blank/null
        )
        self.assertEqual(team_member.role.name, "Designer")
        self.assertIn(team_member, self.role.team_members.all())


class RoleSerializerTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name="Developer")

    def test_role_serializer_fields(self):
        serializer = RoleSerializer(instance=self.role)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Developer')
        self.assertIn('id', data)

    def test_role_serializer_validation(self):
        valid_data = {'name': 'Valid Role'}
        serializer = RoleSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_role_serializer_missing_name(self):
        invalid_data = {}
        serializer = RoleSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)


class TeamMemberSerializerTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name="Project Manager")
        self.team_member = TeamMember.objects.create(
            name="Alice Johnson",
            email="alice@example.com",
            contact_number="555-123-4567",
            role=self.role
            # image field left blank/null
        )

    def test_team_member_serializer_fields(self):
        serializer = TeamMemberSerializer(instance=self.team_member)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Alice Johnson')
        self.assertEqual(data['email'], 'alice@example.com')
        self.assertEqual(data['contact_number'], '555-123-4567')
        self.assertIn('id', data)
        self.assertIn('image', data)
        self.assertIn('role', data)
        self.assertEqual(data['role']['name'], 'Project Manager')

    def test_team_member_serializer_nested_role(self):
        serializer = TeamMemberSerializer(instance=self.team_member)
        data = serializer.data
        
        role_data = data['role']
        self.assertIn('id', role_data)
        self.assertIn('name', role_data)
        self.assertEqual(role_data['name'], 'Project Manager')

    def test_team_member_serializer_validation(self):
        valid_data = {
            'name': 'Bob Wilson',
            'email': 'bob@example.com',
            'contact_number': '555-987-6543'
            # image field left blank/null
        }
        serializer = TeamMemberSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_team_member_serializer_invalid_email(self):
        invalid_data = {
            'name': 'Invalid Member',
            'email': 'not-an-email',
            'contact_number': '555-000-0000'
            # image field left blank/null
        }
        serializer = TeamMemberSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_team_member_serializer_missing_required_fields(self):
        incomplete_data = {
            'name': 'Incomplete Member'
            # image field left blank/null
        }
        serializer = TeamMemberSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertIn('contact_number', serializer.errors)


class TeamMemberAPITest(APITestCase):
    def setUp(self):
        self.role1 = Role.objects.create(name="Frontend Developer")
        self.role2 = Role.objects.create(name="Backend Developer")
        
        TeamMember.objects.create(
            name="Sarah Connor",
            email="sarah@example.com",
            contact_number="555-111-2222",
            role=self.role1
            # image field left blank/null
        )
        
        TeamMember.objects.create(
            name="John Connor",
            email="john@example.com",
            contact_number="555-333-4444",
            role=self.role2
            # image field left blank/null
        )
        
        TeamMember.objects.create(
            name="Kyle Reese",
            email="kyle@example.com",
            contact_number="555-555-6666",
            role=self.role1
            # image field left blank/null
        )

    def test_team_members_api_endpoint(self):
        url = reverse('team-members')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_team_members_api_response_structure(self):
        url = reverse('team-members')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for member in response.data:
            self.assertIn('id', member)
            self.assertIn('name', member)
            self.assertIn('email', member)
            self.assertIn('contact_number', member)
            self.assertIn('image', member)
            self.assertIn('role', member)
            
            role = member['role']
            self.assertIn('id', role)
            self.assertIn('name', role)

    def test_team_members_api_content(self):
        url = reverse('team-members')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        member_names = [member['name'] for member in response.data]
        self.assertIn('Sarah Connor', member_names)
        self.assertIn('John Connor', member_names)
        self.assertIn('Kyle Reese', member_names)
        
        member_emails = [member['email'] for member in response.data]
        self.assertIn('sarah@example.com', member_emails)
        self.assertIn('john@example.com', member_emails)
        self.assertIn('kyle@example.com', member_emails)

    def test_team_members_api_roles(self):
        url = reverse('team-members')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        role_names = [member['role']['name'] for member in response.data]
        self.assertIn('Frontend Developer', role_names)
        self.assertIn('Backend Developer', role_names)
        
        frontend_count = sum(1 for member in response.data if member['role']['name'] == 'Frontend Developer')
        backend_count = sum(1 for member in response.data if member['role']['name'] == 'Backend Developer')
        
        self.assertEqual(frontend_count, 2)
        self.assertEqual(backend_count, 1)

    def test_team_members_api_empty_result(self):
        TeamMember.objects.all().delete()
        
        url = reverse('team-members')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])
