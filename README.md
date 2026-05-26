# AI4E-Learn：面向工程人工智能课程的个性化学习路径规划平台

## 项目简介
用于课程大作业展示的教学辅助 Web 系统，支持学生画像、知识诊断、学习路径推荐、资源推荐与可视化报表。

## 技术栈
- Next.js App Router + TypeScript + Tailwind CSS
- Recharts 图表
- 本地 mock 数据（`lib/data.ts`）

## 系统功能
- 首页 Dashboard
- 学生画像 `/students`
- 知识图谱 `/knowledge-graph`
- 学习诊断 `/diagnosis`
- 路径推荐 `/recommendation`
- 学习资源 `/resources`
- 数据报表 `/analytics`
- AI 模块说明 `/ai-modules`

## 安装与运行
```bash
npm install
npm run dev
```

## 核心 AI 算法
见 `lib/algorithms.ts`：掌握度计算、诊断文本生成、路径推荐、资源推荐、风险预警。

## 数据可视化
使用 Recharts 展示掌握度柱状图、风险分布饼图、雷达图等。

## 项目亮点
- 可运行原型，支持交互式学生选择/目标选择
- 推荐结果由数据动态计算而非静态写死

## 后续优化
- 接入 FastAPI + sklearn 实现模型化风险预测
- 引入 SQLite 持久化与教师端管理
