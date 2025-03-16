from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.cache import never_cache

# @csrf_exempt
# def custom_obtain_auth_token(request):
#     return obtain_auth_token(request)
# @csrf_exempt
# def custom_obtain_auth_token(request):
#     '''
#     在登陆前判断是AD账户登陆还是工号登陆
#     如果登陆成功则返回与AD账户对应的人员id
#     '''
#     # print(request)
#     if request.method == 'POST':
#
#         user_name = request.POST.get('username', '')
#         user_name = user_name.upper()
#         pass_word = request.POST.get('password', '')
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'status': 'ok','token':token.key}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
def login(request):

    post_paras = json.loads(request.body.decode())

    username = post_paras.get('username')
    password = post_paras.get('password')

    # 验证凭据
    user = authenticate(username=username, password=password)

    if user is not None:
        # 如果验证成功，生成或获取 Token

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return JsonResponse({
            'status':'ok',
            'currentAuthority':'admin',
            'data':{
                'token': access,
                'refreshToken': str(refresh),
            }
        }, status=status.HTTP_200_OK)
    else:
        # 如果验证失败，返回错误响应
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
# @csrf_exempt
def get_curUserinfo(request):
    data = {
    "success": True,
    "data": {
        "name": "Serati Ma",
        "avatar": "https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png",
        "userid": "00000001",
        "email": "antdesign@alipay.com",
        "signature": "海纳百川，有容乃大",
        "title": "交互专家",
        "group": "蚂蚁金服－某某某事业群－某某平台部－某某技术部－UED",
        "tags": [
            {"key": "0", "label": "很有想法的"},
            {"key": "1", "label": "专注设计"},
            {"key": "2", "label": "辣~"},
            {"key": "3", "label": "大长腿"},
            {"key": "4", "label": "川妹子"},
            {"key": "5", "label": "海纳百川"},
        ],
        "notifyCount": 12,
        "unreadCount": 11,
        "country": "China",
        "access": 'admin',
        "geographic": {
            "province": {
                "label": "浙江省",
                "key": "330000",
            },
            "city": {
                "label": "杭州市",
                "key": "330100",
            },
        },
        "address": "西湖区工专路 77 号",
        "phone": "0752-268888888",
        },
    }
    print(request)
    return JsonResponse({'code': 200, 'message': '请求成功', **data})