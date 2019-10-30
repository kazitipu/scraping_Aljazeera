from urllib.request import urlopen
from bs4 import BeautifulSoup

url='https://www.aljazeera.com/'
filepath='html/aj.html'


class WebScraper:
    __url  =''
    __data =''
    __wlog = None
    __soup = None

    def __init__(self, url, wlog):
        self.__url=url
        self.__wlog=wlog

    def retrieve_page(self):
        try:
           page=urlopen(self.__url)
        except Exception as e:
            print(e)
            self.__wlog.report(e)
        else:
            self.__data=page.read()
            if len(self.__data) > 0:
                print('page retrieved succesfully')

    def write_data_as_html(self, filepath=filepath, data=''):
        try:
            with open(filepath, 'wb') as file:
                if data:
                    file.write(data)
                else:
                    file.write(self.__data)
        except Exception as e:
            print(e)
            self.__wlog.report(e)

    def read_data_as_html(self,filepath=filepath):
        try:            
            with open(filepath) as file:
                self.__data = file.read()
        except Exception as e:
            print(e)
            self.__wlog.report(e)

    def change_url(self, url):
        self.__url=url

    def print_data(self):
        print(self.__data)

    def convert_data_to_bs4(self):
        self.__soup=BeautifulSoup(self.__data, 'html.parser')

    def soup_parse_to_simple_html(self):
        news_list=self.__soup.find_all(['h1','h2','h3','h4'])
        news_list2=self.__soup.find('div', class_='grouped-stories-links')
        a_divs= news_list2.find_all('a')
          

        htmltext='''

<html>
    <head>
        <title>simple scraper for aljazeera homepage </title>
    </head>
    <body>
        {NEWS_LINKS}
    </body>
</html>
'''      
        news_links='<ol>'

        for tag in news_list:
            if tag.parent.get('href'):
                link=self.__url+tag.parent.get('href')
                title=tag.string
                news_links += "<li><a href='{}' target='_blank'>{}</a></li>\n".format(link, title)

            try:
                if tag.a is not None:
                    link=self.__url+tag.a['href']
                    title=tag.a.string
                    news_links += "<li><a href='{}' target='_blank'>{}</a></li>\n".format(link, title)
            except KeyError:
                pass
        
           
        for a in a_divs:
            link=self.__url+a['href']
            title=a.string
            news_links += "<li><a href='{}' target='_blank'>{}</a></li>\n".format(link, title)


        news_links += '</ol>'
        htmltext=htmltext.format(NEWS_LINKS=news_links)
        self.write_data_as_html(filepath='html/news.html', data=htmltext.encode())



            
        
