from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        abstract = True

class DashDetectFace(BaseModel):
    detect_count = models.IntegerField(default=0)
    detect_valid = models.IntegerField(default=0)
    detect_by_hour = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Dashboard Detect Face'
        verbose_name_plural = 'Dashboard Detect Face'

    def __str__(self):
        return (f'{self.detect_count} - {self.detect_valid} - {self.detect_by_hour}')
    
class DashVerifyFace(BaseModel):
    verify_count = models.IntegerField(default=0)
    verifyt_sucess = models.IntegerField(default=0)
    verify_by_hour = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Dashboard Verify Face'
        verbose_name_plural = 'Dashboard Verify Face'

    def __str__(self):
        return (f'{self.verify_count} - {self.verify_valid} - {self.verify_by_hour}')