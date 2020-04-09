'''诗词大赛主程序'''
import time
import tkinter
import ckcs
import dzcs
import 数据库调用


class SayPoet(object):
    '''出口成诗游戏'''
    def __init__(self):
        self.time_limit = 120
        self.say_poet_interface = None
        self.say_poet = ckcs.PoetGame()
        self.exiting = 0
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
        background_color = ['skyblue', 'green', 'grey']
        self.say_poet_interface = tkinter.Tk()
        self.say_poet_interface.title("出口成诗")
        self.say_poet_interface.geometry("400x400+500+150")
        for i in range(4):
            for j in range(3):
                index = i * 3 + j
                question_button = tkinter.Button(self.say_poet_interface,
                                                 text=self.say_poet.questions[index],
                                                 bg=background_color[self.answering_state[index]],
                                                 font=('楷体', 18),
                                                 activeforeground='green',
                                                 command=lambda index0=i, index1=j: self.word_response(index0, index1))
                question_button.place(relwidth=0.3, relheight=0.1, relx=0+0.35*j, rely=0.02+0.12*i)
        label = tkinter.Label(self.say_poet_interface, text="请输入答案：", font=("宋体", 18))
        label.place(relwidth=0.37, relheight=0.1, relx=0, rely=0.5)
        self.answer = tkinter.Entry(self.say_poet_interface, font=("宋体", 14))
        self.answer.place(relwidth=0.8, relheight=0.1, relx=0, rely=0.6)
        submit_button = tkinter.Button(self.say_poet_interface,
                                       text='提交',
                                       font=('楷体', 18),
                                       activeforeground='green',
                                       command=self.submit_response)
        submit_button.place(relwidth=0.18, relheight=0.1, relx=0.81, rely=0.6)
        exit0 = tkinter.Button(self.say_poet_interface, text="退出游戏", font=('楷体', 18),
                               activeforeground='red', command=self.exit_say_poet)
        exit0.place(relwidth=0.3, relheight=0.1, relx=0.7, rely=0.9)
        back0 = tkinter.Button(self.say_poet_interface, text="返回首页", font=('楷体', 18),
                               activeforeground='red', command=self.back_mode_selection)
        back0.place(relwidth=0.3, relheight=0.1, relx=0, rely=0.9)
        self.say_poet_interface.protocol("WM_DELETE_WINDOW", self.exit_say_poet)
        self.say_poet_interface.mainloop()

    def show_grade(self):
        '''显示回答情况和最终得分'''
        right_amounts = 0
        conclusion = ''
        for i in range(self.say_poet.question_amount):
            if self.say_poet.answers[i] != '':
                right_amounts += 1
                conclusion += '{0:>2}、回答正确：{1}\n'.format(i + 1, self.say_poet.answers[i])
            else:
                conclusion += '{0:>2}、回答错误/未回答。\n'.format(i + 1)
        self.say_poet.grade = right_amounts / self.say_poet.question_amount * 100
        score = '您的总得分为：{0:.1f}分'.format(self.say_poet.grade)
        self.say_poet_interface = tkinter.Tk()
        self.say_poet_interface.title("回答情况总结")
        self.say_poet_interface.geometry("400x400+500+150")
        label = tkinter.Label(self.say_poet_interface, text=conclusion,
                              font=("宋体", 12), anchor='w', justify='left')
        label.place(relwidth=1, relheight=0.55, relx=0, rely=0.05)
        label2 = tkinter.Label(self.say_poet_interface, text=score, font=("宋体", 18), anchor='w')
        label2.place(relwidth=1, relheight=0.1, relx=0, rely=0.65)
        exit0 = tkinter.Button(self.say_poet_interface, text="退出游戏", font=('楷体', 18),
                               activeforeground='red', command=self.exit_say_poet)
        exit0.place(relwidth=0.3, relheight=0.1, relx=0.7, rely=0.85)
        back0 = tkinter.Button(self.say_poet_interface, text="返回首页", font=('楷体', 18),
                               activeforeground='red', command=self.back_mode_selection)
        back0.place(relwidth=0.3, relheight=0.1, relx=0, rely=0.85)
        self.say_poet_interface.protocol("WM_DELETE_WINDOW", self.exit_say_poet)
        self.say_poet_interface.mainloop()

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
        self.click_poet_interface = tkinter.Tk()
        self.click_poet_interface.title("点字成诗")
        self.click_poet_interface.geometry("400x400+500+150")
        if self.question_number > 0:
            if self.answers[self.question_number - 1] == self.click_poet.right_answer[self.question_number - 1]:
                label0 = tkinter.Label(self.click_poet_interface, text='上一题回答正确', font=("宋体", 12), bg='green')
            else:
                label0 = tkinter.Label(self.click_poet_interface, text='上一题回答错误', font=("宋体", 12), bg='red')
            label0.place(relwidth=0.49, relheight=0.08, relx=0, rely=0.01)
        grade = self.right_amount / self.click_poet.question_amount * 100
        score = '当前得分为：{0:.1f}分'.format(grade)
        label2 = tkinter.Label(self.click_poet_interface, text=score, font=("宋体", 12))
        label2.place(relwidth=0.49, relheight=0.08, relx=0.51, rely=0.01)
        for i in range(3):
            for j in range(4):
                index = i * 4 + j
                word = tkinter.Button(self.click_poet_interface, font=('楷体', 18),
                                      bg=background_color[self.click_state[index]],
                                      text=self.click_poet.questions[self.question_number][index],
                                      activeforeground='green',
                                      command=lambda index0=i, index1=j: self.word_response(index0, index1))
                word.place(relwidth=0.1, relheight=0.1, relx=0.12+0.22*j, rely=0.1+0.2*i)
        label = tkinter.Label(self.click_poet_interface, text="请点击上方的字进行回答：", font=("宋体", 18))
        label.place(relwidth=0.7, relheight=0.1, relx=0, rely=0.65)
        see_right_answer = tkinter.Button(self.click_poet_interface, text='查看答案', font=('楷体', 18),
                                          activeforeground='red', command=self.show_right_answer)
        see_right_answer.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.9)
        label2 = tkinter.Label(self.click_poet_interface, text=self.answers[self.question_number],
                               font=("宋体", 18), bg='white', anchor='w', justify='left')
        label2.place(relwidth=0.7, relheight=0.1, relx=0.05, rely=0.76)
        delete_button = tkinter.Button(self.click_poet_interface, text='×', font=('楷体', 18),
                                       activeforeground='red', command=self.delete_response)
        delete_button.place(relwidth=0.1, relheight=0.1, relx=0.85, rely=0.76)
        exit0 = tkinter.Button(self.click_poet_interface, text="退出游戏", font=('楷体', 18),
                               activeforeground='red', command=self.exit_click_poet)
        exit0.place(relwidth=0.3, relheight=0.1, relx=0.7, rely=0.9)
        back0 = tkinter.Button(self.click_poet_interface, text="返回首页", font=('楷体', 18),
                               activeforeground='red', command=self.back_mode_selection)
        back0.place(relwidth=0.3, relheight=0.1, relx=0, rely=0.9)
        self.click_poet_interface.protocol("WM_DELETE_WINDOW", self.exit_click_poet)
        self.click_poet_interface.mainloop()

    def show_right_answer(self):
        window = tkinter.Tk()
        window.title('你说我猜')
        window.geometry('500x150+450+200')
        word_display = tkinter.Label(window, text='来自《' + self.click_poet.poet_name[self.question_number] +
                                                  '》的：' + self.click_poet.right_answer[self.question_number],
                                     bg='green', fg='white', font=('Arial', 12), width=60, height=2)
        word_display.place(relwidth=1, relheight=0.6, relx=0, rely=0.2)
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
        conclusion = ''
        for i in range(self.click_poet.question_amount):
            if self.answers[i] == '':
                conclusion += '{0:>2}、未回答。\n'.format(i + 1)
            else:
                if self.answers[i] == self.click_poet.right_answer[i]:
                    conclusion += '{0:>2}、回答正确。\n'.format(i + 1)
                else:
                    conclusion += '{0:>2}、回答错误。\n'.format(i + 1)
        grade = self.right_amount / self.click_poet.question_amount * 100
        score = '您的总得分为：{0:.1f}分'.format(grade)
        self.click_poet_interface = tkinter.Tk()
        self.click_poet_interface.title("回答情况总结")
        self.click_poet_interface.geometry("400x400+500+150")
        label = tkinter.Label(self.click_poet_interface, text=conclusion,
                              font=("宋体", 14), anchor='w', justify='left')
        label.place(relwidth=1, relheight=0.55, relx=0, rely=0.05)
        label2 = tkinter.Label(self.click_poet_interface, text=score, font=("宋体", 18), anchor='w')
        label2.place(relwidth=1, relheight=0.1, relx=0, rely=0.65)
        exit0 = tkinter.Button(self.click_poet_interface, text="退出游戏", font=('楷体', 18),
                               activeforeground='red', command=self.exit_click_poet)
        exit0.place(relwidth=0.3, relheight=0.1, relx=0.7, rely=0.85)
        back0 = tkinter.Button(self.click_poet_interface, text="返回首页", font=('楷体', 18),
                               activeforeground='red', command=self.back_mode_selection)
        back0.place(relwidth=0.3, relheight=0.1, relx=0, rely=0.85)
        self.click_poet_interface.protocol("WM_DELETE_WINDOW", self.exit_click_poet)
        self.click_poet_interface.mainloop()


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
            self.questions.append(word)
            self.right_answer.append(name)
            while not self.exiting:
                end_time = time.time()
                if end_time - start_time > self.time_limit or self.exiting == 1 or self.see_answer == 1 or \
                        len(self.right_answer[i]) == len(self.answers[i]):
                    break
                self.guess_display()
            if end_time - start_time > self.time_limit or self.exiting == 1:
                break
            if self.answers[i] == self.right_answer[i]:
                self.right_amount += 1
        if self.exiting == 0:
            self.show_grade()

    def guess_display(self):
        '''你说我猜界面'''
        self.guess_interface = tkinter.Tk()
        self.guess_interface.title("你说我猜")
        self.guess_interface.geometry("400x400+500+150")
        if self.question_number > 0:
            if self.answers[self.question_number - 1] == self.right_answer[self.question_number - 1]:
                label0 = tkinter.Label(self.guess_interface, text='上一题回答正确', font=("宋体", 12), bg='green')
            else:
                label0 = tkinter.Label(self.guess_interface, text='上一题回答错误', font=("宋体", 12), bg='red')
            label0.place(relwidth=0.49, relheight=0.08, relx=0, rely=0.01)
        grade = self.right_amount / self.question_amount * 100
        score = '当前得分为：{0:.1f}分'.format(grade)
        label1 = tkinter.Label(self.guess_interface, text=score, font=("宋体", 12))
        label1.place(relwidth=0.49, relheight=0.08, relx=0.51, rely=0.01)
        label2 = tkinter.Label(self.guess_interface, text=self.questions[self.question_number],
                               font=("宋体", 18), wraplength=360)
        label2.place(relwidth=1, relheight=0.3, relx=0, rely=0.2)
        label3 = tkinter.Label(self.guess_interface, text="猜出上方诗句的题目：", font=("宋体", 18))
        label3.place(relwidth=0.7, relheight=0.1, relx=0, rely=0.6)
        self.answer = tkinter.Entry(self.guess_interface, font=("宋体", 14))
        self.answer.place(relwidth=0.7, relheight=0.1, relx=0, rely=0.7)
        submit_button = tkinter.Button(self.guess_interface, text='提交', font=('楷体', 18),
                                       activeforeground='green', command=self.submit_response)
        submit_button.place(relwidth=0.3, relheight=0.1, relx=0.7, rely=0.7)
        see_right_answer = tkinter.Button(self.guess_interface, text='查看答案', font=('楷体', 18),
                                          activeforeground='red', command=self.show_right_answer)
        see_right_answer.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.9)
        exit0 = tkinter.Button(self.guess_interface, text="退出游戏", font=('楷体', 18),
                               activeforeground='red', command=self.exit_guess)
        exit0.place(relwidth=0.3, relheight=0.1, relx=0.7, rely=0.9)
        back0 = tkinter.Button(self.guess_interface, text="返回首页", font=('楷体', 18),
                               activeforeground='red', command=self.back_mode_selection)
        back0.place(relwidth=0.3, relheight=0.1, relx=0, rely=0.9)
        self.guess_interface.protocol("WM_DELETE_WINDOW", self.exit_guess)
        self.guess_interface.mainloop()

    def show_grade(self):
        '''显示回答情况和最终得分'''
        conclusion = ''
        for i in range(self.question_amount):
            if self.answers[i] == '':
                conclusion += '{0:>2}、未回答。\n'.format(i + 1)
            else:
                if self.answers[i] == self.right_answer[i]:
                    conclusion += '{0:>2}、回答正确。\n'.format(i + 1)
                else:
                    conclusion += '{0:>2}、回答错误。\n'.format(i + 1)
        grade = self.right_amount / self.question_amount * 100
        score = '您的总得分为：{0:.1f}分'.format(grade)
        self.guess_interface = tkinter.Tk()
        self.guess_interface.title("回答情况总结")
        self.guess_interface.geometry("400x400+500+150")
        label = tkinter.Label(self.guess_interface, text=conclusion,
                              font=("宋体", 14), anchor='w', justify='left')
        label.place(relwidth=1, relheight=0.55, relx=0, rely=0.05)
        label2 = tkinter.Label(self.guess_interface, text=score, font=("宋体", 18), anchor='w')
        label2.place(relwidth=1, relheight=0.1, relx=0, rely=0.65)
        exit0 = tkinter.Button(self.guess_interface, text="退出游戏", font=('楷体', 18),
                               activeforeground='red', command=self.exit_guess)
        exit0.place(relwidth=0.3, relheight=0.1, relx=0.7, rely=0.85)
        back0 = tkinter.Button(self.guess_interface, text="返回首页", font=('楷体', 18),
                               activeforeground='red', command=self.back_mode_selection)
        back0.place(relwidth=0.3, relheight=0.1, relx=0, rely=0.85)
        self.guess_interface.protocol("WM_DELETE_WINDOW", self.exit_guess)
        self.guess_interface.mainloop()

    def show_right_answer(self):
        window = tkinter.Tk()
        window.title('你说我猜')
        window.geometry('500x150+450+200')
        word_display = tkinter.Label(window, text='来自《' + self.right_answer[self.question_number] +
                                                  '》的：' + self.questions[self.question_number],
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
            mode1 = tkinter.Button(mode_select_interface, text="出口成诗", font=('楷体', 18),
                                   activeforeground='blue', command=saying_poet.run)
            mode1.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.15)
            mode2 = tkinter.Button(mode_select_interface, text="点字成诗", font=('楷体', 18),
                                   activeforeground='blue', command=clicking_poet.run)
            mode2.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.35)
            mode3 = tkinter.Button(mode_select_interface, text="你说我猜", font=('楷体', 18),
                                   activeforeground='blue', command=you_say_i_guess.run)
            mode3.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.55)
            exit0 = tkinter.Button(mode_select_interface, text="退出游戏", font=('楷体', 18),
                                   activeforeground='red', command=self.exit_mode_select)
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
