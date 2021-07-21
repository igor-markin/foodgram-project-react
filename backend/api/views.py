from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='user')
urlpatterns = router.urls