# Full Stack Trivia API Project

## Introduction

This project was created as part of Udacity's Full Stack Developer Nanodegree program in order to practice implementing API endpoints using development best practices. The goal was to complete the backend API for a trivia web app. The frontend was provided. The application:

1) Displays trivia questions (either all questions or those from a specific category). The category and difficulty rating are also displayed for each question. Users can choose to either show or hide the answer. 
2) Provides the ability to add or delete questions.
3) Provides the ability to search for questions based on a text query string.
4) Includes a quiz game, presenting a random question from all questions or questions within a specific category. Previous questions are not presented again until the game ends.

Backend code follows PEP8 style guidelines.

## Getting Started

### Pre-requisites and Local Development

This project requires that you install Python 3, pip and node software on your development workstation. If you wish to do further development on the project, it is recommended that you set up a virtual environment. Please see specific, additional requirements for both the backend and frontend below. 

### Backend

The backend has been developed upon the Flask/SQLAlchemy framework. All necessary dependencies are listed in __requirements.txt__ in the backend directory. To easily install all required packages, navagate to the backend directory and run the following from the bash command line.

```bash
pip install -r requirements.txt
```

#### Database Setup

The project was developed using a Postgres database, thereby requiring the installation of this system if you do not already have it installed. A version of the underlying database can be restored by running the following from the command line in the backend directory:

```bash
psql trivia < trivia.psql
```

#### Starting the server

The server can be started by executing the following commands from the backend directory:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

### Frontend

This project requires that you install Nodejs and Node Package Manager (NPM), both of which can be downloaded together at [https://nodejs.com/en/download](https://nodejs.org/en/download/).

In order to use NPM to manage the frontend's software dependencies, run the following from the command line from the frontend directory:

```bash
npm install
```

#### Starting The Frontend in Development Mode

To start the app in development mode, type the following from the command line in the frontend directory:

```bash
npm start
```

### Tests

To run the tests included in test_flaskr.py, run the following from the command line in the backend directory:

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

Please note that the first line can be dropped the first time that the test is run.

## API Reference 

### Base URL

In its present form, the app can only be run locally. The frontend is hosted locally at http://127.0.0.1:3000/, while the backend can be accessed at http://127.0.0.1:5000/.

### Authentication

The current version of the application does not require either authentication or API keys.

### Error Handling

Errors are returned as JSON objects. The object below is an example of an error returned if the user tries to retrive a page of questions that does not exist:

```
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```

The API will return the following error types:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable

### Resource Endpoint Library

#### GET /categories

Returns a dictionary of categories. The keys are the category ids and the values are the corresponding category name string.

##### Sample Request

```
curl http://127.0.0.1:5000/categories
```

##### Sample Response

```
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

#### GET /questions

Returns a list of question objects, success value, total number of questions, and a dictionary of the question categories. Results are paginated in groups of 10. A request argument to choose page number can be included, starting from 1.

##### Sample Request

```
curl http://127.0.0.1:5000/questions?page=1
```

##### Sample Response

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
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
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
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
    }
  ], 
  "success": true, 
  "total_questions": 20
}
```

#### DELETE /questions/{question_id}

Deletes a quesiton with the given id if it exists. Returns the id of the deleted question, success value, total number of questions, and a list of questions based on current page number to update the frontend.

##### Sample Request

```
curl -X DELETE http://127.0.0.1:5000/questions/14
```

##### Sample Response

```
{
  "deleted": 14, 
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
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
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
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

#### POST /questions - To post a new question

Creates a new question using the submitted question and answer text, category and difficulty level. Returns the id of the created question, success value, total number of questions, and and a list of questions based on current page number to update the frontend.

##### Sample Request

```
curl http://127.0.0.1:5000/questions?page=2 -X POST -H "Content-Type: application/json" -d '{"question":"How many lives does a cat have?", "answer":"Nine", "category":"1", "difficulty":"1"}'
```

##### Sample Response

```
{
  "created": 24, 
  "questions": [
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
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "Nine", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "How many lives does a cat have?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}
```

#### POST /questions - To search

Performs a case insensitive search based upon the provided search string. Returns the success value, total number of questions in the search results, and and a list of questions that match the search criteria to update the frontend.

##### Sample Request

```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'
```

##### Sample Response

```
{
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

#### GET /categories/{category_id}/questions

Based upon a provided category id, returns a list of question objects, success value, total number of questions, current category and a dictionary of the question categories. Results are paginated in groups of 10. 

##### Sample Request

```
curl http://127.0.0.1:5000/categories/2/questions
```

##### Sample Response

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": 2, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
```

#### POST /quizzes

Based upon a provided category and a list of the ids of previously asked questions, returns a single question and a success value. The question is randomly chosen from the questions in the given category that have not yet been presented to the user. 

##### Sample Request

```
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [22], "quiz_category": {"type": "Science", "id": "1"}}'
```

##### Sample Response

```
{
  "question": {
    "answer": "Nine", 
    "category": 1, 
    "difficulty": 1, 
    "id": 24, 
    "question": "How many lives does a cat have?"
  }, 
  "success": true
}
```

## Authors

Maleina Bidek.

Udacity Team. (Some of this readme has been paraphrased from the project instructions and the team also provided the initial starter code.)

## Acknowledgements

Thanks to the entire Udacity Team, especially to our instructor, Caryn, and to my mentor, Sabrina!


