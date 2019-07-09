from django.db import models

# Create your models here.
class Detail(models.Model):
    """用户信息名"""
    text = models.CharField(max_length=20)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text

class Information(models.Model):
    """具体信息"""
    title = models.ForeignKey(Detail, on_delete=models.CASCADE)
    text = models.TextField(max_length=50)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text