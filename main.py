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
    body = db.Column(db.String(3500))

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

    post_id = request.args.get('id')
    empty = not post_id

    posts = Post.query.all()

    if empty:
        return render_template('blog.html', posts=posts)
    else:
        post = Post.query.get(post_id) #this is not written correctly yet
        return render_template('single-post.html', post=post) #for that specific post, or does this need to be a redirect??

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
            new_post = Post(post_title, post_content)
            db.session.add(new_post)
            db.session.commit()
            post_id = new_post.id
            return redirect('/blog?id={0}'.format(post_id))
        else:
            return render_template('newpost.html', post_title_error=post_title_error, 
            post_content_error=post_content_error)


if __name__ == '__main__':
    app.run()

