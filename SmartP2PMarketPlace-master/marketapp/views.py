# request -> response / request handler / action
import os
from datetime import datetime

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.shortcuts import redirect, render
import cloudinary
import cloudinary.api
import cloudinary.uploader
from clarifai.rest import ClarifaiApp
from marketplace.settings import BASE_DIR
from marketapp.forms import *
from marketapp.models import *

# Set up clarifai and define a model
# app = ClarifaiApp(api_key="api_key_str")
# model = app.models.get("general-v1.3")
# Set up cloudinary
# cloudinary.config(
#     cloud_name="cloudinary_cloud_name",
#     api_key="cloudinary_api_key",
#     api_secret="cloudinary_secret",
# )

def welcome(request):
    return render(request, "welcome.html")

# View to the home page
def signup(request):
    today = datetime.now()
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
            #     "Thanks for being a part of my Smart P2P Marketplace. You are awesome :)",
            #     "smartp2pmarketplace.com",
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
        signup_form = SignUpForm()

    # Render the home page
    return render(request, "signup.html", {"signup_form": signup_form})

# View for the login page
def login(request):
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

# The view user has after logging in
# def feed(request):
#     return render(request,'feed.html')

# Post View
def feed(request):
    user = check_validation(request)
    if user:
        if request.method == "GET":
            form = PostForm()
            return render(request, "feed.html", {"form": form})
        elif request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get("image")
                caption = form.cleaned_data.get("caption")
                post = PostModel(user=user, image=image, caption=caption)
                post.save()
                # print 'Image saved in the db'
                path = os.path.join(BASE_DIR, post.image.url)
                # Upload to cloudinary API
                uploaded = cloudinary.uploader.upload(path)
                print((uploaded["secure_url"]))
                post.image_url = uploaded["secure_url"]
                post.save()
                return render(request, "feed_new.html", {"post": post})
        else:
            return redirect("/login/")
    else:
        # If the user is not logged in
        return redirect("/login/")

# Main feed View
def feed_main(request):
    # Validates if the user is logged in or not
    user = check_validation(request)
    print("----Feed Main------")
    if user:
        posts = PostModel.objects.all().order_by("-created_on")
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            comments = CommentModel.objects.filter(post_id=post.id)
            if comments:
                if len(comments) >= 1:
                    for comment in comments:
                        existing_upvote = UpvoteModel.objects.filter(
                            comment=comment.id
                        ).first()
                        print(existing_upvote)
                        if existing_upvote:
                            comment.has_upvoted = True
            # If user has liked the post set the boolean value to True
            if existing_like:
                post.has_liked = True
        return render(request, "feed_main.html", {"posts": posts})
    else:
        return redirect("/login/")

# Like view
def like(request):
    user = check_validation(request)
    if user and request.method == "POST":
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
                #     send_mail(
                #         "Heyy, You got a like from " + post.user.name,
                #         "Check it out at smartp2pmarketplace.com",
                #         "smartp2pmarketplace.com",
                #         [post.post.user.email],
                #         fail_silently=False,
                #     )
            return redirect("/feed/")
    else:
        return redirect("/login/")

# Comment View
def comment(request):
    user = check_validation(request)
    if user and request.method == "POST":
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
            #         "Check it out at smartp2pmarketplace.com",
            #         "smartp2pmarketplace.com",
            #         [comment.post.user.email],
            #         fail_silently=False,
            #     )
            return redirect("/feed")
        else:
            return redirect("/feed/")
    else:
        return redirect("/login")

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
    if user and request.method == "POST":
        form = UpvoteForm(request.POST)
        if form.is_valid():
            print("form valid")
            comment_id = form.cleaned_data.get("comment").id
            print(comment_id)
            existing_upvote = UpvoteModel.objects.filter(
                comment_id=comment_id, user=user
            ).first()
            print(existing_upvote)
            # If user has already registered an upvote, then delete it
            if existing_upvote:
                existing_upvote.delete()
            else:
                # Otherwise create an upvote
                print("Create Upvote")
                post = UpvoteModel.objects.create(comment_id=comment_id, user=user)
                print(post)
                print((UpvoteModel.objects.filter(comment=comment_id)))
                post.save()
            return redirect("/feed/")
        else:
            print("Form not valid")
            return redirect("/feed/")
    else:
        return redirect("/login/")

def func(request, username):
    user = check_validation(request)
    print("----Feed Main------")
    if user:
        usern = UserModel.objects.all().filter(username=username)
        print(usern)
        posts = (
            PostModel.objects.all().filter(user=usern).order_by("-created_on")
        )
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            comments = CommentModel.objects.filter(post_id=post.id)
            if comments:
                if len(comments) >= 1:
                    for comment in comments:
                        existing_upvote = UpvoteModel.objects.filter(
                            comment=comment.id
                        ).first()
                        print(existing_upvote)

                        if existing_upvote:
                            comment.has_upvoted = True
            # If user has liked the post set the boolean value to True
            if existing_like:
                post.has_liked = True
        return render(request, "feed_main.html", {"posts": posts})
    else:
        return redirect("/login/")
    return render(request, "hello.html", {"context": username})