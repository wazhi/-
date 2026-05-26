"use client";
import { useState } from 'react';import { students } from '@/lib/data';import { generateLearningPath } from '@/lib/algorithms';
const goals=['掌握机器学习基础','掌握深度学习基础','完成课程实验','准备期末考试','完成工程项目'];
export default function Rec(){const [id,setId]=useState(students[0].id);const [g,setG]=useState(goals[0]);const path=generateLearningPath(id,g);
return <div className='space-y-4'><div className='card'><h1 className='text-xl font-bold'>个性化路径推荐</h1><div className='flex gap-2 mt-2'><select className='border p-2' value={id} onChange={e=>setId(e.target.value)}>{students.map(s=><option key={s.id} value={s.id}>{s.name}</option>)}</select><select className='border p-2' value={g} onChange={e=>setG(e.target.value)}>{goals.map(x=><option key={x}>{x}</option>)}</select></div></div><div className='grid gap-2'>{path.map(p=><div key={p.day} className='card'><b>Day {p.day} - {p.knowledgeName}</b><p>{p.reason}</p><p>{p.task} | {p.resourceType} | {p.estimatedTime}</p></div>)}</div></div>}
