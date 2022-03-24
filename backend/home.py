
from flask import Flask, flash, render_template, send_from_directory,request,redirect
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/wad"
mongo = PyMongo(app)

@app.route('/')
@app.route('/index/')
def index():
    online_users = mongo.db.user.find({})
    return render_template("index.html",users=online_users)

@app.route('/signup',methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signUp.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if mongo.db.user.count_documents({'username':username})!=0:
            flash('This username is not avalaible. Please, choose another one')
            return redirect('/signup')
        else:
            mongo.db.user.insert_one({"username":username,"password":generate_password_hash(password)})
            return redirect('/auth')
    

@app.route('/auth',methods=['GET','POST'])
def auth():
    if request.method == "GET":
        return render_template("authentication.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = mongo.db.user.find_one({"username":username})
        if user and check_password_hash(user['password'],password):
          return render_template("secret.html")
        else:
            flash('Something went wrong, try again')
            return render_template("authentication.html")
    
@app.route('/auth/success',methods=['POST'])
def success():
    online_users = mongo.db.user.find({})
    return render_template("index.html",users=online_users)

if __name__ == "__main__":
    app.run(host='localhost', port=5001, debug=True)