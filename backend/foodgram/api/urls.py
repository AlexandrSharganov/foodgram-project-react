from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from users.views import APIFollow, FollowViewSet

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register(
    'users/subscriptions',
    FollowViewSet,
    basename='subscriptions'
)

urlpatterns = [
    path('users/<int:pk>/subscribe/', APIFollow.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),
]
