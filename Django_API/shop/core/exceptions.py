from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    # 1. DRF에서 제공하는 exception handler를 response로 받아 둠
    response = exception_handler(exc, context)
    
    # 2. 처리할 수 있는 예외의 종류를 넣어둔다.
    handlers = {
        'ValidationError': _handle_generic_error
    }
    
    # 3. exception의 타입을 식별하기 위한 변수
    exception_class = exc.__class__.__name__

    # 4. 3번에서 담아둔 타입의 중류가 handler에 포함되어 잇으면 해당 예외를 리턴
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
	# 5. handler에 없다면 DRF에서 제공하는 예외처리.
    return response

# 6. handler에서 호출되는 함수. 에러 메시지의 형태를 만든다.
def _handle_generic_error(exc, context, response):
    response.data = {
        'errors': response.data
    }

    return response