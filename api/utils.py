import os
from sqlalchemy import func
from flask import current_app, request, send_file
from flaskBlog.models import Video, User, Post
from flaskBlog import db
from flask_restful import abort, reqparse


video_args = reqparse.RequestParser()
# 下面的resource_fields全部都是对VideoS的装饰,
video_args.add_argument('name',help="invalid values name", required=True)
video_args.add_argument('views', type=int, help="invalid values views", required=True)
video_args.add_argument('likes', type=int, help="invalid values likes", required=True)



#获取所有的Videos帖子
def get_all_videos():
    videos = Video.query.all()
    if not videos:
        abort(404, message="没有...")
    rv ={}
    for v in videos:
        video = {'id':v.id, 'name': v.name, 'views':v.views, 'likes':v.likes}
        rv[v.id] = video
    return rv

#获取特定id的帖子
def get_video(video_id):
    result = Video.query.filter_by(id=video_id).first()
    if not result:
        abort(404, message="没有...")
    video = {'id': result.id, 'name': result.name, 'views':result.views, 'likes':result.likes}
    return video


#创建一个帖子
def create_video(video_id):
    args = video_args.parse_args()
    result = Video.query.filter_by(id=video_id).first()
    if result:
        abort(409, message='ID被占用...')
    video = Video(id=video_id,name=args['name'],views=args['views'],likes=args['likes'])
    db.session.add(video)
    db.session.commit()
    return video

#更新特定id的帖子
def update_video(video_id):
    args = video_args.parse_args()
    result = Video.query.filter_by(id=video_id).first()
    if not result:
        abort(404, message="不存在...")
    result.name = args['name']
    result.views = args['views']
    result.likes = args['likes']
    db.session.commit()
    return result

#删除特定id的帖子
def del_video(video_id):
    result = Video.query.filter_by(id=video_id).first()
    if not result:
        abort(404, message="不存在...")
    db.session.delete(result)
    db.session.commit()
    return '', 204


#获取所有用户的信息
def get_all_users():
    users = User.query.all()
    if not users:
        abort(404, message="用户不存在")
    usersInfor = {}
    for user in users:
        userInfor = {'name':user.username, 'email':user.email}
        usersInfor[user.id] = userInfor
    return usersInfor




#获取特定username帖子图片
def get_image(username):
    user = User.query.filter_by(username=username).first()
    file_path = os.path.join(current_app.root_path,'static',user.image_file)
    return send_file(file_path)


# 获取所有帖子信息
def get_all_posts():
    posts = Post.query.all()
    if not posts:
        abort(404, message="没有帖子")
    allposts = []
    for post in posts:
        p = {'title':post.title,
        'content':post.content, 
        'author':post.author.username, 
        # 'date_posted':post.date_posted
        'img':post.author.image_file
        }
        allposts.append(p)
    return allposts
