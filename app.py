from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Thread, Comment

app = Flask(__name__)

# Configure database
app.config['CACHE_TYPE'] = 'null' # disable if in production environment
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

@app.route('/') 
def discussions():
    if 'user_id' in session:
        messsage = "Welcome, logged in user"
    else:
        message = "Welcome, please log in."

    return render_template('discussions.html', session=session, message=message)
    
# @app.route('/discussion_post/<int:discussion_post_id>')
# def discussion_post(discussion_post_id):
#     discussion_post = Discussion_post.query.get_or_404(discussion_post_id) # returns a 404 error if get fails
#     print(discussion_post)
#     return render_template('discussions.html', discussion_post=discussion_post) # return the discussion_post object

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')
# @app.route('/review_post/<int:review_id>')
# def review_post(review_id):
#     review_post = Review_post.query.get_or_404(thread_id) # returns a 404 error if get fails
#     print(review_post)
#     return render_template('reviews.html', review_post=review_post) # return the review_post object

@app.route('/login')
def login():
    if 'user_id' not in session:
        if request.method == 'POST':  # If the form is submitted
            username = request.form['username']  # Get the username from the form
            password = request.form['password']  # Get the password from the form
            user = User.query.filter_by(username=username).first()  # Query the user by username
            
            if user and check_password(user.password, password):  # Check if user exists and password is correct
                session['user_id'] = user.id  # Set the user ID in the session
                session['username'] = user.username
                session.permanent = True
                return redirect(url_for('discussions'))  # Redirect to homepage
            else:
                error = "your username or password do not match."
                return render_template('error.html', error=error) # Display error page
        
        else:
            return render_template('login.html')  # Render the login template
    else:
        return redirect(url_for('discussions'))  # Redirect to the login page
    

@app.route('/signup')
def signup():
    if 'user_id' not in session:
        if request.method == 'POST':  # If the form is submitted
            username = request.form['username']  # Get the username from the form
            password = request.form['password']  # Get the password from the form
            new_password = generate_password(password) 
            new_user = User(username=username, password=new_password)  # Create a new user object
            db.session.add(new_user)  # Add the new user to the session
            db.session.commit()  # Commit the session to the database
            return redirect(url_for('login'))  # Redirect to the login page
        else:
            return render_template('signup.html')  # Render the register template
    else:
        return redirect(url_for('discussions'))  # Redirect to the login page


@app.route('/add_review')
def add_review():
    return render_template('add_review.html')

@app.route('/add_discussion')
def add_discussion():
    return render_template('add_discussion.html')


@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)  # Remove the user ID from the session
    return redirect(url_for('login'))  # Redirect to the login page




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

if __name__ == '__main__':
    app.run(debug=True)
