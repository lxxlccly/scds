from threading import Thread
import json
import re
import random
import datetime
import struct
import hashlib
import base64
import socket
import time
from urllib import parse


class Processing(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.con = connection
        self.isHandleShake = False
        self.masking = 0
        self.payDataLength = 0

    def run(self):
        while True:
            if not self.isHandleShake:
                # 开始握手阶段
                header = self.analyze_req()
                sec_key = header['Sec-WebSocket-Key']
                accept_key = self.generate_accept_key(sec_key)
                response = "HTTP/1.1 101 Switching Protocols\r\n"
                response += "Upgrade: websocket\r\n"
                response += "Connection: Upgrade\r\n"
                response += "Sec-WebSocket-Accept: %s\r\n\r\n" % (accept_key.decode('utf-8'))
                self.con.send(response.encode())
                self.isHandleShake = True
                #print('response:\r\n' + response)
            else:
                # 读取命令阶段
                op_code = self.getOpcode()
                if op_code == 8:
                    self.con.close()
                    break
                self.get_data_length()
                client_data = self.read_client_data()
                client_data = parse.unquote(client_data)
                #print('客户端数据：' + str(client_data))
                # 处理数据
                ans = self.answer(str(client_data))
                ans = parse.quote(ans)
                self.send_data_to_client(ans)

    def analyze_req(self):
        req_data = self.con.recv(1024).decode()
        req_list = req_data.split('\r\n')
        headers = {}
        for reqItem in req_list:
            if ': ' in reqItem:
                unit = reqItem.split(': ')
                headers[unit[0]] = unit[1]
        return headers

    def generate_accept_key(self, sec_key):
        sha1 = hashlib.sha1()
        sha1.update((sec_key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode())
        sha1_result = sha1.digest()
        accept_key = base64.b64encode(sha1_result)
        return accept_key

    def getOpcode(self):
        first8_bit = self.con.recv(1)
        first8_bit = struct.unpack('B', first8_bit)[0]
        op_code = first8_bit & 0b00001111
        return op_code

    def get_data_length(self):
        second8_bit = self.con.recv(1)
        second8_bit = struct.unpack('B', second8_bit)[0]
        masking = second8_bit >> 7
        data_length = second8_bit & 0b01111111
        pay_data_length = 4
        if data_length <= 125:
            pay_data_length = data_length
        elif data_length == 126:
            pay_data_length = struct.unpack('H', self.con.recv(2))[0]
        elif data_length == 127:
            pay_data_length = struct.unpack('Q', self.con.recv(8))[0]
        self.masking = masking
        self.payDataLength = pay_data_length

    def read_client_data(self):
        masking_key = []
        if self.masking == 1:
            masking_key = self.con.recv(4)
        data = self.con.recv(self.payDataLength)
        if self.masking == 1:
            i = 0
            true_data = ''
            for d in data:
                true_data += chr(d ^ masking_key[i % 4])
                i += 1
            return true_data
        else:
            return data

    def send_data_to_client(self, text):
        send_data = struct.pack('!B', 0x81)
        length = len(text)
        if length <= 125:
            send_data += struct.pack('!B', length)
        elif length <= 0xFFFF:
            send_data += struct.pack("!BH", 126, length)
        else:
            send_data += struct.pack("!BQ", 127, length)
        send_data += text.encode('utf-8')
        #print(text.encode('utf-8'))
        self.con.sendall(send_data)

    def answer(self, data):
        data = re.split(r'#', data)
        if data[0] == "00":  #登录
            return self.verify_user(data)
        elif data[0] == "01":  #注册/管理员添加用户
            return self.register(data)
        elif data[0] == "02":  #管理员登录
            return self.charge(data)
        elif data[0] == "03":  #管理员获取用户
            return self.get_users()
        elif data[0] == "04":  #管理员删除用户
            return self.delete_user(data[1])
        elif data[0] == "05": #管理员修改用户账号
            return self.change(data)
        elif data[0] == "06":  #获得出口成诗题目
            return self.say_poet_question()
        elif data[0] == "07":  #出口成诗回答验证
            return self.say_poet_verify(data)
        elif data[0] == "08":  #出口成诗查看答案
            return self.say_poet_answer(data[1])
        elif data[0] == "09":  #保存成绩
            return self.save_grade(data)
        elif data[0] == "10": #查询成绩记录
            return self.find_notes(data[1])
        elif data[0] == "11":  #删除记录
            return self.delete_note(data)
        elif data[0] == "12":  #点字成诗生成题目
            return self.click_poet_question(data)
        elif data[0] == "13":  #你说我猜生成题目
            return self.guess_question(data)
        else:
            return "1"

    def guess_question(self, data):
        '''你说我猜生成题目'''
        del data[1]
        del data[0]
        all_poet = self.get_library('./poet/你说我猜简单.txt')
        all_explain = self.get_library('./poet/你说我猜简单赏析.txt')
        while 1:
            random_poet = random.randint(0, len(all_poet) - 1)
            if str(random_poet) not in data:
                break
        sentence_amount = len(all_poet[random_poet]) - 1
        random_sentence = random.randint(0, sentence_amount - 1)
        print(all_poet[random_poet][random_sentence + 1])
        sentences = re.findall(r'[\u4E00-\u9FA5]+', all_poet[random_poet][random_sentence + 1])
        explains = re.findall(r'[\u4E00-\u9FA5]+', all_explain[random_poet][random_sentence])
        text = str(random_poet) + "/" + str(len(sentences)) + "/"
        for i in range(len(sentences)):
            text += sentences[i]
            text += "/"
        for i in range(len(explains)):
            text += explains[i]
            text += "/"
        return text

    def get_library(self, path):
        '''你说我猜获取库'''
        with open(path, encoding="utf-8") as file:
            content = file.read()
            x = re.findall(r'[（|(](.*?)[）|)]', content)
            for i in x:
                zifu = '(' + i + ')'
                content = content.replace(zifu, '')
            content = re.split(r'\d', content)
            content = [i for i in content if i != '']
            sc_list = []
            for i in content:
                weak_list = re.split(r'[。\n\s*]', i)
                weak_list = [i for i in weak_list if i != '']
                sc_list.append(weak_list)
        return sc_list

    def click_poet_question(self, data):
        '''生成点字成诗题目'''
        del data[1]
        del data[0]
        with open('./poet/点字成诗简单.json', 'r', encoding='utf-8') as load_f:
            all_poet = json.load(load_f)
        while 1:
            random_poet = random.randint(0, len(all_poet) - 1)
            if str(random_poet) not in data:
                data.append(str(random_poet))
                break
        sentence_amount = len(all_poet[random_poet]['paragraphs'])
        random_sentence = random.randint(0, sentence_amount - 1)
        sentences = re.findall(r'[\u4E00-\u9FA5]+', all_poet[random_poet]['paragraphs'][random_sentence])
        if len(sentences) == 0:
            data.pop(-1)
            return self.click_poet_question(data)
        elif len(sentences) == 1:
            random_sentence = 0
        else:
            random_sentence = random.randint(0, len(sentences) - 1)
        right_answer = sentences[random_sentence]
        print(right_answer)
        questions = re.findall(r'[\u4E00-\u9FA5]', right_answer)
        len_disturb = 12 - len(questions)
        while 1:
            random_poet1 = random.randint(0, len(all_poet) - 1)
            if str(random_poet1) not in data:
                sentence_amount = len(all_poet[random_poet1]['paragraphs'])
                if sentence_amount != 0:
                    random_sentence = random.randint(0, sentence_amount - 1)
                    sentences = re.findall(r'[\u4E00-\u9FA5]+', all_poet[random_poet1]['paragraphs'][random_sentence])
                    if len(sentences) > 0:
                        i = 0
                        j = 0
                        while len_disturb != 0:
                            if i >= len(sentences[0]) or j == 4:
                                break
                            if sentences[0][i] not in questions:
                                questions.append(sentences[0][i])
                                len_disturb -= 1
                                j += 1
                            i += 1
                        if len_disturb == 0:
                            break
        random.shuffle(questions)
        text = ""
        for i in range(len(questions)):
            text += questions[i]
        text = text + "/" + right_answer + "/" + str(random_poet)
        return text

    def delete_note(self, data):
        '''删除记录'''
        with open('./userdata/grade.json', 'r', encoding='utf-8') as load_f:
            all_note = json.load(load_f)
        index = -1
        for i in range(len(all_note)):
            if all_note[i]["username"] == data[1]:
                index = i
                break
        if data[2] == "all":
            all_note[index]["grade"].clear()
            notes = json.dumps(all_note, ensure_ascii=False, indent=4)
            with open('./userdata/grade.json', 'w', encoding='utf-8') as f:
                f.write(notes)
            return "删除成功"
        else:
            all_note[index]["grade"].pop(int(data[2]))
            notes = json.dumps(all_note, ensure_ascii=False, indent=4)
            with open('./userdata/grade.json', 'w', encoding='utf-8') as f:
                f.write(notes)
            return "删除成功"

    def find_notes(self, username):
        '''查询成绩记录'''
        with open('./userdata/grade.json', 'r', encoding='utf-8') as load_f:
            all_grade = json.load(load_f)
        if len(all_grade) == 0:
            return "无记录"
        else:
            grades = ""
            for i in range(len(all_grade)):
                if all_grade[i]['username'] == username and len(all_grade[i]['grade']) > 0:
                    for j in range(len(all_grade[i]['grade'])):
                        grades += all_grade[i]['grade'][j]
                        grades += "/"
                    return grades
            return "无记录"

    def save_grade(self, data):
        '''保存成绩'''
        grade = data[2] + "." + str(datetime.datetime.now().year) + "." + str(datetime.datetime.now().month) + "." + str(datetime.datetime.now().day) + "." + data[3]
        with open('./userdata/grade.json', 'r', encoding='utf-8') as load_f:
            all_grade = json.load(load_f)
        if len(all_grade) == 0:
            all_grade.append({'username': data[1], 'grade': [grade]})
            grades = json.dumps(all_grade, ensure_ascii=False, indent=4)
            with open('./userdata/grade.json', 'w', encoding='utf-8') as f:
                f.write(grades)
            return "保存成功"
        else:
            for i in range(len(all_grade)):
                if data[1] == all_grade[i]['username']:
                    all_grade[i]['grade'].append(grade)
                    grades = json.dumps(all_grade, ensure_ascii=False, indent=4)
                    with open('./userdata/grade.json', 'w', encoding='utf-8') as f:
                        f.write(grades)
                    return "保存成功"
            all_grade.append({'username': data[1], 'grade': [grade]})
            grades = json.dumps(all_grade, ensure_ascii=False, indent=4)
            with open('./userdata/grade.json', 'w', encoding='utf-8') as f:
                f.write(grades)
            return "保存成功"

    def say_poet_answer(self, word):
        '''出口成诗查看答案'''
        with open('./poet/tssbs.json', 'r', encoding='utf-8') as load_f:
            all_poet = json.load(load_f)
        text = '08/'
        for i in range(len(all_poet)):
            for j in range(len(all_poet[i]['paragraphs'])):
                if all_poet[i]['chapter'].find(word) != -1 \
                        or all_poet[i]['paragraphs'][j].find(word) != -1:
                    print(all_poet[i]['paragraphs'][j])
                    sentence = re.findall(r'[\u4E00-\u9FA5]+', all_poet[i]['paragraphs'][j])
                    text += sentence[0] + "/" + sentence[1] + "/"
        return text

    def say_poet_verify(self, data):
        '''出口成诗回答验证'''
        with open('./poet/tssbs.json', 'r', encoding='utf-8') as load_f:
            all_poet = json.load(load_f)
        re_answer = re.findall(r'[\u4E00-\u9FA5]+', data[2])
        for i in range(len(all_poet)):
            for j in range(len(all_poet[i]['paragraphs'])):
                if all_poet[i]['chapter'].find(data[1]) != -1 \
                        or all_poet[i]['paragraphs'][j].find(data[1]) != -1:
                    print(all_poet[i]['paragraphs'][j])
                    sentence = re.findall(r'[\u4E00-\u9FA5]+', all_poet[i]['paragraphs'][j])
                    if re_answer == sentence:
                        return "回答正确"
        return "回答错误"

    def say_poet_question(self):
        '''获得出口成诗题目'''
        all_question = []
        with open('./poet/question.txt', encoding="utf-8") as load_question:
            for row in load_question:
                word = row.replace('\n', '').replace('\r', '')
                all_question.append(word)
        questions = []
        while 1:
            random_poet = random.randint(0, len(all_question) - 1)
            if all_question[random_poet] not in questions:
                questions.append(all_question[random_poet])
            if len(questions) == 12:
                break
        str0 = ""
        for i in range(12):
            str0 += questions[i] + "/"
        return str0

    def change(self, data):
        '''管理员修改用户账号名密码'''
        with open('./userdata/username.json', 'r', encoding='utf-8') as load_f:
            all_user = json.load(load_f)
        all_user[int(data[1])-1000]['username'] = data[2]
        all_user[int(data[1])-1000]['password'] = data[3]
        users = json.dumps(all_user, ensure_ascii=False, indent=4)
        with open('./userdata/username.json', 'w', encoding='utf-8') as f:
            f.write(users)
        return "修改成功"

    def delete_user(self, num):
        with open('./userdata/username.json', 'r', encoding='utf-8') as load_f:
            all_user = json.load(load_f)
        username = all_user[int(num)]["username"]
        all_user.pop(int(num))
        users = json.dumps(all_user, ensure_ascii=False, indent=4)
        with open('./userdata/username.json', 'w', encoding='utf-8') as f:
            f.write(users)
        with open('./userdata/grade.json', 'r', encoding='utf-8') as load_f:
            all_grade = json.load(load_f)
        if len(all_grade) > 0:
            for i in range(len(all_grade)):
                if all_grade[i]["username"] == username:
                    all_grade.pop(i)
                    grades = json.dumps(all_grade, ensure_ascii=False, indent=4)
                    with open('./userdata/grade.json', 'w', encoding='utf-8') as f:
                        f.write(grades)
                    break
        return "删除成功"

    def get_users(self):
        with open('./userdata/username.json', 'r', encoding='utf-8') as load_f:
            all_user = json.load(load_f)
        if len(all_user) == 0:
            return "无账号"
        else:
            users = ""
            for i in range(len(all_user)):
                users = users + all_user[i]['username'] + "/" + all_user[i]['password'] + "/"
            return users

    def charge(self, data):
        if data[1] == "liuxinxin" and data[2] == "liuxinxin":
            return "管理员登录成功"
        else:
            return "管理员登录失败"

    def register(self, data):
        with open('./userdata/username.json', 'r', encoding='utf-8') as load_f:
            all_user = json.load(load_f)
        if len(all_user) == 0:
            all_user.append({'username': data[1], 'password': data[2]})
            users = json.dumps(all_user, ensure_ascii=False, indent=4)
            with open('./userdata/username.json', 'w', encoding='utf-8') as f:
                f.write(users)
            return "注册成功，请重新登录"
        else:
            for i in range(len(all_user)):
                if data[1] == all_user[i]['username']:
                    return "用户名已存在"
            all_user.append({'username': data[1], 'password': data[2]})
            users = json.dumps(all_user, ensure_ascii=False, indent=4)
            with open('./userdata/username.json', 'w', encoding='utf-8') as f:
                f.write(users)
            return "注册成功，请重新登录"

    def verify_user(self, data):
        with open('./userdata/username.json', 'r', encoding='utf-8') as load_f:
            all_user = json.load(load_f)
        if len(all_user) == 0:
            return "账号不存在"
        else:
            for i in range(len(all_user)):
                if data[1] == all_user[i]['username']:
                    if data[2] == all_user[i]['password']:
                        return "登录成功"
                    else:
                        return "密码错误"
            return "账号不存在"


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 9999))
    sock.listen(5)
    while True:
        try:
            connection, address = sock.accept()
            Processing(connection).start()
        except:
            time.sleep(1)


if __name__ == "__main__":
    main()