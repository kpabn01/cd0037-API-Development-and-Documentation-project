import os
from unicodedata import category
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv


# take environment variables from .env
load_dotenv()

# reading the env variables :
DB_USER = os.environ.get("DB_USER")
DB_TEST_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_TEST_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD,
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
        self.assertTrue(data["current_category"])

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
        # May need to provide a valide question id which is in the database
        # Once the test is run change the id manually otherwise this part of the test may fail.
        
        res = self.client().delete('/questions/12')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 12).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 12)
        #self.assertTrue(len(data["questions"]))
        #self.assertTrue(data["total_questions"])
        #self.assertEqual(question, None)

    def test_error_deleting_an_inexisting_question(self):
        res = self.client().delete('/questions/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    #----------------------
    # TESTING QUESTION CREATION
    #----------------------
    def test_create_new_question(self):
        res = self.client().post('/questions/create', 
                json={"question":"are you night_coding ?", "answer": "yes", "category": 3, "difficulty": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertTrue(data["answer"])
        self.assertTrue(data["category"])
        self.assertTrue(data["difficulty"])
        #self.assertTrue(len(data["questions"]))
        #self.assertTrue(data["total_questions"])

    def test_error_if_question_creation_not_allowed(self):
        res = self.client().post('/questions/create')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    #----------------------
    # TESTING QUESTION SEARCH
    #----------------------
    def test_search_question(self):
        res = self.client().post('/questions/search', json={"searchTerm": "title"})
        data = json.loads(res.data)

        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], categories[data["questions"][0]["category"]] )

    def test_error_if_search_not_processed(self):
        res = self.client().post('/questions/search', json={"search":''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    #----------------------
    # TESTING QUESTIONS RETRIEVAL BY CATEGORY
    #----------------------
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], categories[3])

    def test_error_if_question_category_inexistent(self):
        res = self.client().get('/categories/12345/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    #----------------------
    # TESTING QUESTION GENERATION FOR QUIZ 
    #----------------------
    def test_get_questions_to_play_the_quiz(self):
        res = self.client().post('/quizzes',
                json={'previous_questions': [1, 4, 20, 15], 'quiz_category': 'Sports'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        #self.assertEqual(data["previous_questions"], [1, 4, 20, 15])

    def test_error_getting_question_to_play_the_quiz(self):
        res = self.client().post('/quizzes',
                json={"previous_questions": [1, 4, 20, 15], "quiz_category": ""})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()