import random
from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory
from scripts import db
from flask_socketio import SocketIO,emit
import uuid
app=Flask(__name__)
app.config["SECRET_KEY"]="hello"
info={

}
login2sid={

}
socket=SocketIO(app=app)
def check_login(A):
    if A==None:
        return False
    elif len(A)<=4:
        return False
    else:
        return True
@app.route("/")
def main():
    if "hello" not in session:
        return redirect(url_for("sign_up"))
    else:
        rooms=db.get_rooms(session["login"])
        notifications=db.check_notifications(session["login"])
        if notifications==[]:
            return render_template("main.html",rooms=rooms,**info)
        else:
            return render_template("main.html",rooms=rooms,notifications=notifications,**info) 
        
@socket.event
def connect():
    login=session["login"]
    if login not in login2sid:
        login2sid[login]=[]
    login2sid[login].append(request.sid)

@socket.event
def disconnect():
    login=session["login"]
    if login in login2sid:
        login2sid[login].remove(request.sid)
            
    
@app.route("/sign_up",methods=["post","get"])
def sign_up():
    if request.method=="GET":
        return render_template("registration.html")
    if request.method=="POST":
        Login=request.form.get("login")
        Password=request.form.get("password")
        Confirmation=request.form.get("confirm")
        rez=check_login(Login)
        if rez==False:
            return render_template("registration.html",error="Login is not valid")
        if db.check_login(Login)==True:
            return render_template("registration.html",error="Login is taken")
        if Password!=Confirmation:
            return render_template("registration.html",error="Please repeat your confirmation password")
        else:
            db.save_user(Login, Password)
            session["hello"]=True
            session["login"]=Login
            return redirect(url_for("main"))
@app.route("/log_out")
def log_out():
    session.clear()
    return redirect(url_for("sign_up"))

@app.route("/sign_in",methods=["POST","GET"])
def sign_in():
    if request.method=="GET":
        return render_template("sign_in.html")
    if request.method=="POST":
        Login=request.form.get("login1")
        Password=request.form.get("password1")
        print(Login)
        print(Password)
        if db.check(Login,Password)==True:
            session["hello"]=True
            session["login"]=Login
            return(redirect(url_for("main")))
            
        else:
            return render_template("sign_in.html",error="Login or password are wrong")

@app.route("/create_room", methods=["POST","GET"])
def create_room():
    if request.method=="GET":
        info.clear()
        info["show"]=1
        return redirect(url_for("main"))
    if request.method=="POST":
        room=request.form.get("room_name")
        if not room:
            info.clear()
            info["show"]=1
            info["error"]=error="Please enter room name"
            return redirect(url_for("main"))
        else:
            db.new_room(room,session["login"])
            info.clear()
            return redirect(url_for("main"))

@app.route("/room/<int:room_id>",methods=("GET","POST"))
def chat(room_id):
    if "login" not in session:
        return redirect(url_for("sign_up"))
    if db.check_room(session["login"],room_id)!=True:
        return redirect(url_for("main"))
    msg=db.get_messages(room_id,session["login"])
    Users=db.users(room_id) 
    return render_template("room.html",room_id=room_id,msg=msg,Users=Users)

@app.route("/del/<int:room_id>",methods=("GET","POST"))
def del_room(room_id):
    if request.method=="GET":
        db.remove_room(room_id)
        info.clear()
        
        return redirect(url_for("main"))

@app.route("/message/<int:room_id>",methods=("POST",))
def message(room_id):
    img=request.files.get("Image")
    if img==None:
        filename=None 
    else:
        filename=uuid.uuid4().hex
        img.save("images/"+filename)
        Users=db.get_users_by_roomid(room_id) 
        Msg_id=db.new_message(room_id,session["login"],request.form.get("message"),filename)
        for i in Users:
            if i in login2sid:
                for sid in login2sid[i]:
                    socket.emit("message",[room_id,session["login"],request.form.get("message"),filename,Msg_id],to=sid)
   
    return redirect(url_for("chat",room_id=room_id))

@app.route("/get/<string:image_name>",methods=["GET",])
def get_img(image_name):
    
    return send_from_directory("images",image_name)

@app.route("/del/message/<int:message_id>/<int:room_id>",methods=("GET",))
def delete_msg(message_id,room_id):
    number=db.get_message_number(room_id,message_id)
    Users=db.get_users_by_roomid(room_id)
    db.delete(message_id,session["login"])
    for i in Users:
            if i in login2sid:
                for sid in login2sid[i]:
                    socket.emit("delete",[number,room_id],to=sid)
    return redirect(url_for("chat",room_id=room_id))

@app.route("/invite/<int:room_id>",methods=("POST",))
def invite(room_id):
    Name=request.form.get("user_name")
    button=request.form.get("invite")
    if button==button:
        if db.check_login(Name)==False:
            msg=db.get_messages(room_id,session["login"])
            return render_template("room.html",error="User does not exist",room_id=room_id,msg=msg)
        else:
            if Name in login2sid:
                notification_id=db.new_invite(Name,session["login"],room_id)
                for i in login2sid[Name]:
                    socket.emit("invite",[notification_id,session["login"],db.get_roomname_by_roomid(room_id)],to=i)
                return redirect(url_for("chat",room_id=room_id))
            else:
                db.new_invite(Name,session["login"],room_id)
                return redirect(url_for("chat",room_id=room_id))
        
@app.route("/invite/handle/<int:notification_id>", methods=("POST",))
def choice(notification_id):
    choice=request.form.get("Button")
    if choice=="Decline":
        db.delete_notification(notification_id)
        return redirect(url_for('main'))
    if choice=="Accept":
        invitation=db.get_notification_by_id(notification_id)
        Userto=invitation["Userto"]
        room_id=invitation["room_id"]
        db.add_user_to_room(room_id,Userto)
        db.delete_notification(notification_id)
        return redirect(url_for('main'))
    
socket.run(app=app,port=5000,debug=True)