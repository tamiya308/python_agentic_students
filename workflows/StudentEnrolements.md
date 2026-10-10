## Objective
Serve basic GET, POST, PUT and DELETE endpoints for StudentEnrolements. The back end database will be an AWS DyanomoDb Courses table

## Overview of what to create
- Create or update the `StudentEnrolements` endpoints in src\api\StudentEnrolements.py (refer to the Endpoint structure below)
- Create the Pydantic model in `src/models/studentEnrolements.py`
(use the StudentEnrolements sample data below as a reference for the model)
- Create unit tests in `tests/test_student_enrolement_api.py`. Cover every response code for each of the end points. Each test uses a temporary database (`tmp_path`).
- Use the environment variable "DynamoDbConnString" to get the dynamoDb connection string.
- In `main.py` during the program startup generate code using the boto3 library to create the StudentEnrolments table if it doesn't already exist.
- In `seed_StudentEnrolements.py` generate code to seed 5 new records into that table if there is no data. Do not run this code as part of the `main.py` execution. It should only be run on my command. 
- Use the boto3 library to perform operations on the dynamoDb

## StudentEnrolements sample data
{
    "StudentId" : 1000,
    "StudentName" : "Alan Jones",
    "CourseName": "Commerce"
    "UnitsToComplete":[
        {
            "UnitId": 20,
            "UnitName": "Introduction to business",
        },
        {
            "UnitId": 21,
            "UnitName": "Managements basics"
        }
    ]
}

## Endpoint structure
| Name | Request | Responses |
| getAllStudentEnrolements | `GET /studentenrolements` | 200 with the list, ordered by id |
| getStudentEnrolements  | `GET /studentenrolements/{id}` | 200, or 404 if the id doesn't exist |
| postStudentEnrolements  | `POST /studentenrolements` | 201 with the created record; 409 on a duplicate `name`; 422 on invalid input |
| putCourse | `PUT /studentenrolements/{id}` | 200 with the record; replaces the whole record; 404 if missing, 409 on a duplicate `name`, 422 on invalid input |
| deleteCourse | `DELETE /studentenrolements/{id}` | 204 on success; 404 if missing; |
