
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
import os,json,time
from openai import OpenAI
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404
from .models import *

from django.db.models import Count

# 初始化OpenAI客户端
client = OpenAI(
    # api_key=os.getenv("DASHSCOPE_API_KEY"),
    api_key='sk-dcc788ecfde64a9bb0f93695fc3ed2d9',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def authChect(user:UserInfo,conversation:Conversation) -> bool:

    '''独立的权限检查'''

    return conversation.user_link==user

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def stream_response(request,con_uuid):

    body_str = request.body.decode('utf-8')

    # print(con_uuid)

    cur_con = get_object_or_404(Conversation, uuid=con_uuid)

    # 解析 JSON 字符串为字典
    data = json.loads(body_str)

    # 这里判断conversation

    message = data.get('message', '')

    sen_msg = Sentence(sentence_content=message,
             role=2)

    sen_msg.save()

    cur_con.sentence_scope.add(sen_msg)
    cur_con.save()

    try:

        print(message)
        def event_stream(cur_con:Conversation):
            reasoning_content = ""  # 定义完整思考过程
            answer_content = ""     # 定义完整回复
            is_answering = False    # 判断是否结束思考过程并开始回复

            # 创建聊天完成请求
            stream = client.chat.completions.create(
                model="qwen-omni-turbo",  # 此处以 deepseek-v3 为例，可按需更换模型名称
                messages=[
                    {"role": "user", "content": message}
                ],
                stream=True,
                modalities=["text"],
            )

            cur_msg = ''

            # yield f"data: {('=' * 20)} 思考过程 {('=' * 20)}\n\n"

            for chunk in stream:
                # 确保每条数据都以 \n\n 结尾
                res = chunk.choices[0].delta.content
                if res:

                    cur_msg+=chunk.choices[0].delta.content
                    # print(cur_msg)
                    yield f"data: {chunk.choices[0].delta.content}\n\n"
                else:
                    continue

            # print('结束了')
            sen_res = Sentence(sentence_content=cur_msg,
                               role=1)
            sen_res.save()

            cur_con.sentence_scope.add(sen_res)
            cur_con.save()

        return StreamingHttpResponse(event_stream(cur_con), content_type='text/event-stream', headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'  # 如果使用 Nginx，需要禁用其缓冲
        })

    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def conversation_new(request):
    login_user = request.user.userinfo.all().first()

    # 筛选出至少包含一个句子（sentence）的对话（conversation）
    conversations_without_sentences = Conversation.objects.annotate(
        sentence_count=Count('sentence_scope')
    ).filter(user_link=login_user, sentence_count=0)
    # 如果存在符合条件的对话，则创建一个新的对话

    if conversations_without_sentences.exists():
        # 如果不存在符合条件的对话，则尝试获取第一个没有绑定句子的对话
        con_obj = conversations_without_sentences.first()
    else:
        # 如果仍然没有找到合适的对话对象，则创建一个新的
        con_obj = Conversation.objects.create(user_link=login_user)
        con_obj.save()
        con_obj.label = f'对话：{con_obj.uuid}'
        con_obj.save()

    # if not con_obj:
    #     # 如果仍然没有找到合适的对话对象，则创建一个新的
    #     con_obj = Conversation.objects.create(user_link=login_user)
    #     con_obj.label = f'对话：{con_obj.uuid}'
    #     con_obj.save()

    res = {"new_con_uuid": con_obj.uuid}
    return JsonResponse(res, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def sentences_query(request):
    '''
    拉取给定converstaion下所有sens
    '''

    loginUser = request.user.userinfo.all().first()

    post_paras = json.loads(request.body.decode())
    con_uuid = post_paras.get('con_uuid',None)


    if con_uuid:
        cur_obj_uuid_list = Conversation.objects.filter(
            uuid=con_uuid,
            user_link=loginUser
        )
    else:
        cur_obj_uuid_list = Conversation.objects.filter(user_link=loginUser).order_by('-uuid')

    # cur_obj_test = Conversation.objects.filter(uuid=con_uuid,user_link=loginUser).first()
    # print(cur_obj_test)
    # print(cur_obj_test.sentence_scope.all())

    res = {"data":[{
                "key":str(cur_con.uuid),
                "label":cur_con.label,
                "sentences":[
                        {
                            "id":str(_.uuid),
                            "message": _.sentence_content,
                            "status": _.get_role_display(),
                            # "update_time":_.update_time,
                            # "create_time":_.create_time,
                        } for _ in cur_con.sentence_scope.filter(enabled=True)
                    ]
                } for cur_con in cur_obj_uuid_list
            ]}
    return JsonResponse(res, safe=False)