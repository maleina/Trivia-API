import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
# Helper function used to determine the which questions to display for a given page.
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def get_categories():
  # Helper function used to fetch and return all categories.
  categories_query = Category.query.all()
  categories = {}
  for category in categories_query:
    categories[category.id] = category.type
  return categories

def create_app(test_config=None):
  # Create and configure the app here.
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  CORS(app, resources={'/': {'origins': '*'}})

  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
    return response

  '''
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def retrieve_all_categories():
    categories = get_categories()

    # Abort if no categories found in the databse, otherwise return all with "success".
    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': categories
    })

  '''
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, categories. 
  
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def retrieve_all_questions():
    selection = Question.query.all()
    total_questions = len(selection)
    current_questions = paginate_questions(request, selection)
    categories = get_categories()
    
    #Abort if there are no questions in the database, 
    #otherwise return paginated questions, total questions and all categories. 
    
    if len(current_questions) == 0:
      abort(404)
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': total_questions,
      'categories': categories
    })

  '''
  @DONE: 
  Create an endpoint to DELETE question using a question ID. 
  
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
      try:
          question = Question.query.filter(Question.id == id).one_or_none()

          # If the question is not found, abort and return a "Not found" code.
          if question is None:
              abort(404)

          # Otherwise, delete the question and return paginated questions.
          question.delete()
          selection = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request, selection)

          return jsonify({
              'success': True,
              'deleted': id,
              'questions': current_questions,
              'total_questions': len(Question.query.all())
          })

      except:
          abort(422)

  '''
  @DONE: 
  --Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  --Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.   

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    # First, need to parse JSON request data.
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    search = body.get('searchTerm')
        
    try:
        # If the request is a search, process accordingly with case insensitivity.
        if search:
          selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
          current_questions = paginate_questions(request, selection)

          return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection.all())
            })
        #Otherwise, the request is to post a new question and it must be handled accordingly.    
        else:
          # As per the TODO above, I am assuming all fields are required.
          if ((new_question is None) or (new_answer is None) or 
            (new_category is None) or (new_difficulty is None)):
            
            return abort(422)

          # Format and insert the question here.
          question = Question(
            question=new_question, answer=new_answer,
            category=new_category, difficulty=new_difficulty)
          question.insert()

          # Retrieve paginated questions and send them back to the front end,
          # along with the id of the newly created question.
          selection = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request, selection)

          return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_questions,
            'total_questions': len(Question.query.all())
          })
            
    except:
      abort(422)

  '''
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def retrieve_questions_per_category(id):
    selection = Question.query.filter(Question.category == id).all()
    total_questions = len(selection)
    current_questions = paginate_questions(request, selection)
    categories = get_categories()

    if len(current_questions) == 0:
      abort(404)
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': total_questions,
      'current_category': id,
      'categories': categories
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def retrieve_quiz_question():

    body = request.get_json()
    category = body.get('quiz_category', None)
    previous_questions = body.get('previous_questions')

    if ((category is None) or (previous_questions is None)):
      abort(400)
    
    # Format the data retrived from the request for use:
    # (1) Need to get category "id" for use in the query.
    category = int(category['id'])
    # (2) Convert previous questions to a set in order 
    # to more easily test if a question has been used before.
    previous_questions = set(previous_questions)
    
    # Retrieve questions based on category, "0" represents ALL.
    if (category == 0):
        questions = Question.query.all()
    else:
        questions = Question.query.filter(Question.category == category).all()

    # Build a list of possible questions, eliminating those that have been used already.
    poss_qs = []
    for question in questions:
      if question.id not in previous_questions:
        poss_qs.append(question)
    
    # If the list of possible questions is not empty, randomly pick a question.
    # Otherwise the game is over, just return success.
    if len(poss_qs) > 0:
      question = random.sample(poss_qs, 1)[0]
      
      return jsonify({
        'success': True, 
        'question': question.format()
        })
    else:
      return jsonify({
        'success': True
        })

  '''
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
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

  # @app.errorhandler(405)
  # def not_allowed(error):
  #   return jsonify({
  #     "success": False,
  #     "error": 405,
  #     "message": "method not allowed"
  #     }), 405
  
  return app

    