## Objective
Serve basic GET, POST, PUT and DELETE endpoints for StudentEnrolments. The back end database will be an AWS DyanomoDb StudentEnrolments table.

## Overview of what to create
- Create or update the `StudentEnrolments` endpoints in src\api\StudentEnrolments.py (refer to the Endpoint structure below)
- Create the Pydantic model in `src/models/StudentEnrolments.py`
(use the StudentEnrolments sample data below as a reference for the model)
- Create unit tests in `tests/test_student_enrolement_api.py`. Cover every response code for each of the end points. Each test uses mocked Moto db.
- Use the environment variable "DynamoDbUrl" to get the dynamoDb url.
- In `main.py` during the program startup generate code using the boto3 library to create the StudentEnrolments table if it doesn't already exist.
- In `seed_StudentEnrolments_LOCAL.py` (DynamoDB Local) and `seed_StudentEnrolments_DEV.py` (AWS dev, different sample data) generate code to seed 5 students (9 course items, 2 students in 3 courses) into that table if there is no data. Do not run this code as part of the `main.py` execution. It should only be run on my command. 
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

## Table keys
- Partition key: `StudentId` (number). Sort key: `CourseName` (string).
- One item per student per course, so a student can be enrolled in several courses.
- A `StudentName` belongs to one `StudentId` and must be the same on all of that student's course items.

## Endpoint structure
| Name | Request | Responses |
| getAllStudentEnrolments | `GET /StudentEnrolments` | 200 with the list, ordered by StudentId then CourseName |
| getStudentEnrolments  | `GET /StudentEnrolments/{id}` | 200 with all of the student's course enrolments, or 404 if the id doesn't exist |
| getStudentCourseEnrolment | `GET /StudentEnrolments/{id}/{courseName}` | 200, or 404 if the enrolment doesn't exist |
| postStudentEnrolments  | `POST /StudentEnrolments` | 201 with the created record; 409 if the student is already in that course or on a `StudentName` conflict; 422 on invalid input |
| putStudentEnrolments | `PUT /StudentEnrolments/{id}/{courseName}` | 200 with the record; replaces the whole record; 404 if missing, 409 on a `StudentName` conflict, 422 on invalid input |
| deleteStudentEnrolments | `DELETE /StudentEnrolments/{id}/{courseName}` | 204 on success; 404 if missing; |
