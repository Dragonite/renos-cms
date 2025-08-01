from rest_framework import serializers
from .models import ToolCategory, Tool, LinkCategory, ImportantLinks


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'name', 'description', 'image', 'link']


class ToolCategorySerializer(serializers.ModelSerializer):
    tools = ToolSerializer(many=True, read_only=True)
    
    class Meta:
        model = ToolCategory
        fields = ['id', 'name', 'tools']


class ImportantLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantLinks
        fields = ['id', 'label', 'link']


class LinkCategorySerializer(serializers.ModelSerializer):
    important_links = ImportantLinksSerializer(many=True, read_only=True)
    
    class Meta:
        model = LinkCategory
        fields = ['id', 'name', 'important_links']