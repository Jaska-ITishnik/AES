from django.urls import path

from apps.views import AesLogicView

urlpatterns = [
    path('', AesLogicView.as_view(), name="main_page")
]
