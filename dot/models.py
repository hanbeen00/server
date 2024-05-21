from django.db import models
from django.conf import settings

class ImageModel(models.Model):

    REPORT_CHOICES = [
        ('처리전', '처리전'),
        ('처리중', '처리중'),
        ('처리완료', '처리완료'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10,blank=True, null=True)
    address = models.TextField(blank=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    result = models.TextField(null=True)  # 번역 결과를 저장할 필드 추가
    report = models.CharField(max_length=10, choices=REPORT_CHOICES, default='처리전')
    information = models.TextField(blank=True)
    time = models.TextField(blank=True, null=True)

def get_image_url(self):    return '%s%s' %(settings.MEDIA_URL, self.image)
