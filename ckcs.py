'''出口成诗'''
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import json
import random
import time_limit

LIMIT_TIME = 60


class PoetGame(object):
    '''出口成诗函数'''
    def __init__(self):
        self.question_amount = 12
        self.unanswered = [1] * self.question_amount
        self.answers = [''] * self.question_amount
        self.grade = 0
        self.questions = []
        self.all_poet = []

    def start(self):
        '''开始游戏'''
        self.get_question()
        self.get_poet_library()
        a_threading = time_limit.MyThread(target=self.cycle)
        a_threading.start()
        a_threading.join()

    @time_limit.limit_decor(LIMIT_TIME)  # 超时设置(s)
    def cycle(self):
        '''回答（循环）'''
        answer_unfinished = 1
        while answer_unfinished:
            for i in range(self.question_amount):
                if self.unanswered[i] == 1:
                    if (i + 1) % 4 == 0:
                        print('{0:>2}、{1}'.format(i + 1, self.questions[i]))
                    else:
                        print('{0:>2}、{1}'.format(i + 1, self.questions[i]), end=' ')
            print('请输入编号选择问题')
            number = input()
            print('请回答：')
            answer = input()
            re_answer = re.findall(r'[\u4E00-\u9FA5]+', answer)
            for i in range(len(self.all_poet)):
                for j in range(len(self.all_poet[i]['paragraphs'])):
                    if self.all_poet[i]['chapter'].find(self.questions[int(number) - 1]) != -1 \
                            or self.all_poet[i]['paragraphs'][j].find(self.questions[int(number) - 1]) != -1:
                        sentence = re.findall(r'[\u4E00-\u9FA5]+', self.all_poet[i]['paragraphs'][j])
                        if re_answer == sentence:
                            self.answers[int(number) - 1] = answer
                            self.unanswered[int(number) - 1] = 0
            if self.unanswered[int(number) - 1] == 0:
                print('回答正确')
            else:
                print('回答错误')
            if self.unanswered == [0] * self.question_amount:
                answer_unfinished = 0
        return 1

    def verification(self, number, answer):
        re_answer = re.findall(r'[\u4E00-\u9FA5]+', answer)
        for i in range(len(self.all_poet)):
            for j in range(len(self.all_poet[i]['paragraphs'])):
                if self.all_poet[i]['chapter'].find(self.questions[number]) != -1 \
                        or self.all_poet[i]['paragraphs'][j].find(self.questions[number]) != -1:
                    sentence = re.findall(r'[\u4E00-\u9FA5]+', self.all_poet[i]['paragraphs'][j])
                    if re_answer == sentence:
                        self.answers[number] = answer
                        self.unanswered[number] = 0
                        return True
        return False

    def get_question(self):
        '''获得题目'''
        all_question = []
        with open('./poet/question.txt', encoding="utf-8") as load_question:
            for row in load_question:
                word = row.replace('\n', '').replace('\r', '')
                all_question.append(word)
        while 1:
            random_poet = random.randint(0, len(all_question) - 1)
            if all_question[random_poet] not in self.questions:
                self.questions.append(all_question[random_poet])
            if len(self.questions) == self.question_amount:
                break

    def get_poet_library(self):
        '''诗词库'''
        address = './poet/tssbs.json'
        with open(address, 'r', encoding='utf-8') as load_f:
            self.all_poet = json.load(load_f)

    def print_grade(self):
        '''打印成绩'''
        print('总结：')
        right_amounts = 0
        for i in range(self.question_amount):
            if self.answers[i] != '':
                print('{0:>2}、回答正确。您的回答为：{1}'.format(i + 1, self.answers[i]))
                right_amounts += 1
            else:
                print('{0:>2}、回答错误/未回答。'.format(i + 1))
        self.grade = right_amounts / self.question_amount * 100
        print('您的总得分为：%.1f分' % self.grade)


if __name__ == '__main__':
    game = PoetGame()
    game.start()
    game.print_grade()
