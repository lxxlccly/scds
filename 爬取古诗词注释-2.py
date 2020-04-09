from urllib import  request,error
from bs4 import BeautifulSoup
import re
if __name__ == '__main__':

    url = "https://so.gushiwen.org/gushi/tangshi.aspx"

    try:

        req = request.Request(url)

        rsp = request.urlopen(req)

        html = rsp.read().decode()
        soup=BeautifulSoup(html,'lxml')
        html=soup.prettify()
        div = soup.find_all('a',{'target':'_blank'})
        div = div[1:-1]
        name = div[0].string
        f = open('D:\桌面\诗词库-2-赏析.txt','w+',encoding='utf-8')
        num = 1
        shang_xi = []
        for i in div:
        #     print(i.string)
        #     print(i.get('href'))
            name = i.string
            url = i.get('href')
            req = request.Request('https://so.gushiwen.org'+url)
            rsp = request.urlopen(req)
            html = rsp.read().decode()
            
            soup=BeautifulSoup(html,'lxml')
            html=soup.prettify()
            div2 = soup.findAll('div',{'class':'contyishang'})
            # print(div2[0].text)
            string = re.split(r'[注释]', div2[0].text)
            num2 = 0
            yiwen = []
            for i in string:
                if i == '':
                    num2+=1
                if num2 == 2:
                    break
                yiwen.append(i)
            
            yiwen = ''.join(yiwen)
            # print(yiwen)
            yiwen = re.split(r'[。\n∨译文]', yiwen)
            # print(yiwen)
            yiwen = [i for i in yiwen if i != '']
            yiwen = yiwen[1:]
            yiwen = '。'.join(yiwen)
            print(yiwen)
            f.writelines([str(num),'\n',yiwen,'\n'])
            f.close
            num+=1
            

    except error.URLError as e:
        print("URLError:{0}".format(e.reason))
        print("URLError:{0}".format(e))
       

    except Exception as e:
        print(e)

