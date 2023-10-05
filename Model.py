#Model.py

from pydantic import BaseModel, Field, validator
from typing import List

class User(BaseModel):
    ID: str
    Password: str
    Name: str
    Subject: str
    Role: str
    Wallet_Address: str
    Private_Key: str

class UserLogin(BaseModel):
    ID: str
    Password: str

class User_Token(BaseModel):
    Wallet_Address: str

class Criterion(BaseModel):
    name: str
    percentage: float

class GradingCriteria(BaseModel):
    criteria: List[Criterion]

class Score(BaseModel):
    student_ID: str
    score: int
    subject: str
    reason: str

class AllScore(BaseModel):
    AllScore: list[Score]

class UpdateScoreRequest(BaseModel):
    student_id: str
    new_score: int
    subject: str
    reason: str
    teacher_id: str

class ScoreDataResponse(BaseModel):
    status: str
    score_data: dict