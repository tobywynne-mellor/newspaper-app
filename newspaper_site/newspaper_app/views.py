from django.shortcuts import render
from .models import *
# -------------------import for user validation------------
from .forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
# ---------------------------------Model serializers-------------------------
from .serializers import *
# --------------------------Decorators and responses-------------------------
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# -------------------------------Article/Home views-------------------------------------

# Return all articles from database


def Articles_view(request):
    Articles = Article.objects.all()
    context = {"Articles": Articles}
    return render(request, "newspaper_app/index.html", context)

# Return an article with a POST request containing the id of the article


@require_http_methods(["GET"])
@csrf_exempt
def Article_view(request, id):
    article = get_object_or_404(Article, pk=id)
    # likes = Like.objects.filter(article=id)
    # comments = Comment.objects.filter(article=id)
    context = {"article": article}
    return render(request, "newspaper_app/article.html", context)

# -------------------------------Like views-------------------------------------

# Message Decorator


def message(function):
    def new_function(request, *args, **kwargs):
        message = {"success": True}
        try:
            function(request, *args, **kwargs)
        except:
            message = {"success": False}
        return JsonResponse(message)
    return new_function
# GET


@require_http_methods(["GET"])
def Like_view(request, article_id):
    like_set = Like.objects.filter(
        article=get_object_or_404(Article, pk=article_id))
    likes = LikeSerializer(like_set, many=True)
    return JsonResponse(likes.data, safe=False)


# Post
# Required Formdata: {"user_id","article_id"}
@require_http_methods(["POST"])
@csrf_exempt
@message
def Like_post(request):
    like_user = get_object_or_404(Profile, pk=int(request.POST['user_id']))
    like_article = get_object_or_404(
        Article, pk=int(request.POST['article_id']))
    like = Like.objects.create(user=like_user, article=like_article)
    like = LikeSerializer(like, many=False)

# DELETE
# Required Formdata : {"like_id"}


@require_http_methods(["POST"])
@csrf_exempt
@message
def Like_delete(request):
    Like.objects.get(pk=int(request.POST['like_id'])).delete()


# -------------------------------Comment views-------------------------------------
@require_http_methods(["GET"])
def Comment_view(request, article_id):
    comment_set = Comment.objects.filter(
        article=get_object_or_404(Article, pk=article_id))
    comments = CommentSerializer(comment_set, many=True)
    return JsonResponse(comments.data, safe=False)


# Post
# Required Formdata: {"user_id","article_id"}
@require_http_methods(["POST"])
@csrf_exempt
def Comment_post(request):
    comment_user = get_object_or_404(Profile, pk=int(request.POST['user_id']))
    comment_article = get_object_or_404(
        Article, pk=int(request.POST['article_id']))
    comment_content = request.POST['content']
    try:
        comment_replyTo = Comment.objects.get(
            pk=int(request.POST['replyToComment']))
        comment = Comment.objects.create(
            user=comment_user, article=comment_article, content=comment_content, replyToComment=comment_replyTo)
    except:
        comment = Comment.objects.create(
            user=comment_user, article=comment_article, content=comment_content)
    comment = CommentSerializer(comment, many=False)
    return JsonResponse(comment.data, safe=False)

# PUT
# Required Formdata : {"like_id"}
# @require_http_methods(["POST"])
# @csrf_exempt
# @message
# def Comment_put(request):
#     Like.objects.get(pk=int(request.POST['like_id'])).delete()

# DELETE
# Required Formdata : {"comment_id"}


@require_http_methods(["POST"])
@csrf_exempt
@message
def Comment_delete(request):
    Comment.objects.get(pk=int(request.POST['comment_id'])).delete()
# -----------------------------user's profile registration and login-----------------------
# user's profile register and login validation


@require_http_methods(["POST"])
@csrf_exempt
def register_validation(request):
    form = UserCreationForm(request.POST)
    registration_form = ProfileForm(request.POST)
    context = {"form": form, "registration_form": registration_form}
    if(form.is_valid() and registration_form.is_valid()):
        context = {"message": True}
        # Save user's name and password
        user = form.save()
        # login user
        login(request, user)
        profile = registration_form.save(False)
        profile.user = user
        # Save user extra info
        profile.save()
        registration_form.save_m2m()
        return redirect("newspaper_app:index")
    else:
        return render(request, 'newspaper_app/register.html', context)


@require_http_methods(["POST"])
@csrf_exempt
def login_validation(request):
    form = AuthenticationForm(data=request.POST)
    context = {"form": form}
    if(form.is_valid()):
        user = form.get_user()
        login(request, user)
        return redirect("newspaper_app:index")
    else:
        return render(request, 'newspaper_app/login.html', context)


# user's profile register and login form
@require_http_methods(["GET"])
def register_view(request):
    form = UserCreationForm()
    registration_form = ProfileForm()
    context = {"form": form, "registration_form": registration_form}
    return render(request, 'newspaper_app/register.html', context)


@require_http_methods(["GET"])
def login_view(request):
    form = AuthenticationForm()
    context = {"form": form}
    return render(request, 'newspaper_app/login.html', context)


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return redirect("user:base")
