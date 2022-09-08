# API Development and Documentation Final Project

> **PROJECT DESCRIPTION** This project is a quiz application for included in our learning process at Udacity. As a part of the Fullstack Nanodegree, it serves as a practice module for lessons from Course 2: API Development and Documentation. By completing this project, we wil learn and apply our skills structuring and implementing well formatted API endpoints that leverage knowledge of HTTP and API development best practices. 
---
> **APP DESCRIPTION** At the default page of this application we can view the question categories, the total questions paginated in group of 10, and also display these questions by category. We can also delete a question or search for questions providing a `searchTerm`. On another hand, we can create a new question object, providing the question itself,its anwser, difficulty and category.  

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Guidelines

The projet is a follow: there are various 'TODO's marked throughout the porject especially in the files : 
1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

for the `backend/` folder and :
1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

for the `frontend/` folder. 

Theses parts represent the personal work to be done as one completes them. The TODO's in the backend are referenced to those of the fronted in order for the endpoints to match the programmed behavior. 

>**Additional component or behavior are free to be provided.**

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on `localhost:3000`. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb bookshelf_test
createdb bookshelf_test
psql bookshelf_test < books.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 


---
---
## API Reference

### Getting Started
- Base URL: This api can be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 
---
### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return five error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error
---
### Endpoints 
---
#### `GET '/categories'`
- General:
    - Returns a list of category objects and success value.
    - Results are put in dictionary form where the key-value pairs are the category's `id` and `type`. 
- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "categories": {        
    "1": "Science",      
    "2": "Art",
    "3": "Geography",    
    "4": "History",      
    "5": "Entertainment",
    "6": "Sports"        
  },
  "success": true
}
```
---

#### `GET '/questions'`
- General:
    - Returns a list of question objects, success value, total number of questions, categories and current category.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"        
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "total_questions": 29
}
```
---

#### `DELETE '/questions/${id}'`
- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: returns a success value and the id of the deleted question.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/15`

```json
{
  "id": 15,
  "success": true
}
```
---

#### `POST '/questions/create'`
- Sends a post request in order to add a new question.
- Request Body:
- Returns: Returns a success value and the new question object without the id.
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"question": "Where will be held the world cup 2022?", "answer": "Quatar", "category": "6", "difficulty": "3"}' http://127.0.0.1:5000/questions/create`

```json
{
  "question": "Where will be held the world cup 2022?",
  "answer": "Quatar",
  "difficulty": 3,
  "category": 6,
  "success": true}
```
---

#### `POST '/questions/search'`
- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

- Returns: any array of questions, a number of totalQuestions that met the search term, the current category string and a success value.
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' http://127.0.0.1:5000/questions/search`
```json
{
  "questions": [
    {
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
      "answer": "Edward Scissorhands",
      "difficulty": 3,
      "category": 5
    }
  ],
  "success": true,
  "total_questions": 1,
  "current_category": "Entertainment"
}
```
---

#### `GET '/categories/${id}/questions'`
- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, a success value, total questions, and current category string.
- Sample: `curl http://127.0.0.1:5000/categories/4/questions`

```json
{
  "questions": [
    {
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?", 
      "answer": "Muhammad Ali",
      "difficulty": 1,
      "category": 4
    },
    {
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?",
      "answer": "Scarab",
      "difficulty": 4,
      "category": 4
    }
  ],
  "success": true,
  "total_questions": 2,
  "current_category": "History"
}
```
---

#### `POST '/quizzes'`
- Sends a post request in order to get thes question to play the quiz
- Request Body:  takes a category and a list of previous question parameters (empty at the start), the request body is as follow:

```json
{
    "previous_questions": [1, 4, 20, 15],
    "quiz_category": {"type": "History", "id": 4}
}
```
- Returns: return a random questions within the given category, and that is not one of the previous questions and a success value
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1, 4, 20, 15], "quiz_category":  {"type": "History", "id": 4}}' http://127.0.0.1:5000/quizzes`

```json
{
  "question": {
    "id": 9,
    "question": "What boxer's original name is Cassius Clay?",
    "answer": "Muhammad Ali",
    "difficulty": 1,
    "category": 4
  },
  "success": true
}
```

---
---
## Deployment N/A

---
## Authors

---
## Acknowledgements 
The Udacity team.
