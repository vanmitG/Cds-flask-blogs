from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
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


@app.route('/')
def index():
    return render_template('blog-list-sidebar.html', name='khuong', page_name="home")


@app.route('/blogs')
def blogs():
    return redirect(url_for('index'))


# @app.route('/blogs/<id>')
# def blogs():
#     return render_template('blog-details.html')


@app.route('/login')
def login():
    return render_template('login.html', page_name='login')


@app.route('/logout')
def logout():
    pass


@app.route('/blogs/<id>')
def blogDetail(id):
    return render_template('blog-details.html', name='Khuong', page_name='blog', id=1)


@app.route('/create_blog')
def create_blog():
    return render_template('new-blog.html', name='Khuong', page_name='Create Blog', id=1)


@app.route('/signup')
def signup():
    return render_template('signup.html', page_name='registor')


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
