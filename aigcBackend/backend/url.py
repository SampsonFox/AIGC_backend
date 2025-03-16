from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .api import stream_response,conversation_new,sentences_query

urlpatterns = [
                  # path('', views.index, name='index'),

                  # path("logout/", authViews.LogoutView.as_view(), name="logout"),
                  # path("login/", login_func.acc_login, name="login"),

                  # path('individual_view/', views.individual_view, name='individual_view'),
                  path('stream/<int:con_uuid>/', stream_response, name='stream_response'),

                  path('conversation/new/', conversation_new, name='new_conversation'),
                  path('conversation/sentences/query/', sentences_query, name='sentences_query'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)