export type RiskLevel = "低风险" | "中风险" | "高风险";
export type LearningStyle = "理论型" | "实践型" | "综合型";
export type ResourceType = "视频" | "课件" | "代码实验" | "练习题" | "论文阅读";

export type Student = { id: string; name: string; major: string; grade: string; learningStyle: LearningStyle; programmingLevel: number; mathLevel: number; aiFoundation: number; activityScore: number; averageScore: number; riskLevel: RiskLevel; };
export type KnowledgePoint = { id: string; name: string; category: "基础知识" | "机器学习" | "深度学习" | "工程应用"; difficulty: 1 | 2 | 3 | 4 | 5; prerequisites: string[]; description: string; };
export type LearningRecord = { studentId: string; knowledgeId: string; quizScore: number; assignmentScore: number; practiceAccuracy: number; studyTime: number; lastReviewDays: number; };
export type KnowledgeDiagnosis = { knowledgeId: string; knowledgeName: string; mastery: number; level: string; };
export type LearningPathItem = { day: number; knowledgeId: string; knowledgeName: string; reason: string; task: string; resourceType: ResourceType; estimatedTime: string; };
export type LearningResource = { id: string; title: string; knowledgeId: string; type: ResourceType; difficulty: 1 | 2 | 3 | 4 | 5; duration: string; description: string; };
