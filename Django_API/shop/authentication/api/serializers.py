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
        
