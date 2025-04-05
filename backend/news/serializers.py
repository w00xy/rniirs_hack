from rest_framework import serializers

from .models import *
from users.models import CustomUser
from django.conf import settings


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)

    def save(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        instance.save()
        return instance


class NewsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    date = serializers.DateField(required=False)
    category_id = serializers.IntegerField()
    is_confirmed = serializers.BooleanField(default=False, required=False)
    author_id = serializers.IntegerField()

    # Добавляем поле author как "read-only" и динамическое
    author = serializers.SerializerMethodField()

    # Поле category
    category = serializers.SerializerMethodField()

    def get_author(self, obj):
        # Здесь мы извлекаем объект автора по author_id
        try:
            author = CustomUser.objects.get(id=obj.author_id)  # Замените `User` на вашу модель
            return {
                "id": author.id,
                "login": author.login,
            }
        except CustomUser.DoesNotExist:
            return None  # Если автора нет, возвращаем None

    def get_category(self, obj):
        try:
            category = Category.objects.get(id=obj.category_id)  # Замените `Category` на вашу модель
            return {
                "id": category.id,
                "title": category.title,
            }
        except Category.DoesNotExist:
            return None

    def to_representation(self, instance):
        # Используем стандартное поведение сериализатора и добавляем поле author
        representation = super().to_representation(instance)
        representation['author'] = self.get_author(instance)
        representation['category'] = self.get_category(instance)
        return representation

    def save(self, validated_data):
        return News.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        instance.save()
        return instance


class NewsParsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    date = serializers.DateField(required=False)
    category = serializers.CharField()
    is_confirmed = serializers.BooleanField(default=True, required=False)
    author = serializers.CharField(required=False)

    def save(self, validated_data):
        return News.objects.create(title=validated_data.get("title"),
                                   description=validated_data.get("description"),
                                   date=validated_data.get("date"),
                                   category=Category.objects.get_or_create(**validated_data.get("category")),
                                   is_confirmed=validated_data.get("is_confirmed"),
                                   author=CustomUser.objects.get_or_create(login=validated_data.get("author"), password=settings.PARSER_PASSWORD),
                                   )

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        instance.save()
        return instance