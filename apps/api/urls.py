from django.urls import include, path
from rest_framework import routers
from .views import (
    UserViewSet,
)

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)

v1 = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('v1/', include(v1)),
]
