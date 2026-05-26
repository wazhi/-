import { knowledgePoints, learningRecords, learningResources, students } from "./data";
import { KnowledgeDiagnosis, LearningPathItem, LearningRecord, LearningResource, ResourceType, Student } from "./types";

export function calculateMastery(record: LearningRecord): number {
  const normalizedStudyTime = Math.min(record.studyTime / 5, 1) * 100;
  const reviewPenalty = Math.min(record.lastReviewDays / 30, 1) * 100;
  return Number((0.35 * record.quizScore + 0.3 * record.assignmentScore + 0.25 * record.practiceAccuracy + 0.1 * normalizedStudyTime - 0.05 * reviewPenalty).toFixed(2));
}
export function getMasteryLevel(m: number): string { if (m >= 85) return "优秀"; if (m >= 70) return "良好"; if (m >= 60) return "一般"; return "薄弱"; }
export function calculateRiskLevel(student: Student) { if (student.averageScore >= 80 && student.activityScore >= 70) return "低风险" as const; if (student.averageScore >= 60 && student.activityScore >= 50) return "中风险" as const; return "高风险" as const; }
export function diagnoseWeakKnowledge(studentId: string): KnowledgeDiagnosis[] {
  return learningRecords.filter(r => r.studentId === studentId).map(r => { const k = knowledgePoints.find(x => x.id === r.knowledgeId)!; const mastery = calculateMastery(r); return { knowledgeId: k.id, knowledgeName: k.name, mastery, level: getMasteryLevel(mastery) }; }).sort((a,b)=>a.mastery-b.mastery);
}
export function generateDiagnosisText(studentId: string): string {
  const diag = diagnoseWeakKnowledge(studentId); if (!diag.length) return "暂无学习记录。";
  const weak = diag.filter(d=>d.mastery<60).slice(0,2).map(d=>`“${d.knowledgeName}”`); const strong = [...diag].sort((a,b)=>b.mastery-a.mastery).slice(0,2).map(d=>`“${d.knowledgeName}”`);
  return `该学生在${strong.join("和")}方面掌握较好，但在${weak.join("和")}方面较薄弱。建议先补强前置知识，再进行高阶模型学习。`;
}
const goalMap: Record<string,string[]> = {"掌握机器学习基础":["k3","k4","k5","k6","k7","k8","k13","k14"],"掌握深度学习基础":["k9","k10","k11","k12"],"完成课程实验":["k2","k3","k7","k10","k16"],"准备期末考试":["k1","k2","k4","k5","k9","k12","k13","k14"],"完成工程项目":["k2","k7","k12","k15","k16"]};
const styleResource: Record<string, ResourceType[]> = {"理论型":["课件","论文阅读","视频"],"实践型":["代码实验","练习题","视频"],"综合型":["视频","代码实验","课件"]};
export function generateLearningPath(studentId: string, goal: string): LearningPathItem[] {
  const s = students.find(x=>x.id===studentId)!; const targetIds = goalMap[goal] ?? goalMap["准备期末考试"]; const mastery = new Map(diagnoseWeakKnowledge(studentId).map(d=>[d.knowledgeId,d.mastery]));
  const selected = new Set<string>();
  for (const id of targetIds) { const kp = knowledgePoints.find(k=>k.id===id)!; if ((mastery.get(id) ?? 50) < 70) selected.add(id); kp.prerequisites.forEach(p => { if ((mastery.get(p) ?? 50) < 70) selected.add(p); }); }
  const sorted = [...selected].map(id=>knowledgePoints.find(k=>k.id===id)!).sort((a,b)=>a.difficulty-b.difficulty).slice(0,7);
  return sorted.map((k, i) => ({ day: i+1, knowledgeId: k.id, knowledgeName: k.name, reason: `推荐学习“${k.name}”，当前掌握度${(mastery.get(k.id) ?? 50).toFixed(1)}%，且与目标“${goal}”强相关。`, task: `完成${k.name}的核心概念学习与1个练习任务`, resourceType: styleResource[s.learningStyle][i % 3], estimatedTime: `${60 + k.difficulty * 15}分钟` }));
}
export function recommendResources(studentId: string, knowledgeId: string): LearningResource[] {
  const s = students.find(x=>x.id===studentId)!; const mastery = new Map(diagnoseWeakKnowledge(studentId).map(d=>[d.knowledgeId,d.mastery])).get(knowledgeId) ?? 65;
  const style = styleResource[s.learningStyle]; const diffMin = mastery < 70 ? 1 : 3;
  return learningResources.filter(r => r.knowledgeId===knowledgeId).sort((a,b)=> (style.indexOf(a.type)-style.indexOf(b.type)) || (Math.abs(a.difficulty-diffMin)-Math.abs(b.difficulty-diffMin))).slice(0,5);
}
