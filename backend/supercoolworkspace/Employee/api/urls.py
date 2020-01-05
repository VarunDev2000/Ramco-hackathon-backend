from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import EmployeeViewSet,call_model,open_music

router = DefaultRouter()
router.register(r'', EmployeeViewSet, basename='EmployeeInfo')

urlpatterns = router.urls

urlpatterns += [
    path('model',call_model.as_view()),
    path('music',open_music.as_view())
]