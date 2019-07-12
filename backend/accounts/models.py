from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Detail(models.Model):
    """用户信息名"""
    text = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text

class Information(models.Model):
    """具体信息"""
    title = models.ForeignKey(Detail, on_delete=models.CASCADE, null=True)
    text = models.TextField(max_length=50)

    class Meta:
        verbose_name_plural = 'informations'

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text