import markdown
from django.db.models import Q
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings

from blog_app.forms import PostForm
from blog_app.models import Post, Category, Tag
from django.contrib.auth.models import User
from blog_comment.forms import CommentForm

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET


# ########################## HomePage ###################################

class HomeView(ListView):
    # ??? model
    model = Post
    # ?????
    template_name = 'blog_app/index.html'
    # ???????????????
    context_object_name = 'post_list'
    # ???????
    paginate_by = 2



# ########################## Blog Page ################################
def full_posts(request):
    post_list = Post.objects.all()
    return render(request, 'blog_app/full-width.html', locals())


class FullPostView(HomeView):
    model = Post
    template_name = 'blog_app/full-width.html'
    context_object_name = 'post_list'
    paginate_by = 10

# ########################## Query Page: used only in Blog Page  ################################
@require_GET
def query(request):
    _q = request.GET.get('_q')
    error_message = ""

    if not _q:
        error_message = 'Input Keyword'
        return render(request, 'blog_app/full-width.html', locals())

    post_list = Post.objects.filter(Q(title__icontains=_q) | Q(body__icontains=_q))
    return render(request, 'blog_app/full-width.html', locals())


# ########################## About Page ################################
def about(request):
    return render(request, 'blog_app/about.html', None)

# ########################## contact Page ################################
@require_http_methods(['GET', 'POST'])
def contact(request):
    if request.method == 'GET':
        return render(request, 'blog_app/contact.html', None)
    else:
        email = request.POST

        subject = 'Email from ' + email.get("name") + ': ' + email.get("subject")
        body = email.get("message")
        email_addresse = email.get("email")
        send_mail(subject, body, settings.EMAIL_HOST_USER, [email_addresse], fail_silently=False)

        #email = EmailMessage('subject', 'body', to=['bigberlin100@gmail.com'])
        #email = EmailMessage(subject, body, to=[email_addresse])
        #email.send()
        print("Email sent successfully")
        return render(request, 'blog_app/contact.html', None)

# ########################## NewBlog Page ################################
# Submit a new blog and post it into Blog system
@login_required(login_url="/auth/login")
@require_http_methods(['GET', 'POST'])
def new_post(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        tags = Tag.objects.all()
        auth = User.objects.all()
        return render(request, 'blog_app/post_new.html', context={"categories": categories, "tags": tags, })
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            category = form.cleaned_data.get('category')
            tags = form.cleaned_data.get('tags')
            author = request.user
            print(author)
            print(category)
            print(tags)
            post = Post.objects.create(title=title, body=body, category=category, author=author)
            post.tags.add(*tags)
            #return JsonResponse({"code": 200, "message": "???????", "data": {"blog_id": post.id}})
            return redirect(post)
            #post = form.save(commit=False)
            #post.author = post.user
            #post.save()
            #return redirect(post)
        else:
            print(form.errors)
            return JsonResponse({'code': 400, "message": "Parameter error?"})
    #else:
    #    form = PostForm()
    #return render(request, 'blog_app/post_new.html', locals())

# ########################## Page Of Search Result ################################
def search(request):
    # ???????????????????????? name ???
    q = request.GET.get('q')
    error_message = ''

    # ?? q ???????
    if not q:
        error_message = 'Input Keyword'
        return render(request, 'blog_app/index.html', locals())

    # Q ???????????????????????????
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog_app/index.html', locals())




# ########################## ArchivesPage ############################
def archives(request, year):
    post_list = Post.objects.filter(create_time__year=year)
    return render(request, "blog_app/index.html", locals())


class ArchivesView(ListView):
    model = Post
    template_name = 'blog_app/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    # ??????????????????????????????????
    def get_queryset(self):
        # ??????? URL ??????????????? kwargs ???????????
        # ????????????? args ??????????
        year = self.kwargs.get('year')
        # ????????????????????
        return super(ArchivesView, self).get_queryset().filter(create_time__year=year)



# ########################## CategoryPage ############################
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, "blog_app/index.html", locals())


class CategoryView(ListView):
    model = Post
    template_name = 'blog_app/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=category)


# ########################## TagPage ################################
def tags(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag)
    return render(request, 'blog_app/index.html', locals())


class TagView(ListView):
    model = Post
    template_name = "blog_app/index.html"
    context_object_name = "pot_list"
    paginate_by = 10

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)



# ########################## BlogDetailPage #############################
# show the Detail of one specific Post

# The view function 'detail' which is analog to the view class 'PostDetailView'
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # ?????
    post.increase_views()
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    return render(request, "blog_app/detail.html", context={"comment_list": comment_list })


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/detail.html'
    context_object_name = 'post'

    # ???? HttpResponse ?????? get ???????? self.object ???? post ??
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # ?????self.object ??? post ??
        self.object.increase_views()
        return response

    # ?? post ? pk ?????? post ??
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        # ???? post ??????????
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])

        post.body = md.convert(post.body)
        return post

    '''
    # ???????????????????????
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        #form = CommentForm()
        #comment_list = self.object.comment_set.all()
        context.update(locals())
        return context
    '''





