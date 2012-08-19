Django Dash 12
==============

We are helping you to migrate from blog platfrom to Pelican-powered blog, hosted on GitHub.


### Installation

1. Clone repo
2. Run `pip install -r requirements/development.txt` in your virtualenv
3. Run `python manage.py syncdb --migrate`
4. Run `python manage.py runserver`
5. Run in another tab `python manage.py celeryd`
6. Open in your browser http://localhost:8000/
7. Enjoy :)
