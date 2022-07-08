from flask import Blueprint, flash, redirect, request, url_for, render_template
from flask_login import current_user, login_required
from flaskBlog import db
from flaskBlog.models import Post
from flaskBlog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('你已经创建了一条POST', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form)



@posts.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        return redirect(url_for('main.home'))
    form= PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.body = form.body.data
        db.session.commit()
        flash('修改成功', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.body.data = post.body
    return render_template('create_post.html',title='update-post', form=form)


@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        return redirect(url_for('main.home'))
    db.session.delete(post)
    db.session.commit()
    flash('成功删除', 'success')
    return redirect(url_for('main.home'))


