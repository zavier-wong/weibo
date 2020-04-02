import requests
import os
import time
from bs4 import BeautifulSoup
import tkinter.messagebox 
import tkinter as tk  # 使用Tkinter前需要先导入

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}
link='https://s.weibo.com/top/summary'
link_head='https://s.weibo.com'

#每日一句
url = "http://open.iciba.com/dsapi/"
r = requests.get(url)
note = r.json()['note']
#实例化object，建立窗口window

window = tk.Tk()

try:
    r=requests.get(link,headers=headers,timeout=20)
    soup=BeautifulSoup(r.text,'lxml')
    movie=soup.find_all('td',class_='td-02')
except:
    tkinter.messagebox.showerror(title='Hi', message='出错了,网络状态不好！')   
    window.destroy()

n=0
home_list=[]
for each in movie:
                
    new=each.a.text.strip()
    if n==0:
     s=('*\t'+str(new))
     home_list.append(s)
    else:
     s=(str(n)+'\t'+str(new))
     home_list.append(s)
    n+=1
        

#给窗口的可视化起名字

date=time.strftime("%Y-%m-%d", time.localtime())+' 微博热搜榜'
window.title(date)


#设定窗口的大小(长 * 宽)

window.geometry('500x300')  # 这里的乘是小x

 

#在图形界面上创建一个标签label用以显示并放置

var1 = tk.StringVar()  # 创建变量，用var1用来接收鼠标点击具体选项的内容

l = tk.Label(window, fg='gray',font=('Arial', 12), textvariable=var1)
var1.set(note)
l.pack()


#创建Listbox并为其添加内容

var2 = tk.StringVar()

#var2.set((1,2,3,4)) # 为变量var2设置值

#垂直滚动条组件
slb = tk.Scrollbar(window)
slb.pack(side="right", fill="y")

# 创建Listbox

lb = tk.Listbox(window,yscrollcommand=slb.set,font=('Arial', 15), width=300,listvariable=var2)  #将var2的值赋给Listbox
slb.config(command=lb.yview)
# 创建一个list并将值循环添加到Listbox控件中

#list_items = [11,22,33,44,111,222,444]

for item in home_list:

    lb.insert('end', item)  # 从最后一个位置开始加入值

#lb.insert(1, 'first')       # 在第一个位置加入'first'字符
#lb.delete(2)                # 删除第二个位置的字符


lb.pack()

#创建一个方法用于按钮的点击事件

def get_string(n):
    global movie
    pl='收起全文d'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}
    link='https://s.weibo.com/top/summary'
    link_head='https://s.weibo.com'
    
    href=movie[n].a.attrs['href']

    r=requests.get(link_head+href,headers=headers,timeout=20)
    soup=BeautifulSoup(r.text,'lxml')
    a=soup.find('div',class_='content')
    a=a.find_all('p',class_='txt')
    return a[-1].text.strip().replace(pl,'')

def content():
    try:
        value = lb.get(lb.curselection())   # 获取当前选中的文本
        try:
                #var1.set(value)  # 为label设置值
                window_sign_up = tk.Toplevel(window)
                window_sign_up.geometry('400x200')
                window_sign_up.title('微博全文')
                #new_name = tk.StringVar()
                #new_name.set('example@python.com')  # 将最初显示定为'example@python.com'
                a=get_string(lb.curselection()[0])
                # height=5表示文本框初始界面是5个字符高度，当然输入时是可以多于5行的。
                t = tk.Text(window_sign_up,font=('Fixdsys', 15),height=10,)
                #t.configure(state='disabled')
                t.insert('insert', a)
                t.pack()        
        except:
                window_sign_up.destroy()
                tkinter.messagebox.showwarning(title='注意', message='这可能是微博广告哦！')

                    
    except:
        tkinter.messagebox.showwarning(title='小贴士', message='请点击标题以查看！')

    


#创建一个按钮并放置，点击按钮调用print_selection函数

b1 = tk.Button(window, font=('Arial', 12),text='查看全文', width=15, height=2, command=content)

b1.pack()
 

# 第8步，主窗口循环显示

window.mainloop()
