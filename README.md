
# Reddit-DRF

Reddit-inspired project developed using Django Rest Framework.
The project follows the structure of Reddit based on subreddits, posts, and comments.
All calls that are not read-only require authorization.
The supported authorization method is a token authorization.

All of the views are covered with tests.

## Features

**General features:**
- Browsing and adding new subreddits
- Displaying subreddit details
- Browsing a list of posts in the subreddit and adding new posts to the subreddit
- Displaying posts from all subreddits
- Displaying post details
- Browsing post comments and adding new comments to the post
- Generating auth tokens

**Role-related features:**
- Superuser has all the privileges
- Subreddit owner can:
    - Edit and delete the subreddit, posts, and comments in it
    - Manage a list of moderators of the subreddit
- Subreddit moderator can:
    - Edit and delete posts and comments in the subreddit
- Post author:
    - Edit and delete his posts
- Comment author:
    - Edit and delete his comments

## Installation
**Requirements:**
You must have python 3.10 and git installed on your machine.

Clone repository:
```bash
$ git clone https://github.com/bartvbx/reddit-drf.git
$ cd reddit-drf
```

Set and run virtual environment:
```bash
$ py -m venv ./venv
$ . venv/Scripts/activate
```

Install required dependencies and run migrations:
```bash
(venv)$ pip install -r requirements.txt
(venv)$ python manage.py migrate
```

Before starting the Django app, you need to set the 'R_DRF_SECRET_KEY' environment variable or provide a secret key value in settings.py.

You can run tests:
```bash
(venv)$ python manage.py test
```

Now you can run the app:
```bash
(venv)$ python manage.py runserver
```

By default, the app will run at localhost:8000.

## Tech Stack

Backend:
- Python
- Django
- Django REST framework
- SQLite

## License

[MIT](https://choosealicense.com/licenses/mit/)
