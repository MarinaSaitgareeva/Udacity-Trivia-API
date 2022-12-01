# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.11** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip3 install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask --app flaskr --debug run
```

The `--debug` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

### Trivia API Documentation

### Endpoints

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Arguments: None.
- Returns:
    - `success` - the success flag.
    - `categories` - an object of `id: category_string` key: value pairs.

```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

`GET '/questions'`

- Fetches a list of questions paginated by 10 items per page.
- Request Arguments: page (integer) - the current page.
- Returns:
    - `success` - the success flag.
    - `questions` - a list of questions paginated by 10 items per page.
    - `total_questions` - number of total questions.
    - `categories` - an object of `id: category_string` key: value pairs.
    - `current_category` - the current category.

```json
{
  "success": true,
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
    ...
  ],
  "total_questions": 19,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null
}
```

`DELETE '/questions/int:question_id'`

- Delete the question using the question ID.
- Request Arguments: question_id (integer) - the question id.
- Returns:
    - `success` - the success flag.
    - `deleted` - the question id.
    - `questions` - a list of questions paginated by 10 items per page.
    - `total_questions` - number of total questions.

```json
{
  "success": true,
  "deleted": 1,
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
    ...
  ],
  "total_questions": 19
}
```

`POST '/questions'`

- Create a new question.
- Request Arguments:
    - question (string),
    - answer (string),
    - difficulty (int),
    - category (int)
- Returns:
    - `success` - the success flag.
    - `added` - the new question ID.
    - `new_question` - the new question string.
    - `total_questions` - number of total questions.

```json
{
  "success": true,
  "added": 25,
  "new_question": "What is ...?",
  "total_questions": 20
}
```

`POST '/questions/search'`

- Search a question.
- Request Arguments: search term (string).
- Returns:
    - `success` - the success flag.
    - `questions` - a list of questions paginated by 10 items per page.
    - `total_questions` - number of total questions.
    - `current_category` - the current category.

```json
{
  "success": true,
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
    ...
  ],
  "total_questions": 19,
  "current_category": null
}
```

`GET '/categories/int:category_id/questions'`

- Fetches a list of questions paginated by 10 items per page based on the category.
- Request Arguments: category_id (integer) - the category id.
- Returns:
    - `success` - the success flag.
    - `category` - the category name.
    - `questions` - a list of questions paginated by 10 items per page.
    - `total_questions` - number of total questions.

```json
{
  "success": true,
  "category": "Science",
  "questions": [
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
    }
  ],
  "total_questions": 19
}
```

`POST '/quizzes'`

- Fetches a question to play the quiz.
- Request Arguments:
    - quiz_category (integer, id),
    - previous_questions (list of strings)
- Returns:
    - `success` - the success flag.
    - `question` - a question to play in quiz.

```json
{
  "success": true,
  "question":
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
}
```

### Errors

`Error 400`

- Returns: an object with these keys: success, error and message.

```json
{
  "success": false,
  "error": 400,
  "message": "Bad Request"
}
```

`Error 404`

- Returns: an object with these keys: success, error and message.

```json
{
  "success": false,
  "error": 404,
  "message": "Resource Not Found"
}
```

`Error 405`

- Returns: an object with these keys: success, error and message.

```json
{
  "success": false,
  "error": 405,
  "message": "Method Not Allowed"
}
```

`Error 422`

- Returns: an object with these keys: success, error and message.

```json
{
  "success": false,
  "error": 422,
  "message": "Unprocessable resource"
}
```

`Error 500`

- Returns: an object with these keys: success, error and message.

```json
{
  "success": false,
  "error": 500,
  "message": "Internal server error"
}
```


### Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```