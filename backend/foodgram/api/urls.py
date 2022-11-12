from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from users.views import APIFollow, FollowViewSet

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name='api'

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(
    r'users/subscriptions',
    FollowViewSet,
    basename='subscriptions'
)

urlpatterns = [
    path('users/<pk>/subscribe/', APIFollow.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),
]
