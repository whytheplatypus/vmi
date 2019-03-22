from django.urls import include, path
from rest_framework import routers
from rest_framework_nested import routers
from views import (
    UsersViewSet,
    IdentifiersViewSet,
    AddressViewSet,
)

router = routers.SimpleRouter()
router.register(r'user', DomainViewSet)

identifier_router = routers.NestedSimpleRouter(router, r'user', lookup='user')
identifier_router.register(r'identifier', IdentifierViewSet)

address_router = routers.NestedSimpleRouter(router, r'user', lookup='user')
address_router.register(r'address', AddressViewSet)

v1 = [
    path('', include(router.urls)),
    path('', include(identifier_router.urls)),
    path('', include(address_router.urls)),
]

urlpatterns = [
    path('v1/', include(v1)),
]
