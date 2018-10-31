from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:lc101@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

def something_input(string):
    try:
        good_input = len(string) > 0
        return good_input
    except: 
        return False

def get_posts():
    return Post.query.all()

@app.route('/blog', methods=['POST', 'GET'])
def index():

    posts = Post.query.all()
    return render_template('blog.html', posts=posts)

@app.route('/newpost', methods=['GET', 'POST'])
def create_post():
    
    if request.method == "GET":
        return render_template('newpost.html')

    else:
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
            new_post = Post(post_title, post_content) #something not quite right here; throwing lots o errors
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')
        else:
            return render_template('newpost.html', post_title_error=post_title_error, post_content_error=post_content_error)


if __name__ == '__main__':
    app.run()

