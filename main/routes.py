import os
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for, Request
from flaskBlog.main.forms import PostsSearch
from flaskBlog.models import Post, User
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

@main.context_processor
def base():
    form = PostsSearch()
    return dict(form=form)

@main.route('/')
@main.route('/home/', methods=['GET', 'POST'])
def home():
    q = request.args.get('q')
    if q :
        return redirect(url_for('main.posts_search', q=q))
    else:
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    # form = PostsSearch()
    # if form.validate_on_submit():
    #     v = form.c.data
    #     return redirect(url_for('main.posts_search', v=v))
    return render_template('home.html', posts=posts, q=q)

@main.route('/about', methods=['GET','POST'])
def about():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('未选中视频', 'info')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('未选中', 'info')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(current_app.root_path, 'static/uploads', filename))
            return redirect(url_for('main.display_video', filename=filename))
    return render_template('about.html', title="about")


@main.route('/about/<filename>')
def display_video(filename):
    video_file = url_for('static', filename='uploads/'+ filename)
    # return redirect(url_for('static', filename='uploads/' + filename), code=301)
    filename = video_file
    return render_template('about_video.html', filename=filename)

@main.route('/search/<string:q>/', methods=['POST', 'GET'])
def posts_search(q):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.title.contains(q) | Post.content.contains(q)).order_by(Post.date_posted.desc()).paginate(page=page,per_page=3)

#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.filter(Post.content.like(f'%{v}%'))\
#             .order_by(Post.date_posted.desc())\
#             .paginate(page=page,per_page=2)
    return render_template('posts_search.html', posts=posts,q=q)

@main.route('/api/about')
def api_about():
    users = User.query.all()
    use = {}
    for u in users:
        userInfor = {'id':u.id, 'username':u.username, 'email':u.email, 'image':u.image_file}
        use[u.id] = userInfor
    return jsonify(use)







