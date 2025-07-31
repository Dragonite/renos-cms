from django.urls import path
from .views import ToolCategoryListView

urlpatterns = [
    path('', ToolCategoryListView.as_view(), name='tool-categories'),
]