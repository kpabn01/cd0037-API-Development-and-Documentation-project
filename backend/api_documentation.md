# API Reference (TRIVIA)

## Getting Started
- Base URL: This api can be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 
---
## Error Handling
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
## Endpoints 
---
### `GET '/categories'`
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

### `GET '/questions'`
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

### `DELETE '/questions/${id}'`
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

### `POST '/questions/create'`
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

### `POST '/questions/search'`
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

### `GET '/categories/${id}/questions'`
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

### `POST '/quizzes'`
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
