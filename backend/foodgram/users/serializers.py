from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Recipe
from api.serializers import AddRecipeSerializer

from .models import Follow, User


class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователей."""

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'password'
        )


class UserSerializer(UserSerializer):
    """Сериализатор получения пользователей."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Метод определения подписки на пользователей."""
        if self.context:
            username = self.context['request'].user
            if not username.is_authenticated or obj.username == username:
                return False
            user = get_object_or_404(User, username=username)
            author = get_object_or_404(User, username=obj.username)
            return Follow.objects.filter(user=user, author=author).exists()
        return False


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


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор создания подписки."""

    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
            )
        ]

    def validate(self, data):
        """Валидируем подписку на себя."""
        if data.get('user') == data.get('author'):
            raise serializers.ValidationError(
                'Нельзя подписаться на себя!')
        return data
