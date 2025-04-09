# Big Data Migration API

This is a Big Data Migration Demo API. It has the following features:

- Load jobs, departments and employees data into a database from:
    - An enpoint request (with a limit of 1000 records per request)
    - A file 
 - Create backups from tables into AVRO files
 - Restore tables from said backup files
 - Return analytical queries:
    - Quater by quarter hired employees by department
    - Top hiring departments

## Table of contents

1. Endpoints
2. Run it locally
3. Run it in the cloud


## 1. Endpoints

* Load data endpoints:

    Each endpoint has a GET and POST method implemented, in order to read and write records respectively.

    - <code>/data-load/job</code>
    - <code>/data-load/department</code>
    - <code>/data-load/employee</code>

* Import data from files:
    
    This endpoint loads data into one of the three tables from a file located in a GCS bucket (or also a local file if executed locally).

    - <code>/file-load/</code>

* Create backup from table into a AVRO file:

    This method export all the data from a table into an AVRO file located in a GCS bucket
    - <code>/backup/</code>


* Restore table from backup AVRO file:

    This method restores the data of a table from an AVRO file located in a GCS bucket

    - <code>/backup/restore/</code>

* Analytical endpoints:

    This methods return analytical queries

    - <code>/analytics/quarter-by-quarter/</code>

        Returns all the quarter by quarter hires by department and job names from 2021.

    - <code>/analytics/top-hiring-departments/</code>

        Returns all the departments that had a greater than average number of hires in 2021.


## 2. Run it locally

1. Clone the repository into a local directory

2. Create a Docker image

    Use the file called `Dockerfile` to build a Docker image

3. Run your Docker image into a container
    
    This will expose the API in the port 8000.
    Also it will create a local SQLlite database.

    And your base endpoint will look like `http://127.0.0.1:8000/`


4. Test all the endpoints!

## 3. Run it in the cloud

This API was also designed to run in a GCP enviroment.
For this we use services like:
- `Cloud Run`: To deploy our FastAPI application as a backend service
- `Cloud SQL`: To instanciate a PostgreSQL database
- `Cloud Storage`: To create a bucket to store all our files
- `Secret Manager`: To store the database connection credentials
- `Artifact Registry`: To upload our Docker image

To deploy this app into your GCP project you need to use the `cloudbuild.yaml` file and the following command:

```
gcloud builds submit --config cloudbuild.yaml \ 

--substitutions="\
    _SERVICE_ACCOUNT=<YOUR_SERVICE_ACCOUNT>,
    _CLOUD_SQL_URI=<YOUR_CLOUD_SQL_URI>,
    _SECRET_NAME=<YOUR_SECRET_NAME>,
    _REPO=<YOUR_ARTIFACT_REGISTRY_REPOSITORY>
```

You need to replace the following parameters:

- `<YOUR_SERVICE_ACCOUNT>`: 

    With a service account with the necessary permissions to connect to a Cloud SQL instance, read a Secret Manager and access a Cloud Storage bucket.

- `<YOUR_CLOUD_SQL_URI>`: 

    With a string with the following format: `project:region:instance-name`.

- `<YOUR_SECRET_NAME>`: 

    With the name of your Secret Manager which stores the database connection credentials.

- `<YOUR_ARTIFACT_REGISTRY_REPOSITORY>`: 

    With the name of your Artifact Registry Repository configured to store Docker images.
