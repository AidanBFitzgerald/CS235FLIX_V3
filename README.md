# CS235FLIX_V3
## Description

A web application that demonstrates use of Python's Flask framework. The application makes use of libraries such as the Jinja templating library and WTForms. Architectural design patterns and principles including Repository, Dependency Inversion and Single Responsibility have been used to design the application. The application uses Flask Blueprints to maintain a separation of concerns between application functions. Testing includes unit and end-to-end testing using the pytest tool.
This web app displays a database of 1000 movies

## Installation

**Installation via requirements.txt** 

```shell
$ cd CS235FLIX_V3
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

## Execution

**Running the application**

From the CS235FLIX_V3 directory, and within the activated virtual environment (see venv\Scripts\activate above):

```shell
$ flask run
```


## Testing

**Running the application tests**

From the CS235FLIX_V3 directory, and within the activated virtual environment (see venv\Scripts\activate above):

```shell script
$ python -m pytest
```
