# Flask Hospital Management System

A web based hospital management system built in [flask](flask.palletsprojects.com) | the python framework

## Features
    
- User management *(Admin/User)*
- Manage Patients
- Manage Doctors
- Manage Appointments
- Manage Departments
- Uses [Postgresql](https://postgresql.org) as database


## Required Dependency

install *psycopg2* for database connection

```
pip3 install psycopg2
```

## Usage

After cloning repo open the *.env* file and paste the **APP_SETTINGS** & **DATABASE_URL** to console.
```
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql:///hospital_db"
```
then run the *app.py* file.



## Contribution

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository.
