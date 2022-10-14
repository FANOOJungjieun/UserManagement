from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated # permission_classes 에 넣어줄 옵션
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView

from .serializers import (
    RegistrationSerializer, LoginSerializer, UserSerializer #만든 클래스들 이곳에 추가
    )

from .renderers import UserJSONRenderer

# Create your views here.
# Endpoint로 사용할 view를 생성함. 클라이언트에게 사용자를 생성할 url를 만들어준다.

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,) # allowany : 인증 여부에 상관 없이 뷰 호출 허용
    serializer_class = RegistrationSerializer # serializers.py에서 만든 클래스
    renderer_classes = (UserJSONRenderer,) # renderers.py에서 만든 클래스
    
    def post(self, request):
        # client가 요청한 데이터(request.data)를 받아와 직렬화(self.serializer_class(data=user)하고
        # 유효성(serializer.is_valid)을 확인해서 저장(serializer.save( ))
        
        user = request.data
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer # 로그인 Serializer클래스 불러옴.
    
    # 1.입력받은 값을 서버로 보내 확인하기 위해 post 기능 추가
    def post(self, request):
        # 2. 받은 data를 user에 보관
        user = request.data
        
        # 3. 받아온 user로 유효성검사
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        
        # 4. 정보 반환
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    
    # 1.RetrieveUpdateAPIView에서 제공하는 get메소드. 업데이트를 위해 기존 자료를 불러옴.
    def get(self, request, *args, **kwargs):
        # 2. user객체를 client에 보내주는 용도.
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 3. 객체 부분 업데이트 method
    def patch(self, request, *args, **kwargs):
        serializer_data = request.data
        # 4.instance(request.user), validated_data(serializer_data)를 serializer에 전달
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True # 부분업데이트 가능
        )
        
        serializer.is_valid(raise_exception=True)
        # 5. 업데이트된 객체 저장
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)