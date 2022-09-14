
from flask import Flask, render_template, request
from flask import session,redirect
import json
with open("config.json","r") as c:
    params=json.load(c)["params"]

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
#this is for getting the inputs from the chatbot and running the same through the model to be updated when model is made



#for signup page aka dashboard
#this is the route for the dashboard page for editing and customizing the data
@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if request.method=="POST":
            if "content" in request.form:
                with open("text.txt","w")as f:
                    f.write(request.form["content"])
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



#this is for logging out of the signin page 
@app.route('/logout')
def logout(): 
    if 'user' in session: 
        session.pop('user')
        return redirect('/dashboard')
    else:
        return render_template('index.html')



#this is for about button on navibar just for info purpose
@app.route("/about")
def about():
    return render_template('about.html')

app.run(debug=True)