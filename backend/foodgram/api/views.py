from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import User
from users.serializers import UserRecipeSerializer
from rest_framework.views import APIView

from .filters import IngredientFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     Cart, Tag)
from .pagination import CustomPagination
from .permissions import OwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeCreateSerializer, TagSerializer)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    pagination_class = CustomPagination
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
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
        user = get_object_or_404(User, username=request.user)
        recipe = get_object_or_404(Recipe, pk=pk)
        if str(request.method) == 'POST':
            Favorite.objects.get_or_create(user=user, recipe=recipe)
            recipe_serializer = UserRecipeSerializer(recipe)
            return Response(recipe_serializer.data, status=status.HTTP_201_CREATED)
        instance = get_object_or_404(Favorite, user=user, recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_path=r'(?P<pk>\d+)/shopping_cart'
    )
    def cart_create_delete(self, request, pk=None):
        user = get_object_or_404(User, username=request.user)
        recipe = get_object_or_404(Recipe, pk=pk)
        if str(request.method) == 'POST':
            Cart.objects.get_or_create(user=user, recipe=recipe)
            recipe_serializer = UserRecipeSerializer(recipe)
            return Response(recipe_serializer.data, status=status.HTTP_201_CREATED)
        instance = get_object_or_404(Cart, user=user, recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False,
        url_path='download_shopping_cart'
    )
    def load_shopping_list(self, request):
        user = get_object_or_404(User, username=request.user)
        recipes_id = Cart.objects.filter(user=user).values('recipe')
        recipes = Recipe.objects.filter(pk__in=recipes_id)
        result_dict = {}
        for recipe in recipes:
            ingredients_list = IngredientAmount.objects.filter(recipe=recipe)
            for ingredient in ingredients_list:
                if ingredient.ingredient.name in result_dict:
                    result_dict[ingredient.ingredient.name][0] += ingredient.amount
                else:
                    result_dict[ingredient.ingredient.name] = [
                        ingredient.amount,
                        ingredient.ingredient.measurement_unit
                    ]
        result = (
            f'Список покупок:\n'
        )
        for key, value in result_dict.items():
            result += f'\n{key} ({value[1]}) = {str(value[0])}'
        return HttpResponse(result, content_type='text/plain')
