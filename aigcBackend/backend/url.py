from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .api import stream_response

urlpatterns = [
                  # path('', views.index, name='index'),

                  # path("logout/", authViews.LogoutView.as_view(), name="logout"),
                  # path("login/", login_func.acc_login, name="login"),

                  # path('individual_view/', views.individual_view, name='individual_view'),
                  path('stream/', stream_response, name='stream_response'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)