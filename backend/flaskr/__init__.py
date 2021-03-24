import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10
# create and configure the app
def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  CORS(app)
  # @TODO: Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

  
  @app.route('/', methods=['GET'])
  def index():
    return jsonify({
      'success': True,
      'message': 'Hello World'
    })

  # Helper functions
  #Get all categories helper function
  def get_all_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = [category.format() for category in categories]
    print('formatted_categories: ', formatted_categories)
    categoriesHashTable = {k: v for d in formatted_categories for k, v in d.items()}
    print('categoriesHashTable: ', categoriesHashTable)
    return formatted_categories

  #Paginate questions helper function
  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions
  
  #@TODO: Create an endpoint to handle GET requests for all available categories.
  @app.route('/categories', methods=['GET'])
  def retrieve_all_categories():
    categories = get_all_categories()
    print('get_categories > ', categories)

    return jsonify({
      'success': True,
      'categories': categories,
      'current_category': None
    })
  
  '''
  @TODO: Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    categories = get_all_categories()

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': categories,
      'current_category': None
    })

  '''
  @TODO: Create an endpoint to DELETE question using a question ID. 
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(404)

      question.delete()
      db.session.commit()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      return jsonify({
        'success': True,
        'deleted_id': question.id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })

    except:
      db.session.rollback()
      abort(422)

  '''
  @TODO: Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    try:
      body = request.get_json()
      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_category = body.get('category', None)
      new_difficulty = body.get('difficulty', None)

      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'created_id': question.id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })
    except:
      abort(422)

  '''
  @TODO: Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  ''' 
  # get questions based on a search term
  @app.route('/questions/search', methods=['POST'])
  def search_questions_by_term():
    search_term = request.get_json()['search_term']
    selection = Question.query.filter(Question.question.ilike('%{}%').format(search_term))
    current_questions = paginate_questions(request, selection)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection.all())
    })

  @app.route('/questions/<int:question_id>', methods=['GET'])
  def get_specific_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()

    if question is None:
      abort(404)

    return jsonify({
      'success': True,
      'id': question.id,
      'question': question.question,
      'answer': question.answer
    })

  '''
  @TODO: Create a GET endpoint to get questions based on category. 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_based_on_category(category_id):
    selection = Question.query.filter(Question.category == category_id).all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'current_category': category_id,
      'questions': current_questions,
      'total_questions': len(selection),
    })

  '''
  @TODO: Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/play', methods=['POST'])
  def init_play_trivia():
    try:
      body = request.get_json()
      previous_questions = body['previous_questions']
      curr_category_id = body['quiz_category']['id']
      print('previous_questions/category_id: ', previous_questions, curr_category_id)

      if curr_category_id == 0:
        selection = Question.query.filter(Question.id.notin_(previous_questions)).all()
      else:
        selection = Question.query.filter(Question.category==curr_category_id, Question.id.notin_(previous_questions)).all()

      current_questions = [question.format() for question in selection]
      if selection:
        new_question = current_questions[random.randint(0, len(selection)-1)]
      else:
        new_question = None

      return jsonify({
        'success': True,
        'question': new_question,
      })

    except:
      abort(422)
  
  #Setup error handling
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  
  @app.errorhandler(405)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed"
      }), 405
  
  return app

""" 
pip3 install -r requirements.txt

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

flask run

http://127.0.0.1:5000/

FLASK_APP=app.py FLASK_DEBUG=true flask run 
http://127.0.0.1:5000/
"""