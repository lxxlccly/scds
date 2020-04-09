from urllib import  request,error
from bs4 import BeautifulSoup

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
        f = open('D:\桌面\诗词库2.txt','w+',encoding='utf-8')
        num = 1
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
            div2 = soup.find('div',{'class':'contson'})
            # print(div2.get('content'))
            print(div2.get_text())
            f.writelines([str(num),name,'\n',div2.get_text(),'\n'])
            f.close
            num+=1
            
    except error.URLError as e:
        print("URLError:{0}".format(e.reason))
        print("URLError:{0}".format(e))
       

    except Exception as e:
        print(e)