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

paginate_by_default = 2


# ########################## HomePage ###################################

class HomeView(ListView):
    model = Post
    template_name = 'blog_app/index.html'
    paginate_by = paginate_by_default

    # Variable name for storing the corresponding model list data
    context_object_name = 'post_list'


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
    # request.GET.get('_q') refers to accessing the value of the _q parameter from the query string of an HTTP GET request.
    # For example, if your URL is http://example.com/search?_q=keyword, then request.GET.get('_q') would return 'keyword'.
    _q = request.GET.get('_q')
    error_message = ""

    # if _q is empty, return an error message
    if not _q:
        error_message = 'Input Keyword'
        return render(request, 'blog_app/full-width.html', locals())
    else:
        # Q objects are used to encapsulate query expressions, which are used to provide complex query logic.
        # search the value of _q in the title and body of the Post model
        post_list = Post.objects.filter(Q(title__icontains=_q) | Q(body__icontains=_q))
        return render(request, 'blog_app/full-width.html', locals())


# ########################## About Page ################################
def about(request):
    return render(request, 'blog_app/about.html', None)


# ########################## contact Page ################################
# send email to the the user who submit the contact form
@require_http_methods(['GET', 'POST'])
def contact(request):
    if request.method == 'GET':
        return render(request, 'blog_app/contact.html', None)
    else:
        email = request.POST

        subject = 'Email from ' + email.get("name") + ': ' + email.get("subject")
        body = email.get("message")
        email_addresse = email.get("email")
        send_mail(subject, body, settings.EMAIL_HOST_USER, [email_addresse, settings.EMAIL_HOST_USER], fail_silently=False)

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
            # return JsonResponse({"code": 200, "message": "???????", "data": {"blog_id": post.id}})
            return redirect(post)
        else:
            print(form.errors)
            return JsonResponse({'code': 400, "message": "Parameter error?"})


# ########################## Page Of Search Result ################################
def search(request):
    # Get the search keyword submitted by the user, the key value of the dictionary is the same as the name attribute value in the template
    q = request.GET.get('q')
    error_message = ''

    # If q is empty, prompt the user to input
    if not q:
        error_message = 'Input Keyword'
        return render(request, 'blog_app/index.html', locals())

    # Q object is used to wrap the query expression, its function is to provide complex query logic
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog_app/index.html', locals())


# ########################## ArchivesPage ############################

'''
def archives(request, year):
    post_list = Post.objects.filter(create_time__year=year)
    return render(request, "blog_app/index.html", locals())
'''


class ArchivesView(ListView):
    model = Post
    template_name = 'blog_app/index.html'
    context_object_name = 'post_list'
    paginate_by = paginate_by_default

    # get_queryset: Fetching a list; this method by default retrieves all list data for the specified model, and can be overridden to change its default behavior.
    def get_queryset(self):
        # In class-based views, named captured parameters from the URL are stored in the instance's kwargs attribute (a dictionary),
        # while non-named captured parameters are stored in the instance's args attribute (a list).
        year = self.kwargs.get('year')
        # Overriding to specify filtering conditions and retrieve a list based on those conditions
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
    paginate_by = paginate_by_default

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
    context_object_name = "post_list"
    paginate_by = paginate_by_default

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


# ########################## BlogDetailPage #############################
# show the Detail of one specific Post

# The view function 'detail' which is analog to the view class 'PostDetailView'
'''
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
    return render(request, "blog_app/detail.html", context={"comment_list": comment_list})
'''

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/detail.html'
    context_object_name = 'post'

    # Return an HttpResponse instance; the self.object attribute, representing the post instance, is available only after the get method has been called.
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # increase the views of this post. Increment operation where self.object represents the post object.
        self.object.increase_views()
        return response

    # Retrieve the corresponding post instance based on the pk value of the post.
    # The DetailView's get_object method already knows how to fetch an object by the slug. We just need to override it to add the markdown rendering logic.
def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        # Performing rendering operations using the retrieved post instance.
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])

        post.body = md.convert(post.body)
        return post
