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
    image = models.ImageField(upload_to='tools/', blank=True, null=True)
    link = models.URLField()
    category = models.ForeignKey(ToolCategory, on_delete=models.CASCADE, related_name='tools')
    
    def __str__(self):
        return self.name


class LinkCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Link Categories"


class ImportantLinks(models.Model):
    label = models.CharField(max_length=200)
    link = models.URLField()
    category = models.ForeignKey(LinkCategory, on_delete=models.CASCADE, related_name='important_links')
    
    def __str__(self):
        return self.label
    
    class Meta:
        verbose_name_plural = "Important Links"
