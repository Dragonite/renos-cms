from django.db import models


class TestingAccountEnvironment(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Testing Account Environments"


class TestingAccount(models.Model):
    label = models.CharField(max_length=200)
    description = models.TextField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    environment = models.ForeignKey(TestingAccountEnvironment, on_delete=models.CASCADE, related_name='testing_accounts')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.label} ({self.environment.name})"
    
    class Meta:
        verbose_name_plural = "Testing Accounts"


class SyntheticEventTarget(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Synthetic Event Targets"


class SyntheticEventType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Synthetic Event Types"


class SyntheticEvent(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    target = models.ForeignKey(SyntheticEventTarget, on_delete=models.CASCADE, related_name='synthetic_events')
    event_type = models.ForeignKey(SyntheticEventType, on_delete=models.CASCADE, related_name='synthetic_events')
    
    def __str__(self):
        return f"{self.name} ({self.event_type.name})"
    
    class Meta:
        verbose_name_plural = "Synthetic Events"
