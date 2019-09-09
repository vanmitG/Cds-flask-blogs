from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "KhoaTheBestDestroyer"
login_mgr = LoginManager(app)
login_mgr.login_view = 'login'
login_mgr.init_app(app)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://coderSchool:abc123@localhost:5432/blogsCDS'
db = SQLAlchemy(app)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), index=True, unique=True)
    user_name = db.Column(db.String(80), default="User")
    password_hash = db.Column(db.String(128), nullable=False)
    img_url = db.Column(db.String(128), default="images/team/a2.png")
    posts = db.relationship("Posts", backref="users", lazy="dynamic")
    comments = db.relationship("Comments", backref="users", lazy="dynamic")
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_date = db.Column(db.DateTime, default=datetime.now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    quote = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(128), default="images/blog/6.png")
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_date = db.Column(db.DateTime, default=datetime.now)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comments', backref="posts", lazy="dynamic")


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_date = db.Column(db.DateTime, default=datetime.now)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)


db.create_all()


@login_mgr.user_loader
def load_user(id):
    return Users.query.get(int(id))


@login_mgr.unauthorized_handler
def unauthorized():
    # do stuff
    # return a_response
    pass


@app.route('/')
def index():
    return render_template('blog-list-sidebar.html', page_name="home")


@app.route('/blogs')
def blogs():
    return redirect(url_for('index'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(email=request.form.get("email")).first()
        if user is not None and user.check_password(request.form["password"]):
            # success
            login_user(user)
            flash(f'Yeah! Welcome, {user.user_name}', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Incorect username or password', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', page_name='login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out, lets come back', 'info')
    return redirect(url_for('login'))


@app.route('/blogs/<id>')
@login_required
def blogDetail(id):
    return render_template('blog-details.html', page_name='blog', id=1)


@app.route('/create_blog', methods=['POST', 'GET'])
@login_required
def create_blog():
    if request.method == "POST":
        new_post = Posts(title=request.form.get("title"),
                         quote=request.form.get("quote"),
                         body=request.form.get("body"),
                         img_url=request.form.get("img_url"), author=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash(
            f'Successfuly create new blog "{new_post.title}".', 'success')
        post_id = 1
        return redirect(url_for('blogDetail', id=post_id))
    else:
        flash('method not Post', 'info')
        return render_template('new-blog.html', page_name='Create Blog')


# TODO validate input data
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        new_user = Users(first_name=request.form.get("first_name"),
                         last_name=request.form.get("last_name"),
                         user_name=request.form.get("user_name"),
                         img_url=request.form.get("img_url"), email=request.form.get("email"))
        new_user.set_password(request.form["password"])
        db.session.add(new_user)
        db.session.commit()
        flash(
            f'Successfuly sign up {new_user.email}. Please Login!!!', 'success')
        return redirect(url_for('login'))
    else:
        flash('Please sign up!!!', 'info')
        return render_template('signup.html', page_name='register')


@app.route('/profile')
def profile():
    return render_template('profile.html', name="Khuong", page_name='profile', id=1)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)

# TODO disable this when running production because it does not let browser cache static content.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0