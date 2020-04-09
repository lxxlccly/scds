import sys  
import re  
import os,time
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='newbegin',db='lsj',charset='utf8')
cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

class WordCreate():
    def __init__(self,path):
        '''
        导入文件进行解析
        '''
        with open(path,encoding="utf-8") as file:
            content = file.read()
            
            x = re.findall(r'[（|(](.*?)[）|)]', content)
            print(x)
            for i in x:
                zifu = '('+i+')'
                content = content.replace(zifu,'')
                
            content = re.split(r'\d', content)
            content = [i for i in content if i != '']
            self.sc_list = []
            for i in content:
                weak_list = re.split(r'[、。；！？\n\s*]',i)
                weak_list = [i for i in weak_list if i != '']
                self.sc_list.append(weak_list)
        # print(self.sc_list)
    def OperationSql(self):
        num=130
        for i in self.sc_list:
            for _ in range(62-len(i)):  #导入诗词为62 导入赏析为61
                i.append('NULL')
                # print(len(i))
            
            num2 = 1
            for _ in range(61):
                sql = "UPDATE poetry SET yiwen_{}='{}' WHERE id ={}".format(num2, i[num2-1], num)
                print(sql)
                cur.execute(sql)
                num2 += 1
            # for _ in range(61):
            #     sql = "UPDATE poetry SET sentense_{}='{}' WHERE id ={}".format(num2, i[num2], num)
            #     print(sql)
            #     cur.execute(sql)
            #     num2 += 1
            conn.commit()
            num+=1
def main():
    
    generator = WordCreate('D:\桌面\诗词库-2-赏析.txt')  #选择合适的路径
    generator.OperationSql()
    
    
if __name__ == '__main__':
    main()