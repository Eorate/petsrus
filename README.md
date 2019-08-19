**Introduction**

Implement website to manage pets.

**Root URL**

```
http://localhost/petrus/api/v1.0/
```

**Resource list**

HTTP Method | URI | Action
------------|-----|-------
GET | `/login` | Login to the site
POST | `/register` | Add users to the site
GET | `/pets` | Retrieve list of pets
POST | `/pets` | Add a new pet
GET | `/pets/<id>` | Retrieve details for a particular pet
PUT | `/pets/<id>` | Change the details for a particular pet

**Sample env file**

```
$ less test.env
export FLASK_ENV=development
export APP_SETTINGS="config.TestingConfig"
export DEBUG=True
export DATABASE_URL=sqlite:///test.db
export SECRET_KEY=<insert a random string here>
export TESTING=True                         
```

**To run**

```
$ source test.env
$ python3 run.py
```

**To run tests**

```
$ cd /home/vagrant/mypets
$ source test.env
# To run all tests
$ python3 -m unittest
# To run specific tests
$ python3 -m unittest petsrus.tests.test_views
```

**Sources**

- https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
- https://realpython.com/flask-by-example-part-1-project-setup/
- https://overiq.com/sqlalchemy-101/defining-schema-in-sqlalchemy-orm/
- https://overiq.com/sqlalchemy-101/crud-using-sqlalchemy-orm/
- https://flask-sqlalchemy.palletsprojects.com/en/2.x/
- https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
