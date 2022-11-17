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
        'id',
        'name',
        'author',
    )
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'author__username',)
    list_filter = ('name', 'author', 'tags',)
    readonly_fields = ('count_in_favorite',)
    empty_value_display = '-пусто-'

    def count_in_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    count_in_favorite.short_description = 'Сколько раз добавлен в избранное'


class IngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов."""

    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('name',)
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
