from app import app, db
from app.models import User, Post
from flask import render_template, flash, redirect, url_for, \
    url_for, request
from app.forms import RegisterForm, AddProductForm, LoginForm, \
    EditProfileForm, PostForm
from flask_login import login_user, logout_user, login_required, \
    current_user
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    "Index URL"
    posts = Post.query.all()

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template(
        'index.html',
        title='Home',
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url)

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template(
        'edit_profile.html',
        title='Edit Profile',
        form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/logout')
def logout():
    logout_user()
    return redirect(('login'))

@app.route('/about-me')
def about_me():
    """About me URL"""
    return render_template('about_me.html', title='about me page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register URL"""
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'You are requesting to register as {form.username.data}')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login URL"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('index')
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome {form.username.data}')
        return redirect('index')
    return render_template('login.html', title='Login', form=form)


@app.route('/user/<username>/profile', methods=['GET', 'POST'])
@login_required
def profile(username):
    """Profile page"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body= form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is live!')
        return redirect(url_for('index'))
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = current_user.post.paginate(
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False)
    next_url = url_for('profile', username=current_user.username, page=page.next_num) \
            if posts.has_next else None
    prev_url = url_for('profile', username=current_user.username, page=posts.prev_num) \
            if posts.has_prev else None
    

    return render_template(
        'profile.html',
        title='Profile',
        user=user,
        form=form,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url)

@app.route('/test-error')
def test_error():

    result = 1 / 0 
    return "This will never render"