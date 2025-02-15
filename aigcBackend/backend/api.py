
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
import os,json,time
from openai import OpenAI

# 初始化OpenAI客户端
client = OpenAI(
    # api_key=os.getenv("DASHSCOPE_API_KEY"),
    api_key='sk-dcc788ecfde64a9bb0f93695fc3ed2d9',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
@csrf_exempt
# @api_view(['POST'])
def stream_response(request):

    body_str = request.body.decode('utf-8')

    # 解析 JSON 字符串为字典
    data = json.loads(body_str)

    message = data.get('message', '')

    try:

        print(message)
        def event_stream():
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

            # yield f"data: {('=' * 20)} 思考过程 {('=' * 20)}\n\n"

            for chunk in stream:
                # 确保每条数据都以 \n\n 结尾
                res = chunk.choices[0].delta.content
                print(res)
                if res:
                    yield f"data: {chunk.choices[0].delta.content}\n\n"
                else:
                    continue

        return StreamingHttpResponse(event_stream(), content_type='text/event-stream', headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'  # 如果使用 Nginx，需要禁用其缓冲
        })

    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)