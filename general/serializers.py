from rest_framework import serializers
from .models import ToolCategory, Tool


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'name', 'description', 'image', 'link']


class ToolCategorySerializer(serializers.ModelSerializer):
    tools = ToolSerializer(many=True, read_only=True)
    
    class Meta:
        model = ToolCategory
        fields = ['id', 'name', 'tools']