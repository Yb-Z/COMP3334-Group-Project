# request -> response / request handler / action
import os
from datetime import datetime

from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
import cloudinary
# from clarifai.rest import ClarifaiApp
from marketplace.settings import BASE_DIR
from marketapp.forms import *
from marketapp.models import *
from dotenv import load_dotenv
load_dotenv()

# Set up clarifai and define a model
# app = ClarifaiApp(api_key="api_key_str")
# model = app.models.get("general-v1.3")
# Set up cloudinary
cloudinary.config(
    cloud_name=os.getenv("C_NAME"),
    api_key=os.getenv("C_KEY"),
    api_secret=os.getenv("C_SECRET"),
)

def welcome(request):
    user = check_validation(request)
    if not user:
        return render(request, "welcome.html")
    
    return render(request, "dashboard.html", {"user": user})

# View to the home page
def signup(request):
    user = check_validation(request)
    if request.method == "POST":
        signup_form = SignUpForm(request.POST)

        if signup_form.is_valid():
            # Extract the details from the form
            username = signup_form.cleaned_data["username"]
            name = signup_form.cleaned_data["name"]
            email = signup_form.cleaned_data["email"]
            password = signup_form.cleaned_data["password"]

            # Saving data to the database
            user = UserModel(
                name=name,
                password=make_password(password),
                email=email,
                username=username,
            )
            user.save()

            # Send an email to the user on successful sign up
            # send_mail(
            #     "Welcome",
            #     "Thanks for being a part of my Digital Artwork Platform. You are awesome :)",
            #     "digitalartworkplatform.com.com",
            #     [email],
            #     fail_silently=False,
            # )
            # To prevent header injection https://docs.djangoproject.com/es/1.11/topics/email/#preventing-header-injection
            # except BadHeaderError:
            # return HttpResponse('Invalid header found')
            # Show the success page
            return render(request, "success.html")
        else:
            print("Error occured while signing up")
            return render(request, "signup.html", {"context": signup_form.errors})
    else:
        exist_user = check_validation(request)
        if exist_user:
            redirect("/feed")
        signup_form = SignUpForm()
    return render(request, "signup.html", {"signup_form": signup_form})

# View for the login page
def login(request):
    exist_user = check_validation(request)
    if exist_user:
        redirect("/feed")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = UserModel.objects.filter(username=username).first()
            if user:
                if check_password(password, user.password):
                    # User is Valid
                    print("Valid")
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect("/feed/")
                    response.set_cookie(key="session_token", value=token.session_token)
                    return response
                else:
                    # User is not valid
                    print("Invalid User")
                    return render(
                        request,
                        "login.html",
                        {"context": "Your password is not correct! Try Again!"},
                    )
            else:
                # User does not exist'
                print("User doesnt exist")
                return render(
                    request, "login.html", {"context": "Username not registered"}
                )
        else:
            # Form is not Valid
            print("Invalid Form")
            return render(
                request,
                "login.html",
                {
                    "context": "Could not log you in. Please fill all the fields correctly"
                },
            )
    else:
        form = LoginForm()
    return render(request, "login.html")

# Check if the current session is valid
def check_validation(request): # TODO: Check this!
    if request.COOKIES.get("session_token"):
        session = SessionToken.objects.filter(
            session_token=request.COOKIES.get("session_token")
        ).first()
        if session:
            return session.user
    else:
        return None

# Post View
def post(request):
    user = check_validation(request)
    if not user:
        return redirect("/login/")
    elif request.method not in ['GET', 'POST']:
        return redirect("/login/")
        
    if request.method == "GET":
        form = PostForm()
        return render(request, "post-upload.html", {"form": form})
    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get("image")
            caption = form.cleaned_data.get("caption")
            post = PostModel(user=user, image=image, caption=caption)
            post.save()
            path = BASE_DIR + post.image.url
            # Upload to cloudinary API
            uploaded = cloudinary.uploader.upload(path)
            # print((uploaded["secure_url"]))
            post.image_url = uploaded["secure_url"]
            post.save()
            return render(request, "post-success.html", {"post": post})

# Main feed View
def feed(request):
    # Validates if the user is logged in or not
    user = check_validation(request)
    if not user:
        return redirect("/login/")

    posts = PostModel.objects.all().order_by("-created_on")
    for post in posts:
        existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
        post.has_liked = True if existing_like else False
        comments = CommentModel.objects.filter(post_id=post.id)
        for comment in comments:
            existing_upvote = UpvoteModel.objects.filter(
                comment_id=comment.id,
            ).first()
            print(f"upvote: {existing_upvote}")
            comment.has_upvoted = True if existing_upvote else False
    return render(request, "feed.html", {"posts": posts})

def manage(request):
    # Validates if the user is logged in or not
    user = check_validation(request)
    if not user:
        return redirect("/login/")
    if request.method == "POST":
        return redirect("/manage/")

    users = UserModel.objects.all().exclude(email=user.email)
    posts = PostModel.objects.filter(user=user).order_by("-created_on")
    for post in posts:
        existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
        post.has_liked = True if existing_like else False
    return render(request, "manage.html", {"posts": posts, "users":users})

def transfer(request):
    user = check_validation(request)
    if not user:
        return redirect("/login/")
    elif request.method != "POST":
        return redirect("/feed/")
    
    form = TransferForm(request.POST)
    print(f"form: {form.is_valid()}, req: {request.POST}")
    if form.is_valid():
        dest_email = form.data.get("user")
        post_id = form.data.get("id")
        dest_user = UserModel.objects.get(email=dest_email)
        print(f"{dest_email} {post_id} {dest_user}")
        PostModel.objects.filter(id=post_id).update(user=dest_user)
    
    return redirect('/manage')

# Like view
def like(request):
    user = check_validation(request)
    if not user:
        return redirect("/login/")
    elif request.method != "POST":
        return redirect("/feed/")
    
    form = LikeForm(request.POST)
    if form.is_valid():
        post_id = form.cleaned_data.get("post").id
        existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
        # If user has already registered a like, then delete it
        if existing_like:
            existing_like.delete()
        else:
            # Otherwise create a like
            post = LikeModel.objects.create(post_id=post_id, user=user)
            # Send email if the one who liked was someone other than the
            # one who posted the comment
            # if post.user.email != post.post.user.email:
            # ! for testing
            if True:
                send_mail(
                    f"Updates to Your Artwork {post.post.caption}",
                    f"Dear {post.post.user.username},\n\nYour Artwork {post.post.caption}: {post.post.image_url} is liked by buyer {post.user.name}: {post.user.email}.\nYou can check it out at digitalartworkplatform.com.\n\nDAP",
                    settings.EMAIL_HOST_USER,
                    [post.post.user.email,],
                    fail_silently=False,
                )
        return redirect("/feed/")

# Comment View
def comment(request):
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
            # if comment.user.email != comment.post.user.email:
            #     send_mail(
            #         "Heyy, You got a comment from " + comment.user.name,
            #         "Check it out at digitalartworkplatform.com.com",
            #         "digitalartworkplatform.com.com",
            #         [comment.post.user.email],
            #         fail_silently=False,
            #     )
            return redirect("/feed")
        else:
            return redirect("/feed/")

# View to log the user out
def logout(request):
    user = check_validation(request)
    if user:
        response = redirect("/")
        response.delete_cookie(key="session_token")
        return response
    else:
        return redirect("/feed/")

# Upvote view
def upvote(request):
    user = check_validation(request)
    if not user:
        return redirect("/login/")
    elif request.method == "POST":
        form = UpvoteForm(request.POST)
        if form.is_valid():
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
        else:
            print("Form not valid")
            return redirect("/feed/")

def func(request, username):
    user = check_validation(request)
    if not user:
        return redirect("/login/")
    
    usern = UserModel.objects.all().filter(username=username)
    print(usern)
    posts = (
        PostModel.objects.all().filter(user=usern).order_by("-created_on")
    )
    for post in posts:
        existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
        comments = CommentModel.objects.filter(post_id=post.id)
        if comments:
            for comment in comments:
                existing_upvote = UpvoteModel.objects.filter(
                    comment=comment.id
                ).first()

                if existing_upvote:
                    comment.has_upvoted = True
        # If user has liked the post set the boolean value to True
        if existing_like:
            post.has_liked = True
    return render(request, "feed.html", {"posts": posts})