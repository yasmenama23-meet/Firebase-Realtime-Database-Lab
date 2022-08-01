from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {

  "apiKey": "AIzaSyAD4GfFEryVSOtmCwg8K31i9ARTCDnKPPQ",

  "authDomain": "yasmena1-d7852.firebaseapp.com",

  "projectId": "yasmena1-d7852",

  "storageBucket": "yasmena1-d7852.appspot.com",

  "messagingSenderId": "883793147528",

  "appId": "1:883793147528:web:8151bfd6c196e1badad13d",

  "measurementId": "G-NM1BS96RRV",
  "databaseURL": "https://project-6517378840567117056-default-rtdb.firebaseio.com/  "}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db= firebase.database()



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']

       try:
          login_session['user'] = auth.create_user_with_email_and_password(email, password)
          user={"name":request.form['full_name'],"email":email }
          db.child("users").child(login_session['user']['localId']).set(user)
          return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
    return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method=='POST':
        title=request.form['title']
        text=request.form['text']
        try:
            tweet={"title":title,"text":text}
            db.child("tweets").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            pass
    return render_template("add_tweet.html") 

@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
    return render_template("tweet.html", tweets=db.child('tweets').get().val().values())
if __name__ == '__main__':
    app.run(debug=True)