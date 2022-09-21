
from flask import Flask, render_template, request
from flask import session,redirect, flash 
import json
import chatbot
with open("config.json","r") as c:
    params=json.load(c)["params"]

#this is just an extention since we were getting 1 input from the form in the files
def chatbot_response(usertext):
    with open("text.txt","r") as f:
        data=f.read()
    s=chatbot.question_answer(usertext,data)
    return s.capitalize()+"."

app = Flask(__name__)
app.secret_key="super-secret-key"

#this is for index page
@app.route("/")
def home():
    return render_template('index.html',params=params)

#this is the flask for textchat aka chatbot 
@app.route("/textchat")
def textchat():
    return render_template('textchat.html')
#this is for getting the inputs from the chatbot and running the same through the model to be updated when model is made
@app.route("/textchat/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)



#for signup page aka dashboard
#this is the route for the dashboard page for editing and customizing the data
@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if request.method=="POST":
            if "content" in request.form:
                with open("text.txt","w")as f:
                    f.write(request.form["content"])
                flash("Data Update Successfully","success")
            else:
                username = request.form.get("uname")
                userpass = request.form.get("pass")
                if username==params['admin_user'] and userpass==params['admin_password']:
                    # set the session variable
                    session['user']=username
                    with open("text.txt","r") as f:
                        data=f.read()
                        params["dataset"]=data
                    return render_template("dashboard.html", params=params)
                else:
                    flash("Username or Password Incorrect","danger")
                    return render_template("signin.html", params=params)

    if "user" in session and session['user']==params['admin_user']:
        with open("text.txt","r") as f:
            data=f.read()
            params["dataset"]=data
        return render_template("dashboard.html", params=params)
    else:
        return render_template("signin.html", params=params)


#this is for voicechat left to be implemented in the website
@app.route("/voicechat")
def voice():
    return render_template("voicechat.html")
@app.route("/voicechat/get")
def get_bot_response2():
    userText = request.args.get('msg')
    return chatbot_response(userText)



#this is for logging out of the signin page 
@app.route('/logout')
def logout(): 
    if 'user' in session: 
        session.pop('user')
        return redirect('/dashboard')
    else:
        return render_template('index.html',params=params)



#this is for about button on navibar just for info purpose
@app.route("/about")
def about():
    return render_template('about.html',params=params)

app.run(debug=True)
