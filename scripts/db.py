import pickle
import random
from google import genai
import threading


Users_info={

}
Rooms_info={

}
Messages=[]
room_users=[]
free_id=0
MSG=0
noti_id=0
invitations=[]
def save():
    F=open("db","wb")
    pickle.dump([Messages,Rooms_info,Users_info,room_users,MSG,free_id,invitations,noti_id],F)
    F.close()

def load():
    global Messages,Users_info,Rooms_info,room_users,MSG,free_id,invitations,noti_id
    F=open("db","rb")
    T=pickle.load(F)
    Messages=T[0]
    Users_info=T[2]
    Rooms_info=T[1]
    room_users=T[3]
    MSG=T[4]
    free_id=T[5]
    invitations=T[6]
    noti_id=T[7]
    F.close()

def save_user(Login,Password):
    Users_info[Login]=Password
    save()

def check(Login,Password):
    print(Users_info)
    if Login in Users_info:
        if Users_info[Login]==Password:
            return True
        else:
            return False
    else:
        return False
    
def check_login(Login):
    if Login not in Users_info:
        return False
    else:
        return True
    
def new_room(room_name,user_login):
    global free_id
    room_id=free_id
    free_id=free_id+1
    Rooms_info[room_id]=room_name
    room_users.append([room_id,user_login])
    save()

def get_rooms(user_login):
    result=[]
    for i in room_users:
        if user_login in i:
            room_id=i[0]
            room_name=Rooms_info[i[0]]
            room={
                "room_id":i[0],
                "room_name":Rooms_info[i[0]]
            }
            result.append(room)
    return result
try:
    load()
except:
    print("error")
def remove_room(room_id):
    del Rooms_info[room_id]
    for i in room_users:
        if i[0]==room_id:
            room_users.remove(i)

def new_message(room_id,user_name,message,image_name):
    global MSG
    Msg={
        "room_id":room_id,
        "user_name":user_name,
        "message":message,
        "Msg_id":MSG
    }
    if image_name==None:
        pass
    else:
        Msg["image"]=image_name
    if Msg["message"].replace(" ","")=="" and "image" not in Msg:
            pass
    else:
        MSG=MSG+1
        Messages.append(Msg)
        save()
    return MSG-1

def get_messages(room_id,userfrom):
    result=[]
    for i in Messages:
        if i["room_id"]==room_id and i["user_name"]==userfrom:
            i["mine"]=True
            result.append(i)
        if i["room_id"]==room_id and i["user_name"]!=userfrom:
            i["mine"]=False
            result.append(i)
    return(result)

def delete(Msg_id,userfrom):
    for i in Messages:
        if i["Msg_id"]==Msg_id and i["user_name"]==userfrom:
            Messages.remove(i)

def new_invite(Userto,Userfrom,room_id):
    global invitations,noti_id
    invitation={
        "Userto":Userto,
        "Userfrom":Userfrom,
        "room_id":room_id,
        "room_name":Rooms_info[room_id],
        "id":noti_id
    }
    invitations.append(invitation)
    noti_id=noti_id+1
    save()
    return noti_id-1

def check_notifications(User):
    notification=[]
    for i in invitations:
        if i["Userto"]!=User:
            pass
        else:
            notification.append(i)
    return notification

def delete_notification(noti_id):
    global invitations
    for i in invitations:
        if i["id"]==noti_id:
            invitations.remove(i)

def get_notification_by_id(noti_id):
    global invitations
    for i in invitations:
        if noti_id==i["id"]:
            return i

def add_user_to_room(room_id,user):
    room_users.append([room_id,user])
    
def check_message(Msg):
    text=Msg["message"]
    client = genai.Client(api_key="AIzaSyCsYY_zijaYFRxT-AFvIpMgV3Phu2sxk70")
    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents="Проанализируй следующий текст и напиши 'да' если текст агрессивный и 'нет' если не агрессивный.Пиши только 'да' или 'нет' и больше ничего! Вот текст"+text
    )
    print(response.text)
    if response.text=="да":
        Messages.remove(Msg)

def users(room_id):
    global room_users
    Count=0
    for i in room_users:
        if i[0]==room_id:
            Count=Count+1
    return Count

def check_room(login,room_id):
    for i in room_users:
        if i[1]==login and i[0]==room_id:
            return True
    return False

def get_roomname_by_roomid(room_id):
    return Rooms_info[room_id]

def get_users_by_roomid(room_id):
    Users=[]
    for i in room_users:
        if i[0]==room_id:
            Users.append(i[1])
    return Users

def get_message_number(room_id,message_id):
    number=0
    for i in Messages:
        if i["room_id"]==room_id:
            number=number+1
            if i["Msg_id"]==message_id:
                return number