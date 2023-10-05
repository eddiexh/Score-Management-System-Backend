# Function.py
from fastapi import APIRouter
from Model import UpdateScoreRequest, User
from MongoDB import connectDB
from smart_contract import getScore, invokeUpdateScore
from datetime import datetime
from fastapi import Response

Function_Router = APIRouter(tags=["Function"])

@Function_Router.post('/update_score')
async def update_score(request: UpdateScoreRequest):
    if request.new_score < 0 or request.new_score > 100:
        return Response(content="成績範圍:0-100")

    receipt = await invokeUpdateScore(request.student_id, request.new_score, request.subject, request.reason, request.teacher_id)
    return Response(content="成績已更新")


@Function_Router.get("/get_the_newest_score/{user_id}")
async def fetch_the_newest_score(user_id: str):
    # 從智能合約中讀取成績
    result = await getScore(user_id)

    scores = result[0]
    subjects = result[1]
    block_timestamps = result[3]

    # 創建一個字典來存儲各科最新成績
    latest_scores = {
        "Chinese": {"score": 0, "blockTimestamp": 0},
        "English": {"score": 0, "blockTimestamp": 0},
        "Math": {"score": 0, "blockTimestamp": 0},
        "Social_Studies": {"score": 0, "blockTimestamp": 0},
        "Science": {"score": 0, "blockTimestamp": 0}
    }

    for i in range(len(scores)):
        score_value = scores[i]
        subject = subjects[i]
        block_timestamp = block_timestamps[i]

        # 檢查是否為需要的科目，並更新最新成績
        if subject in latest_scores:
            if block_timestamp > latest_scores[subject]["blockTimestamp"]:
                latest_scores[subject] = {
                    "score": score_value,
                    "blockTimestamp": block_timestamp
                }

    # 計算總分和平均分
    total_score = 0
    subject_count = 0

    for subject, score_data in latest_scores.items():
        total_score += score_data["score"]
        subject_count += 1

    average_score = total_score / subject_count

    # 構建輸出字典
    output = {}
    for subject, score_data in latest_scores.items():
        output[subject] = str(score_data["score"])

    output["total"] = str(total_score)
    output["average"] = str(average_score)

    db = connectDB()
    student_data = db.User.find_one({'ID': user_id})['Name']
    output["User_ID"] = user_id
    output["Name"] = str(student_data)

    return output


@Function_Router.get("/get_all_score/{user_id}")
async def fetch_all_score(user_id: str):
     # 從智能合約中讀取成績
    result = await getScore(user_id)
    scores = result[0]
    subjects = result[1]
    reasons = result[2]
    block_timestamps = result[3]
    teacherIDs = result[4]

    formatted_scores = []
    for i in range(len(scores)):
        score_value = scores[i]
        subject = subjects[i]
        reason = reasons[i]
        block_timestamp = block_timestamps[i]
        teacherID = teacherIDs[i]

        # 將Unix時間戳轉換為日期和時間字符串
        timestamp = datetime.fromtimestamp(block_timestamp)
        formatted_timestamp = timestamp.strftime("%Y/%m/%d %H:%M")

        db = connectDB()
        formatted_scores.append({
            "name": db.User.find_one({"ID": user_id}, {"_id": 0, "Name": 1}),
            "student_ID": user_id,
            "score": score_value,
            "subject": subject,
            "reason": reason,
            "blockTimestamp": formatted_timestamp,
            "teacherID": teacherID
        })

    return formatted_scores


@Function_Router.get('/view_student')
async def view_student():
    db = connectDB()
    student_data = db.User.find({"Role": "Student"}, {"_id": 0, "ID": 1})

    student_ids = [{"ID": str(student["ID"])} for student in student_data]

    response_data = {"students": student_ids}
    return response_data