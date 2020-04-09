import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox

import sys  
import re   
import random
from random import randrange
import os,time
import 数据库调用

window = tk.Tk()

window.title('诗词游戏')

window.geometry('400x150') 
buttons = []
neirong = []

def des(index,n):
    window = tk.Tk()
    window.title('你说我猜')
    window.geometry('500x150')
    var=n[0]
    word_display = tk.Label(window, text=var, bg='green', fg='white', font=('Arial', 12), width=60, height=2)
    word_display.place(x=250,y=75,anchor='s')
    answer_button = tk.Button(window,text='点击查看答案', font=('Arial', 12), width=10, height=1, command=lambda :word_display.config(text='来自《'+n[1]+'》的：'+n[2]))
    answer_button.place(x=250,y=120,anchor='s')

def game_1():
    game_choice_1.destroy()
    game_choice_2.destroy()
    buttons = []
    neirong = []
    refresh_button = tk.Button(window, text='换一批', font=('Arial', 12), width=10, height=1, command=game_1)
    refresh_button.place(x=200,y=140,anchor='s')
    for i in range(3):
        
        for j in range(4):
            index = j+i*4
            word,name,sentence =  数据库调用.CallMySql()#这里用方法给word name sentence赋值即可
            sc_list = [word, name, sentence]
            neirong.append(sc_list)
            n = neirong[index]
            c = tk.Button(window, text=word, font=('Arial', 12), width=10, height=1, command=lambda index=index,n=n:des(index,n))
            c.grid(row=i, column=j, padx=1, pady=1, ipadx=1, ipady=1)
            buttons.append(c)
def game_2():
    game_choice_1.destroy()
    game_choice_2.destroy()
    buttons = []
    neirong = []
    refresh_button = tk.Button(window, text='换一批', font=('Arial', 12), width=10, height=1, command=game_2)
    refresh_button.place(x=200,y=140,anchor='s')
    for i in range(3):
        
        for j in range(4):
            index = j+i*4
            word,name,sentence =  数据库调用.CallMySql2()#这里用方法给word name sentence赋值即可
            sc_list = [word, name, sentence]
            neirong.append(sc_list)
            n = neirong[index]
            print(word)
            c = tk.Button(window, text=word, font=('Arial', 12), width=10, height=1, command=lambda index=index,n=n:des(index,n))
            c.grid(row=i, column=j, padx=1, pady=1, ipadx=1, ipady=1)
            buttons.append(c)

def choice():
    b.destroy()
    game_choice_1.place(x=200,y=60, anchor='s')
    game_choice_2.place(x=200,y=120, anchor='s')
    
            
b = tk.Button(window, text='进入游戏', font=('Arial', 12), width=10, height=1, command=choice)
b.place(x=200, y=70, anchor='s')
game_choice_1 = tk.Button(window, text='出口成诗', font=('Arial', 12), width=10, height=1, command=game_1)
game_choice_2 = tk.Button(window, text='你说我猜', font=('Arial', 12), width=10, height=1, command=game_2)
window.mainloop()
