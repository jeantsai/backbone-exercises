import sys
import logging
from flask import Flask, jsonify, abort, make_response, request, url_for, g
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from flask_redis import FlaskRedis
from dns_resolver import get_redis_address


# Setup logging facility
console = logging.StreamHandler(sys.stdout)
console.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s'))
log = logging.getLogger('')
log.addHandler(console)
log.setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# Fetch the address of service redis from Consul
(redis_ip, redis_port) = get_redis_address()
redis_url = "redis://%s:%s/0" % (redis_ip, redis_port)
logger.info('Got the address of service redis as: %s' % redis_url)

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['REDIS_URL'] = redis_url

redis_store = FlaskRedis(app)
API_USAGE_KEY = 'visit:api:total'

courses = [
    {
        'id': 1,
        'title': u'Software Architecture',
        'description': u'Software architecture refers to the high level structures of a software system, the discipline of creating such structures, and the documentation of these structures.',
        'done': False
    },
    {
        'id': 2,
        'title': u'Software Management',
        'description': u'Software project management is an art and science of planning and leading software projects.',
        'done': False
    }
]

# Get API usage
@app.route('/ce/api/v1.0/usages', methods=['GET'])
def get_usage():
    count = redis_store.get(API_USAGE_KEY)
    # count = 12345
    return jsonify({"count": str(count, encoding='utf-8')})

@app.before_request
def before_request():
    redis_store.incr(API_USAGE_KEY)


# GET one specific course
@app.route('/ce/api/v1.0/courses/<int:course_id>', methods=['GET'])
# @auth.login_required
def get_course(course_id):
    course = list(filter(lambda t: t['id'] == course_id, courses))
    if len(course) == 0:
        abort(404)
    return jsonify( course[0] )

# transfer error page into JSON format
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)

# POST a new course
@app.route('/ce/api/v1.0/courses', methods=['POST'])
# @auth.login_required
def create_course():
    if not request.json or not 'title' in request.json:
        abort(400)
    course = {
        'id': courses[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    courses.append(course)
    return jsonify( course ), 201

# PUT an update
@app.route('/ce/api/v1.0/courses/<int:course_id>', methods=['PUT'])
# @auth.login_required
def update_course(course_id):
    course = list(filter(lambda t: t['id'] == course_id, courses))
    if len(course) == 0:
        abort(404)
    if not request.json:
        abort(400)
    # if 'title' in request.json and type(request.json['title']) != unicode:
    #     abort(400)
    # if 'description' in request.json and type(request.json['description']) is not unicode:
    #     abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    course[0]['title'] = request.json.get('title', course[0]['title'])
    course[0]['description'] = request.json.get('description', course[0]['description'])
    course[0]['done'] = request.json.get('done', course[0]['done'])
    return jsonify( course[0] )

# DELETE a course
@app.route('/ce/api/v1.0/courses/<int:course_id>', methods=['DELETE'])
# @auth.login_required
def delete_course(course_id):
    course = list(filter(lambda t: t['id'] == course_id, courses))
    if len(course) == 0:
        abort(404)
    courses.remove(course[0])
    return jsonify({'result': True})

# optimize web service interface: change id into url
def make_client_course(course):
    new_course = {}
    for field in course:
        if field == 'id':
            new_course['url'] = url_for('get_course', course_id=course['id'],_external=True)
        else:
            new_course[field] = course[field]
    return new_course

# @app.route('/ce/api/v1.0/courses',methods=['GET'])
# def get_courses():
#     return jsonify({'courses': list(map(make_client_course, courses))})

# strengthen security: login session

# @auth.get_password
# def get_password(username):
#     if username == 'miguel':
#         return 'python'
#     return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

# @app.route('/ce/api/v1.0/courses', methods=['GET'])
# # @auth.login_required
# def get_courses():
#     return jsonify({'courses': list(map(make_client_course, courses))})

db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

# must be here to create db
db.create_all()

# POST a new user
@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/ce/api/v1.0/courses')
# @auth.login_required
# def get_resource():
#     return jsonify({'data': 'Hello, %s!' % g.user.username})
def get_courses():
    return jsonify({'courses': courses})

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


if __name__ == '__main__':
    # Run the main function of this module
    app.run(host='0.0.0.0', port=5000, debug=True)
