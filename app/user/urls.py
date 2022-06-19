from django.urls import path

from user.views import CreateUserView, CustomAuthToken, ManageUserView

app_name = 'user'

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path('token/', CustomAuthToken.as_view(), name='token'),
    path('profile/', ManageUserView.as_view(), name='profile'),
]