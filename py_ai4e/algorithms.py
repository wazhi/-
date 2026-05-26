from .data import knowledge_points, learning_records, learning_resources, students

def calculate_mastery(r):
    normalized=min(r.studyTime/5,1)*100
    penalty=min(r.lastReviewDays/30,1)*100
    return round(0.35*r.quizScore+0.30*r.assignmentScore+0.25*r.practiceAccuracy+0.10*normalized-0.05*penalty,2)

def mastery_level(m):
    return "优秀" if m>=85 else "良好" if m>=70 else "一般" if m>=60 else "薄弱"

def diagnose(student_id):
    rows=[]
    for r in [x for x in learning_records if x.studentId==student_id]:
        k=next(k for k in knowledge_points if k.id==r.knowledgeId)
        m=calculate_mastery(r)
        rows.append({"knowledgeId":k.id,"knowledgeName":k.name,"mastery":m,"level":mastery_level(m)})
    return sorted(rows,key=lambda x:x["mastery"])

def diagnosis_text(student_id):
    d=diagnose(student_id)
    if not d:return "暂无学习记录。"
    weak=[x["knowledgeName"] for x in d if x["mastery"]<60][:2]
    strong=[x["knowledgeName"] for x in sorted(d,key=lambda x:x["mastery"],reverse=True)[:2]]
    return f"该学生在“{'、'.join(strong)}”方面掌握较好，但在“{'、'.join(weak or ['暂无明显薄弱项'])}”方面较弱。建议先补前置再学高阶内容。"

def risk_level(student):
    if student.averageScore>=80 and student.activityScore>=70:return "低风险"
    if student.averageScore>=60 and student.activityScore>=50:return "中风险"
    return "高风险"

goal_map={"掌握机器学习基础":["k3","k4","k5","k6","k7","k8","k13","k14"],"掌握深度学习基础":["k9","k10","k11","k12"],"完成课程实验":["k2","k3","k7","k10","k16"],"准备期末考试":["k1","k2","k4","k5","k9","k12","k13","k14"],"完成工程项目":["k2","k7","k12","k15","k16"]}
style_pref={"理论型":["课件","论文阅读","视频"],"实践型":["代码实验","练习题","视频"],"综合型":["视频","代码实验","课件"]}

def learning_path(student_id,goal):
    s=next(x for x in students if x.id==student_id)
    m={x['knowledgeId']:x['mastery'] for x in diagnose(student_id)}
    selected=set()
    for kid in goal_map.get(goal,goal_map['准备期末考试']):
        k=next(x for x in knowledge_points if x.id==kid)
        if m.get(kid,50)<70:selected.add(kid)
        for pre in k.prerequisites:
            if m.get(pre,50)<70:selected.add(pre)
    ks=sorted([next(x for x in knowledge_points if x.id==i) for i in selected],key=lambda x:x.difficulty)[:7]
    return [{"day":i+1,"knowledgeId":k.id,"knowledgeName":k.name,"reason":f"{k.name}掌握度{m.get(k.id,50):.1f}%且与目标“{goal}”相关。","task":f"学习{k.name}并完成练习","resourceType":style_pref[s.learningStyle][i%3],"estimatedTime":f"{60+k.difficulty*15}分钟"} for i,k in enumerate(ks)]

def recommend_resources(student_id,knowledge_id):
    s=next(x for x in students if x.id==student_id)
    m={x['knowledgeId']:x['mastery'] for x in diagnose(student_id)}.get(knowledge_id,65)
    target=1 if m<70 else 3
    prefs=style_pref[s.learningStyle]
    cand=[r for r in learning_resources if r.knowledgeId==knowledge_id]
    cand.sort(key=lambda r:(prefs.index(r.type) if r.type in prefs else 99,abs(r.difficulty-target)))
    return [r.model_dump() for r in cand[:5]]
