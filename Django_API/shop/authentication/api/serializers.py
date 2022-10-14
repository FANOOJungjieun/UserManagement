from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers # setting에서 추가했던 rest_framework 앱

from authentication.models import User


# serializer를 통해 사용자 등록을 위한 요청(request)과 응답(response)을 직렬화(serialize)

class RegistrationSerializer(serializers.ModelSerializer): # serializers.ModelSerializer를 상속받아 만든 클래스

    # ModelSerializer 클래스는 모델 필드에 해당하는 필드가 있는 Serializer 클래스를 자동으로 만들 수 있도록 해줍니다.
    # 별도의 구체적인 내용없이 Meta 클래스만 작성해주더라도 ModelSerializer는 해당 Model에 있는 값들을 Serializing 해줍니다.
    
    password = serializers.CharField(
        max_length = 128,
        min_length = 8,
        write_only = True
        # password를 updating, creating 할 때는 사용되지만, serializing 할 때는 포함되지 않도록 하기 위해 Write_only 체크함.
    )
    
    token = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 
            'username',
            'phone_number',
            'password',
            'token'
            ]
        
    def create(self, validated_data):

        return User.objects.create_user(**validated_data)



class LoginSerializer(serializers.Serializer): # serializers.Serializer상속받음
    email = serializers.EmailField()
    # 1. password는 읽히면 안 되므로 write_only. 나머지는 수정하면 안 되므로 read_only
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    last_login = serializers.CharField(max_length=255, read_only=True)
    
    # 2. LoginSerializer의 인스턴스가 유효한지 판별
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        
        # 3. data로 전달받은 email,password가 제대로 있는지 판별
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        
        # 4. data로 받아온 값과 db에 저장된 값을 비교해 해당하는 유저를 찾아냄. 없을시 none
        user = authenticate(username=email, password=password)
        
        # 5. 4번의 오류 메시지
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        
        # 6. 마지막 로그인 시간 업데이트
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # 7. 결과값 반환
        return {
            'email': user.email,
            'username': user.username,
            'last_login': user.last_login
        }

# 1.User 객체를 serialization 과 deserialization을 처리
class UserSerializer(serializers.ModelSerializer):
    
    # 2. 쓰기 옵션만 활성화
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'token'
        ]
        
        # 3.'read_only_fields' 옵션은 각 field에 'read_only=True'와 같은 역할
        read_only_fields = ('token', )
        
    # 4.사용자의 정보를 업데이트 할 때 실행
    def update(self, instance, validated_data):
        # 5.password는 다른 field들과 달리 'setattr'로 처리하면 안됨.
        password = validated_data.pop('password', None)
        
        # 6.변경된 데이터 목록을 for문으로 순회
        for (key, value) in validated_data.items():
            # 7.속성을 추가하거나(key가객체가 없을경우) 속성값을 바꾸는 함수.(객체,속성명,속성값)
            setattr(instance, key, value)

        if password is not None:
            # 8.password수정
            instance.set_password(password)

        # 9. 객체 정보 저장
        instance.save()

        return instance
        
