from flask import Flask, request, make_response
import pymongo
from pymongo import MongoClient
from dotenv import dotenv_values
import bcrypt
from bson import ObjectId
import jwt
import time

config = dotenv_values(".env")
app = Flask(__name__)
flag = config["flag"]
db = MongoClient(config["database_url"]).igb
users = db.users
accounts = db.accounts
jwt_secret = config["jwt_secret"]
target_amount = 1000

def fixuserobj(user):
    user["_id"] = str(user["_id"])
    user["password"] = user["password"].decode("UTF-8")
    return user

def fixaccounts(accounts):
    for i, val in enumerate(accounts):
        accounts[i]['owner'] = str(val['owner'])
        accounts[i]['_id'] = str(val['_id'])
    return accounts

@app.route("/user/register", methods=["POST"])
def register():
    data = request.json # email, name, password
    if users.find_one({'email':data['email']}) is not None:
        return "Account with email already exists", 400
    else:
        result = users.insert_one({"email":data["email"],"name":data["name"],"id_validated":False,"password":bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt())})
        if ObjectId.is_valid(result.inserted_id):
            resp = make_response("Ok")
            resp.set_cookie('auth', jwt.encode({"id": str(result.inserted_id)}, "secret", algorithm="HS256"))
            return resp
    return "",500

@app.route("/user/login", methods=["POST"])
def login():
    data = request.json # mail, password
    user = users.find_one({"email":data['email']})
    print(user)
    if user['password'] is not None:
        check = bcrypt.checkpw(data["password"].encode("UTF-8"), user["password"])
        if check:
            resp = make_response("Ok")
            resp.set_cookie('auth', jwt.encode({"id": str(user["_id"])}, jwt_secret, algorithm="HS256"))
            return resp
    return ""

@app.route("/user/getbyid", methods=["POST"])
def get_me():
    data = request.json # mail, password
    reqid = data["id"]
    jwt_auth = request.headers["auth"]
    decoded = jwt.decode(jwt_auth, jwt_secret, algorithms=["HS256"])
    if decoded['id'] == reqid:
        user = fixuserobj(users.find_one({"_id":ObjectId(decoded['id'])}))
        if user is not None:
            return user
        else:
            return "User not found",501
    else:
        return "IDs don't match", 500
    return "Error", 500

@app.route("/account/new", methods=["GET"])
def new_account():
    jwt_auth = request.headers["auth"]
    print("OKKK")
    decoded = jwt.decode(jwt_auth, jwt_secret, algorithms=["HS256"])
    user = fixuserobj(users.find_one({"_id":ObjectId(decoded['id'])}))

    if user:
        user_accounts = list(accounts.find({"owner":ObjectId(user["_id"])}))
        if len(user_accounts) > 4:
            return "You can only open 5 bank accounts per user", 400
        else:
            result = accounts.insert_one({"owner":ObjectId(user["_id"]),"balance":2000})
            if ObjectId.is_valid(result.inserted_id):
                return "Successfully opened account with id {}".format(str(result.inserted_id))
            else:
                return "Error", 500
    return "User not found", 500

@app.route("/account/list", methods=["GET"])
def list_accounts():
    jwt_auth = request.headers["auth"]
    decoded = jwt.decode(jwt_auth, jwt_secret, algorithms=["HS256"])
    user = fixuserobj(users.find_one({"_id":ObjectId(decoded['id'])}))
    if user:
        user_accounts = fixaccounts(list(accounts.find({"owner":ObjectId(user["_id"])})))
        return {"user":user['_id'],"accounts":user_accounts}
    return ""


@app.route("/account/transfer/<fromacc>/<toacc>/", methods=["POST"])
def transfer_funds(fromacc, toacc): # BUG IS IN THIS ENDPOINT. Some parts have been programmed in a "weird" way so that the exploiting is easier
    jwt_auth = request.headers["auth"]
    data = request.json # amount
    try:
        amount = int(data["amount"])
    except:
        return "Amount not int", 400
    decoded = jwt.decode(jwt_auth, jwt_secret, algorithms=["HS256"])
    user = fixuserobj(users.find_one({"_id":ObjectId(decoded['id'])}))
    if user:
        user_accounts = fixaccounts(list(accounts.find({"owner":ObjectId(user["_id"])})))
        from_ok = False
        to_ok = False
        amount_ok = False
        for account in user_accounts:
            if account["_id"] == fromacc:
                fromaccobj = account
                from_ok = True
                if account["balance"] >= amount:
                    amount_ok = True
            if account["_id"] == toacc:
                toaccobj = account
                to_ok = True

        if from_ok and to_ok and amount_ok:

            accounts.update_one({"_id":ObjectId(toacc)}, {"$set": {"balance":toaccobj["balance"]+amount}}, upsert=True)
            time.sleep(0.05)
            accounts.update_one({"_id":ObjectId(fromacc)}, {"$set": {"balance":fromaccobj["balance"]-amount}}, upsert=True)

        else:
            if from_ok == False:
                return "You can only transfer funds from your own account!", 400
            elif amount_ok == False:
                return "Not enough funds", 400
            else:
                return "Only confirmed users can tranfer funds to other users", 400
        return {"user":user['_id'],"accounts":user_accounts}
    return ""


@app.route("/buy_spaceship/<account>/", methods=["GET"])
def buy_spaceship(account):
    jwt_auth = request.headers["auth"]
    decoded = jwt.decode(jwt_auth, jwt_secret, algorithms=["HS256"])
    user = fixuserobj(users.find_one({"_id":ObjectId(decoded['id'])}))
    if user:
        account = accounts.find_one({"owner":ObjectId(user["_id"]), "balance": {"$gte":target_amount}})
        if account is not None:
            return {"message": flag}
        else:
            return {"message": "Not enough money to buy a spaceship"}
    return ""
