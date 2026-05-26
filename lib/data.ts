import { KnowledgePoint, LearningRecord, LearningResource, Student } from "./types";

export const students: Student[] = [
  { id: "s1", name: "李明", major: "自动化", grade: "2023", learningStyle: "实践型", programmingLevel: 82, mathLevel: 70, aiFoundation: 68, activityScore: 85, averageScore: 78, riskLevel: "中风险" },
  { id: "s2", name: "王雪", major: "计算机", grade: "2023", learningStyle: "理论型", programmingLevel: 76, mathLevel: 88, aiFoundation: 84, activityScore: 72, averageScore: 86, riskLevel: "低风险" },
  { id: "s3", name: "张强", major: "机械", grade: "2022", learningStyle: "综合型", programmingLevel: 60, mathLevel: 64, aiFoundation: 58, activityScore: 45, averageScore: 59, riskLevel: "高风险" },
  { id: "s4", name: "刘洋", major: "电子", grade: "2023", learningStyle: "实践型", programmingLevel: 88, mathLevel: 66, aiFoundation: 72, activityScore: 80, averageScore: 74, riskLevel: "中风险" },
  { id: "s5", name: "陈雨", major: "软件工程", grade: "2022", learningStyle: "理论型", programmingLevel: 70, mathLevel: 90, aiFoundation: 80, activityScore: 68, averageScore: 82, riskLevel: "低风险" },
  { id: "s6", name: "赵晨", major: "信息工程", grade: "2024", learningStyle: "综合型", programmingLevel: 67, mathLevel: 72, aiFoundation: 65, activityScore: 61, averageScore: 69, riskLevel: "中风险" },
  { id: "s7", name: "孙婷", major: "机器人", grade: "2023", learningStyle: "实践型", programmingLevel: 74, mathLevel: 63, aiFoundation: 60, activityScore: 55, averageScore: 62, riskLevel: "中风险" },
  { id: "s8", name: "周航", major: "计算机", grade: "2024", learningStyle: "理论型", programmingLevel: 55, mathLevel: 58, aiFoundation: 52, activityScore: 40, averageScore: 56, riskLevel: "高风险" },
];

export const knowledgePoints: KnowledgePoint[] = ["Python基础|基础知识|1||编程基础", "数据预处理|基础知识|2|k1|清洗标准化", "特征工程|机器学习|3|k2|特征构造", "线性回归|机器学习|2|k1,k2|回归基础", "逻辑回归|机器学习|2|k1,k2|分类基础", "决策树|机器学习|2|k1,k2|可解释分类", "随机森林|机器学习|3|k6|集成学习", "支持向量机|机器学习|3|k5|间隔分类", "神经网络基础|深度学习|3|k3,k5|反向传播", "CNN|深度学习|4|k9|卷积模型", "RNN|深度学习|4|k9|时序模型", "Transformer|深度学习|5|k9|注意力机制", "模型评估指标|机器学习|2|k4,k5|精确率召回率", "过拟合与正则化|机器学习|3|k4,k5|泛化能力", "超参数优化|工程应用|4|k13,k14|调优方法", "工程部署基础|工程应用|3|k7,k10,k12|部署上线"].map((s, i) => { const [name, category, d, p, description] = s.split("|"); return { id: `k${i+1}`, name, category: category as any, difficulty: Number(d) as any, prerequisites: p ? p.split(",").filter(Boolean) : [], description }; });

export const learningRecords: LearningRecord[] = students.flatMap((st, si) => knowledgePoints.slice(0, 8 + (si % 8)).map((k, ki) => ({
  studentId: st.id, knowledgeId: k.id,
  quizScore: Math.max(40, Math.min(95, st.averageScore + (ki % 5) * 2 - si * 2)),
  assignmentScore: Math.max(45, Math.min(96, st.averageScore + (ki % 4) * 3 - si)),
  practiceAccuracy: Math.max(35, Math.min(94, st.programmingLevel + (ki % 6) * 2 - si)),
  studyTime: Math.max(1, 2 + (ki % 4) + Math.floor(st.activityScore / 30)),
  lastReviewDays: Math.max(1, 5 + si * 2 + (ki % 10))
})));

export const learningResources: LearningResource[] = knowledgePoints.flatMap((k, i) => ([
  { t: "视频", d: Math.max(1, k.difficulty - 1) },
  { t: "课件", d: k.difficulty },
  { t: "代码实验", d: k.difficulty },
]).map((x, j) => ({ id: `r${i*3+j+1}`, title: `${k.name}${x.t}资源`, knowledgeId: k.id, type: x.t as any, difficulty: x.d as any, duration: `${20 + j*15}分钟`, description: `面向${k.name}的${x.t}学习材料` }))).concat([
  { id: "r100", title: "Transformer论文精读", knowledgeId: "k12", type: "论文阅读", difficulty: 5, duration: "60分钟", description: "Attention Is All You Need 导读" },
  { id: "r101", title: "机器学习综合练习", knowledgeId: "k13", type: "练习题", difficulty: 3, duration: "45分钟", description: "评估指标与模型选择" }
]);
