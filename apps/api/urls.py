from django.urls import include, path
from rest_framework_nested import routers
from .views import (
    UserViewSet,
    IdentifierViewSet,
    AddressViewSet,
)

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)

identifier_router = routers.NestedSimpleRouter(router, r'user', lookup='user')
identifier_router.register(r'id-assurance', IdentifierViewSet, base_name='identifier')
identifier_router.register(r'address', AddressViewSet, base_name='address')

v1 = [
    path('', include(router.urls)),
    path('', include(identifier_router.urls)),
]

urlpatterns = [
    path('v1/', include(v1)),
]
