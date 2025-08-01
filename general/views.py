from rest_framework import generics
from rest_framework.response import Response
from .models import ToolCategory, LinkCategory
from .serializers import ToolCategorySerializer, LinkCategorySerializer


class ToolCategoryListView(generics.ListAPIView):
    queryset = ToolCategory.objects.prefetch_related('tools').all()
    serializer_class = ToolCategorySerializer


class ImportantLinksListView(generics.ListAPIView):
    queryset = LinkCategory.objects.prefetch_related('important_links').all()
    serializer_class = LinkCategorySerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        result = {}
        for category_data in serializer.data:
            result[category_data['name']] = category_data['important_links']
        
        return Response(result)
