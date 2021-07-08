import tkinter as tk
import tkinter.ttk as ttk
import webbrowser

import requests
from bs4 import BeautifulSoup
from Root import ProgramBase

class PTTCrawler() :
    def __init__(self , board = 'movie'):
        self.domain = 'https://www.ptt.cc'
        self.page = self.domain + '/bbs/{0}/index.html'.format(board)

    def getPosts(self , board) :
        self.page = self.domain + '/bbs/{0}/index.html'.format(board)
        response = requests.get(self.page)
        soup = BeautifulSoup(response.text, 'lxml')

        articles = soup.find_all('div', 'r-ent')
        posts = []
        for article in articles :
            meta = article.find('div', 'title').find('a')
            if not meta :
                continue
            posts.append({
                'title': meta.getText().strip(),
                'link': meta.get('href'),
                'push': article.find('div', 'nrec').getText(),
                'date': article.find('div', 'date').getText(),
                'author': article.find('div', 'author').getText(),
            })
        return posts

    def getPage(self) :
        return self.page

    def getDomain(self):
        return self.domain

class PTTViewer(ProgramBase) :
    postbg = '#ddeedd'
    def __init__(self , root , width = 800 , height = 600) :
        super().__init__(root , width , height)
        self.root.title("PTT Posts")
        self.crawler = PTTCrawler()
        self.posts = []
        self.loadLayout()
    
    def getBoards(self) :
        url = 'https://www.ptt.cc/bbs/hotboards.html'
        urlbase = 'https://www.ptt.cc'

        r = requests.get(url)
        web_content = r.text
        soup = BeautifulSoup(web_content, 'html.parser')

        boardNameElements = soup.find_all('div', class_='board-name')
        boardNames = [e.text for e in boardNameElements] #becomes a  list
        print (boardNames)
        return boardNames

    def showPage(self , board) :
        self.posts = self.crawler.getPosts(board)
        self.root.title("PTT BOARD - " + board.upper())
        self.showMessage(self.crawler.getPage())
        self.showPosts(self.posts)
        

    def loadLayout(self) :
        align_mode = 'nswe'
        padding= 2
        msgHeight = 40
        optHeight = 40
        self.dataWidth = self.root.width
        self.dataHeight = self.root.height - optHeight - msgHeight

        self.divOptions = tk.Frame(self.root,  width=self.dataWidth , height=optHeight)
        self.divOptions.grid(row=0 ,padx=padding, pady=padding, sticky=align_mode)

        self.divData = tk.Frame(self.root,  width=self.dataWidth , height=self.dataHeight ,bg=self.postbg)
        self.divData.grid(row=1, padx=padding, pady=padding, sticky=align_mode)

        self.divMsg = tk.Frame(self.root,  width=self.dataWidth , height=msgHeight , bg='black')
        self.divMsg.grid(row=2, columnspan = 4 ,padx=padding, pady=padding, sticky=align_mode) 

        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.divData.columnconfigure(0, weight=1)
        self.divData.columnconfigure(1, weight=10)
        self.divData.columnconfigure(2, weight=1)
        self.divData.columnconfigure(3, weight=2)

        self.lblMsg = tk.Label(self.divMsg, text='show message here', bg='black', fg='white')
        self.lblMsg.grid(row=0, column=0, sticky='w')

    def showOptions(self , boards):
        padding = 1
        label = tk.Label( self.divOptions,  text=" PTT Board Selection: ")
        label.grid(row=0, column=0, sticky='nswe')

        combobox = ttk.Combobox(self.divOptions, values=boards, width=20 , height = 30)
        combobox.current(0)   # select first one
        combobox.grid(row=0, column=1, columnspan=3, padx=padding, pady=padding) 
        combobox.bind('<<ComboboxSelected>>', self.optSelected)
        
    def showPosts(self , posts):
        padding = 2
        for child in self.divData.winfo_children():
            child.destroy()

        for row in range(len(posts)):
            color = 'black'

            number = tk.Label(self.divData, fg=color, bg=self.postbg, text=posts[row]['push'])
            number.grid(row=row, column = 0 ,padx=padding, pady=padding, sticky='e')
            title = tk.Label(self.divData, fg=color, bg=self.postbg, text=posts[row]['title'])
            title.grid(row=row, column=1, padx=padding, pady=padding, sticky='w')
            date = tk.Label(self.divData, fg=color, bg=self.postbg, text=posts[row]['date'])
            date.grid(row=row, column=2, padx=padding, pady=padding, sticky='w')
            author = tk.Label(self.divData, fg=color, bg=self.postbg, text=posts[row]['author'])
            author.grid(row=row, column=3, padx=padding, pady=padding, sticky='w')
            
            # bind mouse events
            title.bind("<Enter>", self.onEnter)
            title.bind("<Leave>", self.onLeave)
            title.bind("<Button-1>", self.onClick)

    def onEnter(self, event):
        event.widget.config(fg='blue')

    def onLeave(self, event):
        event.widget.config(fg='black')

    def onClick(self , event , row) :
        for i in range(0, len(self.posts)):
            if self.posts[i]['title'] == event.widget['text']:
                link = self.crawer.getDomain() +  self.posts[i]['link']
                webbrowser.open_new(link)

    def optSelected(self , event) :
        print (event.widget.get())
        self.showPage(event.widget.get())

    def showMessage(self, msg):
        self.lblMsg['text'] = msg

if __name__ == '__main__' :
    program = PTTViewer(tk.Tk())
    boards = program.getBoards()
    program.showOptions(boards)
    program.showPage('Gossiping')
    program.run()