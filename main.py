from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:lc101@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

app.secret_key = 'xokdtuzu'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(3500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Post', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

def something_input(string):
    try:
        good_input = len(string) > 0
        return good_input
    except: 
        return False

def get_posts():
    return Post.query.all()

@app.before_request #this route tells the program to run this function before every other request
def require_login():
    allowed_routes = ['login', 'register', 'blog_posts', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session: #what function in the code is the user trying to execute
        return redirect('/login')

@app.route('/')
def index():
    user_list = User.query.all()
    return render_template('index.html', user_list=user_list) 

@app.route('/blog', methods=['POST', 'GET'])
def blog_posts():

    posts=Post.query.all()

    if request.method == "POST":
        post_id = request.args.get('id')
        empty = not post_id

        if empty:
            # users = #ugh
            return render_template('blog.html', posts=posts)
        else:
            post = Post.query.get(post_id) #this is where another problem is
            # owner = post.owner_id #yeah?
            # user = User.query.get(owner)#how do I do this with just a postid? Use the first filter??
            return render_template('single-post.html', post=post)
            
    else:
        user_id = request.args.get('user')
        empty = not user_id

        if empty:
            return render_template('blog.html', posts=posts)
        else:
            user = User.query.get(user_id)
            user_posts = Post.query.filter_by(owner_id=user_id)
            return render_template('user-posts.html', user_posts=user_posts, user=user)

@app.route('/newpost', methods=['GET', 'POST'])
def create_post():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        post_title = request.form.get('title')
        post_content = request.form.get('body')

        post_title_error = ""
        post_content_error = ""

        if not something_input(post_title):
            post_title_error = "Please choose a title"
            post_title = ""

        if not something_input(post_content):
            post_content_error = "Write something"
            post_content = ""

        if not post_title_error and not post_content_error:
            new_post = Post(post_title, post_content, owner)
            db.session.add(new_post)
            db.session.commit()
            post_id = new_post.id
            return redirect('/blog?id={0}'.format(post_id))
        else:
            return render_template('newpost.html', post_title_error=post_title_error, 
            post_content_error=post_content_error)

    return render_template('newpost.html')

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()
        matching_pw = (password == verify)
        long_pw = (len(password) > 4)

        if not existing_user and matching_pw and long_pw:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        elif existing_user:
            flash("You already have an account!")
            return render_template('login.html')
        elif not matching_pw:
            flash("Passwords don't match")
            return render_template('register.html')
        elif not long_pw:
            flash("Password is not long enough")
            return render_template('register.html')

    return render_template('register.html') #this happens first if it's a GET request

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user:
            flash("That user doesn't exist!", 'error')
            return render_template('register.html')
        elif user.password != password:
            flash("Password is incorrect", 'error')
            return render_template('login.html')
        else: #this checks if user is anything other than "NONE" and compares the passwords to verify
            #"remember" that the user has logged in
            session['username'] = username #session is a dictionary
            flash("Logged in")
            print(session)      # TODO is this line still necessary?
            return redirect ('/blog') #TODO what will happen after someone logs in? Not sure if this is the right place to redirect to

    return render_template('login.html')

@app.route('/logout')
def logout():
    flash("Logged out")
    del session['username']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()

