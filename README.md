[![CircleCI](https://circleci.com/gh/Eorate/petsrus.svg?style=shield)](https://circleci.com/gh/Eorate/petsrus)
[![Maintainability](https://api.codeclimate.com/v1/badges/f65b3b686e29acc8e177/maintainability)](https://codeclimate.com/github/Eorate/petsrus/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f65b3b686e29acc8e177/test_coverage)](https://codeclimate.com/github/Eorate/petsrus/test_coverage)

**Introduction**

Implement a simple python-flask website to manage pets.


**Sample env file**

```
$ less test.env
export APP_SETTINGS="config.TestingConfig"
export AWS_ACCESS_KEY_ID=<aws-access-key-id>
export AWS_SECRET_ACCESS_KEY=<aws-secret-access-key>
export AWS_DEFAULT_REGION=<aws-default-region>
export BACKBLAZE_URL=<backblaze-url>
export DEBUG=True
export DATABASE_URL=sqlite:///test.db
# or 
export DATABASE_URL="postgresql://<databaseuser>:<password>@<host>:5432/<database>"
export FLASK_ENV=development
export S3_BUCKET=<s3-bucket-name>
export SECRET_KEY=<insert a random string here>
export SENTRY_ENVIRONMENT=testing
export SENTRY_URL=<sentry-url>
export TESTING=True                         
export UPLOADED_IMAGE_URL=<uploaded-image-url>

# Test data credentials
export TEST_USERNAME=<test-username>
export TEST_PASSWORD=<test-password>
export EMAIL_ADDRESS=<test-email-address>

```

**To run**

```
$ cd /home/vagrant/mypets
$ source env/bin/activate
$ source test.env
$ python3 run.py
```

**To run tests**

```
$ cd /home/vagrant/mypets
$ source env/bin/activate
$ source test.env
# To run all tests
$ python3 -m unittest
# To run specific tests
$ python3 -m unittest petsrus.tests.test_views
or
$ python3 -m unittest petsrus.tests.test_views.PetsRUsTests.test_edit_pets
# To get coverage
$ coverage run -m unittest
$ coverage report
```

**To add sample data**

```
$ cd /home/vagrant/mypets
$ source env/bin/activate
$ source test.env
$ python3 populate_data.py
```

**Sources**

- https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
- https://realpython.com/flask-by-example-part-1-project-setup/
- https://overiq.com/sqlalchemy-101/defining-schema-in-sqlalchemy-orm/
- https://overiq.com/sqlalchemy-101/crud-using-sqlalchemy-orm/
- https://flask-sqlalchemy.palletsprojects.com/en/2.x/
- https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
- https://www.fullstackpython.com/flask-sqlalchemy-model-examples.html
- https://www.w3schools.com/bootstrap4/default.asp
- https://bootsnipp.com/snippets/DOXy4
