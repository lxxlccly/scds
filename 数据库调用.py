import pymysql
import random
import jieba
def CallMySql():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='newbegin', db='lsj', charset='utf8') #改为自己的数据库密码

    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = 'select * from poetry WHERE id = {}'.format(random.randint(1,449))
    cur.execute(sql)
    poetry = cur.fetchall()
    poetry = poetry[0]
    

    poetry = {i:poetry[i] for i in poetry if poetry[i] != 'NULL'}

    poetry_len = int((len(poetry) - 2)/2)
    key = random.randint(1,poetry_len)
    #print(poetry)
    sentence = poetry['sentense_'+str(key)]
    seg_sentence = jieba.cut(sentence, cut_all=False)
    seg_sentence = list(seg_sentence)
    seg_sentence = [i for i in seg_sentence if i !='，']
    key_word = random.choice(seg_sentence)
    
    return key_word,poetry['name'],sentence
def CallMySql2():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='244466666', db='lsj', charset='utf8') #改为自己的数据库密码

    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = 'select * from poetry WHERE id = {}'.format(random.randint(1,449))
    # sql = 'select * from poetry WHERE id = {}'.format(268)
    cur.execute(sql)
    poetry = cur.fetchall()
    poetry = poetry[0]
    poetry = {i:poetry[i] for i in poetry if poetry[i] != 'NULL'}
    poetry_len = 0
    for i in range(10):
        sentence = 'sentense_' + str(i + 1)
        if sentence in poetry:
            poetry_len += 1
    while 1:
        key = random.randint(1,poetry_len)
        if 'sentense_' + str(key) in poetry and 'yiwen_' + str(key) in poetry:
            break

    # return key_word,random_poetry['name'],sentence
    return poetry['yiwen_'+str(key)],poetry['name'],poetry['sentense_'+str(key)]
