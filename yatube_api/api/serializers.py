from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Post, Group, Comment, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False,
        allow_null=True
    )
    image = serializers.ImageField(required=False, allow_null=True, use_url=True) # use_url=True is good practice

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created', 'post')
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        # UniqueTogetherValidator is implicitly handled by model's UniqueConstraint
        # but can be added for more explicit API error messages if desired.
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=Follow.objects.all(),
        #         fields=('user', 'following'),
        #         message="Вы уже подписаны на этого пользователя."
        #     )
        # ]


    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError("Нельзя подписаться на самого себя.")
        return value

    def validate(self, data):
        # data['following'] will exist due to field definition
        # user is derived from default or context
        user = self.context['request'].user
        following_user = data['following'] # This is already a User instance due to SlugRelatedField

        if Follow.objects.filter(user=user, following=following_user).exists():
            raise serializers.ValidationError(
                {"following": "Вы уже подписаны на этого пользователя."} # Or a non-field error
            )
        return data