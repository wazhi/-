from pydantic import BaseModel
from typing import Literal

LearningStyle = Literal["理论型", "实践型", "综合型"]
RiskLevel = Literal["低风险", "中风险", "高风险"]
ResourceType = Literal["视频", "课件", "代码实验", "练习题", "论文阅读"]

class Student(BaseModel):
    id: str; name: str; major: str; grade: str
    learningStyle: LearningStyle
    programmingLevel: int; mathLevel: int; aiFoundation: int
    activityScore: int; averageScore: int; riskLevel: RiskLevel

class KnowledgePoint(BaseModel):
    id: str; name: str
    category: Literal["基础知识", "机器学习", "深度学习", "工程应用"]
    difficulty: int; prerequisites: list[str]; description: str

class LearningRecord(BaseModel):
    studentId: str; knowledgeId: str
    quizScore: float; assignmentScore: float; practiceAccuracy: float
    studyTime: float; lastReviewDays: float

class LearningResource(BaseModel):
    id: str; title: str; knowledgeId: str; type: ResourceType
    difficulty: int; duration: str; description: str
