from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.constraints import UniqueConstraint

User = get_user_model()


class Group(models.Model):
    """Модель для групп сообщества."""
    title = models.CharField('Заголовочек', max_length=200)
    slug = models.SlugField('Слаг адрес', unique=True)
    description = models.TextField('Описание группы')

    def __str__(self):
        return self.title


class Post(models.Model):
    """Посты сообщества."""
    text = models.TextField('Мысли великих')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Могучие группы'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Коммментарии сообщества к постам."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор поста'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Пост'
    )
    text = models.TextField('Текст коммента')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Follow(models.Model):
    """Подписки на авторов."""
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Подписка',
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follower'
            ),
        )
