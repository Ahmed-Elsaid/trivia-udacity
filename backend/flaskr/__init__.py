import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r'/api/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, PATCH, OPTIONS')
      return response

    def pagination(collection):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', QUESTIONS_PER_PAGE, type=int)
        start = (page - 1) * limit
        end = start + limit
        return collection[start:end]

    def getQuestionBasedOnCategory(collection):
        category = request.args.get('category')
        print(category)
        questions = []
        for item in collection:
            if item['category_name'] == category:
                questions.append(item)
        return questions

    @app.route('/')
    def index():
        return '<h1 style="color:#333">Welcome to Trivia App</h1>'

    ##################################################
    # Get All Questions
    ##################################################
    @app.route('/api/questions')
    def questions():
        try:
            questions = db.session.query(Question, Category).join(
                Category).order_by(Question.id).all()
            categories = Category.query.all()
            data = []
            for q in questions:
                data.append({
                    "id": q.Question.id,
                    "question": q.Question.question,
                    "answer": q.Question.answer,
                    "difficulty": q.Question.difficulty,
                    "category_id": q.Category.id,
                    "category_name": q.Category.type
                })
            if(len(questions) == 0):
                abort(404)
            if(request.args.get('page') or request.args.get('limit')):
                data = pagination(data)
                if len(data) == 0: abort(404)
            if request.args.get('category'):
                data = getQuestionBasedOnCategory(data)
            return jsonify({
                "success": True,
                "total_questions": len(questions),
                "questions": data,
                "categories":[category.format() for category in categories]
            })
        except:
            abort(404, description='No Questions Listed Yet')

    ##################################################
    # Get All Categories
    ##################################################

    @app.route('/api/categories')
    def categories():
        try:
            categories = Category.query.all()
            if len(categories) == 0:
                abort(404)
            data = [category.format() for category in categories]
            return jsonify({
                "success": True,
                "categories": data,
                "total_categories": len(categories)
            })
        except:
            abort(404, description='No Categries Listed yet')

    ##################################################
    # Delete Question By ID
    ##################################################
    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if not question:
                abort(404)
            question.delete()
            return jsonify({
                "success": True,
                "id": question.id,
                "message": "Question has been deleted"
            })
        except:
            abort(404, description='Question Not Found')

    ##################################################
    # Create New Question
    ##################################################
    @app.route('/api/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        question = body.get('question')
        answer = body.get('answer')
        difficulty = body.get('difficulty')
        category = body.get('category')
        try:
            newQuestion = Question(
                question=question, answer=answer, difficulty=difficulty, category=category)
            isQuestionExist = Question.query.filter(
                Question.question == question).first()
            if isQuestionExist:
                abort(400)
            newQuestion.insert()
            return jsonify({
                "success": True,
                "id": newQuestion.id,
                "total_questions": len(Question.query.all())
            })
        except:
            abort(
                400, description='The Question Already Exist, Please insert a new one!!')

    ##################################################
    # Get Question based on Category
    ##################################################

    @app.route('/api/categories/<int:category_id>/questions')
    def get_question_by_category(category_id):
        try:
            questions = db.session.query(Question, Category).join(
                Category).filter(Question.category == category_id).all()
            if len(questions) == 0:
                abort(404)
            data = []
            for q in questions:
                data.append({
                    "id": q.Question.id,
                    "question": q.Question.question,
                    "answer": q.Question.answer,
                    "difficulty": q.Question.difficulty,
                    "category_id": q.Category.id,
                    "category_name": q.Category.type
                })
            return jsonify({
                "success": True,
                "questions": data,
                "total_questions": len(Question.query.all())
            })
        except:
            abort(404, description='No Questions based on this Category')

    ##################################################
    # Get Question based on Search
    ##################################################
    @app.route('/api/questions/search', methods=['POST'])
    def get_question_by_search():
        try:
            keyword = request.get_json().get('searchTerm')
            questions = db.session.query(Question, Category).join(
                Category).filter(Question.question.ilike(f'%{keyword}%')).all()
            if len(questions) == 0:
                return jsonify({
                "success": True,
                "questions": [],
                "total_questions": len(Question.query.all())
            })
            data = []
            for q in questions:
                data.append({
                    "id": q.Question.id,
                    "question": q.Question.question,
                    "answer": q.Question.answer,
                    "difficulty": q.Question.difficulty,
                    "category_id": q.Category.id,
                    "category_name": q.Category.type
                })
            return jsonify({
                "success": True,
                "questions": data,
                "total_questions": len(Question.query.all())
            })
        except:
            print(sys.exc_info())
            abort(404)

    ##################################################
    # Get Question based on Quiz Game
    ##################################################
    @app.route('/api/quizzes', methods=['POST'])
    def quiz_game():
        try:
            body = request.get_json()
            print(body)
            prevQuestions = body.get('previous_questions')
            category = body.get('quiz_category')
            questions = Question.query.filter(
                Question.category == category['id']).all()
            if category['id'] == 0 :
                questions = Question.query.all()
            selected_questions = []
            for question in questions:
              if question.id not in prevQuestions:
                selected_questions.append(question)
            if len(prevQuestions) == len(questions): 
                return jsonify({
                "success": True,
                "question":'',
                "count": len(questions)
            })
            random_question = random.choice(selected_questions)
            return jsonify({
                "success": True,
                "question": random_question.format(),
                "total_question": len(questions)
            })
        except:
          print(sys.exc_info())
          abort(404)

    ##################################################
    # Error Handler Functions
    ##################################################
    @app.errorhandler(400)
    def not_found(e):
      return jsonify({
          "success": False,
          "error": 400,
          "message": e.__dict__['description'] if e.__dict__.get('description') else 'Asset Already Exist, please insert a new one!!'
      }), 400

    @app.errorhandler(404)
    def not_found(e):
      return jsonify({
          "success": False,
          "error": 404,
          "message": e.__dict__['description'] if e.__dict__.get('description') else 'Asset Not Found, please try again!!'
      }), 404

    @app.errorhandler(405)
    def not_found(e):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "Method Not Allowed"
      }), 405

    
    return app

#   '''
# @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
# '''

#   '''
# @TODO: Use the after_request decorator to set Access-Control-Allow
# '''

#   '''
# @TODO:
# Create an endpoint to handle GET requests
# for all available categories.
# '''

#   '''
# @TODO:
# Create an endpoint to handle GET requests for questions,
# including pagination (every 10 questions).
# This endpoint should return a list of questions,
# number of total questions, current category, categories.

# TEST: At this point, when you start the application
# you should see questions and categories generated,
# ten questions per page and pagination at the bottom of the screen for three pages.
# Clicking on the page numbers should update the questions.
# '''

#   '''
# @TODO:
# Create an endpoint to DELETE question using a question ID.

# TEST: When you click the trash icon next to a question, the question will be removed.
# This removal will persist in the database and when you refresh the page.
# '''

#   '''
# @TODO:
# Create an endpoint to POST a new question,
# which will require the question and answer text,
# category, and difficulty score.

# TEST: When you submit a question on the "Add" tab,
# the form will clear and the question will appear at the end of the last page
# of the questions list in the "List" tab.
# '''

#   '''
# @TODO:
# Create a POST endpoint to get questions based on a search term.
# It should return any questions for whom the search term
# is a substring of the question.

# TEST: Search by any phrase. The questions list will update to include
# only question that include that string within their question.
# Try using the word "title" to start.
# '''

#   '''
# @TODO:
# Create a GET endpoint to get questions based on category.

# TEST: In the "List" tab / main screen, clicking on one of the
# categories in the left column will cause only questions of that
# category to be shown.
# '''

#   '''
# @TODO:
# Create a POST endpoint to get questions to play the quiz.
# This endpoint should take category and previous question parameters
# and return a random questions within the given category,
# if provided, and that is not one of the previous questions.

# TEST: In the "Play" tab, after a user selects "All" or a category,
# one question at a time is displayed, the user is allowed to answer
# and shown whether they were correct or not.
# '''

#   '''
# @TODO:
# Create error handlers for all expected errors
# including 404 and 422.
# '''
