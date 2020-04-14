'''诗词大赛主程序'''
import time
import re
import tkinter
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import ckcs
import dzcs
import 数据库调用


class GradeInterface(object):
    '''显示答案界面'''
    def __init__(self):
        self.grade_interface = None

    def exit_grade_interface(self):
        '''显示答案界面的退出游戏函数'''
        global is_running
        is_running = False
        self.grade_interface.destroy()

    def run(self, mode, question_amount, answers, right_answer=[]):
        '''显示答案界面的运行函数'''
        right_amounts = 0
        conclusion = '回答情况如下：\n\n'
        for i in range(question_amount):
            if answers[i] != '':
                if mode == 1:
                    right_amounts += 1
                    conclusion += '{0:>2}、回答正确：{1}\n'.format(i + 1, answers[i])
                else:
                    if answers[i] == right_answer[i]:
                        right_amounts += 1
                        conclusion += '{0:>2}、回答正确。\n'.format(i + 1)
                    else:
                        conclusion += '{0:>2}、回答错误。\n'.format(i + 1)
            else:
                conclusion += '{0:>2}、未回答。\n'.format(i + 1)
        grade = right_amounts / question_amount * 100
        score = '您的总得分为：{0:.1f}分'.format(grade)
        self.grade_interface = tkinter.Tk()
        self.grade_interface.title("回答情况总结")
        self.grade_interface.geometry("400x400+500+150")
        img = Image.open("./image/背景5.jpg")
        photo = ImageTk.PhotoImage(img)
        bg_photo = tkinter.Canvas(self.grade_interface, width=400, height=400)
        bg_photo.create_image(250, 300, image=photo)
        if mode == 1:
            bg_photo.create_text(120, 200, text=conclusion, fill='black', font=("宋体", 14))
        if mode == 2 or mode == 3:
            bg_photo.create_text(80, 200, text=conclusion, fill='black', font=("宋体", 16))
        bg_photo.create_text(120, 18, text=score, fill='black', font=("宋体", 18))
        bg_photo.pack()
        exit0 = tkinter.Button(self.grade_interface, text="退出游戏", font=('楷体', 18), bg='springgreen',
                               activebackground='lime', command=self.exit_grade_interface)
        exit0.place(relwidth=0.3, relheight=0.1, relx=0.7, rely=0.9)
        back0 = tkinter.Button(self.grade_interface, text="返回首页", font=('楷体', 18), bg='springgreen',
                               activebackground='lime', command=self.grade_interface.destroy)
        back0.place(relwidth=0.3, relheight=0.1, relx=0, rely=0.9)
        self.grade_interface.protocol("WM_DELETE_WINDOW", self.exit_grade_interface)
        self.grade_interface.mainloop()


class SayPoet(object):
    '''出口成诗游戏'''
    def __init__(self):
        self.time_limit = 120
        self.say_poet_interface = None
        self.say_poet = ckcs.PoetGame()
        self.exiting = 0
        self.right_amount = 0
        self.answering_state = [0] * self.say_poet.question_amount
        self.answer = None

    def run(self):
        '''出口成诗运行函数'''
        global mode_select_interface
        mode_select_interface.destroy()
        self.say_poet.get_question()
        self.say_poet.get_poet_library()
        start_time = time.time()
        while not self.exiting:
            end_time = time.time()
            if end_time - start_time > self.time_limit:
                break
            self.say_poet_display()
            if self.exiting == 1:
                break
            if self.say_poet.unanswered == [0] * self.say_poet.question_amount:
                break
        if self.exiting == 0:
            self.show_grade()

    def word_response(self, index0, index1):
        '''点击单词的响应'''
        index = index0 * 3 + index1
        if self.answering_state[index] == 0:
            for i in range(self.say_poet.question_amount):
                if self.answering_state[i] == 1:
                    self.answering_state[i] = 0
            self.say_poet_interface.destroy()
            self.answering_state[index] = 1

    def say_poet_display(self):
        '''出口成诗界面'''
        background_color = ['skyblue', 'limegreen', 'grey']
        self.say_poet_interface = tkinter.Tk()
        self.say_poet_interface.title("出口成诗")
        self.say_poet_interface.geometry("400x400+500+150")
        img = Image.open("./image/背景5.jpg")
        photo = ImageTk.PhotoImage(img)
        bg_photo = tkinter.Canvas(self.say_poet_interface, width=400, height=400)
        bg_photo.create_image(250, 300, image=photo)
        bg_photo.create_text(150, 290, text='请选词后在下方输入答案：', fill='black', font=("宋体", 18))
        bg_photo.pack()
        p1 = ttk.Progressbar(self.say_poet_interface, mode="determinate")
        p1.place(relwidth=1, relheight=0.02, relx=0, rely=0.01)
        p1["maximum"] = self.say_poet.question_amount
        p1["value"] = self.right_amount
        for i in range(4):
            for j in range(3):
                index = i * 3 + j
                question_button = tkinter.Button(self.say_poet_interface,
                                                 text=self.say_poet.questions[index],
                                                 bg=background_color[self.answering_state[index]],
                                                 font=('楷体', 18),
                                                 command=lambda index0=i, index1=j: self.word_response(index0, index1))
                question_button.place(relwidth=0.3, relheight=0.14, relx=0.025+0.325*j, rely=0.04+0.16*i)
        self.answer = tkinter.Entry(self.say_poet_interface, font=("宋体", 14))
        self.answer.place(relwidth=0.8, relheight=0.1, relx=0, rely=0.78)
        submit_button = tkinter.Button(self.say_poet_interface, text='提交', font=('楷体', 18), bg='springgreen',
                                       activebackground='lime', command=self.submit_response)
        submit_button.place(relwidth=0.18, relheight=0.1, relx=0.81, rely=0.78)
        exit0 = tkinter.Button(self.say_poet_interface, text="退出游戏", font=('楷体', 18), bg='springgreen',
                               activebackground='lime', command=self.exit_say_poet)
        exit0.place(relwidth=0.3, relheight=0.1, relx=0.7, rely=0.9)
        back0 = tkinter.Button(self.say_poet_interface, text="返回首页", font=('楷体', 18), bg='springgreen',
                               activebackground='lime', command=self.back_mode_selection)
        back0.place(relwidth=0.3, relheight=0.1, relx=0, rely=0.9)
        self.say_poet_interface.protocol("WM_DELETE_WINDOW", self.exit_say_poet)
        self.say_poet_interface.mainloop()

    def show_grade(self):
        '''显示回答情况和最终得分'''
        grade_interface = GradeInterface()
        grade_interface.run(1, self.say_poet.question_amount, self.say_poet.answers)

    def submit_response(self):
        '''提交回答并处理'''
        number = 0
        for i in range(self.say_poet.question_amount):
            if self.answering_state[i] == 1:
                number = i
        answers = self.answer.get()
        answer_right = self.say_poet.verification(number, answers)
        if answer_right:
            self.answering_state[number] = 2
            self.right_amount += 1
            messagebox.showinfo(message="回答正确！")
        else:
            messagebox.showinfo(message="回答错误！")
        self.say_poet_interface.destroy()

    def exit_say_poet(self):
        '''出口成诗界面的退出游戏函数'''
        global is_running
        is_running = False
        self.say_poet_interface.destroy()
        self.exiting = 1

    def back_mode_selection(self):
        '''出口成诗界面返回游戏模式选择界面的函数'''
        self.say_poet_interface.destroy()
        self.exiting = 1


class ClickPoet(object):
    def __init__(self):
        self.click_poet_interface = None
        self.click_poet = dzcs.PoetGame()
        self.question_number = 0
        self.exiting = 0
        self.time_limit = 120
        self.answers = [''] * self.click_poet.question_amount
        self.click_state = [0] * 12
        self.right_amount = 0
        self.see_answer = 0

    def run(self):
        '''点字成诗运行函数'''
        global mode_select_interface
        mode_select_interface.destroy()
        start_time = time.time()
        end_time = 0
        for i in range(self.click_poet.question_amount):
            self.see_answer = 0
            self.click_state = [0] * 12
            self.question_number = i
            self.click_poet.get_question(i)
            print(self.click_poet.right_answer[i])
            while not self.exiting:
                end_time = time.time()
                if end_time - start_time > self.time_limit or self.exiting == 1 or self.see_answer == 1 or\
                        len(self.click_poet.right_answer[i]) == len(self.answers[i]):
                    break
                self.click_poet_display()
            if end_time - start_time > self.time_limit or self.exiting == 1:
                break
            if self.answers[i] == self.click_poet.right_answer[i]:
                self.right_amount += 1
        if self.exiting == 0:
            self.show_grade()

    def word_response(self, index0, index1):
        '''字的响应函数'''
        index = index0 * 4 + index1
        if self.click_state[index] == 0:
            self.answers[self.question_number] += self.click_poet.questions[self.question_number][index]
            self.click_state[index] = 1
            self.click_poet_interface.destroy()

    def click_poet_display(self):
        '''点字成诗界面'''
        background_color = ['skyblue', 'grey']
        score = ''
        if self.question_number > 0:
            if self.answers[self.question_number - 1] == self.click_poet.right_answer[self.question_number - 1]:
                score += '上一题回答正确；'
            else:
                score += '上一题回答错误；'
        grade = self.right_amount / self.click_poet.question_amount * 100
        score += '当前得分为：{0:.1f}分'.format(grade)
        self.click_poet_interface = tkinter.Tk()
        self.click_poet_interface.title("点字成诗")
        self.click_poet_interface.geometry("400x400+500+150")
        img = Image.open("./image/背景5.jpg")
        photo = ImageTk.PhotoImage(img)
        bg_photo = tkinter.Canvas(self.click_poet_interface, width=400, height=400)
        bg_photo.create_image(250, 300, image=photo)
        bg_photo.create_text(160, 280, text='请点击上方的字凑成一句诗：', fill='black', font=("宋体", 18))
        bg_photo.create_text(150, 34, text=score, fill='black', font=("宋体", 12))
        bg_photo.pack()
        p1 = ttk.Progressbar(self.click_poet_interface, mode="determinate")
        p1.place(relwidth=1, relheight=0.02, relx=0, rely=0.01)
        p1["maximum"] = self.click_poet.question_amount
        p1["value"] = self.question_number + 1
        next_question = tkinter.Button(self.click_poet_interface, text='下一题', font=('楷体', 18), bg='springgreen',
                                       activebackground='lime', command=self.next_question_response)
        next_question.place(relwidth=0.2, relheight=0.08, relx=0.8, rely=0.04)
        for i in range(3):
            for j in range(4):
                index = i * 4 + j
                word = tkinter.Button(self.click_poet_interface, font=('楷体', 18),
                                      bg=background_color[self.click_state[index]],
                                      text=self.click_poet.questions[self.question_number][index],
                                      activeforeground='green',
                                      command=lambda index0=i, index1=j: self.word_response(index0, index1))
                word.place(relwidth=0.225, relheight=0.15, relx=0.02+0.245*j, rely=0.15+0.17*i)
        see_right_answer = tkinter.Button(self.click_poet_interface, text='查看答案', font=('楷体', 18),
                                          bg='springgreen', activebackground='lime', command=self.show_right_answer)
        see_right_answer.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.9)
        label2 = tkinter.Label(self.click_poet_interface, text=self.answers[self.question_number],
                               font=("宋体", 18), bg='white', anchor='w', justify='left')
        label2.place(relwidth=0.7, relheight=0.1, relx=0.02, rely=0.76)
        delete_button = tkinter.Button(self.click_poet_interface, text='×', font=('楷体', 18), bg='springgreen',
                                       activebackground='lime', command=self.delete_response)
        delete_button.place(relwidth=0.24, relheight=0.1, relx=0.74, rely=0.76)
        exit0 = tkinter.Button(self.click_poet_interface, text="退出游戏", font=('楷体', 18), bg='springgreen',
                               activebackground='lime', command=self.exit_click_poet)
        exit0.place(relwidth=0.3, relheight=0.1, relx=0.7, rely=0.9)
        back0 = tkinter.Button(self.click_poet_interface, text="返回首页", font=('楷体', 18), bg='springgreen',
                               activebackground='lime', command=self.back_mode_selection)
        back0.place(relwidth=0.3, relheight=0.1, relx=0, rely=0.9)
        self.click_poet_interface.protocol("WM_DELETE_WINDOW", self.exit_click_poet)
        self.click_poet_interface.mainloop()

    def show_right_answer(self):
        window = tkinter.Tk()
        window.title('你说我猜')
        window.geometry('500x150+450+200')
        img = Image.open("./image/背景3.jpg")
        photo = ImageTk.PhotoImage(img)
        bg_photo = tkinter.Canvas(self.click_poet_interface, width=400, height=400)
        bg_photo.create_image(350, 163, image=photo)
        bg_photo.pack()
        word_display = tkinter.Label(window, text='来自《' + self.click_poet.poet_name[self.question_number] +
                                                  '》的：' + self.click_poet.right_answer[self.question_number],
                                     bg='green', fg='white', font=('Arial', 12), width=60, height=2)
        word_display.place(relwidth=1, relheight=0.6, relx=0, rely=0.2)
        self.see_answer = 1
        self.click_poet_interface.destroy()

    def next_question_response(self):
        self.see_answer = 1
        self.click_poet_interface.destroy()

    def exit_click_poet(self):
        '''点字成诗界面的退出游戏函数'''
        global is_running
        is_running = False
        self.click_poet_interface.destroy()
        self.exiting = 1

    def back_mode_selection(self):
        '''点字成诗界面返回游戏模式选择界面的函数'''
        self.click_poet_interface.destroy()
        self.exiting = 1

    def delete_response(self):
        '''删除选择的字'''
        if len(self.answers[self.question_number]) > 0:
            string0 = self.answers[self.question_number][len(self.answers[self.question_number]) - 1]
            self.answers[self.question_number] = self.answers[self.question_number][
                                                 0:len(self.answers[self.question_number]) - 1]
            for i in range(12):
                if string0 == self.click_poet.questions[self.question_number][i]:
                    self.click_state[i] = 0
                    break
            self.click_poet_interface.destroy()

    def show_grade(self):
        '''显示回答情况和最终得分'''
        grade_interface = GradeInterface()
        grade_interface.run(2, self.click_poet.question_amount, self.answers, self.click_poet.right_answer)


class YouSayIGuess(object):
    def __init__(self):
        self.guess_interface = None
        self.question_number = 0
        self.exiting = 0
        self.question_amount = 10
        self.questions = []
        self.right_answer = []
        self.time_limit = 120
        self.answers = [''] * self.question_amount
        self.answer = None
        self.right_amount = 0
        self.see_answer = 0

    def run(self):
        '''你说我猜运行函数'''
        global mode_select_interface
        mode_select_interface.destroy()
        start_time = time.time()
        end_time = 0
        for i in range(self.question_amount):
            self.see_answer = 0
            self.question_number = i
            word, name, sentence = 数据库调用.CallMySql2()  # 这里用方法给word name sentence赋值即可
            print(sentence)
            self.questions.append(word)
            self.right_answer.append([name, sentence])
            while not self.exiting:
                end_time = time.time()
                if end_time - start_time > self.time_limit or self.exiting == 1 or self.see_answer == 1 or \
                        len(self.right_answer[i]) == len(self.answers[i]):
                    break
                self.guess_display()
            if end_time - start_time > self.time_limit or self.exiting == 1:
                break
            if re.findall(r'[\u4E00-\u9FA5]+', self.answers[i]) == re.findall(r'[\u4E00-\u9FA5]+',
                                                                              self.right_answer[i][1]):
                self.right_amount += 1
        if self.exiting == 0:
            self.show_grade()

    def guess_display(self):
        '''你说我猜界面'''
        score = ''
        if self.question_number > 0:
            if re.findall(r'[\u4E00-\u9FA5]+', self.answers[self.question_number - 1]) == re.findall(
                    r'[\u4E00-\u9FA5]+', self.right_answer[self.question_number - 1][1]):
                score += '上一题回答正确；'
            else:
                score += '上一题回答错误；'
        grade = self.right_amount / self.question_amount * 100
        score += '当前得分为：{0:.1f}分'.format(grade)
        self.guess_interface = tkinter.Tk()
        self.guess_interface.title("你说我猜")
        self.guess_interface.geometry("400x400+500+150")
        img = Image.open("./image/背景5.jpg")
        photo = ImageTk.PhotoImage(img)
        bg_photo = tkinter.Canvas(self.guess_interface, width=400, height=400)
        bg_photo.create_image(250, 300, image=photo)
        bg_photo.create_text(150, 34, text=score, fill='black', font=("宋体", 12))
        bg_photo.create_text(170, 260, text='请猜出上方内容所描述的诗句：', fill='black', font=("宋体", 18))
        bg_photo.pack()
        p1 = ttk.Progressbar(self.guess_interface, mode="determinate")
        p1.place(relwidth=1, relheight=0.02, relx=0, rely=0.01)
        p1["maximum"] = self.question_amount
        p1["value"] = self.question_number + 1
        label2 = tkinter.Label(self.guess_interface, text='译文：' + self.questions[self.question_number],
                               font=("宋体", 14), wraplength=360, bg='lightsteelblue')
        label2.place(relwidth=1, relheight=0.3, relx=0, rely=0.2)
        next_question = tkinter.Button(self.guess_interface, text='下一题', font=('楷体', 18), bg='springgreen',
                                       activebackground='lime', command=self.next_question_response)
        next_question.place(relwidth=0.2, relheight=0.08, relx=0.8, rely=0.04)
        self.answer = tkinter.Entry(self.guess_interface, font=("宋体", 14))
        self.answer.place(relwidth=0.7, relheight=0.1, relx=0, rely=0.7)
        submit_button = tkinter.Button(self.guess_interface, text='提交', font=('楷体', 18), bg='springgreen',
                                       activebackground='lime', command=self.submit_response)
        submit_button.place(relwidth=0.28, relheight=0.1, relx=0.71, rely=0.7)
        see_right_answer = tkinter.Button(self.guess_interface, text='查看答案', font=('楷体', 18), bg='springgreen',
                                          activebackground='lime', command=self.show_right_answer)
        see_right_answer.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.9)
        exit0 = tkinter.Button(self.guess_interface, text="退出游戏", font=('楷体', 18), bg='springgreen',
                               activebackground='lime', command=self.exit_guess)
        exit0.place(relwidth=0.3, relheight=0.1, relx=0.7, rely=0.9)
        back0 = tkinter.Button(self.guess_interface, text="返回首页", font=('楷体', 18), bg='springgreen',
                               activebackground='lime', command=self.back_mode_selection)
        back0.place(relwidth=0.3, relheight=0.1, relx=0, rely=0.9)
        self.guess_interface.protocol("WM_DELETE_WINDOW", self.exit_guess)
        self.guess_interface.mainloop()

    def show_grade(self):
        '''显示回答情况和最终得分'''
        grade_interface = GradeInterface()
        grade_interface.run(3, self.question_amount, self.answers, self.right_answer)

    def next_question_response(self):
        self.see_answer = 1
        self.guess_interface.destroy()

    def show_right_answer(self):
        window = tkinter.Tk()
        window.title('你说我猜')
        window.geometry('500x150+450+200')
        word_display = tkinter.Label(window, text='来自《' + self.right_answer[self.question_number][0] +
                                                  '》的：' + self.right_answer[self.question_number][1],
                                     bg='green', fg='white', font=('Arial', 12), wraplength=360)
        word_display.place(relwidth=1, relheight=0.6, relx=0, rely=0.2)
        self.see_answer = 1
        self.guess_interface.destroy()

    def exit_guess(self):
        '''你说我猜界面的退出游戏函数'''
        global is_running
        is_running = False
        self.guess_interface.destroy()
        self.exiting = 1

    def back_mode_selection(self):
        '''你说我猜界面返回游戏模式选择界面的函数'''
        self.guess_interface.destroy()
        self.exiting = 1

    def submit_response(self):
        '''提交回答并处理'''
        answer1 = self.answer.get()
        self.answers[self.question_number] = answer1
        self.see_answer = 1
        self.guess_interface.destroy()


class ModeSelection(object):
    '''诗词大赛游戏'''
    def start(self):
        '''开始游戏'''
        global is_running
        while is_running:
            self.selection()

    def selection(self):
        '''模式选择界面'''
        saying_poet = SayPoet()
        clicking_poet = ClickPoet()
        you_say_i_guess = YouSayIGuess()
        global is_running, mode_select_interface
        if is_running:
            mode_select_interface = tkinter.Tk()
            mode_select_interface.title("游戏模式选择")
            mode_select_interface.geometry("400x400+500+150")
            img = Image.open("./image/背景3.jpg")
            photo = ImageTk.PhotoImage(img)
            bg_photo = tkinter.Canvas(mode_select_interface, width=400, height=400)
            bg_photo.create_image(350, 163, image=photo)
            bg_photo.pack()
            mode1 = tkinter.Button(mode_select_interface, text="出口成诗", font=('楷体', 18), bg='skyblue',
                                   activebackground='limegreen', command=saying_poet.run)
            mode1.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.15)
            mode2 = tkinter.Button(mode_select_interface, text="点字成诗", font=('楷体', 18), bg='skyblue',
                                   activebackground='limegreen', command=clicking_poet.run)
            mode2.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.35)
            mode3 = tkinter.Button(mode_select_interface, text="你说我猜", font=('楷体', 18), bg='skyblue',
                                   activebackground='limegreen', command=you_say_i_guess.run)
            mode3.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.55)
            exit0 = tkinter.Button(mode_select_interface, text="退出游戏", font=('楷体', 18), bg='skyblue',
                                   activebackground='limegreen', command=self.exit_mode_select)
            exit0.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.75)
            mode_select_interface.protocol("WM_DELETE_WINDOW", self.exit_mode_select)
            mode_select_interface.mainloop()

    def exit_mode_select(self):
        '''模式选择界面的退出游戏函数'''
        global mode_select_interface, is_running
        is_running = False
        mode_select_interface.destroy()


if __name__ == '__main__':
    mode_select_interface = None
    is_running = True
    game = ModeSelection()
    game.start()
    print('游戏结束')
