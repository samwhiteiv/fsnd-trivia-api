# Full Stack Trivia API

This project is a web app that manages and allows users to play a trivia game, with an API built in Flask and a frontend built in React.

## Prerequisites & Installation
- Local Development, including how to set up the local development environment and run the project locally
### Installing PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend micro-services framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first en sure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

# Full Stack Trivia API Frontend

## Getting Setup

### Installing Dependencies

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```

# Endpoints
### GET '/categories'
- Fetches a list/array of categories made up of objects, each with an id and type
- Request Arguments: None
- Returns: A list/array of objects with of id and category type

Example: `curl http://localhost:5000/categories`
```
{
  {
    id: 1
    type: "Science", 
  },
  {
    id: 2
    type: "Art", 
  }, 
  {
    id: 3
    type: "Geography", 
  },
  {
    id: 4
    type: "History", 
  },
  {
    id: 5
    type: "Entertainment", 
  },
  {
    id: 6
    type: "Sports", 
  }
}
```

### GET '/questions'
- Fetches a dictionary of questions, paginated in groups of 10. 
- Returns JSON object of categories, questions dictionary with answer, category, difficulty, id and question.

Example: `curl http://localhost:5000/questions`
```
{
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "current_category": [],
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
        ...
    ],
    "success": true,
    "total_questions": 33
}
```

### DELETE '/questions/<int:question_id>'
- Deletes selected question by id
- Returns 200 if question is successfully deleted.
- Returns 404 if question did not exist
- Returns JSON object of deleted id, remaining questions, and length of total questions

Example: `curl -X DELETE http://localhost:5000/question/2`
```
{
    "deleted_id": 2,
    "questions": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }    
        ...
    ],
    "success": true,
    "total_questions": 32
}
```

### POST '/questions'
- Creates a new question posted from the form on the react front end.
- Fields: answer, difficulty and category. 
- Returns a success value and ID of the question.
- If search field is present will return matching expressions

Example (Create):
`curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who is Tony Stark?", "answer":"Iron Man", "category":"4", "difficulty":"2"}'`
```
{
  "success": true, 
  "total_questions": 35
}

Example (Search):
curl http://localhost:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"Lestat"}'

{
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

### GET '/categories/<cat_id>/questions'
- Returns JSON response of current_category, and the questions pertaining to that category

Example: `curl http://localhost:5000/categories/1/questions`
```
{
 "current_category": {
    "id": 1, 
    "type": "Science"
  }, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
   ...
  ], 
  "success": true, 
  "total_questions": 6
}
```

### POST '/play'
- Generates a quiz based on category or a random selection depending on what the user chooses.

Example: `curl http://localhost:5000/play -X POST -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"type":"Art","id":2}}'`
```
{
  "question": {
    "answer": "One", 
    "category": 2, 
    "difficulty": 4, 
    "id": 18, 
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  }, 
  "success": true
}
```

## Error Handlers

When an error occurs a JSON response is returned
- Returns these error types when the request fails
	- 400: Bad Request
	- 404: Resource Not Found
	- 422: Not Processable
Example for "404: Resource Not Found":
```
{
	"success": False,
	"error": 404,
	"message": "Resource Not Found"
}
```

## Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

6. Authors

7. Acknowledgements