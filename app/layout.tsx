import './globals.css';import Sidebar from '@/components/layout/sidebar';
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang='zh-CN'><body><div className='flex'><Sidebar/><main className='flex-1 p-6'><div className='mb-4 card'><h2 className='text-xl font-semibold'>面向工程人工智能课程的个性化学习路径规划平台</h2></div>{children}</main></div></body></html>}
