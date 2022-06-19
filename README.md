# Django Custom User Model with TDD, Docker and PostgreSQL with Token-based auth.

**Some kinds of projects may have authentication requirements for which Django's built-in User Model is not always appropriate. For instance, on some sites it makes more sense to user an e-mail address as your verification token instead of Username.**

**Django allows us to overwrite the default User Model where we can use e-mail address instead of username.**

**It is highly recommended to setup a Custom User Model, even if the default User Model is sufficient for you.**

**Custom User Model behaves identically to the default User Model**

## Details
* This simple authentication app is made using Django, Django REST Framework, Docker and PostgreSQL database. This webapp uses e-mail address instead of username for authentication purposes.

* Docker is used for ease of spinning up the env and all related services such as database etc..
* PostgreSQL is used with docker-compose and Dockerfile.
* Included tests for Custom User Model using Test Driven Development.


## Setting up the project

* You need to have Docker and Docker-compose installed on your local machine to run this webapp smoothly.

* Clone this repository into your local machine and enter command :~ `docker build .` and `docker-compose build` which will build the docker images used to run the app. This commands built the images that stores all the deps required for this app.

* Run the command `docker-compose up`. This will start the containers (all the services such as django server and postgres as the database).

* Create a superuser by entering the command :~ `docker-compose run project sh -c "python manage.py createsuperuser`

* Go to admin page at ~`127.0.0.1:8000/admin` and login with superuser credentials. I have added the django admin setup for user database.


![Screenshot (38)](https://user-images.githubusercontent.com/55087178/110636058-d664a480-81d1-11eb-8665-fbdfe8a69666.png)

* After logging in as a superuser, you will come across the custom admin page. This looks quite different than the default admin page as it now has included different fieldsets.


![Screenshot (36)](https://user-images.githubusercontent.com/55087178/110634265-c946b600-81cf-11eb-8f13-3795e70454e7.png)



