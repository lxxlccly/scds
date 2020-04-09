import pymysql
import random
import jieba
def CallMySql():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='newbegin', db='lsj', charset='utf8') #改为自己的数据库密码

    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = 'select * from poetry WHERE id = {}'.format(random.randint(1,129))
    cur.execute(sql)
    poetry = cur.fetchall()
    poetry = poetry[0]
    

    poetry = {i:poetry[i] for i in poetry if poetry[i] != 'NULL'}

    poetry_len = int((len(poetry) - 2)/2)
    key = random.randint(1,poetry_len)
    print(poetry)
    sentence = poetry['sentence_'+str(key)]
    seg_sentence = jieba.cut(sentence, cut_all=False)
    seg_sentence = list(seg_sentence)
    seg_sentence = [i for i in seg_sentence if i !='，']
    key_word = random.choice(seg_sentence)
    
    return key_word,poetry['name'],sentence
def CallMySql2():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='newbegin', db='lsj', charset='utf8') #改为自己的数据库密码

    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = 'select * from poetry WHERE id = {}'.format(random.randint(1,129))
    # sql = 'select * from poetry WHERE id = {}'.format(268)
    cur.execute(sql)
    poetry = cur.fetchall()
    poetry = poetry[0]
    # print(poetry)
    poetry = {i:poetry[i] for i in poetry if poetry[i] != 'NULL'}
    print(poetry)
    poetry_len = int((len(poetry) - 2)/2)
    key = random.randint(1,poetry_len)

    # return key_word,random_poetry['name'],sentence
    return poetry['sentence_'+str(key)],poetry['name'],poetry['sentence_'+str(key)]
