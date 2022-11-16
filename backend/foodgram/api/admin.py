from django.contrib import admin

from users.models import Follow

from .models import (Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag,
                     TagRecipe)


class TagInline(admin.TabularInline):
    """Добавление тегов в админку рецептов."""

    model = TagRecipe
    extra = 0


class IngredientsInline(admin.TabularInline):
    """Добавление ингредиентов в админку рецептов."""

    model = IngredientAmount
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    """Админка рецептов."""

    inlines = (TagInline, IngredientsInline)
    list_display = (
        'id', 'name', 'author', 'cooking_time', 'image', 'pub_date',
    )
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'author__username',)
    list_filter = ('tags', 'pub_date',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов."""

    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientAmountAdmin(admin.ModelAdmin):
    """Админка количества ингредиентов."""

    list_display = ('id', 'ingredient', 'recipe', 'amount',)
    list_display_links = ('id', 'ingredient',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    """Админка тегов."""

    list_display = ('id', 'name', 'slug', 'color',)
    list_display_links = ('id', 'name',)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Cart)
admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagRecipe)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
