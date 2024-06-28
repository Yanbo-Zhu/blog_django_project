from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from blog_app.models import Post
from blog_comment.forms import CommentForm
from blog_comment.models import Comment

@login_required(login_url="/auth/login")
@require_http_methods(['POST'])
def post_comment(request,post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            author = request.user
            content = form.cleaned_data.get('content')
            comment = Comment.objects.create(author=author, content=content, post=post, email=author.email)
            return redirect(post)
        else:
            print(form.errors)
            return JsonResponse({'code': 400, "message": "Parameter error?"})
    else:
        return redirect(post)


