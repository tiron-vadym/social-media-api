# Social Media API

RESTful API for a social media platform. 
The API allow users to create profiles, follow other users, create and retrieve posts,
and perform basic social media actions.

## Installing using GitHub

Install PostgresSQL and create db

```shell
git clone https://github.com/tiron-vadym/social-media-api
cd social_media_API
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db username>
set DB_PASSWORD=<your db user password>
set SECRET_KEY=<your secret key>
python manage.py migrate
python manage.py runserver
```

## Getting access

* create user via /api/user/register
* get access token via /api/user/token

## Features

#### User Registration and Authentication:
* Users be able to register with their email and password to create an account.
* Users be able to login with their credentials and receive a token for authentication.
* Users be able to logout and invalidate their token.

#### User Profile:
* Users be able to create and update their profile, including profile picture, bio, and other details.
* Users be able to retrieve their own profile and view profiles of other users.
* Users be able to search for users by username or other criteria.

#### Follow/Unfollow:
* Users be able to follow and unfollow other users.
* Users be able to view the list of users they are following and the list of users following them.

#### Post Creation and Retrieval:
* Users be able to create new posts with text content and optional media attachments (e.g., images). (Adding images is optional task)
* Users be able to retrieve their own posts and posts of users they are following.
* Users be able to retrieve posts by hashtags or other criteria.

#### API Permissions:
* Only authenticated users be able to perform actions such as creating posts, liking posts, and following/unfollowing users.
* Users only be able to update and delete their own posts and comments.
* Users only be able to update and delete their own profile.

#### API Documentation:
* The API well-documented with clear instructions on how to use each endpoint.
* The documentation include sample API requests and responses for different endpoints.

#### Technical points:
* Used Django and Django REST framework to build the API.
* Used token-based authentication for user authentication.
* Used appropriate serializers for data validation and representation.
* Used appropriate views and viewsets for handling CRUD operations on models.
* Used appropriate URL routing for different API endpoints.
* Used appropriate permissions and authentication classes to implement API permissions.
* Follow best practices for RESTful API design and documentation.

## DB schema

![social media schema.png](social%20media%20schema.png)

