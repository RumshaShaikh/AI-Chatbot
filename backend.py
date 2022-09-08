
from flask import Flask, render_template, request
from flask import session,redirect
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key="super-secret-key"

#this is for index page
@app.route("/")
def home():
    return render_template('index.html')

#this is the flask for textchat aka chatbot 
@app.route("/textchat")
def textchat():
    return render_template('textchat.html')
#this is for getting the inputs from the chatbot and running the same through the model



#for signup page aka dashboard
#this is the route for the dashboard page for editing and customizing the data
@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    return render_template("dashboard.html")


#this is for voicechat
@app.route("/voicechat")
def voice():
    return render_template("voicechat.html")



#this is for logging out of the signin page 
# @app.route('/logout')
# def logout():
#     session.pop('user')
#     return redirect('/dashboard')



#this is for about button on navibar just for info purpose
@app.route("/about")
def about():
    return render_template('about.html')

app.run(debug=True)