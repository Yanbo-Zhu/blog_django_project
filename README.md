# Blog_Django_Project

<HR>

- [Blog_Django_Project](#blog-django-project)
  * [Projekt Description](#projekt-description)
  * [System Dependency](#system-dependency)
  * [Depolyment process](#depolyment-process)
  * [Main View](#main-view)
  * [Usage](#usage)
    + [Login and Register](#login-and-register)
    + [Blog System](#blog-system)
      - [Home Page](#home-page)
      - [Post Detail Page](#post-detail-page)
      - [Blog List](#blog-list)
      - [About me](#about-me)
      - [Contact me](#contact-me)
      - [Post New](#post-new)
      - [Search and Logout](#search-and-logout)
  * [Administration System](#administration-system)
  * [Authentication](#authentication)
  * [Restful API](#restful-api)
  * [Database](#database)
    + [blog_app](#blog-app)
      - [Table: Post](#table--post)
      - [Table: Tag](#table--tag)
      - [Table: Category](#table--category)
    + [blog_comment](#blog-comment)
      * [Table: Comment](#table--comment)
  * [Other](#other)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Projekt Description
Through this Django project we can deploy a personal blog.

It is a pure Django project without frontend and backend separation. 

SQLite is used as Database


## System Dependency
Python3, Django and Third Party Dependency ( written in requirements.txt)

## Depolyment process

1. Install the thrid-party Library according to requirements.txt: `pip install -R requirement.txt`
2. run Django Project through execute `python manage.py runserver 8000`


## Main View
- admin
  - [admin page](http://127.0.0.1:8000/admin)
- blog_app
  - [Home Page](http://127.0.0.1:8000/blog/home)
  - [Blog List](http://127.0.0.1:8000/blog/full)
  - [About me](http://127.0.0.1:8000/blog/about/)
  - [Contact me](http://127.0.0.1:8000/blog/contact/)
  - [Post new ](http://127.0.0.1:8000/blog/contact/)
- blog_auth
  - [login](http://127.0.0.1:8000/auth/login)
  - [register](http://127.0.0.1:8000/auth/register)
  - [logout](http://127.0.0.1:8000/auth/logout): logout the current user and redirect to the login page auotmatically
- blog_api
  - [posts](http://127.0.0.1:8000/api/posts/): show all posts
  - [categories](http://127.0.0.1:8000/api/categories/): show all categories
  - [tags](http://127.0.0.1:8000/api/tags/): show all tags
  - [users](http://127.0.0.1:8000/api/users/): show all users

View map
![](readme_picture/view_map.png)


## Usage 

### Login and Register
There are two page: login and register.

In the login mode, you can choose remember me or not. If you choose remember me, the session will be saved for 14 days. Otherwise, the session will expire after the browser is closed.

![](readme_picture/blog_auth/01_login.png)

In the register mode, you need to set the username, the password and the email. The username and the email should be unique. The password should be at least 8 characters long. After you have registered, you will be redirected to the login page. you have to login with the username and the password you have just set.

![](readme_picture/blog_auth/02_register.png)

Moreover, you can also enter to the Home page and The Page for creating new post directly through the main bar. Enter the Home page you don't need to login. But if you want to create a new post, you need to login first. Otherwise, you will be redirected to the login page.


### Blog System

There are five main pages in the blog system: Home Page, Blog List and About me, Contact me and Post new. They are all accessible through the main bar.

The welcome word "Hello, \<Username of current session\>" will be shown in the main bar if you have logged in.

#### Home Page

The Blog are display in the link part of the Home Page. The first 3 posts are shown in the Home Page. You can click the title of the post to see the detail of the post.

The navigation bar is shown in the right side of the Home Page. The option blow are listed in the navigation bar:
- The latest 5 posts
- Archive: The posts are grouped by year
- category: The posts are grouped by category. you can click the category to see the posts in this category
- tag: The posts are grouped by tag. you can click the tag to see the posts in this tag

![](readme_picture/blog_app/01_homePage.png)

#### Post Detail Page 

The detail of the post is shown in the Detail Page of one Post. You can see the title, the author, the create time, the modified time, the category, the tags and the content of the post. 

The view number of the post is shown blow the title of the post. The view number will be increased by 1 every time you enter the detail page of the post.

The comments of the post are shown below the post. You can add a comment to the post if you have logged in. The comments are paginated by 10 comments per page.

![](readme_picture/blog_app/02_BlogDetail.png)

#### Blog List
All Blog are shown in the Blog List. You can click the title of the post to see the detail of the post. The blogs are paginated by 10 posts per page.

![](readme_picture/blog_app/03_blogList.png)

#### About me
The information about the author is shown in the About me page.

#### Contact me
A Email form is shown in the Contact me page. You can send an email to the Host of this Blog system through this form. The same message will also be sent to the the email of the author who has edit this contact form .

![](readme_picture/blog_app/05_contactMe.png)


The email is sent through the SMTP server. The SMTP server is set in the settings.py of project. **In order to enable sending Email, you have to change the SMTP server by changing the following code in the settings.py**. The authtiocation of the SMTP server is required and is your email address and the password of the email address.

```angular2html
EMAIL_PORT = '<EMAIL_PORT>'
EMAIL_HOST = '<EMAIL_HOST>'
EMAIL_HOST_USER = '<Email_Addresse>'
EMAIL_HOST_PASSWORD = '<sensetive_data>'
```

#### Post New

if you want to create a new post, you need to login first. Otherwise, you will be redirected to the login page.

After you have already logged in, you can create a new post through the Post new page. You can set the title, the category, the tags and the content of the post. The category and the tags are selectable. You can also add a new category or a new tag. 

The Author of the post is the current user. The create time and the modified time of the post are set automatically. The excerpt of the post is the first 50 characters of the content.

After you have created the post, you will be redirected to the detail page of the post.

![](readme_picture/blog_app/06_newPost.png)

#### Search and Logout

In the main bar you can also search the post by title or content and logout the current user. Only the **title** and the **content** of the post will be searched.

After logout, you will be redirected to the login page.

![](readme_picture/blog_app/07_searchAndLogout.png)

## Administration System

The administration system is accessible through the link of the admin page in the main bar. You can login with the superuser account or other user to manage the blog system.

![](readme_picture/admin/01_adminLogin.png)

![](readme_picture/admin/02_adminContent.png)


## Authentication

Once you register a new user through Register page, this new created user will be registered into the Built-in User table of Django. The password of the user is hashed by the Django built-in hash function. The password is not stored in the database directly.

The User below are available in the system. You can login with the username and the password below. Or you can also create a new user through the Register page.

| username | password  | email                  | permission  |
|----------|-----------|------------------------|-------------|
| admin    | django123 | bigberlin100@gmail.com | superuser   |
| Thomas   | django123 | bigberlin200@gmail.com | normal user |
| Dylan    | django123 | bigberlin300@gmail.com | normal user   |
| Jens     | django123 | bigberlin400@gmail.com | normal user   |
| Florian  | django123 | bigberlin500@gmail.com | normal user   |

## Restful API

The Restful API is accessible through the link of the api page in the main bar. You can see all posts, categories, tags and users through the api page.

The result of the api is in JSON format. The api is paginated by 3 items per page.

you can filter the result by the following query parameters:
- posts: filter the posts by title
  - The verbose filter is also supported: e.g. http://127.0.0.1:8000/api/posts/?title=ad
- categories: filter the categories by name
- tags: filter the tags by name
- users: filter the users by username


posts:
![](readme_picture/blog_api/01_posts.png)
![](readme_picture/blog_api/02_posts.png)

categories: 
![](readme_picture/blog_api/03_categories.png)

tags: 
![](readme_picture/blog_api/04_tags.png)

users: 
![](readme_picture/blog_api/05_users.png)
![](readme_picture/blog_api/06_users.png)

## Database

### blog_app
#### Table: Post
The Post in the Blog System

Attributes
- title: title of the post
- body: content of the post
- create_time: create time of the post
- modified_time: modified time of the post
- excerpt: if empty, the first 50 characters of body is used
- views: how many times this post is viewed
- category: As ForeignKey to table Category
- tags: mapping to the name in the table Tag
- author = As ForeignKey to table User

#### Table: Tag
Tag of post

Attributes
- name: name of tag

#### Table: Category
Category of post

Attributes
- name: name of category

### blog_comment
##### Table: Comment
Comment of post

Attributes
- author: ForeignKey to User
- email: email of the author
- url: url of the author
- text: content of the comment
- create_time: create time of the comment
- post: ForeignKey to Post


## Other
@Coding=UTF-8  
@Auther:Yanbo Zhu
@Time:2024-06  
@ProjectName:Personal Blog