from PIL import Image
from django.contrib.auth.models import User
from django.db import models

STATUS = ((0, "Draft"), (1, "Publish"))


# распределение прав в джанго
# нужно с помощью сигнала(pre_save) оотменить создание новыого поста
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    cover = models.ImageField(upload_to='images/', blank=True)  # blank=True
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} {self.id}"

    def post_ratings(self):
        """
        Считает лайки и дизлайки для поста по id
        """
        try:
            _rating = PostRatingModel.objects.filter(post=self)
            return {
                "dislikes": _rating.filter(is_like=False).count(),
                "likes": _rating.filter(is_like=True).count()
            }
        except Exception as error:
            return {"dislikes": 0, "likes": 0}

    def is_user_post_ratings(self, user: User) -> int:
        """
        Смотрит, поставил ли я пользователь или дизлайк этому посту
        """
        _rating = PostRatingModel.objects.filter(post=self, user=user)
        if _rating.count() < 1:
            return 0
        else:
            obj = _rating[0]
            if obj.is_like is True:
                return 1
            else:
                return -1

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("post_detail")


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.name)


class Img(models.Model):
    title = models.TextField()
    description = models.TextField('Описание', max_length=300000000000)
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title


class PostRatingModel(models.Model):
    """
    Модель Рейтинга Поста
    """
    user = models.ForeignKey(
        editable=True,
        blank=True,
        null=True,
        default=None,
        verbose_name='Пользователь',
        help_text='<small class="text-muted">ForeignKey</small><hr><br>',

        to=User,
        on_delete=models.SET_NULL,
    )
    post = models.ForeignKey(
        editable=True,
        blank=True,
        null=True,
        default=None,
        verbose_name='Пост',
        help_text='<small class="text-muted">ForeignKey</small><hr><br>',

        to=Post,
        on_delete=models.CASCADE,
    )
    is_like = models.BooleanField(
        editable=True,
        blank=True,
        null=False,
        default=False,
        verbose_name='Рейтинг',
        help_text='<small class="text-muted">BooleanField</small><hr><br>',
    )

    class Meta:
        app_label = 'blog'
        ordering = ('-post', 'user')
        verbose_name = 'Лайк поста'
        verbose_name_plural = 'Лайки постов'

    def __str__(self):
        return f"{self.user}({self.id}) | {'Лайкнул' if self.is_like else 'Дизлайкнул'} | {self.post.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(
        default='avatar.jpg',  # default avatar
        upload_to='profile_avatars'  # dir to store the image
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.avatar.path)
