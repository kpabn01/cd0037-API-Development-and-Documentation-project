import os
from unicodedata import category
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env
# reading the env variables :
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", DATABASE_PASSWORD,
                             "localhost:5432", self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #----------------------
    # TESTING CATEGORIES RETRIEVAL
    #----------------------
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_error_getting_categories(self):
        res = self.client().get('/categories/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    #----------------------
    # TESTING QUESTIONS RETRIEVAL
    #----------------------
    def test_get_paginated_question(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["currentCategory"])

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    #----------------------
    # TESTING QUESTION DELETION
    #----------------------
    def test_delete_a_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['deleted'], 5)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)

    def test_error_deleting_an_inexisting_question(self):
        res = self.client().delete('/questions/500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    #----------------------
    # TESTING QUESTION CREATION
    #----------------------
    def test_create_new_question(self):
        res = self.client().post("/questions", json={"question":"night?", "answer": "yes", "category": 3, "difficulty": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))

    def test_error_if_question_creation_not_allowed(self):
        res = self.client().post("/questions/45", json={"question":"night?", "answer": "yes", "category": 3, "difficulty": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")



    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------




    #----------------------
    # TESTING PAGINATION
    #----------------------





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()