## Objective
Serve basic GET, POST, PUT and DELETE endpoints for StudentEnrolments. The back end database will be an AWS DyanomoDb StudentEnrolments table.

## Overview of what to create
- Create or update the `StudentEnrolments` endpoints in src\api\StudentEnrolments.py (refer to the Endpoint structure below)
- Create the Pydantic model in `src/models/StudentEnrolments.py`
(use the StudentEnrolments sample data below as a reference for the model)
- Create unit tests in `tests/test_student_enrolement_api.py`. Cover every response code for each of the end points. Each test uses mocked Moto db.
- Use the environment variable "DynamoDbUrl" to get the dynamoDb url.
- In `main.py` during the program startup generate code using the boto3 library to create the StudentEnrolments table if it doesn't already exist.
- In `seed_StudentEnrolments_LOCAL.py` (DynamoDB Local) and `seed_StudentEnrolments_DEV.py` (AWS dev, different sample data) generate code to seed 5 new records into that table if there is no data. Do not run this code as part of the `main.py` execution. It should only be run on my command. 
- Use the boto3 library to perform operations on the dynamoDb

## StudentEnrolments sample data
{
    "StudentId" : 1000,
    "StudentName" : "Alan Jones",
    "CourseName": "Commerce",
    "UnitsToComplete":[
        {
            "UnitId": 20,
            "UnitName": "Introduction to business"
        },
        {
            "UnitId": 21,
            "UnitName": "Managements basics"
        }
    ]
}

## Endpoint structure
| Name | Request | Responses |
| getAllStudentEnrolments | `GET /StudentEnrolments` | 200 with the list, ordered by StudentId |
| getStudentEnrolments  | `GET /StudentEnrolments/{id}` | 200, or 404 if the id doesn't exist |
| postStudentEnrolments  | `POST /StudentEnrolments` | 201 with the created record; 422 on invalid input |
| putStudentEnrolments | `PUT /StudentEnrolments/{id}` | 200 with the record; replaces the whole record; 404 if missing, 409 on a duplicate `name`, 422 on invalid input |
| deleteStudentEnrolments | `DELETE /StudentEnrolments/{id}` | 204 on success; 404 if missing; |
