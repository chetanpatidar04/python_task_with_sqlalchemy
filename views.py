from flask import Flask,request,jsonify,Response,make_response
from flask_sqlalchemy import SQLAlchemy
import json
import sys
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:chetan123@localhost/games"
app.config["SQLALCHEMY_DATABASE_URI"]='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='chetan123', server='localhost', database='games')
# username:password@localhost/db_name
db = SQLAlchemy(app)


class Games_data(db.Model):
    id = db.Column(db.Integer, primary_key = True,nullable=True)
    title = db.Column(db.String, unique=False, nullable=True,)
    platform = db.Column(db.String, unique=False, nullable=True)
    score = db.Column(db.Float, unique=False, nullable=True)
    genre = db.Column(db.String, unique=False, nullable=True)
    editors_choice = db.Column(db.String, unique=False, nullable=True)

    def __init__(self, title, platform,score,genre,editors_choice):
        self.title = title
        self.platform = platform
        self.score = score
        self.genre = genre
        self.editors_choice = editors_choice

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100))
    name = db.Column(db.String(50))
    password = db.Column(db.String(150))
    admin = db.Column(db.Boolean)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']        
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:            
            data =jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator


@app.route('/register', methods=['POST'])
def signup_user():
    """This api will register the new user"""
    try:
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)        
        db.session.add(new_user)  
        db.session.commit()
        response = {"status": True, "message": "User registered successfully"}
    except Exception as e:
        response = {"status": False, "message": "error {}".format(e.__repr__())}
    return Response(json.dumps(response), mimetype="application/json")    

@app.route('/login', methods=['POST'])  
def login_user():
    """this api will login the user and create a new token"""
    try: 
        auth = request.authorization
        
        if not auth or not auth.username or not auth.password:  
            return jsonify({"status": False,'Message' : "could not verify"})
        user = Users.query.filter_by(name=auth.username).first()            
        if check_password_hash(user.password, auth.password):
            token = jwt.encode({"username":auth.username,"public_id":user.public_id}, "secret", algorithm="HS256")
            response = {"status": True,'token' : token}
            return Response(json.dumps(response), mimetype="application/json") 
    except Exception as e:
        response = {"status": False, "message": "could not verify ,error{}".format(e.__repr__())}
    return Response(json.dumps(response), mimetype="application/json")


@app.route('/addgame',methods=["POST"])
@token_required
def addgame(self):
    """this api will add a new game details """
    try:	
        json_data = request.get_json()
        title_j = json_data.get("title","")
        platform_j = json_data.get("platform","")
        score_j = json_data.get("score",0)
        genre_j = json_data.get("genre","")
        editors_choice_j = json_data.get("editors_choice","")    
        entry = Games_data(title_j,platform_j,score_j,genre_j,editors_choice_j)
        db.session.add(entry)
        db.session.commit()
        response ={"status": True,"Message": "Game details saved successfully"}
    except Exception as e:
        response = {"status": False, "message": "Unable to save ,error{}".format(e.__repr__())}
    return Response(json.dumps(response), mimetype="application/json")


@app.route('/searchgame',methods=["POST"])
@token_required
def search_game(self):
    """this api will search a game based on the title in the payload"""
    try:
        """ serach all the games based on the title"""
        json_data = request.get_json()
        title_j = json_data.get("title")
        data = Games_data.query.filter_by(title=title_j).all()
        games_list =[]
        for i in data:
            games_list.append({"title":i.title,"platform":i.platform,"genre":i.genre,"score":i.score,"editors_choice":i.editors_choice})
        response = {"status":True,"Search result":[games_list]}
    except Exception as e:
        response = {"status": False, "message": "No serach results for this game ,error{}".format(e.__repr__())}
    return Response(json.dumps(response), mimetype="application/json")
        

@app.route('/updategame', methods = ['PUT'])
@token_required
def update(self):
    """ Api for update data based on id """
    try:
        data_json = request.get_json()
        id_j = int(data_json.get("id"))
        data = Games_data.query.filter_by(id=id_j).first()
        if data_json.get("score"):            
            data.score = float(data_json.get("score"))
        if data_json.get("title"):            
            data.title = data_json.get("title")
        if data_json.get("platform"):            
            data.platform = data_json.get("platform")
        if data_json.get("genre"):            
            data.genre = data_json.get("genre")
        if data_json.get("editors_choice"):
            data.editors_choice = data_json.get("editors_choice")
        db.session.commit()
        response = {"status":True,"Message":"Games data Updated Successfully"}
    except Exception as e:
        response = {"status": False, "message": "Unable to update ,error{}".format(e.__repr__())}
    return Response(json.dumps(response), mimetype="application/json")    


@app.route('/deletegame/<id>', methods = ['DELETE'])
@token_required
def deletegame(self,id):
    """ Delete game based on the id"""
    try:
        my_data = Games_data.query.get(id)
        if my_data:
            db.session.delete(my_data)
            db.session.commit()
            response ={"status":True,"Message":"Game Details Deleted Successfully"}
        else:
            response = {"status":False,"Message":"No game with this id"}
    except Exception as e:
        response = {"status": False, "message": "Unable to delete the game ,error{}".format(e.__repr__())}
    return Response(json.dumps(response), mimetype="application/json")


@app.route('/filtergames',methods=["POST"])
@token_required
def allgames(self):
    """this api will filter data based on the paylod key and value"""
    try:
        li=[]
        json_data = request.get_json()
        if json_data.get("title"):
            data = Games_data.query.filter_by(title=json_data.get("title")).all()
        elif json_data.get("platform"):
            data = Games_data.query.filter_by(platform=json_data.get("platform")).all()
        elif json_data.get("genre"):
            data = Games_data.query.filter_by(genre=json_data.get("genre")).all()
        elif json_data.get("score"):
            data = Games_data.query.filter_by(score=float(json_data.get("score"))).all()
        elif json_data.get("editors_choice"):
            data = Games_data.query.filter_by(editors_choice=json_data.get("editors_choice")).all()        
        else:
            data = Games_data.query.filter_by().all()
        for i in data:
            li.append({"title":i.title,"platform":i.platform,"genre":i.genre,"score":i.score,"editors_choice":i.editors_choice})
        if json_data.get("sort_order"):
            if json_data.get("sort_order").upper() =="ASC":
                sort_orders = sorted(li, key = lambda i: i['score'])
            if json_data.get("sort_order").upper() =="DESC":    
                sort_orders = sorted(li, key = lambda i: i['score'],reverse=True)                
        else:
            response = {"Status":True,"Filter result":li}
            return Response(json.dumps(response), mimetype="application/json")
        response ={"Status":True,"Filter result":sort_orders}
    except Exception as e:
        response = {"status": False, "message": "Unable to filter games ,error{}".format(e.__repr__())}
    return Response(json.dumps(response), mimetype="application/json")


        
if __name__ == '__main__':
	app.run(debug=True)
