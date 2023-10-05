from MongoDB import connectDB

def userID_to_WalletAddress(user_id: str) -> str:
    if not user_id:
        return "錯誤:User ID不得為空值"

    db = connectDB()
    collection = db["User"]
    student = collection.find_one({'ID': user_id})

    if student is None:
        return False

    wallet_address = student.get('wallet_address')

    return wallet_address


def WalletAddress_to_userID(wallet_address: str) -> str:
    if not wallet_address:
        return "錯誤：錢包地址不得為空值"

    db = connectDB()
    collection = db["User"]
    user = collection.find_one({'wallet_address': wallet_address})

    if user is None:
        return "錯誤：找不到相應的用戶"

    user_id = user.get('ID')

    return user_id