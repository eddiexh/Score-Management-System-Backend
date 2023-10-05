# Account.py
from fastapi import APIRouter, HTTPException
from MongoDB import connectDB
from Model import User, UserLogin
from eth_account import Account

Account_Router = APIRouter(tags=["Account"])

@Account_Router.post("/Login")
def login_user(user: UserLogin):
    ID = user.ID
    Password = user.Password

    # 連接MongoDB
    db = connectDB()
    collection = db["User"]

    # 資料庫查詢
    user = collection.find_one({"ID": ID})
    if user and user["Password"] == Password:
        return {
            "ID": user["ID"],
            "Password": user["Password"],
            "Name": user["Name"],
            "Subject": user["Subject"],
            "Role": user["Role"],
            "Wallet_Address": user["Wallet_Address"],
            "Private_Key": user["Private_Key"]
        }

    raise HTTPException(status_code=401, detail="帳號或密碼錯誤")

@Account_Router.post("/Register")
def register_user(User: User):
    user_dict = User.dict()

    # 資料庫驗證
    db = connectDB()

    if db.User.find_one({"ID": user_dict["ID"]}):
        raise HTTPException(status_code=400, detail="用戶ID已存在")
        
    # 新增錢包地址及私鑰，並新增至資料庫
    wallet = Account.create()
    wallet_address = wallet.address
    private_key = wallet.key.hex()
    user_dict["Wallet_Address"] = wallet_address
    user_dict["Private_Key"] = private_key
        
    db.User.insert_one(user_dict)
    return {"detail": "註冊成功"}