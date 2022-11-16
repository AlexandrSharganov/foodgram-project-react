from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import AddRecipeSerializer
from users.models import User

from .filters import IngredientFilter, RecipeFilter
from .models import Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag
from .pagination import CustomPagination
from .permissions import OwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeReadSerializer, TagSerializer)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """Вьюсет для работы с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (OwnerOrReadOnly,)


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """Вьюсет для работы с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = (OwnerOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с рецептами."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    pagination_class = CustomPagination
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Метод выбора сериализатора при разных запросах."""
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_path=r'(?P<pk>\d+)/favorite'
    )
    def favorite_create_delete(self, request, pk=None):
        """Метод добавления и удаления из избранного."""
        user = get_object_or_404(User, username=request.user)
        recipe = get_object_or_404(Recipe, pk=pk)
        if str(request.method) == 'POST':
            Favorite.objects.get_or_create(user=user, recipe=recipe)
            recipe_serializer = AddRecipeSerializer(recipe)
            return Response(recipe_serializer.data,
                            status=status.HTTP_201_CREATED)
        instance = get_object_or_404(Favorite, user=user, recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_path=r'(?P<pk>\d+)/shopping_cart'
    )
    def cart_create_delete(self, request, pk=None):
        """Метод добавления и удаления из списка покупок."""
        user = get_object_or_404(User, username=request.user)
        recipe = get_object_or_404(Recipe, pk=pk)
        if str(request.method) == 'POST':
            Cart.objects.get_or_create(user=user, recipe=recipe)
            recipe_serializer = AddRecipeSerializer(recipe)
            return Response(recipe_serializer.data,
                            status=status.HTTP_201_CREATED)
        instance = get_object_or_404(Cart, user=user, recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False,
        url_path='download_shopping_cart'
    )
    def load_shopping_list(self, request):
        """Метод скачивания списка продуктов."""
        user = get_object_or_404(User, username=request.user)
        recipes_id = Cart.objects.filter(user=user).values('recipe')
        recipes = Recipe.objects.filter(pk__in=recipes_id)
        result_dict = {}
        for recipe in recipes:
            ingredients_list = IngredientAmount.objects.filter(recipe=recipe)
            for ingredient in ingredients_list:
                if ingredient.ingredient.name in result_dict:
                    result_dict[ingredient.ingredient.name][0] += (
                        ingredient.amount
                    )
                else:
                    result_dict[ingredient.ingredient.name] = [
                        ingredient.amount,
                        ingredient.ingredient.measurement_unit
                    ]
        result = (
            'Список покупок:\n'
        )
        for key, value in result_dict.items():
            result += f'\n{key} ({value[1]}) = {str(value[0])}'
        return HttpResponse(result, content_type='text/plain')
