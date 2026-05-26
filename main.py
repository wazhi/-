from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from py_ai4e.data import students, knowledge_points
from py_ai4e.algorithms import diagnose, diagnosis_text, learning_path, recommend_resources

app=FastAPI(title="AI4E-Learn")
templates=Jinja2Templates(directory="py_ai4e/templates")

def base_ctx():
    return {"students":[s.model_dump() for s in students],"knowledge_points":[k.model_dump() for k in knowledge_points]}

@app.get("/",response_class=HTMLResponse)
def dashboard(request:Request):
    avg=sum(s.averageScore for s in students)/len(students)
    return templates.TemplateResponse(request,"dashboard.html",{"avg":round(avg,1),"high":len([s for s in students if s.riskLevel=='高风险']),"student_count":len(students),"kp_count":len(knowledge_points),**base_ctx()})

@app.get("/students",response_class=HTMLResponse)
def students_page(request:Request,student_id:str="s1"):
    s=next(x for x in students if x.id==student_id)
    return templates.TemplateResponse(request,"students.html",{"selected":s.model_dump(),**base_ctx()})

@app.get("/knowledge-graph",response_class=HTMLResponse)
def kg_page(request:Request,kid:str="k1"):
    k=next(x for x in knowledge_points if x.id==kid)
    return templates.TemplateResponse(request,"knowledge.html",{"selected":k.model_dump(),**base_ctx()})

@app.get("/diagnosis",response_class=HTMLResponse)
def diag_page(request:Request,student_id:str="s1"):
    return templates.TemplateResponse(request,"diagnosis.html",{"diag":diagnose(student_id),"text":diagnosis_text(student_id),"student_id":student_id,**base_ctx()})

@app.get("/recommendation",response_class=HTMLResponse)
def rec_page(request:Request,student_id:str="s1",goal:str="准备期末考试"):
    return templates.TemplateResponse(request,"recommendation.html",{"goal":goal,"student_id":student_id,"items":learning_path(student_id,goal),"goals":["掌握机器学习基础","掌握深度学习基础","完成课程实验","准备期末考试","完成工程项目"],**base_ctx()})

@app.get("/resources",response_class=HTMLResponse)
def resource_page(request:Request,student_id:str="s1",knowledge_id:str="k1"):
    return templates.TemplateResponse(request,"resources.html",{"items":recommend_resources(student_id,knowledge_id),"student_id":student_id,"knowledge_id":knowledge_id,**base_ctx()})

@app.get('/analytics',response_class=HTMLResponse)
def analytics_page(request:Request):
    rows=[]
    for k in knowledge_points:
        ms=[]
        for s in students:
            d={x['knowledgeId']:x['mastery'] for x in diagnose(s.id)}
            ms.append(d.get(k.id,50))
        rows.append({"name":k.name,"avg":round(sum(ms)/len(ms),1)})
    return templates.TemplateResponse(request,'analytics.html',{"rows":rows,**base_ctx()})

@app.get('/ai-modules',response_class=HTMLResponse)
def ai_modules(request:Request):
    return templates.TemplateResponse(request,'ai_modules.html',base_ctx())
