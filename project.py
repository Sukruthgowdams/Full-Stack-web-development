from flask import *   
import pyrebase as pyrebase
from flask import Flask, session
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


firebaseConfig = {
  "apiKey"           : "AIzaSyDgmrEYltHWhU3weMa1XMyyCtpNMo0A_FM",
  "authDomain"       : "victus-525c8.firebaseapp.com",
  "databaseURL"      : "https://victus-525c8-default-rtdb.firebaseio.com",
  "projectId"        : "victus-525c8",
  "storageBucket"    : "victus-525c8.appspot.com",
  "messagingSenderId": "394755840208",
  "appId"            : "1:394755840208:web:6aca03439246d30d2da6d5",
  "measurementId"    : "G-RRMM6VN54E"
};
count=0
firebase = pyrebase.initialize_app(firebaseConfig)

rdb=firebase.database()
sdb=firebase.storage()

@app.route("/", methods=["GET", "POST"])
def mainfun():
    if 'logged_in' not in session:
        session['logged_in'] = False
    global count

    if(request.form):
        clicked=request.form["btn"]
        if ((clicked=="loginbtn") or (clicked == "login")):
            if(count==3):
                return render_template("homepage.html" , message="Your account has been blocked since maximum attempts has reached")
            else:
                return render_template("login.html")
        elif (clicked=="signupbtn"):
            return render_template("signup.html")
        elif (clicked=="Signup"):
            name=request.form["name"]
            email=request.form["email"]
            password=request.form["psw"]
            phonenumber=request.form["phonenumber"]
            photo=request.files["photo"]
            user = {
                "name": name,
                "email": email,
                "psw":password,
                "phonenumber": phonenumber,
        
            }
            if rdb.child(name).get().val() is not None:
                return render_template("signup.html", message="Username is already taken! Please provide a different username")            
            rdb.child(name).update(user)
            sdb.child(name).put(photo)
            return render_template("login.html", message2="Sign up successful.You can now login!")
        elif (clicked=="loginsubmit"):
            lname = request.form["lname"]
            lpsw= request.form["lpsw"]
            fdbname=rdb.child(lname).child("name").get().val()
            fdbpsw=rdb.child(lname).child("psw").get().val()
            
            if lname == fdbname and lpsw == fdbpsw:
                session['logged_in'] = True  
                return render_template("main.html", message=" " + lname)


            
            if ((lname==fdbname)and(lpsw==fdbpsw)):
                return render_template("main.html", message=" "+lname)
                
                
            else:
                count+=1
                if(count>=3):
                    return render_template("homepage.html", message="Login unsuccessful. Account blocked")
                else:
                    return render_template("login.html", message1="Login unsuccessful. Please try again. You have(" +str(3-count)+")attempts left")
    return render_template("homepage.html", name="Sukruth")
@app.route("/logout", methods=["GET"])
def logout():
    session['logged_in'] = False 
    return redirect(url_for('mainfun'))

if __name__ == '__main__':
    app.run(debug=True, port=5005)
"""background-image: url("");"""