from flask import Blueprint
from flask_restful import Resource, fields, marshal_with, Api
from flaskBlog.api.utils import get_all_posts, get_all_users, get_image, update_video, create_video, get_video, get_all_videos



api_bp = Blueprint('api',  __name__)
apis = Api(api_bp)


resource_fields = {
    'id': fields.String,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class VideoS(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        return get_video(video_id),200
        
    @marshal_with(resource_fields)
    def put(self, video_id):
        return create_video(video_id), 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        return update_video(video_id)

class VideoL(Resource):
    def get(self):
        return get_all_videos()

#获取图片
class Image(Resource):
    def get(self, username):
        return get_image(username)

class UsersList(Resource):
    def get(self):
        return get_all_users()

#获取特定数量帖子信息(4)
class PostsList(Resource):
    def get(self):
        return get_all_posts()

apis.add_resource(UsersList, '/api/users')
apis.add_resource(VideoS, '/api/videos/<int:video_id>')
apis.add_resource(VideoL, '/api/videos')
apis.add_resource(PostsList, '/api/posts')
apis.add_resource(Image, '/api/images/<username>')