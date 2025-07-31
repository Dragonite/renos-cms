from django.db import models


class ToolCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Tool Categories"


class Tool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='tools/')
    link = models.URLField()
    category = models.ForeignKey(ToolCategory, on_delete=models.CASCADE, related_name='tools')
    
    def __str__(self):
        return self.name
