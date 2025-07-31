from rest_framework import generics
from .models import ToolCategory
from .serializers import ToolCategorySerializer


class ToolCategoryListView(generics.ListAPIView):
    queryset = ToolCategory.objects.prefetch_related('tools').all()
    serializer_class = ToolCategorySerializer
