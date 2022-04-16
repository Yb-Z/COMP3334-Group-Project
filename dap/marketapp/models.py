import uuid
from django.db import models

class UserModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, null=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=120, unique=True)
    password = models.CharField(max_length=40)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class SessionToken(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=120)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    
    def create_token(self):
        self.session_token = uuid.uuid4()

class PostModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    # belonged = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user_images")
    hash = models.CharField(max_length=256)
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def like_count(self):
        return len(LikeModel.objects.filter(post=self))

    @property
    def comments(self):
        return CommentModel.objects.filter(post=self).order_by("created_on")

class LikeModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name="likes")
    confirmed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class CommentModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    # likes = models.ForeignKey(LikeModel)
    comment_text = models.CharField(max_length=555)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # has_upvoted = False

    @property
    def upvote_count(self):
        return len(UpvoteModel.objects.filter(comment=self))

class UpvoteModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class TransactionModel(models.Model):
    # A wants to buy B's post
    # A sends a request
    # B approves the request
    # A start a transaction 
    # system completes the ownership transfer
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name="transactions")
    # A is the sender
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="as_sender")
    # B is the receiver
    receiver = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="as_receiver")
    amount = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)