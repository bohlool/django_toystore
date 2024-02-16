Here's a toy store app using Python, django and a sqlite database. We'll use django for the web framework.

This app has two main parts. One is a blog app and the other is store.

The blog app has ten SSR endpoint:

- `GET /post/new/`: Adds a new post to the blog. 
- `GET /`: Returns a list of all posts in the blog.
- `GET /post/<int:pk>/`: Shows post detail.
- `GET /post/<int:pk>/edit/`: Edits a post
- `GET /post/<int:pk>/delete/`: Deletes a post
- `GET /post/<int:pk>/delete/`: Deletes a post
- `GET /post/<str:subject>/`: Shows posts with specified subject
- `GET /subject-auto-complete/`: Returns available subjects for auto complete in post form
- `GET /post/<int:pk>/comment/`: Creates a comment for specified post
- `GET /post/<int:post_pk>/comment/<int:comment_pk>/delete/`: Deletes a comment from database

Copy sample_settings.py to local_settings.py and add ADMIN_URL. 

To execute this app open terminal and change directory to tamrin2 then run following commands:

```shell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd myblog
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Visit http://127.0.0.1:8000/<ADMIN_URL>/ to add contacts through the admin interface. 

We can use the front end to list, edit, and delete posts and comments too.

We can now also test our API endpoints using tools like Postman or cURL. Here are the endpoints we've created:

For the  Post  model: 
 
- Create:  POST api/posts/  
- Read (list):  GET api/posts/  
- Read (detail):  GET api/posts/{post_id}/  
- Update:  PUT api/posts/{post_id}/  or  PATCH api/posts/{post_id}/  
- Delete:  DELETE api/posts/{post_id}/  
- Comments of post:  GET api/posts/{post_id}/comments  
 
For the  Comment  model: 
 
- Create:  POST api/comments/  
- Read (list):  GET api/comments/  
- Read (detail):  GET api/comments/{comment_id}/  
- Update:  PUT api/comments/{comment_id}/  or  PATCH api/comments/{comment_id}/  
- Delete:  DELETE api/comments/{comment_id}/  
This setup provides a full CRUD API for our posts using Django Rest Framework.