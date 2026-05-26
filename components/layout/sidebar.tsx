"use client";
import Link from "next/link";import { usePathname } from "next/navigation";
const menus=[['/','首页总览'],['/students','学生画像'],['/knowledge-graph','知识图谱'],['/diagnosis','学习诊断'],['/recommendation','路径推荐'],['/resources','学习资源'],['/analytics','数据报表'],['/ai-modules','AI模块说明']];
export default function Sidebar(){const p=usePathname();return <aside className='w-56 bg-white border-r min-h-screen p-4'><h1 className='font-bold text-lg text-blue-600 mb-4'>AI4E-Learn</h1><nav className='space-y-1'>{menus.map(([href,name])=><Link key={href} href={href} className={`block px-3 py-2 rounded ${p===href?'bg-blue-100 text-blue-700':'hover:bg-slate-100'}`}>{name}</Link>)}</nav></aside>}
