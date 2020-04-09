'''点字成诗'''
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import json
import random
import time_limit

LIMIT_TIME = 60


class PoetGame(object):
    '''点字成诗函数'''
    def __init__(self):
        self.question_amount = 10
        self.right_answer = []
        self.answers = []
        self.grade = 0
        self.questions = []
        self.poet_number = []
        self.all_poet = []

    def start(self):
        '''开始游戏。'''
        for i in range(self.question_amount):
            print('当前得分：%u' % self.grade)
            self.get_question(i)
            print('第%u题：' % int(i + 1))
            print('请从以下十二个字中拼凑出一句诗：')
            print(self.questions[i])
            a_threading = time_limit.MyThread(target=self.answer_question)
            a_threading.start()
            a_threading.join()
            if a_threading.get_result() == 0:
                self.answers.append('')
            if self.answers[i] == self.right_answer[i]:
                print('回答正确')
                self.grade += 100/self.question_amount
            else:
                print('回答错误，正确答案为：' + self.right_answer[i])
        self.print_grade()

    @time_limit.limit_decor(LIMIT_TIME)  # 超时设置(s)
    def answer_question(self):
        '''回答问题'''
        print('请输入答案：')
        answer = input()
        self.answers.append(answer)
        return 1

    def get_sentence(self):
        '''获得一个诗句

        #从58000首诗里随机获取题目的代码
        while 1:
            random_poet0 =  random.randint(0, 57999)
            if random_poet0 not in self.poet_number:
                self.poet_number.append(random_poet0)
                break
        random_poet = self.poet_number[len(self.poet_number) - 1]
        address = './poet/poet.song.' + str(int(random_poet // 1000 * 1000)) + '.json'
        with open(address, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
            sentence_amount = len(load_dict[int(random_poet % 1000)]['paragraphs'])
            random_sentence = random.randint(0, sentence_amount - 1)
            sentences = re.findall(r'[\u4E00-\u9FA5]+',
                                  load_dict[int(random_poet % 1000)]['paragraphs'][random_sentence])
            random_sentence = random.randint(0, len(sentences) - 1)
            sentence = sentences[random_sentence]
        self.right_answer.append(sentence)
        words = re.findall(r'[\u4E00-\u9FA5]', sentence)
        self.questions.append(words)
        '''
        address = './poet/tssbs.json' #从唐诗三百首里随机获取题目的代码
        with open(address, 'r', encoding='utf-8') as load_f:
            self.all_poet = json.load(load_f)
        while 1:
            random_poet = random.randint(0, len(self.all_poet) - 1)
            if random_poet not in self.poet_number:
                self.poet_number.append(random_poet)
                break
        sentence_amount = len(self.all_poet[random_poet]['paragraphs'])
        random_sentence = random.randint(0, sentence_amount - 1)
        sentences = re.findall(r'[\u4E00-\u9FA5]+',
                               self.all_poet[self.poet_number[len(self.poet_number) - 1]]['paragraphs'][random_sentence])
        if len(sentences) == 0:
            random_sentence = 0
        else:
            random_sentence = random.randint(0, len(sentences) - 1)
        sentence = sentences[random_sentence]
        self.right_answer.append(sentence)
        words = re.findall(r'[\u4E00-\u9FA5]', sentence)
        self.questions.append(words)

    def get_disturb(self, number, len_question):
        '''获得对诗句进行干扰的汉字

        #随机汉字
        i = 0
        while i < len_disturb:
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xfe)
            val = f'{head:x} {body:x}'
            word = bytes.fromhex(val).decode('gb2312', errors='ignore') #或者用decode('gbk')
            self.questions[number].append(word)
            i += 1
        '''
        len_disturb = 12 - len_question
        while 1:
            random_poet = random.randint(0, len(self.all_poet) - 1)
            if random_poet not in self.poet_number:
                sentence_amount = len(self.all_poet[random_poet]['paragraphs'])
                if sentence_amount != 0:
                    random_sentence = random.randint(0, sentence_amount - 1)
                    sentences = re.findall(r'[\u4E00-\u9FA5]+', self.all_poet[random_poet]['paragraphs'][random_sentence])
                    i = 0
                    while len_disturb > 4:
                        if sentences[0][i] not in self.questions[number]:
                            self.questions[number].append(sentences[0][i])
                            len_disturb -= 1
                        i += 1
                    i = 0
                    while len_disturb > 0:
                        if sentences[1][i] not in self.questions[number]:
                            self.questions[number].append(sentences[1][i])
                            len_disturb -= 1
                        i += 1
                    break

    def get_question(self, number):
        '''获得题目'''
        self.get_sentence()
        self.get_disturb(number, len(self.questions[number]))
        random.shuffle(self.questions[number])

    def print_grade(self):
        '''打印成绩'''
        print('总结：')
        for i in range(len(self.right_answer)):
            if self.answers[i] == self.right_answer[i]:
                print('{0:>2}、回答正确。您的回答：{1}；正确答案：{2}'
                      .format(i + 1, self.answers[i], self.right_answer[i]))
            else:
                print('{0:>2}、回答错误。您的回答：{1}；正确答案：{2}'
                      .format(i + 1, self.answers[i], self.right_answer[i]))
        print('您的总得分为：%s分' % str(self.grade))


if __name__ == '__main__':
    game = PoetGame()
    game.start()
