from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, questions):
    page = request.args.get("page", 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in questions]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        '''
        CORS Headers
        '''
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods",
            "GET,PUT,POST,DELETE,OPTIONS"
        )

        return response

    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=["GET"])
    def retrieve_categories():
        """
        Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
        """
        categories = Category.query.order_by(Category.type).all()

        if len(categories) == 0:
            abort(404)
        
        return jsonify({
            "success": True,
            "categories": {
                category.id: category.type for category in categories
            }
        })

    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=["GET"])
    def retrieve_questions():
        """
        Fetches a list of questions paginated by 10 items per page.
        """
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.order_by(Category.type).all()

        if len(current_questions) == 0:
            abort(404)
        
        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(questions),
            "categories": {category.id: category.type for category in categories},
            "current_category": None
        })

    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """
        Delete the question using the question ID.
        """
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            
            question.delete()

            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            return jsonify({
                "success": True,
                "deleted_question_id": question_id,
                "questions": current_questions,
                "total_questions": len(questions)
            })
        
        except:
            abort(422)

    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        """
        Create a new question.
        """
        body = request.get_json()

        if not ("question" in body and "answer" in body and "difficulty" in body and "category" in body):
            abort(422)

        question = body.get("question", None)
        answer = body.get("answer", None)
        difficulty = body.get("difficulty", None)
        category = body.get("category", None)

        questions = Question.query.order_by(Question.id).all()

        try:
            question = Question(
                            question=question,
                            answer=answer,
                            difficulty=difficulty,
                            category=category
                        )
            question.insert()

            return jsonify({
                "success": True,
                "created_question_id": question.id,
                "created_question_text": question.question,
                "total_questions": len(questions)
            })

        except:
            abort(422)
            
    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        """
        Search a question based on a search term.
        """
        body = request.get_json()
        search_term = body.get("searchTerm", None)

        try:
            if search_term:
                questions = Question.query.order_by(Question.id).filter(Question.question.ilike(f"%{search_term}%")).all()
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(questions),
                    "current_category": None
                })

        except:
            abort(404)

    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def retrieve_questions_by_category(category_id):
        """
        Fetches a list of questions paginated by 10 items per page based on the category.
        """
        category = Category.query.filter(Category.id == category_id).one_or_none()

        if category is None:
            abort(404)

        questions_in_category = Question.query.order_by(Question.id).filter(Question.category == str(category_id)).all()

        if questions_in_category is None:
            abort(404)

        current_questions = paginate_questions(request, questions_in_category)

        return jsonify({
            "success": True,
            "category": category.type,
            "questions": current_questions,
            "total_questions": len(questions_in_category)
        })

    """
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def add_quiz():
        """
        Fetches a question to play the quiz.
        """
        body = request.get_json()

        if not ("quiz_category" in body and "previous_questions" in body):
            abort(422)

        quiz_category = body.get("quiz_category", None)
        previous_questions = body.get("previous_questions", None)

        try:
            if quiz_category["id"]:
                available_questions = Question.query.filter_by(category=quiz_category['id']).filter(Question.id.not_in((previous_questions))).all()
            else:
                available_questions = Question.query.filter(Question.id.not_in((previous_questions))).all()
            
            if len(available_questions) > 0:
                new_question = available_questions[random.randrange(0, len(available_questions))].format()

                return jsonify({
                    "success": True,
                    "question": new_question
                })

            else:
                return jsonify({
                    "success": True,
                    "question": None
                })
        
        except:
            abort(422)

    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable resource"
        }), 422

    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    return app