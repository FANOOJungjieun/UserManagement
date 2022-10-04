from django.contrib.auth.models import BaseUserManager

#  https://docs.djangoproject.com/en/4.0/ref/contrib/auth/
#  위 문서에 명시된 BaseUserManager 클래스의 기본제공 모델을 가져와 적용/수정한다.
#  
class UserManager(BaseUserManager):

    # 유저 생성
    def create_user(self, username, email, password=None, **extra_fields):
        # 빈 값일 경우 에러처리
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if password is None:
            raise TypeError('Users must have a password.')

        user = self.model(
        username = username,
        # 이메일은 중복 최소화를 위한 정규화
        email=self.normalize_email(email),
        **extra_fields
        ) # 모델 인스턴스 구성

        # django 에서 제공하는 password 설정 함수
        user.set_password(password)
        user.save()
        
        return user

    # 관리자 생성
    def create_superuser(self, username, email, password, **extra_fields):
        
        if password is None:
            raise TypeError('Superuser must have a password.')
        
        # "create_user"함수를 이용해 우선 사용자를 DB에 저장
        user = self.create_user(username, email, password, **extra_fields)
        # 관리자로 지정. 기본제공 변수.
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user