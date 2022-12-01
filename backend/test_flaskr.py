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
        self.database_path = "postgresql://{}/{}".format("localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "123",
            "answer": "123",
            "difficulty": 1,
            "category": 1
        }
      
        self.new_question_with_error = {
            "question": "123",
            "difficulty": 1
        }

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
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """

    # ---------------------------------------#
    # Test categories
    # ---------------------------------------#
    def test_retrieve_all_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))


    # ---------------------------------------#
    # Test questions
    # ---------------------------------------#
    def test_retrieve_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertIsInstance(data['categories'], dict)
        self.assertEqual(data["current_category"], None)
        
    
    def test_404_sent_requesting_questions_beyond_valid_page(self):
        res = self.client().get("/questions?page=10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")


    def test_delete_question(self):
        with self.app.app_context():
            new_question = Question(question=self.new_question["question"], answer=self.new_question["answer"], difficulty=self.new_question["difficulty"], category=self.new_question["category"])
            new_question.insert()
            question_id = new_question.id
        res = self.client().delete(f"/questions/{question_id}")
        data = json.loads(res.data)

        with self.app.app_context():
            question = Question.query.filter(Question.id ==  question_id).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], (question_id))
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertEqual(question, None)


    def test_422_delete_question_with_not_valid_id(self):
        res = self.client().delete("/questions/10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable resource")


    def test_add_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["added"])
        self.assertTrue(data["new_question"])
        self.assertTrue(data["total_questions"])

    
    def test_422_add_new_question_if_not_enough_data(self):
        res = self.client().post("/questions", json=self.new_question_with_error)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable resource")

    
    def test_search_questions_with_result(self):
        res = self.client().post("/questions/search", json={"searchTerm": "which"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertIsInstance(data["questions"], list)
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], None)


    def test_search_questions_without_result(self):
        res = self.client().post("/questions/search", json={"searchTerm": "ffffff"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 0)
        self.assertIsInstance(data["questions"], list)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(data["current_category"], None)

    
    def test_get_questions_by_category(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["category"])
        self.assertTrue(data["questions"])
        self.assertIsInstance(data["questions"], list)
        self.assertEqual(len(data["questions"]), 4)
        self.assertEqual(data["total_questions"], 4)


    def test_404_get_questions_by_category_with_not_valid_id(self):
        res = self.client().get("/categories/10000/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    
    # ---------------------------------------#
    # Test quiz
    # ---------------------------------------#
    def test_quiz(self):
        new_quiz_play = {"previous_questions": [], "quiz_category": {"type": "Sports", "id": 10}}
        res = self.client().post("/quizzes", json=new_quiz_play)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    
    def test_422_quiz_if_not_enough_data(self):
        new_quiz_play = {"previous_questions": []}
        res = self.client().post("/quizzes", json=new_quiz_play)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable resource")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()