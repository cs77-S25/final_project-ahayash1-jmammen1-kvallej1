from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Discussion, Review, Comment, User, Vote
from datetime import date, timedelta, datetime
from flask_migrate import Migrate
from pprint import pprint

app = Flask(__name__)

# Configure database
app.config['CACHE_TYPE'] = 'null' # disable if in production environment
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Enable CORS
CORS(app)

# Initialize db to be used with current Flask app
with app.app_context():
    db.init_app(app)
    # Create the database if it doesn't exist
    # Note: create_all does NOT update tables if they are already in the database. 
    # If you change a model’s columns, use a migration library like Alembic with Flask-Alembic 
    # or Flask-Migrate to generate migrations that update the database schema.
    db.create_all()

#migrate = Migrate(app,db)

@app.route('/home') #code for our home page that allows users to select discussions and reviews tab
def home():
    discussions=db.session.query(Discussion).filter_by(author=session["username"]).all()
    reviews=db.session.query(Review).filter_by(author=session["username"]).all()
    discussion_data=[]
    review_data=[]
    for discussion in discussions:
        discussion_data.append({
            'id': discussion.id,
            'title': discussion.title,
            'author': discussion.author,
            'created_at': discussion.created_at,
            'content': discussion.content,
            'course': discussion.course,
            'up_votes': discussion.up_votes,
        })
    for review in reviews:
        review_data.append({
            'id': review.id,
            'title': review.title,
            'author': review.author,
            'created_at': review.created_at,
            'content': review.content,
            'rating': review.rating,
        })
    return render_template('home.html', discussions=discussion_data, reviews=review_data)

#DISCUSSIONSSSS SECTION!

#discussions routes/functions are separated into 4 different functions to assist with the correct sorting by filtering

@app.route('/discussions', methods=['GET', 'POST']) 
def discussions():
    discussions=Discussion.query.order_by(Discussion.created_at.desc()).all() #puts the discussions in the most recent to least recent order
    discussions_data=[]
    for discussion in discussions:
        discussions_data.append({
            'id': discussion.id,
            'title': discussion.title,
            'author': discussion.author,
            'created_at': discussion.created_at,
            'content': discussion.content,
            'course': discussion.course,
            'up_votes': discussion.up_votes,
        })
    # db.session.commit()
    return render_template('discussions.html', discussions=discussions_data)



@app.route('/discussions1', methods=['POST','GET']) 
def discussions1():
    discussions=Discussion.query.order_by(Discussion.created_at.asc()).all() #puts the discussions in the least recent to most recent order
    discussions_data=[]
    for discussion in discussions:
        discussions_data.append({
            'id': discussion.id,
            'title': discussion.title,
            'author': discussion.author,
            'created_at': discussion.created_at,
            'content': discussion.content,
            'course': discussion.course,
            'up_votes': discussion.up_votes,
        })
    # db.session.commit()
    return render_template('discussions.html', discussions=discussions_data)


@app.route('/discussions2', methods=['POST','GET']) 
def discussions2():
    discussions=Discussion.query.order_by(Discussion.up_votes.desc()).all() #puts the discussions in the most upvotes to least upvotes order
    discussions_data=[]
    for discussion in discussions:
        discussions_data.append({
            'id': discussion.id,
            'title': discussion.title,
            'author': discussion.author,
            'created_at': discussion.created_at,
            'content': discussion.content,
            'course': discussion.course,
            'up_votes': discussion.up_votes,
        })
    # db.session.commit()
    return render_template('discussions.html', discussions=discussions_data)


@app.route('/discussions3', methods=['POST','GET']) 
def discussions3():
    discussions=Discussion.query.order_by(Discussion.up_votes.asc()).all() #puts the discussions in the least upvotes to most upvotes order
    discussions_data=[]
    for discussion in discussions:
        discussions_data.append({
            'id': discussion.id,
            'title': discussion.title,
            'author': discussion.author,
            'created_at': discussion.created_at,
            'content': discussion.content,
            'course': discussion.course,
            'up_votes': discussion.up_votes,
        })
    # db.session.commit()
    return render_template('discussions.html', discussions=discussions_data)

#creates a new discussion post with the listed attributes
@app.route('/new_discussion', methods=['POST'])
def new_discussion():
    print("here")
    form =  request.get_json()
    title = form["title"]
    content = form["content"]
    author = session["username"]
    course = form["course"]
    created_at = datetime.now()
    #discussions = Discussion.query.all()
    if title and content:
        new_discussion = Discussion(title=title, content=content, author=author, created_at=created_at, course=course)
        # use .count and  .filterby
        print(new_discussion)
        db.session.add(new_discussion)
        db.session.commit()
        print(f"Added new discussion: {new_discussion.serialize()}")  
        return make_response(jsonify({"success": "true", "discussion": new_discussion.serialize()}), 200)
    return make_response(jsonify({"success": "false"}), 400) # return both JSON object and HTTP response status (400: bad request)

#takes the user to a specific discussion post with a unique discussion id 
@app.route('/discussion/<int:discussion_id>')
def dis_posts(discussion_id):
    discussion = Discussion.query.get_or_404(discussion_id) # returns a 404 error if get fails
    print(discussion)
    #print(discussion)
    #db.session.commit()
    return render_template('dis_posts.html', discussion=discussion) # return the discussion_post object

@app.route('/upvote/<int:discussion_id>', methods=['POST'])
def upvote(discussion_id):
    # UPDATE Thread
    user_id = session.get('user_id')  # Get the user ID from the session
    if not user_id:
        return make_response(jsonify({"success": "false", "message": "Login required"}), 401)
    
    user = User.query.get(user_id)

    update_discussion = Discussion.query.get_or_404(discussion_id) # check if user exists, return Users object or None

    existing_vote = Vote.query.filter_by(user_id=user.id, discussion_id=update_discussion.id).first()
    if existing_vote:
        return make_response(jsonify({"success": "false", "message": "Already voted"}), 400)
    
    new_vote = Vote(user_id=user.id, discussion_id=update_discussion.id)
    db.session.add(new_vote)

    newupvotes = update_discussion.up_votes + 1
    update_discussion.up_votes = newupvotes
    db.session.commit()

    return make_response(jsonify({"success": "true", "discussion": update_discussion.serialize()}), 200)
    # else:
    #     print("Discussion not found.")
    # # error = False
    # # if error:
    # #     return redirect(url_for('error'))
    # return make_response(jsonify({"success": "false"}), 400) 


#REVIEWSSSSS SECTION!

#reviews routes/functions are separated into 4 different functions to assist with the correct sorting by filtering

@app.route('/reviews', methods=['POST','GET']) 
def reviews():
    reviews=Review.query.order_by(Review.created_at.desc()).all() #puts the reviews in the most recent to least recent order
    reviews_data=[]
    for review in reviews:
        reviews_data.append({
            'id': review.id,
            'title': review.title,
            'author': review.author,
            'created_at': review.created_at,
            'content': review.content,
            'rating': review.rating,
            'major': review.major,
        })
    return render_template('reviews.html', reviews=reviews_data)

@app.route('/reviews1', methods=['POST','GET']) 
def reviews1():
    reviews=Review.query.order_by(Review.created_at.asc()).all() #puts the reviews in the least recent to most recent order
    reviews_data=[]
    for review in reviews:
        reviews_data.append({
            'id': review.id,
            'title': review.title,
            'author': review.author,
            'created_at': review.created_at,
            'content': review.content,
            'rating': review.rating,
            'major': review.major,
        })
    return render_template('reviews.html', reviews=reviews_data)

@app.route('/reviews2', methods=['POST','GET']) 
def reviews2():
    reviews=Review.query.order_by(Review.rating.desc()).all() #puts the reviews in the highest ranked to lowest ranked order
    reviews_data=[]
    for review in reviews:
        reviews_data.append({
            'id': review.id,
            'title': review.title,
            'author': review.author,
            'created_at': review.created_at,
            'content': review.content,
            'rating': review.rating,
            'major': review.major,
        })
    return render_template('reviews.html', reviews=reviews_data)

@app.route('/reviews3', methods=['POST','GET']) 
def reviews3():
    reviews=Review.query.order_by(Review.rating.asc()).all() #puts the reviews in the lowest ranked to highest ranked order
    reviews_data=[]
    for review in reviews:
        reviews_data.append({
            'id': review.id,
            'title': review.title,
            'author': review.author,
            'created_at': review.created_at,
            'content': review.content,
            'rating': review.rating,
            'major': review.major,
        })
    return render_template('reviews.html', reviews=reviews_data)

#creates a new review with the following attributes
@app.route('/new_review', methods=['POST'])
def new_review():
    print("here")
    form =  request.get_json()
    title = form["title"]
    content = form["content"] # add authors field here
    author = session["username"]
    major = form["major"]
    rating = form["rating"]
    created_at = datetime.now()

    if title and content:
        new_review = Review(title=title, content=content, author=author, created_at=created_at, rating=int(rating), major=major)
        # use .count and  .filterby
        db.session.add(new_review)
        db.session.commit()
        print(f"Added new review: {new_review.serialize()}")  
        return make_response(jsonify({"success": "true", "review": new_review.serialize()}), 200)

    return make_response(jsonify({"success": "false"}), 400) # return both JSON object and HTTP response status (400: bad request)

#takes the user to a specific review post with a unique review id 
@app.route('/review/<int:review_id>')
def rev_posts(review_id):
    review = Review.query.get_or_404(review_id) # returns a 404 error if get fails
    review = db.session.query(Review).get(review_id)
    return render_template('rev_posts.html', review=review)


#COMMENTSSSS SECTION!

@app.route('/discussion/<int:discussion_id>/comment', methods=['POST'])
def discussion_comment(discussion_id):
    content = request.form.get('comment')
    author = session["username"]
    created_at = datetime.now()
    
    if content and author:
        new_comment = Comment(discussion_id=discussion_id, author=author, created_at=created_at, content=content) # should display created and author
        db.session.add(new_comment)
        print(new_comment)
        db.session.commit()

    return redirect(url_for('dis_posts', discussion_id=discussion_id)) # set variable thread_id to be thread_id

@app.route('/review/<int:review_id>/comment', methods=['POST'])
def review_comment(review_id):
    content = request.form.get('comment')
    author = session["username"]
    created_at = datetime.now()
    
    if content and author:
        new_comment = Comment(review_id=review_id, author=author, created_at=created_at, content=content) # should display created and author
        db.session.add(new_comment)
        print(new_comment)
        db.session.commit()

    return redirect(url_for('rev_posts', review_id=review_id))


#LOGINNNN SECTION!

#where the user logs into SwatShare
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user_id' not in session:
        if request.method == 'POST':  # If the form is submitted
            username = request.form.get('username')  # Get the username from the form
            password = request.form['password']  # Get the password from the form
            user = User.query.filter_by(username=username).first()  # Query the user by username
            
            if user and check_password(user.password, password):  # Check if user exists and password is correct
                session['user_id'] = user.id  # Set the user ID in the session
                session['username'] = user.username
                session.permanent = True
                return redirect(url_for('home'))  # Redirect to homepage
            else:
                error = "your username or password do not match."
                return render_template('error.html', error=error) # Display error page
        
        else:
            return render_template('login.html')  # Render the login template
    else:
        return redirect(url_for('home'))  # Redirect to the home page

#checks if password is valid
def check_password(a,b):
    # if check_password_hash(user.password, password):
    if a == b:
        return True
    else: 
        return False

# Remove me in production
def generate_password(a):
    # return generate_password_hash(password, method='sha256')
    return a
    
#creates signup for user
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' not in session:
        if request.method == 'POST':  # If the form is submitted
            username = request.form['username']  # Get the username from the form
            password = request.form['password']  # Get the password from the form
            email = request.form['email']
            #check if email is swarthmore
            print(username)
            new_password = generate_password(password) 
            new_user = User(username=username, password=new_password)  # Create a new user object
            db.session.add(new_user)  # Add the new user to the session
            db.session.commit()  # Commit the session to the database
            return redirect(url_for('login'))  # Redirect to the login page
        else:
            return render_template('signup.html')  # Render the register template
    else:
        return redirect(url_for('discussions'))  # Redirect to the login page

#where the user logs out of SwatShare
@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)  # Remove the user ID from the session
    return redirect(url_for('login'))  # Redirect to the login page

if __name__ == '__main__':
    app.run(debug=True)

#     threads = Thread.query.order_by(Thread.created_at.desc()).all()
#     return render_template('home.html', threads=threads) # return list of threads

# @app.route('add_post', methods=['POST'])
# def add_post():
#     form = request.get_json()
#     title = form["title"]
#     content = form["content"]
#     if title and content:
#         add_post = Add_post(title=title, content=content)
#         db.session.add(add_post)
#         db.session.commit()
#         print(f"Added new post: {add_post.serialize()}")
#         return make_response(jsonify({"success": "true", "add_post": add_post.serialize()}), 200) # return both JSON object and HTTP response status (200: OK)

#     return make_response(jsonify({"success": "false"}), 400) # return both JSON object and HTTP response status (400: bad request)

# @app.route('/thread/<int:thread_id>')
# def thread(thread_id):
#     thread = Thread.query.get_or_404(thread_id) # returns a 404 error if get fails
#     print(thread)
#     return render_template('thread.html', thread=thread) # return the thread object

# @app.route('/new_thread', methods=['POST'])
# def new_thread():
#     form = request.get_json()
#     title = form["title"]
#     content = form["content"]
#     if title and content:
#         new_thread = Thread(title=title, content=content)
#         db.session.add(new_thread)
#         db.session.commit()
#         print(f"Added new thread: {new_thread.serialize()}")
#         return make_response(jsonify({"success": "true", "thread": new_thread.serialize()}), 200) # return both JSON object and HTTP response status (200: OK)

#     return make_response(jsonify({"success": "false"}), 400) # return both JSON object and HTTP response status (400: bad request)

# @app.route('/comment/<int:thread_id>', methods=['POST'])
# def comment(thread_id):
#     thread = Thread.query.get_or_404(thread_id) # returns a 404 error if get fails
#     comment_text = request.form.get('comment')
#     if comment_text:
#         new_comment = Comment(thread_id=thread.id, content=comment_text)
#         db.session.add(new_comment)
#         db.session.commit()

#     return redirect(url_for('thread', thread_id=thread_id)) # set variable thread_id to be thread_id


# @app.route('/upvote/<int:discussion_id>', methods=['POST'])
# def upvote(discussion_id):
#     update_discussion = Discussion.query.get_or_404(discussion_id)
#     if update_discussion:
#         newupvotes = update_discussion.upvotes +1
#         update_discussion.upvotes = newupvotes
#         db.session.commit()
#         return make_response(jsonify({"Success": "true", "discussion": update_discussion.serialize()}), 200)
#     else:
#         print("Discussion not found.")
#     return make_response(jsonify({"Success": "false"}), 400)


# @app.route('/review_post/<int:review_id>')
# def review_post(review_id):
#     review_post = Review_post.query.get_or_404(thread_id) # returns a 404 error if get fails
#     print(review_post)
#     return render_template('reviews.html', review_post=review_post) # return the review_post object
    
# @app.route('/reviews')
# def reviews():
#     reviews=Review.query.order_by(Review.created_at.desc()).all()

#     reviews_data=[]
#     for review in reviews:
#         reviews_data.append({
#             'id': review.id,
#             'title': review.title,
#             'author': review.author,
#             'created_at': review.created_at,
#             'content': review.content,
#             'rating': review.rating,
#         })
#     return render_template('reviews.html', reviews=reviews_data)