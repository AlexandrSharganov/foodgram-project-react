from django_filters import rest_framework

from .models import Ingredient, Recipe, Tag


class IngredientFilter(rest_framework.FilterSet):
    """Фильтр ингредиентов."""

    name = rest_framework.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(rest_framework.FilterSet):
    """Фильтр рецептов."""

    author = rest_framework.CharFilter()
    is_favorited = rest_framework.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='get_is_in_shopping_cart'
    )
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )

    def get_is_favorited(self, queryset, name, value):
        """Queryset для избранного."""
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        """Queryset для покупок."""
        if value and self.request.user.is_authenticated:
            return queryset.filter(cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)
