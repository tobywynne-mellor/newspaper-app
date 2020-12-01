from django.shortcuts import render
from .models import *
import json
from django.http import QueryDict
# -------------------import for user validation------------
from .forms import ProfileForm, ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

# ---------------------------------Model serializers-------------------------
from .serializers import *
# ------------------------------Import for sending emails----------------------
from django.core.mail import send_mail
# --------------------------Decorators and responses-------------------------
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# ----------------------------Profile----------------------
# Initial render view


@login_required(login_url="newspaper_app:login_form")
@require_http_methods(["GET"])
def Profile_initial_render(request):
    # ------------------Get the user-----------------------
    current_user = User.objects.get(pk=request.user.id)
    # ------------------Get the user's profile-----------------------
    profile = get_object_or_404(Profile, user=current_user)
    # ----------------------Get all preference in db------------------------
    available_cate = Category.objects.all()
    preferences = profile.pref_cate
    context = {"Profile": profile, "Preference": preferences, "Category": available_cate,
               "Profile_update_form": ProfileUpdateForm}
    return render(request, "newspaper_app/profile.html", context)

# GET


@login_required(login_url="newspaper_app:login_form")
@require_http_methods(["GET"])
def Profile_view(request):
    # ------------------Get the user-----------------------
    current_user = User.objects.get(pk=request.user.id)
    # ------------------Get the user's profile-----------------------
    profile_set = get_object_or_404(Profile, user=current_user)
    profile = ProfileSerializer(profile_set)
    return JsonResponse(profile.data, safe=False)
# PUT


# @login_required(login_url="newspaper_app:login_form")
@require_http_methods(["POST"])
@csrf_exempt
def Profile_put(request):
    # ------------------Get the user-----------------------
    current_user = User.objects.get(pk=request.user.id)
    # ------------------Get the user's profile-----------------------
    profile_set = get_object_or_404(Profile, user=current_user)
    profile_update_form = ProfileUpdateForm(
        request.POST, request.FILES, instance=profile_set)
    if(profile_update_form.is_valid()):
        new_profile = profile_update_form.save(False)
        profile_update_form.save_m2m()
        new_profile.save()
        return JsonResponse(ProfileSerializer(new_profile).data, safe=False)
    else:
        return JsonResponse({"Message": "False"})


# -------------------------------Article/Home views-------------------------------------

# Return all articles from database


def Articles_view(request):
    if(request.user.is_authenticated):
        # ------------------Get the user-----------------------
        current_user = User.objects.get(pk=request.user.id)
        # ------------------Get the user's profile-----------------------
        profile = get_object_or_404(Profile, user=current_user)
        # ------------------Get the profile's preference-----------------------
        
        preferences = profile.pref_cate
        Articles = Article.objects.filter(
            category__in=preferences.values("id"))
        
        # If no filtered articles
        if not Articles:
            Articles = Article.objects.all()

        context = {"Articles": Articles}
        return render(request, "newspaper_app/index.html", context)
    else:
        Articles = Article.objects.all()
        context = {"Articles": Articles}
        return render(request, "newspaper_app/index.html", context)


# Return an article with a POST request containing the id of the article


@require_http_methods(["GET"])
@csrf_exempt
def Article_view(request, id):
    # ---------------------Article----------------------
    article = get_object_or_404(Article, pk=id)
    # ---------------------Article's likes----------------------
    likes = Like.objects.filter(
        article=get_object_or_404(Article, pk=id))
    # ---------------------Article's comments----------------------
    comments = Comment.objects.filter(
        article=get_object_or_404(Article, pk=id))


    if(request.user.is_authenticated):
        # ------------------Get the user-----------------------
        current_user = User.objects.get(pk=request.user.id)
        # ------------------Get the user's profile-----------------------
        profile = get_object_or_404(Profile, user=current_user)

        like = Like.objects.filter(article=article.id, user=profile).first() 

        context = {"article": article, "likes": likes, "profile": profile, "like":like}
    else:
        context = {"article": article, "likes": likes}
    return render(request, "newspaper_app/article.html", context)

# -------------------------------Like views-------------------------------------

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
@login_required(login_url="newspaper_app:login_form")
def Like_post(request):
    like_user = get_object_or_404(Profile, user=User.objects.get(id=int(request.POST['user_id'])))
    like_article = get_object_or_404(
        Article, pk=int(request.POST['article_id']))
    like = Like.objects.create(user=like_user, article=like_article)
    like = LikeSerializer(like, many=False)
    return JsonResponse(like.data,status=200)

# DELETE
# Required Formdata : {"like_id"}
# i.e. /like_delete/2/


@require_http_methods(["DELETE"])
@csrf_exempt
@login_required(login_url="newspaper_app:login_form")
def Like_delete(request, like_id):
    like = get_object_or_404(Like, pk=like_id)
    like.delete()
    return JsonResponse({'message': 'Like: {} was deleted successfully.'.format(like_id)}, status=204)


# -------------------------------Comment views-------------------------------------
#@login_required(login_url="newspaper_app:login_form")
@require_http_methods(["GET"])
def Comment_view(request, article_id):
    comment_set = Comment.objects.filter(
        article=get_object_or_404(Article, pk=article_id))
    comments = CommentSerializer(comment_set, many=True)
    data = comments.data
    for d in data:
        profile = Profile.objects.get(pk=d.get("user"))
        d['username'] = profile.user.username
        if profile.profile_pic:
            d['profile_pic'] = profile.profile_pic.url
    return JsonResponse(data, safe=False)


# Post
# Required Formdata: {"user_id","article_id", "content"}
@require_http_methods(["POST"])
@login_required(login_url="newspaper_app:login_form")
@csrf_exempt
def Comment_post(request):
    # ------------------Get the user-----------------------
    current_user = User.objects.get(pk=request.user.id)

    profile = get_object_or_404(Profile, user=current_user)

    comment_article = get_object_or_404(
        Article, pk=int(request.POST['article_id']))
    comment_content = request.POST['content']
    try:
        comment_replyTo = Comment.objects.get(
            pk=int(request.POST['replyToComment']))
        comment = Comment.objects.create(
            user=profile,
            article=comment_article,
            content=comment_content,
            replyToComment=comment_replyTo
        )
    except:
        comment = Comment.objects.create(
            user=profile, article=comment_article, content=comment_content)
    comment = CommentSerializer(comment, many=False)
    data = comment.data
    profile = Profile.objects.get(pk=data.get("user"))
    data['username'] = profile.user.username
    if profile.profile_pic:
        data['profile_pic'] = profile.profile_pic.url
    return JsonResponse(data, safe=False)

# PUT
# Required Formdata : {"comment_id", "content"}
# TODO serialise form data if possible


@require_http_methods(["PUT"])
@csrf_exempt
@login_required(login_url="newspaper_app:login_form")
def Comment_put(request):
    body = QueryDict(request.body)  # in order to parse the PUT body
    comment_id = int(body.get('comment_id'))
    content = body.get('content')
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.content = content
    comment.save()
    return HttpResponse("comment changed to '"+content+"'", status=200)

# DELETE
# i.e. /comment_delete/9/


@require_http_methods(["DELETE"])
@csrf_exempt
@login_required(login_url="newspaper_app:login_form")
def Comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return JsonResponse({'message': 'Comment: {} was deleted successfully.'.format(comment_id)}, status=204)

# -----------------------------user's profile registration and login-----------------------
# user's profile register and login validation


@require_http_methods(["POST"])
@csrf_exempt
def register_validation(request):
    form = UserCreationForm(request.POST)
    form.fields['username'].widget.attrs['class'] = "form-control"
    form.fields['password1'].widget.attrs['class'] = "form-control"
    form.fields['password2'].label = "Confirm Password:"
    form.fields['password2'].widget.attrs['class'] = "form-control"

    registration_form = ProfileForm(request.POST, request.FILES)
    registration_form.fields['profile_pic'].label = "Profile Picture:"
    registration_form.fields['profile_pic'].widget.attrs['class'] = "btn upload"
    registration_form.fields['email'].widget.attrs['class'] = "form-control"
    registration_form.fields['dob'].label = "Date of Birth (YYYY-MM-DD)"
    registration_form.fields['dob'].widget.attrs['class'] = "form-control"
    registration_form.fields['pref_cate'].label = "Preferred Category(s):"

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
        # ---------------------------------------Welcome email view-----------------------------
        print(profile.email)
        send_mail(
            'Welcome to FakeNews',
            'Only the truth for you.',
            'bestfakenews3010@gmail.com',
            [str(profile.email)],
            fail_silently=False,
        )
        return redirect("newspaper_app:profile")
    else:
        return render(request, 'newspaper_app/register.html', context)


@require_http_methods(["POST"])
@csrf_exempt
def login_validation(request):
    form = AuthenticationForm(data=request.POST)

    form.fields['username'].widget.attrs['class'] = "form-control"
    form.fields['password'].widget.attrs['class'] = "form-control"

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
    form.fields['username'].widget.attrs['class'] = "form-control"
    form.fields['password1'].widget.attrs['class'] = "form-control"
    form.fields['password2'].label = "Confirm Password:"
    form.fields['password2'].widget.attrs['class'] = "form-control"

    registration_form = ProfileForm()
    registration_form.fields['profile_pic'].label = "Profile Picture:"
    registration_form.fields['profile_pic'].widget.attrs['class'] = "btn upload"
    registration_form.fields['email'].widget.attrs['class'] = "form-control"
    registration_form.fields['dob'].label = "Date of Birth (YYYY-MM-DD)"
    registration_form.fields['dob'].widget.attrs['class'] = "form-control"
    registration_form.fields['pref_cate'].label = "Preferred Category(s):"

    context = {"form": form, "registration_form": registration_form}
    return render(request, 'newspaper_app/register.html', context)


@require_http_methods(["GET"])
def login_view(request):
    form = AuthenticationForm()

    form.fields['username'].widget.attrs['class'] = "form-control"
    form.fields['password'].widget.attrs['class'] = "form-control"

    context = {"form": form}
    return render(request, 'newspaper_app/login.html', context)


@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    return redirect("newspaper_app:index")
