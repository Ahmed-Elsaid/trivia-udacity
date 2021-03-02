import os
import sys
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
        self.database_path = "postgresql:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.newQuestion = {
            'question': 'where is egypt',
            'answer': 'north-east africa',
            'difficulty': 1,
            'category': 3
        }

        self.existedQuestion = {
            'question': "What boxer's original name is Cassius Clay?",
            'answer': " Muhammad Ali",
            'difficulty': 1,
            'category': 4
        }
        self.quiz = {
            'previous_questions': [20],
            'quiz_category': {
                "type": "Science",
                "id": 1
            }
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    ##################################################
    # Test Get All Questions
    ##################################################
    def test_get_all_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])

    ##################################################
    # Test Get Paginated Questions
    ##################################################
    def test_get_paginated_questions(self):
        res = self.client().get('/api/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    ##################################################
    # Test 404 Sent Requesting Beyond Valid Page
    ##################################################
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/api/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    ##################################################
    # Test Get All Categories
    ##################################################
    def test_get_all_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['count'])

    ##################################################
    # Test Delete Question
    ##################################################
    def test_delete_question(self):
        res = self.client().delete('/api/questions/21')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 21)
        self.assertTrue(data['message'])

    ##################################################
    # Test Create a New Question
    ##################################################
    def test_create_new_question(self):
        res = self.client().post('/api/questions', json=self.newQuestion)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['count'])

    ##################################################
    # Test 405 If Question Creation Not Allowed
    ##################################################
    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/api/questions/5', json=self.newQuestion)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed")

    ##################################################
    # Test 400 If Question Creation Already Exist
    ##################################################
    def test_400_if_question_creation_already_exist(self):
        res = self.client().post('/api/questions', json=self.existedQuestion)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    ##################################################
    # Test Get Question By Category
    ##################################################
    def test_get_question_by_category(self):
        res = self.client().get('/api/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], len(Question.query.all()))

    ##################################################
    # Test Get Question By Search with Result
    ##################################################
    def test_get_question_by_search_with_result(self):
        res = self.client().post('/api/questions/search',
                                 json={"searchTerm": "clay"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], len(Question.query.all()))

    ##################################################
    # Test Get Question By Search without Result
    ##################################################
    def test_get_question_by_search_without_result(self):
        res = self.client().post('/api/questions/search',
                                 json={"searchTerm": "sevensky"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], len(Question.query.all()))

    ##################################################
    # Test Get Question Based on Quiz Game
    ##################################################
    def test_get_question_based_on_quiz_game(self):
        res = self.client().post('/api/quizzes', json=self.quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['count'])

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
