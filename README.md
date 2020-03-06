# Metrics Project

I created a RESTful api in Django framework.

#### Requirements
- `python 3.x`
- `Django 3.0.3`
- `djangorestframework 3.11.0`
- `djangorestframework-jwt 1.11.0`
- `django-filter 2.2.0`
- `Faker 4.0.1`

#### Running the Project
To run the project, from the `cmd`, go to `metrics_project` folder (where is `manage.py` script) and run `python manage.py runserver` command, then on the browser go to the http://127.0.0.1:8000/api/info (`<localhost ip>/api/info`).

In order to login (as administrator for now), go to [/admin](http://127.0.0.1:8000/admin) then login with:

- `id`: admin
- `password`: admin

If the database is empty, there is a script to populate the database with dummy data (generated with `Faker` library), which is located in: 
```
metrics_project
	├── ...
	└── metrics 
		├── ...
		└── management   
			├── ...
			└── commands 
				└── populate_db.py 
```
The script can be runned as a Django-admin command: from the `metrics_project` folder, in the `cmd` run `python manage.py <number_of_records> <user> <password>` (e.g. `python manage.py 1000 admin admin`).

#### The Endpoints
The database has two tables (`Info`, `Category`) and each of them has three endpoints.

For `logged user`:

- For Category:
	- [/api/category](http://127.0.0.1:8000/api/category) -> `GET` endpoint which returns the categories
	- [/api/category/post](http://127.0.0.1:8000/api/category/post) -> `POST` endpoint which requires a string for the category name
	- [/api/category/\<pk\>](http://127.0.0.1:8000/api/category/1) -> `GET` endpoint which returns the selected data with that specific pk and let you to `Get`/ `Put`/ `Patch`/ `Delete` (`RUD`)

- For Info:
	- [/api/info](http://127.0.0.1:8000/api/info) -> `GET` endpoint which returns the data sequentially over time
	- [/api/info/post](http://127.0.0.1:8000/api/info/post) -> `POST` endpoint which requires:
	    - Category (`ForeignKey` to Category tabel) = a string that is already saved in Category tabel
	    - Tags (`TextField` with specific validations) = a string or a list of strings divided by
	    - Value (`FloatField`) = a float
	    - Date (`DateField`) = a date with YYYY-MM-DD format (e.g. 2020/10/23)
	    - Time (`TimeField`) = a time with H:M AM/PM format (e.g. 10:23 PM)
	- [/api/info/\<pk\>](http://127.0.0.1:8000/api/info/1) -> `GET` endpoint which returns the selected data with that specific pk and let you to `Get`/ `Put`/ `Patch`/ `Delete` (`RUD`)

The `unauthenticated user` can access the endpoints in Read Only mode (basically, can use only the `GET` endpoints).

#### Available Filters
The Info `GET` endpoint ([/api/info](http://127.0.0.1:8000/api/info)) supports filters on:
- date after (e.g. `/api/info/?date_after=2000-4-27`) = retrieves only the data with: date field > date_after (e.g. 2000-5-10)
- date before (e.g. `/api/info/?date_before=2000-4-27`) = retrieves only the data with: date field < date_before (e.g. 2000-4-10)
- time after (e.g. `/api/info/?time_after=3:00PM`) = retrieves only the data with: time field > time_after (e.g. 5:00 PM)
- time before (e.g. `/api/info/?time_before=3:00PM`) = retrieves only the data with: time field < time_before (e.g. 10:00 AM)
- category (e.g. `/api/info/?category=oneCateg`) = retrieves only the data with that specific category
- tags (e.g. `/api/info/?tags=random,tags,insert here`) = retrieve only the data which has all the mentioned tags
- all of the above at once (e.g. `/api/info/?date_after=2020-10-10&date_before=2020-10-20&time_after=10:10AM&time_before=3:00PM&category=randomCateg&tags=random,tags,insert here`)

#### Unit Tests
There are unit tests (which can be runned with `python manage.py test` command from the `metrics_project` folder) for the Info endpoints with an unauthenticated user and with a logged user: 
- `POST` 
- `GET` list of items
- `GET`/ `PUT`/ `PATCH`/ `DELETE` an item
- `GET` with filters
    
#### Basic Workflow
Basic Workflow in order to post data if there is no category created (for the logged user):

1. go to [/api/category/post](http://127.0.0.1:8000/api/category/post) -> save a category, for example:
```
{
	"name": "randomCategory"
}
```
2. go to [/api/info/post](http://127.0.0.1:8000/api/info/post) -> save a metric, for example:
```
{
	"category": "randomCategory",
	"tags": "insert tags, here if needed",
	"value": -23.22,
	"date": "2020-10-25",
	"time": "11:23 AM"
}
```
3. go to [/api/info/post](http://127.0.0.1:8000/api/info/post) -> save another measurement, for example:
```
{
	"category": "randomCategory",
	"tags": "",
	"value": 5.56,
	"date": "2000-11-22",
	"time": "2:00PM"
}
```
#### Project Main Files
The main files for the api are in:
```
metrics_project
	├── ...
	└── metrics 
		├── ...
		└── api   
			├── ...
			├── views.py
			├── urls.py
			└── serializers.py 
```
   
The database tabels are in:
```
metrics_project
	├── ...
	└── metrics 
		├── ...
		└── models.py   
```

The unit test scripts are in:
```
metrics_project
	├── ...
	└── metrics 
		├── ...
		└── api   
			├── ...
			└── test
				├── ...
				├── test_delete.py
				├── test_filter.py
				├── test_get.py
				├── test_patch.py
				├── test_post.py
				└── test_put.py 
```
#### The Dashboard
Also, I made a design for the Dashboard page which can be accessed at: [/metrics](http://127.0.0.1:8000/metrics)
The chart which is on the Dashboard page gets the data from the api.