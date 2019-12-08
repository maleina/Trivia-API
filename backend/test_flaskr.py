import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case."""

    def setUp(self):
        """ Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # This is a sample question to be used during the test
        # of the insertion endpoint.
        self.new_question = { 
            "question":"How many lives does a cat have?",
            "answer":"Nine",
            "category":1,
            "difficulty":1
            }
        # This is sample request data to be used during the 
        # test of the quiz function.
        self.quiz = { 
            "previous_questions":[22],
            "quiz_category":{'type': 'Science', 'id': '1'}
            }

        # Binds the app to the current context.
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # Create all tables.
            self.db.create_all()
    
    def tearDown(self):
        """ Executed after reach test."""
        pass

    """
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_retrieve_all_categories(self):
        # Test for successful retrival of all categories.
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_retrieve_categories_fails(self):
        # Test for failed retrival of categories.
        res = self.client().get('/categories/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_retrieve_all_questions(self):
        # Test for successful paginated retrival of all questions.
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_retrieve_questions_beyond_valid_page(self):
        # Test for unsuccessful paginated retrival of questions, i.e. 
        # the page is beyond the available amount of pages.
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        # Test for the sucessful deletion of a question.
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 5).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)

    def test_422_delete_if_question_does_not_exist(self):
        # Test for failure when the question to be deleted
        # doesn't exist.
        res = self.client().delete('/questions/500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_question(self):
        # Test for the successful creation of a new question.
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))


    def test_422_question_creation_fails(self):
        # Test the failure case for creating a new question.
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_question_search_with_results(self):
        # Test for the successful retrieval of a search request.
        res = self.client().post('/questions', json={'searchTerm':'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']), 2)

    def test_question_search_without_results(self):
        # Test for the sucessful processing of a search with no results.
        res = self.client().post('/questions', json={'searchTerm':'BlahBlahBlahBlahBlah'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

    def test_retrieve_questions_by_category(self):
        # Test for successful paginated retrival of questions by a given category.
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_fail_retrieve_questions_bad_category(self):
        # Test for unsuccessful paginated retrival of questions when 
        # the category does not exist.
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_quiz(self):
        # Test that the quiz returns valid questions that have 
        # not previously been used.
        res = self.client().post('/quizzes', json=self.quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    def test_quiz_fail(self):
        # Test for the failure of the quiz when a bad 
        # request has been sent.
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

# Make the tests conveniently executable.
if __name__ == "__main__":
    unittest.main()