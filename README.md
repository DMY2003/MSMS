# Team Dragonfly Small Group project

## Team members
The members of the team are:
- *[DAMIAN MITROFAN](https://github.com/DMY2003)*
- *[GEORGE KORODIMOS](https://github.com/LuxionDev)*
- *[MOHAMMED CHOWDHURY](https://github.com/ihtasham42)*
- *[SAMIUL ISLAM](https://github.com/Samiul687)*
- *[REIBJOK (Reb) OTHOW](https://github.com/Rebjok)*

## Project structure
The project is called `msms` (Music School Management System).  It currently consists of a single app `lessons` where all functionality resides.

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

## Sources
The packages used by this application are specified in `requirements.txt`

*[Mobirise.com](https://mobirise.com/) - Website Builder - To further edit the home page with Google Maps API etc.*
