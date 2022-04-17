# request -> response / request handler / action
import os
import hashlib

from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template import *
import cloudinary
from marketplace.settings import BASE_DIR
from marketapp.forms import *
from marketapp.models import *
from dotenv import load_dotenv
load_dotenv()


# Set up cloudinary
cloudinary.config(
    cloud_name=os.getenv("C_NAME"),
    api_key=os.getenv("C_KEY"),
    api_secret=os.getenv("C_SECRET"),
)

# Check if the current session is valid
def check_validation(request):
    if not request.COOKIES.get("session_token"):
        return None
    
    session = SessionToken.objects.filter(
        session_token=request.COOKIES.get("session_token")
    ).first()
    return session.user if session else None

def welcome(request):
    user = check_validation(request)
    if not user:
        return render(request, "welcome.html", {"path": request.path})
    
    return render(request, "dashboard.html", {"userinfo": user, "path": request.path})

def signup(request):
    user = check_validation(request)
    if request.method != "POST":
        if user:
            return redirect("/feed/")
        else:
            signup_form = SignUpForm()
            return render(request, "signup.html", {"signup_form": signup_form, "path": request.path})
    else:
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data["username"]
            name = signup_form.cleaned_data["first_name"]
            email = signup_form.cleaned_data["email"]
            password = signup_form.cleaned_data["password"]

            user = User.objects.create_user(
                username = username,
                first_name = name,
                email = email,
                password = password
            )
            user.save()

            # Send an email to the user on successful sign up
            """send_mail(
                f"Welcome to Digital Artwork Platform",
                f"Dear {name},\n\nThank you for registration on dap.com.\n\nDAP",
                settings.EMAIL_HOST_USER,
                [email,],
                fail_silently=False,
            )"""
            return render(request, "success.html", {"path": request.path})
        else:
            return render(request, "signup.html", {"context": signup_form.errors, "path": request.path})

def login(request):
    exist_user = check_validation(request)
    if exist_user:
        redirect("/feed/")
    if request.method != "POST":
        form = LoginForm()
        return render(request, "login.html", {"path": request.path})
    
    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(
            request,
            "login.html",
            {
                "context": "Could not log you in. Please fill all the fields correctly",
                "path": request.path
            },
        )
    
    username = form.cleaned_data.get("username")
    password = form.cleaned_data.get("password")
    user = User.objects.filter(username=username).first()
    if not user:
        return render(
            request, "login.html", {"context": "Username not registered", "path": request.path}
        )
    if not user.check_password(password):
        print(password)
        return render(
            request,
            "login.html",
            {"context": "Your password is not correct! Try Again!", "path": request.path},
        )
    
    token = SessionToken(user=user)
    token.create_token()
    token.save()
    response = redirect("/feed/")
    response.set_cookie(key="session_token", value=token.session_token)
    return response

def post(request):
    user = check_validation(request)
    if (not user) or (request.method not in ['GET', 'POST']):
        return redirect("/login/")
        
    if request.method == "GET":
        form = PostForm()
        return render(request, "post-upload.html", {"form": form, "path": request.path})
    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if not form.is_valid():
            return redirect("/post/")

        # first save the image locally
        image = form.cleaned_data.get("image")
        caption = form.cleaned_data.get("caption")
        post = PostModel(user=user, image=image, caption=caption)
        post.save()
        # check the validity of the image
        path = f"{BASE_DIR}{post.image.url}"
        with open(path, "rb") as f:
            # hash the image and find hash duplication in the database
            val = hashlib.sha256(f.read()).hexdigest()
            if PostModel.objects.filter(hash=val).exists():
                post.delete()
                return render(request, "post-upload.html", {"form": form, "path": request.path, "context": "Image already exists"})
            post.hash = val
            # Upload to cloudinary API
            uploaded = cloudinary.uploader.upload(path)
            post.image_url = uploaded["secure_url"]
            post.save()
            print(post.user.first_name)
            return render(request, "post-success.html", {"post": post, "path": request.path})
           
def feed(request):
    """
    Get the posts of all the users
    """
    user = check_validation(request)
    if not user:
        return redirect("/login/")

    msg = request.session.pop("form_message", {})
    if msg:
        messages.add_message(request, msg.get("level", messages.INFO), msg.get("text", "default message"))
    
    posts = PostModel.objects.all().order_by("-created_on")
    for post in posts:
        existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
        post.has_liked = True if existing_like else False
        comments = CommentModel.objects.filter(post_id=post.id)
        for comment in comments:
            existing_upvote = UpvoteModel.objects.filter(
                comment_id=comment.id,
            ).first()
            comment.has_upvoted = True if existing_upvote else False
    return render(request, "feed.html", {"posts": posts, "path": request.path})

def manage(request):
    """
    Manage the posts of the user
    """
    user = check_validation(request)
    if not user:
        return redirect("/login/")
    if request.method == "POST":
        return redirect("/manage/")
 
    msg = request.session.pop("form_message", {})
    if msg:
        messages.add_message(request, msg.get("level", messages.INFO), msg.get("text", "default message"))
        
    posts = PostModel.objects.filter(user=user).order_by("-created_on")
    for post in posts:
        existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
        post.has_liked = True if existing_like else False
    return render(request, "manage.html", {"posts": posts, "path": request.path})

def transfer(request):
    """
    Owner approves the transfer of the artwork
    Create a new trasaction, awaiting buyer payment
    """
    user = check_validation(request)
    if not user:
        return redirect("/login/")
    elif request.method != "POST":
        return redirect("/feed/")
    
    request.session['form_message'] = {
        "level": messages.ERROR,
        "text": "Error: Failed to approve the request!"
    }
    
    form = TransferForm(request.POST)
    if form.is_valid():
        # a transfer request, 
        # from the current user (as transaction sender) 
        # to the post author (as transaction receiver)
        sender_username = form.data.get("user")
        post_id = form.data.get("id")
        like = LikeModel.objects.filter(post_id=post_id, username=sender_username).first()
        if like.confirmed:
            request.session['form_message'] = {
                "level": messages.ERROR,
                "text": f"Error: You have already approved the request to buyer {sender_username}!"
            }
            return redirect('/manage/')
            
        print(f"auth: {user.username == sender_username}, where {user.username}, {sender_username}, {post_id}")
        sender = User.objects.get(username=sender_username)
        post = PostModel.objects.get(id=post_id)
        existed = TransactionModel.objects.filter(post=post, sender=sender, receiver=post.user, completed=False)
        if existed:
            request.session['form_message'] = {
                "level": messages.ERROR,
                "text": f"Error: You have already approved the request to buyer {sender_username}!"
            }
            return redirect('/manage/')
        TransactionModel.objects.create(post=post, sender=sender, receiver=post.user)
        like.confirmed = True
        like.save()
        request.session['form_message'] = {
            "level": messages.SUCCESS,
            "text": "Success: request approved!"
        }
    return redirect('/manage/')

def transact(request):
    """
    Get the transactions of the user
    """
    user = check_validation(request)
    if not user:
        return redirect("/login/")
    if request.method not in ["GET", "POST"]:
        return redirect("/feed/")
    if request.method == "GET":
        msg = request.session.pop("form_message", {})
        if msg:
            messages.add_message(request, msg.get("level", messages.INFO), msg.get("text", "default message"))
        transactions = user.as_sender.all() | user.as_receiver.all()
        return render(request, "transact.html", {"transactions": transactions, "userinfo": user, "path": request.path})
    else:
        form = TransactionForm(request.POST)
        # sender is the current user
        # receiver is the current post author
        print(f"flag: {form.is_valid()}, form: {form}, req: {request.POST}")
        request.session['form_message'] = {
            "level": messages.ERROR,
            "text": "Error: failed to transact! [form invalid]"
        }
        if form.is_valid():
            post = form.cleaned_data.get("post")
            transaction = TransactionModel.objects.filter(post=post, sender=user, completed=False).first()
            request.session['form_message']['text'] = "Error: failed to transact! [no such transaction]"
            if transaction:
                # transfer the ownership of the post to the receiver
                transaction.confirmed = True
                transaction.save()
                post.user = user
                post.save()
                # mark the like as completed
                like = LikeModel.objects.filter(post=post, user=user).first()
                if like:
                    like.delete()
                request.session['form_message'] = {
                    "level": messages.SUCCESS,
                    "text": "Success: transaction completed!"
                }
        return redirect("/transact/")

def like(request):
    """
    Like the post
    """
    user = check_validation(request)
    if not user:
        return redirect("/login/")
    elif request.method != "POST":
        return redirect("/feed/")
    
    form = LikeForm(request.POST)
    if not form.is_valid():
        return redirect("/feed/")
    
    post_id = form.cleaned_data.get("post").id
    post = PostModel.objects.get(id=post_id)
    if post.user == user:
        request.session['form_message'] = {
            "level": messages.ERROR,
            "text": "Error: You cannot request your own post!"
        }
        return redirect("/feed")
        
    existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
    # If user has already registered a like, then delete it
    if existing_like:
        existing_like.delete()
        request.session['form_message'] = {
            "level": messages.SUCCESS,
            "text": "Success: You have deleted the request!"
        }
    else:
        # Otherwise create a like
        like = LikeModel.objects.create(post_id=post_id, user=user)
        send_mail(
            f"Updates to Your Artwork {like.post.caption}",
            f"Dear {like.post.user.first_name},\n\nYour Artwork {like.post.caption}: {like.post.image_url} is liked by buyer {like.user.first_name}: {like.user.email}.\nYou can check it out at dap.com.\n\nDAP",
            settings.EMAIL_HOST_USER,
            [like.post.user.email,],
            fail_silently=False,
        )
        request.session['form_message'] = {
            "level": messages.SUCCESS,
            "text": "Success: You have sent the request, please wait for author's response!"
        }
    return redirect("/feed")

def comment(request):
    """
    Comment on the post
    """
    user = check_validation(request)
    if not user:
        return redirect("/login")
    elif request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get("post").id
            comment_text = form.cleaned_data.get("comment_text")
            # Create a CommentModel object and save it in the database
            comment = CommentModel.objects.create(
                user=user, post_id=post_id, comment_text=comment_text
            )
            comment.save()
            # Send email if the one who liked was someone other than the
            # one who posted the comment
            """if comment.user.email != comment.post.user.email:
                send_mail(
                    f"New comment from {comment.user.first_name} on Your Post {comment.post.caption}",
                    f"Dear {comment.post.user.first_name}:\n\n{comment.user.first_name}: {comment_text}\n\nCheck it out at dap.com\n\n DAP",
                    settings.EMAIL_HOST_USER,
                    [comment.post.user.email],
                    fail_silently=False,
                )"""
        return redirect("/feed")

# View to log the user out
def logout(request):
    user = check_validation(request)
    if user:
        response = redirect("/")
        response.delete_cookie(key="session_token")
        return response
    else:
        return redirect("/login/")

# Upvote view
def upvote(request):
    user = check_validation(request)
    if not user:
        return redirect("/login/")
    if request.method == "POST":
        form = UpvoteForm(request.POST)
        if not form.is_valid():
            return redirect("/feed/")
        comment_id = form.cleaned_data.get("comment").id
        existing_upvote = UpvoteModel.objects.filter(
            comment_id=comment_id, user=user
        ).first()
        # If user has already registered an upvote, then delete it
        if existing_upvote:
            existing_upvote.delete()
        else:
            # Otherwise create an upvote
            post = UpvoteModel.objects.create(comment_id=comment_id, user=user)
            print(post)
            print((UpvoteModel.objects.filter(comment=comment_id)))
            post.save()
        return redirect("/feed/")
            
def feed_by_user(request, name):
    user = check_validation(request)
    if not user:
        return redirect("/login/")
    usern = User.objects.all().filter(first_name=name).first()
    # print(usern)
    posts = PostModel.objects.filter(user=usern).order_by("-created_on")
    for post in posts:
        existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
        post.has_liked = True if existing_like else False
        comments = CommentModel.objects.filter(post_id=post.id)
        for comment in comments:
            existing_upvote = UpvoteModel.objects.filter(
                comment_id=comment.id,
            ).first()
            # print(f"upvote: {existing_upvote}")
            comment.has_upvoted = True if existing_upvote else False
    return render(request, "feed.html", {"posts": posts, "path": request.path})

def feed_by_post(request, post_id):
    user = check_validation(request)
    if not user:
        return redirect("/login/")
    post = PostModel.objects.all().get(id=eval(post_id))
    if post:
        existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
        post.has_liked = True if existing_like else False
        comments = CommentModel.objects.filter(post_id=post.id)
        for comment in comments:
            existing_upvote = UpvoteModel.objects.filter(
                comment_id=comment.id,
            ).first()
            comment.has_upvoted = True if existing_upvote else False
    return render(request, "feed.html", {"posts": [post], "path": request.path})