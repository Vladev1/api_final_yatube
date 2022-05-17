from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    """Какие поля модели Пост отображаются."""
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'group', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Какие поля модели Коммент отображаются."""
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    """Какие поля модели Группа отображаются."""
    class Meta:
        fields = ('title','slug', 'description' )
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    """Какие поля модели Подписок отображаются."""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            ),# Исключаем из подбора самого юзера
        )

    def validate_following(self, following):
        if self.context.get('request').user == following:
            raise serializers.ValidationError(
                'Невозможно подписаться на себя.')
        return following # Ошибка при попытке подписаться

