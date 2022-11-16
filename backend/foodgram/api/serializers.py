from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserSerializer

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User, Follow
from users.serializers import MyUserSerializer

from .models import (Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag,
                     TagRecipe)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор количества ингредиентов."""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAmountCreateSerializer(serializers.ModelSerializer):
    """Сериализатор количества ингредиентов при создании рецепта."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецепта."""

    image = Base64ImageField()
    author = MyUserSerializer(read_only=True)
    ingredients = IngredientAmountCreateSerializer(
        source='ingredientamount_set',
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients',
                  'tags', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        """Определение избранных рецептов."""
        username = self.context['request'].user
        user = get_object_or_404(User, username=username)
        return (username.is_authenticated
                and Favorite.objects.filter(user=user, recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        """Определение рецептов для покупки."""
        username = self.context['request'].user
        user = get_object_or_404(User, username=username)
        return (username.is_authenticated
                and Cart.objects.filter(user=user, recipe=obj).exists())

    def validate_ingredients(self, value):
        """Метод валидации ингредиентов в рецепте."""
        ingredients_list = []
        ingredients = value
        if len(ingredients) == 0:
            raise serializers.ValidationError(
                'Без ингредиентов нельзя!')
        for ingredient in ingredients:
            check_object = ingredient.get('id')
            if check_object in ingredients_list:
                raise serializers.ValidationError(
                    'Продукты в рецепте повторяются!')
            ingredients_list.append(check_object)
        return value

    def validate_tags(self, value):
        """Метод валидации тегов в рецепте."""
        tags_list = []
        tags = value
        if len(tags) == 0:
            raise serializers.ValidationError(
                'Без тегов нельзя!')
        for tag in tags:
            tag_to_check = get_object_or_404(Ingredient, id=tag.id)
            if tag_to_check in tags_list:
                raise serializers.ValidationError(
                    'Данный тэг уже есть в рецепте!')
            tags_list.append(tag_to_check)
        return value

    def create(self, validated_data):
        """Метод создания рецептов."""
        ingredients = validated_data.pop('ingredientamount_set')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            TagRecipe.objects.create(tag=tag, recipe=recipe)
        recipe_ingredients = [
            IngredientAmount(
                ingredient=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(recipe_ingredients)
        return recipe

    def update(self, instance, validated_data):
        """Метод редактирования рецептов."""
        ingredients = validated_data.pop('ingredientamount_set')
        tags = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientAmount.objects.filter(recipe=instance).delete()
        for tag in tags:
            TagRecipe.objects.create(tag=tag, recipe=instance)
        recipe_ingredients = [
            IngredientAmount(
                ingredient=ingredient['id'],
                recipe=instance,
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(recipe_ingredients)
        instance.save()
        return instance


class RecipeReadSerializer(serializers.ModelSerializer):
    author = MyUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        source='ingredientamount_set',
        many=True
    )
    image = Base64ImageField()
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients',
                  'tags', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        """Определение избранных рецептов."""
        user = self.context['request'].user
        return (not user.is_anonymous
                and Favorite.objects.filter(user=user, recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        """Определение рецептов для покупки."""
        user = self.context['request'].user
        return (not user.is_anonymous
                and Cart.objects.filter(user=user, recipe=obj).exists())


class AddRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов для включения их в список избранного и покупок."""

    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'cooking_time')


class FollowListSerializer(UserSerializer):
    """Сериализатор списка подписчиков."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def get_is_subscribed(self, obj):
        """Метод определения подписки на пользователей."""
        if self.context:
            username = self.context['request'].user
            if not username.is_authenticated or obj.username == username:
                return False
            user = get_object_or_404(User, username=username)
            author = get_object_or_404(User, username=obj.username)
            return Follow.objects.filter(user=user, author=author).exists()
        return True

    def get_recipes(self, obj):
        """Получаем рецепты."""
        request = self.context.get('request')
        try:
            limit = request.GET.get('recipes_limit')
        except AttributeError:
            limit = False
        author = get_object_or_404(User, username=obj.username)
        recipes = Recipe.objects.filter(author=author)
        if limit:
            recipes = recipes.all()[:int(limit)]
        return AddRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        """Считаем рецепты."""
        author = get_object_or_404(User, username=obj.username)
        return Recipe.objects.filter(author=author).count()
