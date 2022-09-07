#from crypt import methods
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        selection = Category.query.all()
        categories = {}
        if len(selection) == 0:
            abort(404)
        else:
            for category in selection:
                categories[category.id] = category.type

        return jsonify({
            "success": True,
            "categories": categories
        })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": categories,
                "current_category": categories[current_questions[0]["category"]]
            }
        )
    

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": id,
                    #"questions": current_questions,
                    #"total_questions": len(Question.query.all()),
                }
            )
        except:
            abort(422)


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions/create', methods=["POST"])
    def create_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)

        try:
            if body == None:
                abort(400)
            question = Question(question=new_question, answer=new_answer, 
                                category=new_category, difficulty=new_difficulty)
            question.insert()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "question": question.question,
                    "answer": question.answer,
                    "category": question.category,
                    "difficulty": question.difficulty
                    #"created": question.id,
                    #"questions": current_questions,
                    #"total_questions": len(Question.query.all()),
                }
            )
        except:
            raise
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=["POST"])
    def search_question():
        body = request.get_json()
        search = body.get("searchTerm", None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))
                ).all()
                categories = {}
                for category in Category.query.all():
                    categories[category.id] = category.type
                if len(selection) == 0:
                    abort(404)
                else:
                    matching_questions = paginate_questions(request, selection)
                    return jsonify(
                        {
                            "success": True,
                            "questions": matching_questions,
                            "total_questions": len(selection),
                            "current_category": categories[matching_questions[0]["category"]]
                        }
                    )
            else:
                abort(405)
        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        #body = request.get_json()
        #category = body.get("category", None)

        try:
            selection = Question.query.order_by(Question.id).filter(Question.category==id).all()
            if len(selection) == 0:
                abort(404)
            matching_questions = paginate_questions(request, selection)
            categories = {}
            for category in Category.query.all():
                categories[category.id] = category.type

            return jsonify(
                {
                    "success": True,
                    "questions": matching_questions,
                    "total_questions": len(selection),
                    "current_category": categories[id]
                }
            )
        except:
            raise
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=["POST"])
    def create_quizz():
        #previous_questions = []
        body = request.get_json()
        previous_questions =  body.get("previous_questions")
        quiz_category = body.get("quiz_category")

        try:
            categories = {}
            for category in Category.query.all():
                categories[category.id] = category.type
                if category.type == quiz_category["type"]:
                    category_id = category.id

            selection = Question.query.order_by(Question.id).filter(Question.category==category_id).all()
            question = random.choice(selection)

            while question.id in previous_questions:
                question = random.choice(selection)

            #previous_questions.append(question.id)
            formated_question = question.format()

            return jsonify(
                {
                    "success": True,
                    "question": formated_question,
                    #"previous_questions": previous_questions
                }
            )
        except:
            raise
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )
    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405
        )
    
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "internal server error"}),
            500
        )

    return app

