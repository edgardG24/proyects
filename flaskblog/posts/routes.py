from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
import psycopg2

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        cur = conn.cursor()
    	cur.execute(f"INSERT INTO post ( title, date_posted, content, user_id) VALUES ('{form.title.data}' , current_timestamp, '{form.content.data}', '{current_user}');")
	conn.commit()
        #db.session.add(post)
        #db.session.commit()
        flash('¡Tu post ha sido creado!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='Nuevo Post',
                           form=form, legend='Nuevo Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

conn = psycopg2.connect(
	database="d3qgi53uaj1knr",
	user="tyiuqokgzyrbem",
	password="7a906139c3b520dab15e6f603d3ff0c40f7b88d313d1db6cd4f603a04961c0b3",
	host="ec2-34-195-115-225.compute-1.amazonaws.com",
	port="5432"
)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('¡Tu post sea actualizado!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Actualizar Post',
                           form=form, legend='Actualizar Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('¡Tu post ha sido eliminado!', 'success')
    return redirect(url_for('main.home'))
