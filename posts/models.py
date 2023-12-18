from django.db import models
from django.contrib.auth import get_user_model
from common.models import TimeStampModel
import uuid

User = get_user_model()

# Models here.
class Tag(TimeStampModel):
    title = models.CharField(unique=True, max_length=100)

    def __str__(self) -> str:
        return "#" + self.title.strip()
    
    def clean(self) -> None:
        self.title = self.title.lower()
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

class Post(TimeStampModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/post_images')
    caption = models.TextField()
    like_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, through='PostTag', related_name='posts')

    def __str__(self) -> str:
        return str(self.id) + " posted by " + str(self.user_id)
    
class PostLike(TimeStampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post_id', 'user_id'],
                name = 'unique_user_post_like',
            )
        ]

    def __str__(self) -> str:
        return str(self.post_id) + " liked by " + str(self.user_id)
    
class Comment(TimeStampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies')

class PostTag(TimeStampModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tag_id', 'post_id'],
                name='unique_post_tag',
            )
        ]