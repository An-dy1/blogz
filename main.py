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

    def __init__(self, title):
        self.title = name

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

    if request.method == "POST":
        post_title = request.form['title']
        post_content = request.form['content']

        post_title_error = ""
        post_content_error = ""

        if not something_input(post_title):
            post_title_error = "Please choose a title"
            post_title = ""

        if not something_input(post_content):
            post_content_error = "Write something"
            post_content = ""

        if not post_title_error and not post_content_error:
            return redirect('/blog')
        else:
            return render_template('newpost.html')

    #does this need to be different???:
        db.session.add(new_post)
        db.session.commit()

    return render_template('blog.html', posts=get_posts())

@app.route('/newpost', methods=['POST'])
def create_post():

    post_id = int(request.form['post-id'])
    post = Post.query.get(post-id)

    db.session.add(post)
    db.session.commit()

    return redirect('/blog')

if __name__ == '__main__':
    app.run()

