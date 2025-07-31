from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import ToolCategory, Tool
from .serializers import ToolSerializer, ToolCategorySerializer


class ToolSerializerTest(TestCase):
    def setUp(self):
        self.category = ToolCategory.objects.create(name="Development Tools")
        self.tool_data = {
            'name': 'Test Tool',
            'description': 'A test tool for development',
            'image': SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            'link': 'https://example.com',
            'category': self.category
        }
        self.tool = Tool.objects.create(**self.tool_data)

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
            image=SimpleUploadedFile("tool1.jpg", b"file_content", content_type="image/jpeg"),
            link='https://tool1.com',
            category=self.category
        )
        
        self.tool2 = Tool.objects.create(
            name='Tool 2',
            description='Second tool',
            image=SimpleUploadedFile("tool2.jpg", b"file_content", content_type="image/jpeg"),
            link='https://tool2.com',
            category=self.category
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
