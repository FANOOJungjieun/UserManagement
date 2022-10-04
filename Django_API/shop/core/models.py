# 각 앱의 model들이 공통적으로 사용하는 model을 위한 class 혹은 function

from django.db import models


class TimestampedModel(models.Model):
	
    # 생성된 날짜를 기록
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정된 날짜를 기록
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']