from rest_framework import serializers
from .models import User, Category, Post
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    categories_names = serializers.StringRelatedField(source='categories', many=True, read_only=True)
    categories = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True
    )

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'categories', 'categories_names', 'date', 'image']
        read_only_fields = ['id', 'date', 'author_username', 'categories_names']

    def create(self, validated_data):
        category_names_data = validated_data.pop('categories')

        with transaction.atomic():
            post = Post.objects.create(**validated_data)

            category_objects = []
            for category_name in category_names_data:
                category_name = category_name.strip()
                if category_name:
                    category, _ = Category.objects.get_or_create(name=category_name)
                    category_objects.append(category)

            post.categories.set(category_objects)

        return post

    def update(self, instance, validated_data):
        if 'categories' in validated_data:
            category_names_data = validated_data.pop('categories')

            with transaction.atomic():
                category_objects = []
                for category_name in category_names_data:
                    category_name = category_name.strip()
                    if category_name:
                        category, _ = Category.objects.get_or_create(name=category_name)
                        category_objects.append(category)
                instance.categories.set(category_objects)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
