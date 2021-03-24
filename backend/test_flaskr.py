import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
  """This class represents the trivia test case"""

  def setUp(self):
    """Define test variables and initialize app."""
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "trivia_test"
    self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)

    # binds the app to the current context
    with self.app.app_context():
        self.db = SQLAlchemy()
        self.db.init_app(self.app)
        # create all tables
        self.db.create_all()

    self.new_question = {
      "category": 2,
      "difficulty": 3,
      "question": "Some question lorem ipsum?",
      "answer": "Some answer lorem ipsum",
    }
  
  def tearDown(self):
      """Executed after reach test"""
      pass

  #TODO: Write at least one test for each test for successful operation and for expected errors.
  #@app.route('/categories', methods=['GET'])
  def test_get_all_categories(self):
    response = self.client.get('/categories')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertTrue(data['categories'])
    self.assertTrue(data['current_category'] is None)

  #@app.route('/questions', methods=['GET'])
  def test_retrieve_questions(self):
    response = self.client().get('/questions')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertTrue(data['questions'])
    self.assertTrue(data['categories'])
    self.assertTrue(data['total_questions'] > 0)
  
  #@app.route('/questions/<int:question_id>', methods=['DELETE'])
  def test_delete_question(self):
    response = self.client().delete('/questions/2')
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['deleted_id'], 2)
    self.assertTrue(data['total_questions'] > 0)

  #@app.route('/questions', methods=['POST']) 
  def test_create_question(self):
    response = self.client.post('/questions', json=self.new_question)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(data['created_id'] > 0)
    self.assertTrue(data['current_questions'] > 0)
    self.assertTrue(data['total_questions'] > 0)
  
  #@app.route('/questions/search', methods=['POST'])
  def test_search_questions_by_term(self):
    response = self.client().post('/questions/search', json={'searchTerm': 'autobiography is entitled'})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertTrue(data['questions'])
    self.assertEqual(data['total_questions'], 1)

  #@app.route('/questions/<int:question_id>', methods=['GET'])
  def test_get_specific_question(self):
    response = self.client.get('/questions/9')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['id'], 9)
    self.assertTrue(data['question'])
    self.assertTrue(data['answer'])

  #@app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def test_get_questions_based_on_category(self):
    response = self.client().get('/categories/5/questions')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertTrue(data['total_questions'] > 0)
    self.assertTrue(data['questions'])

  #@app.route('/play', methods=['POST'])
  def test_init_play_trivia(self):
    test_trivia_json = {'previous_questions': [], 'quiz_category': {'type': 'Art', 'id': 5}} 
    response = self.client().post('/play', json=test_trivia_json)
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertTrue(data['question'])
  
  # @app.errorhandler(404)
  def test_404_on_get_questions(self):
    res = self.client().get('/questions?page=1000')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False )

  # @app.errorhandler(405)
  def test_405_on_add_questions_per_category(self):
    res = self.client().post('/categories/5/questions', json=self.new_question)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 405)
    self.assertEqual(data['success'], False)

  # @app.errorhandler(422)
  def test_422_on_quizz_play(self):
    res = self.client().post('/play', json={'previous_questions': [], 'id': 5})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()