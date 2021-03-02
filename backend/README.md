# Trivia API

## Introduction
Trivia is an API that control of a set of questions and their categories and help you to do the following :
- Get all available  questions
- Get all available  categories
- Get questions based on category type
- Create a new question
- Delete a specific question
- Provide a quiz game with random question from a set of questions share the same category
- Search through the entire data base for a certain question by just using substring of this question

## Getting Started

### Instruction to run the Application
- #### python 3.7 
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
- #### Install Virtual Environment 
```sh
pip3 install virtualenv
```
- #### navigating to the `/backend` directory:
```sh
cd backend
```
- #### Run the Virtual Environment
  Create virtual environment
  ```sh
  python3 -m venv env
  ```
  and then
  - for mac and linux
  ```sh
    source env/bin/activate
  ```
  - for windows
  ```sh
    env/Scripts/activate
  ```
- #### Installing Dependencies
Once you have your virtual environment setup and running, install dependencies

```sh
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:
- for mac and linux
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
- for windows
```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 
### API Reference

 - BASE URL: Since the application isn't deployed yet and still hosted on the local machine so the base URL is `127.0.0.1:500/api`.
 - Authentication: This version of the application doesn't require authentication or API Keys.

### Errors

#### Errors are returned as JSON object in the following format:

``` json
{
    "success":False,
    "error":404,
    "message":"Not Found"
}
```

#### The API will return 3 error types

- 400 Bad Request
- 404 Not Found
- 405 Method Not Allowed

### Endpoints

##### GET `/questions`

- Returns a list of questions , categories, total_questions and success

- Pagination: add query page `/questions?page=1` and by default return 10 per page but you can specify the limit for each page by adding limit query `/questions?page=1&limit=15`

-  sample : 

  ```sh
  curl http://127.0.0.1:500/api/questions
  ```

- Response Object:

  ```json
  {
    "categories": [
      {
        "id": 1, 
        "type": "Science"
      }, 
      {
        "id": 2, 
        "type": "Art"
      }, 
      {
        "id": 3, 
        "type": "Geography"
      }, 
      {
        "id": 4, 
        "type": "History"
      }, 
      {
        "id": 5, 
        "type": "Entertainment"
      }, 
      {
        "id": 6, 
        "type": "Sports"
      }
    ], 
    "questions": [
      {
        "answer": "Maya Angelou", 
        "category_id": 4, 
        "category_name": "History", 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }, 
      {
        "answer": "Edward Scissorhands", 
        "category_id": 5, 
        "category_name": "Entertainment", 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }, 
      {
        "answer": "Muhammad Ali", 
        "category_id": 4, 
        "category_name": "History", 
        "difficulty": 1, 
        "id": 9, 
        "question": "What boxer's original name is Cassius Clay?"
      }, 
      {
        "answer": "Brazil", 
        "category_id": 6, 
        "category_name": "Sports", 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "Uruguay", 
        "category_id": 6, 
        "category_name": "Sports", 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }
    ], 
    "success": true, 
    "total_questions": 25
  }
  ```

##### GET `/categories`

- Returns a list of categories, ,total_categories and success

- sample:

  ```sh
  curl http://127.0.0.1:500/api/categories
  ```

- Response Object:

  ```json
  {
    "categories": [
      {
        "id": 1, 
        "type": "Science"
      }, 
      {
        "id": 2, 
        "type": "Art"
      }, 
      {
        "id": 3, 
        "type": "Geography"
      }, 
      {
        "id": 4, 
        "type": "History"
      }, 
      {
        "id": 5, 
        "type": "Entertainment"
      }, 
      {
        "id": 6, 
        "type": "Sports"
      }
    ], 
    "success": true, 
    "total_categories": 6
  }
  ```

##### DELETE `/questions/{question_id}`

- Delete the the question based on the provided question_id and return success, id of the deleted question and the deletion message.

- sample:

  ```sh
  curl -X DELETE http://127.0.0.1:5000/api/questions/{question_id}
  ```

- Response object:

  ```json
  {
    "id": 12,
    "message": "Question has been deleted",
    "success": true
  }
  ```

##### POST `/questions`

- Create a new questions based on the provided data

- Return the success, created question id and the count of total questions

- sample:

  ```sh
  curl -X POST http:/127.0.0.1:5000/api/questions -H 'Content-Type:application/json' -d '{"question":"Where is Egypt Located?", "answer":"north-east of africa", "difficulty":1, "category":3}'
  ```

- Response Object:

  ```json
  {
    "id": 33,
    "success": true,
    "total_questions": 25
  }
  ```

##### GET `categories/{category_id}/questions`

- Get all question based on the provided category_id 

- Return questions with same category, success and total questions

- sample:

  ```sh
  curl http:/127.0.0.1:5000/api/categories/{category_id}/questions
  ```

- Response Object:

  ```json
  {
    "questions": [
      {
        "answer": "Lake Victoria",
        "category_id": 3,
        "category_name": "Geography",
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
      },
      {
        "answer": "The Palace of Versailles",
        "category_id": 3,
        "category_name": "Geography",
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
      },
      {
        "answer": "Agra",
        "category_id": 3,
        "category_name": "Geography",
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
      },

      {
        "answer": "north-east of africa",
        "category_id": 3,
        "category_name": "Geography",
        "difficulty": 1,
        "id": 33,
        "question": "Where is Egypt Located?"
      }
    ],
    "success": true,
    "total_questions": 25
  }
  ```

##### POST `/questions/search`

- Get all questions based on the provided search keyword 

- Return questions, success and the count of total questions

- sample:

  ```sh
  curl -X POST http:/127.0.0.1:5000/api/questions/search -H 'Content-Type:application/json' -d '{"searchTerm":"egypt"}'
  ```

- Response Object:

  ```json
  {
    "questions": [
      {
        "answer": "north-east of africa",
        "category_id": 3,
        "category_name": "Geography",
        "difficulty": 1,
        "id": 33,
        "question": "Where is Egypt Located?"
      },
      {
        "answer": "Scarab",
        "category_id": 4,
        "category_name": "History",
        "difficulty": 4,
        "id": 23,
        "question": "Which dung beetle was worshipped by the ancient Egyptians?"
      }
    ],
    "success": true,
    "total_questions": 25
  }
  ```

##### GET `/quizzes`

- The client which is quiz game send data that contains list of previous questions id that been answered and their category id and type

- The endpoint will go through this list of question id to exclude those questions and get a list of the rest 

- then select a question randomly from that list 

- and return this random question, success and count of total questions

- sample:

  ```sh
  curl -X POST http:/127.0.0.1:5000/api/quizzes -H 'Content-Type:application/json' -d '{"previous_questions":[20], "quiz_category":{"type":"Science", "id":1}}'
  ```

- Response Object:

  ```json
  {
    "question": {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    "success": true,
    "total_question": 4
  }
  ```

  