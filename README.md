## Forge Focus Api
Created by Jamie Connell Student of CodeInstitute 2024

This is an API which will provide full CRUD functionality for the management of task data. This will include areas such as goals, and sub categories within a users main goal. This API utilizes the Django-Rest-Framework and is created to provide backend functionality to the "Forge Focus" application. 

**Link for API will go here when available**
**Link for deployed Heroku App will go here when available**
**Link for frontend react repository will go here when available**

## Table of Contents
- [Design of the API](#Design-of-the-API)
- [API Features](#API-Features)
- [Future Features For API](#Future-Features-for-API)
- [Lanuages Used](#Lanuages-Used)
- [Frameworks and Libraries Used](#Frameworks-and-Linraries-used)
- [Tools and Technologies Used](#Tools-and-Technologies-Used)
- [Validatrion and Testing](#Validation-and-Testing)
- [Known Bugs and Fixes](#Known-Bugs-and-Fixes)
- [Deployment](#deployment)
    - [Cloning Repository](#Cloning-Repository)
        - [CodeAnywhere](#CodeAnywhere)
        - [GitPod](#Gitpod)
    - [Forking Repository](#Forking-Repository)
- [Connecting to this API](#Connecting-to-this-API)
- [Credits](#Credits)
- [Acknowledgements](#Acknoledgements)

## Design of the API

### Aim

The aim of the API is to store task data that includes setting areas to refine ("goals"), create tasks
which can be independantly worked on or linked to a main goal.

provide a full range of CRUD functionality to any linked applications.  

### Considerations when creating

The following were taken into consideration when creating the API 

1. User authentication will be included within the API, with read, update and delete functionality initially only available to the owner of the data. A Later function maybe added that will allow for access to be granted to team member users.

2. Secret keys etc. will be hidden and Debug set to False for the deployed API.

3. Only trusted URLs, specified directly within the API, will be able to make requests to the API and access any CRUD functionality.

## API Features

### Security Features

Only the following can be accessed by users who are not authenticated, all other endpoints of the API
can be accessed if a user has created an account and is authorised.

- The base root, This give the user a welcome message and a some information
- The /dj-rest-auth/registration/ endpoint, this will allow new users to register to the application.
- The /dj-rest-auth/login/ endpoint, which allows registered users to log in.

Only owners of a data instance can access any CRUD functionality related to it. All get requests
made by a user/owner will return a list with only the items belonging to that user/owner. 
Any requests made by a user/owner for a specific item that user/owner does not own will be denied.

### User Model
Users of the page can, Register, Login and Logout

| Field | Automatic/Required/Optional | Notes|
|--|--|--|
| Username| Required  | Must be Unique and cannot be same as already registered user|--|--|--|
| Email Address | Required | Must be unique and in correct format and cannot be already registered|--|--|--|
|Password |Required | Must pass complexity rules to prevent common or easily guessable passwords

Below are the endpoints for the user model
|URL| notes |
|--|--|
| dj-rest-auth/registration/ | register a new user account |
|dj-rest-auth/login/ | allow user to login |
|dj-rest-auth/logout/ | allow user to logout |

### User Model


### Goals Model
Users can store goals that they wish to work on this can be given a "reason", describing why they have set the goal and if they wish the user can upload an image to the goal.

Fields held within the database:
|Field| Automatic/required/optional | notes  |
|--|--|--|
| owner	 | Automatically Generated | Foreign key link to a user instance |
|created_at|Automatically Generated | DateTime
|updated_at|Automatically Generated | DateTime
|name| required | text of max 50 characters|
| reason |optional | text |
|image| default provided if non given| stored in cloudinary, only images smaller than 2mbs, height 4096 and width: 4096 will be accepted|

Extra fields generated and returned with a GET request:
 - is owner field, which will return true if the authorized user is the owner 

Endpoints for the goals model:
|URL| http request | notes
|--|--|--|
| goals/  | GET  | Returns a list of the user's goals ordered by created_at with with the most recently created listed first.
| goals/ | POST | Create a new goal |
| goals/id | GET | Get a specific goal using it's ID |
| goals/id | PUT | Update a goal |
| goals/id | PATCH | update a field within a goal |
| goals/id | DELETE | Delete a focus area using its ID |

### Tasks Model

Users can store tasks, these tasks can be independent or can be linked to a goal. They can be toggled as active or not.

Fields held within the database:

|Field| Automatic/required/optional | notes  |
|--|--|--|
| owner	 | Automatically Generated | Foreign key link to a user instance |
| goal | optional | Foreign key lined to a goal, input goal ID |
|created_at|Automatically Generated | DateTime
|updated_at|Automatically Generated | DateTime
|name| required | text of max 50 characters|
| reason |optional | text |
|image| default provided if non given| stored in cloudinary, only images smaller than 2mbs, height 4096 and width: 4096 will be accepted|