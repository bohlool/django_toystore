Here's a toy store app using Python, django, bootstrap and a sqlite database. We'll use django for the web framework.

This app has two main parts. One is a blog app and the other is store.

The blog app has ten SSR endpoint:

- `GET /post/new/`: Adds a new post to the blog. 
- `GET /post/`: Returns a list of all posts in the blog.
- `GET /post/<int:pk>/`: Shows post detail.
- `GET /post/<int:pk>/edit/`: Edits a post
- `GET /post/<int:pk>/delete/`: Deletes a post
- `GET /post/<int:pk>/delete/`: Deletes a post
- `GET /post-by-subject/<int:subject>/`: Shows posts with specified subject
- `GET /subject-auto-complete/`: Returns available subjects for auto complete in post form
- `GET /post/<int:pk>/comment/`: Creates a comment for specified post
- `GET /post/<int:post_pk>/comment/<int:comment_pk>/delete/`: Deletes a comment from database

The store app has nine SSR endpoint:
- `GET /`: Returns a list of categories in the store.
- `GET /categories/<int:category_id>/products/`: Shows products of a category.
- `GET /products/<int:pk>/`: Shows product detail.
- `GET /products/<int:product_id>/comment/`: Creates a comment for specified product
- `GET /cart/`: List of products available in the cart
- `POST /add-to-cart/<int:product_id>/`: Adds a product to the cart
- `POST /remove-from-cart/<int:item_id>/`: Removes an item from the cart
- `GET /checkout/`: Create order from products available in the cart
- `GET /orders/`: List of previous orders of a user

Copy sample_settings.py to local_settings.py and add ADMIN_URL. 

To execute this app open terminal and change directory to django_toystore then run following commands:

```shell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Visit http://127.0.0.1:8000/<ADMIN_URL>/ to add contacts through the admin interface. 

We can use the front end to list, edit, and delete posts and comments too.

We can now also test our API endpoints using tools like Postman or cURL. Here are the endpoints we've created:

For the  Post  model: 
 
- Create:  POST api/blog/posts/  
- Read (list):  GET api/blog/posts/  
- Read (detail):  GET api/blog/posts/{post_id}/  
- Update:  PUT api/blog/posts/{post_id}/  or  PATCH api/blog/posts/{post_id}/  
- Delete:  DELETE api/blog/posts/{post_id}/  
- Comments of post:  GET api/blog/posts/{post_id}/comments  
 
For the blog Comment  model: 
 
- Create:  POST api/blog/comments/  
- Read (list):  GET api/blog/comments/  
- Read (detail):  GET api/blog/comments/{comment_id}/  
- Update:  PUT api/blog/comments/{comment_id}/  or  PATCH api/blog/comments/{comment_id}/  
- Delete:  DELETE api/blog/comments/{comment_id}/  
This setup provides a full CRUD API for our posts using Django Rest Framework.

For the  category  model: 
 
- Create:  POST api/categories/  
- Read (list):  GET api/categories/  
- Read (detail):  GET api/categories/{category_id}/  
- Update:  PUT api/categories/{category_id}/  or  PATCH api/categories/{category_id}/  
- Delete:  DELETE api/categories/{category_id}/  
- products of the category:  GET api/categories/{category_id}/products  


For the  product  model: 
 
- Create:  POST api/products/  
- Read (list):  GET api/products/  
- Read (detail):  GET api/products/{product_id}/  
- Update:  PUT api/products/{product_id}/  or  PATCH api/products/{product_id}/  
- Delete:  DELETE api/products/{product_id}/  
- comments of the product:  GET api/products/{product_id}/comments  
- images of the product:  GET api/products/{product_id}/images  
- videos of the product:  GET api/products/{product_id}/videos  


For the product image gallery  model: 
 
- Create:  POST api/image-gallery/  
- Read (list):  GET api/image-gallery/  
- Read (detail):  GET api/image-gallery/{image_id}/  
- Update:  PUT api/image-gallery/{image_id}/  or  PATCH api/image-gallery/{image_id}/  
- Delete:  DELETE api/image-gallery/{image_id}/

For the product video gallery  model: 
 
- Create:  POST api/video-gallery/  
- Read (list):  GET api/video-gallery/  
- Read (detail):  GET api/video-gallery/{video_id}/  
- Update:  PUT api/video-gallery/{video_id}/  or  PATCH api/video-gallery/{video_id}/  
- Delete:  DELETE api/video-gallery/{video_id}/



For the product Comment  model: 
 
- Create:  POST api/comments/  
- Read (list):  GET api/comments/  
- Read (detail):  GET api/comments/{comment_id}/  
- Update:  PUT api/comments/{comment_id}/  or  PATCH api/comments/{comment_id}/  
- Delete:  DELETE api/comments/{comment_id}/ 



For the cart  model: 
  
- Read (list):  GET api/cart/view-cart  
- Read (detail):  GET api/cart/view-cart/{cart_id}/
- items of the cart:  GET api/cart/{cart_id}/items  

For the cart items  model: 
 
- Create:  POST api/cart/cart-items/  
- Read (list):  GET api/cart/cart-items/  
- Read (detail):  GET api/cart/cart-items/{item_id}/  
- Update:  PUT api/cart/cart-items/{item_id}/  or  PATCH api/cart/cart-items/{item_id}/  
- Delete:  DELETE api/cart/cart-items/{item_id}/

For the order  model: 
 
- Create:  POST api/order/orders/  
- Read (list):  GET api/order/orders/  
- Read (detail):  GET api/order/orders/{order_id}/  
- Update:  PUT api/order/orders/{order_id}/  or  PATCH api/order/orders/{order_id}/  
- Delete:  DELETE api/order/orders/{order_id}/
