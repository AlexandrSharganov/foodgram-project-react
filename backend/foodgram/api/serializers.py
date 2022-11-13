from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import User
from users.serializers import UserSerializer

from .models import (Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag,
                     TagRecipe)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAmountCreateSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
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
        username = self.context['request'].user
        if not username.is_authenticated:
            return False
        user = get_object_or_404(User, username=username)
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        username = self.context['request'].user
        if not username.is_authenticated:
            return False
        user = get_object_or_404(User, username=username)
        return Cart.objects.filter(user=user, recipe=obj).exists()

    def create(self, validated_data):
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
    author = UserSerializer(read_only=True)
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
        username = self.context['request'].user
        if not username.is_authenticated:
            return False
        user = get_object_or_404(User, username=username)
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        username = self.context['request'].user
        if not username.is_authenticated:
            return False
        user = get_object_or_404(User, username=username)
        return Cart.objects.filter(user=user, recipe=obj).exists()
