# Create your models here.
import jwt
from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import BooleanField

from .managers import UserManager #같은 폴더의 managers파일에서 UserManater클래스를 가져온다.
from core.models import TimestampedModel #core폴더의 models파일에서 TimestampedModel클래스를 가져온다.


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    phone_number = models.CharField(max_length=255)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    
    # 로그인 아이디
    USERNAME_FIELD = 'email'
    
    # 반드시 받아야 하는 정보들 목록
    REQUIRED_FIELDS = [
        'username',
        'phone_number'
    ]
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username


    # jwt document : https://pyjwt.readthedocs.io/en/latest/

    @property
    def token(self): # 토큰 발행 함수를 편리하게 호출
        return self._generate_jwt_token( ) # 토큰 발행 함수

    def _generate_jwt_token(self):
        dt = datetime.now( ) + timedelta(days=60) # days:만료일자

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256') # 시크릿 키를 키로 삼고, HS256알고리즘을 사용해 다음과 같은 데이터를 인코딩하여 토큰으로 만든다.

        return token # 그 토큰을 리턴.