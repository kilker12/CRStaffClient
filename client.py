from Tkinter import *
from ttk import *
import socket
import sys

class ClientSock():
    loggedinusername = None
    sock = None
    root = None
    secukey = None
    status = None
    def __init__(self, main):
        self.root = main
        try:
            self.sock = socket.socket()
            self.sock.connect(("mc.craftrealms.com", 9999))
            print "1"
        except:
            Label(self.root, text="Cannot get connection to server!").pack()
            Button(self.root, text="Close").pack()
    def login(self, username, password):
        if len(username) > 2 and len(password) > 2:
            prep = "login:" + username + ":" + password
            self.sock.send(prep.encode())
            reply = self.sock.recv(1024)
            reply = reply.split(":")
            if reply[0] == "ok":
                self.loggedinusername = username
                self.secukey = reply[1] + "," + username + ":"
                return 1
    def search(self, string):
        if len(string) > 2:
            prep = self.secukey + "search:" + string
            self.sock.send(prep.encode())
            reply = self.sock.recv(10240)
            reply = reply.split(",")
            return reply
    def getinfo(self, player):
        if len(player) > 2:
            prep = self.secukey + "getinfo:" + player
            self.sock.send(prep.encode())
            data = self.sock.recv(10240)
            return eval(data)

class Data:
    root = Tk()
    server = None
    rank = StringVar()
    ip = StringVar()
    coordinates = StringVar()
    lasttp = StringVar()
    lastlogin = StringVar()
    lastlogout = StringVar()
    money = StringVar()
    banned = StringVar()
    muted = StringVar()
    banreason = StringVar()
    commands = {}
    notes = {}
    playerfull = {}

    def __init__(self, server):
        self.server = server
        
    def refreshdata(self, player, server):
        self.playerfull = self.server.getinfo(player)
        print self.playerfull['servers']['survival']
        self.rank.set(self.playerfull['rank'])
        self.ip.set(self.playerfull['servers']['survival']['ipAddress'])
        

class App:
    root = None
    userentry = StringVar()
    passentry = StringVar()
    currentplayer = None
    currentserver = None
    firstsearch = True
    server = ClientSock(root)
    data = Data(server)
    loginframe = Frame(root)
    searchframe = Frame(root)
    searchstr = StringVar()
    searchentry = Entry(root, textvariable=searchstr)
    searchscroll = Scrollbar(searchframe)
    searchresults = Listbox(searchframe, selectmode=SINGLE, yscrollcommand=searchscroll.set)
    userframe = Frame(root)
    serverbox = None
    serverselection = Frame(userframe)
    serverframe = Frame(userframe)

    def __init__(self):
        self.root = self.data.root
        self.root.geometry("300x500")
        self.root.resizable(width=FALSE, height=FALSE)
        self.loginframe.pack(fill=BOTH)
        Label(self.loginframe, text="Please login below").pack()
        Label(self.loginframe, text="Username:").pack()
        userentry = Entry(self.loginframe, textvariable=self.userentry)
        userentry.pack(fill=X, expand=1)
        userentry.focus()
        Label(self.loginframe, text="Password:").pack()
        passentry = Entry(self.loginframe, textvariable=self.passentry)
        passentry.pack(fill=X, expand=1)
        passentry.bind("<Return>", self.dologin)
        Button(self.loginframe, text="Login", command=self.dologin).pack(fill=X)
        print "4"
        
    def dologin(self, event=None):
        login = self.server.login(self.userentry.get(), self.passentry.get())
        if login:
            self.loginframe.pack_forget()
            self.loginframe.destroy()
            self.opensearchframe()

    def clearsearch(self, event=None):
        if self.firstsearch:
            self.searchstr.set("")

    def opensearchframe(self):
        self.searchstr.set("Search for player...")
        if self.firstsearch:
            self.searchstr.trace("w", lambda name, index, mode, sv=self.searchstr: self.dosearch(sv))
            self.searchentry.pack(fill=X)
            self.searchentry.bind("<Button-1>", self.clearsearch)
            self.searchresults.bind("<<ListboxSelect>>", self.selectplayer)
        self.searchresults.pack(fill=BOTH, expand=1)

        self.searchframe.pack(fill=BOTH, expand=1)

    def dosearch(self, stringvar):
        search = self.server.search(stringvar.get())
        if not search == None:
            self.searchresults.delete(0, END)
            for user in search:
                self.searchresults.insert(END, user)
            self.searchscroll.config(command=self.searchresults.yview)

    def selectplayer(self, event):
        self.currentplayer = self.searchresults.get(self.searchresults.curselection()[0])
        self.searchframe.pack_forget()
        count = 1
        serverselect = {}
        self.serverselection.pack(side=TOP)
        self.currentserver = 'survival'
        self.serverbox = Combobox(self.serverselection, values="Survival HG PVP Hub", width=295)
        self.serverbox.pack(fill=X, expand=1)
        self.serverbox.current(newindex=0)
        self.serverbox.bind('<<ComboboxSelected>>', self.changeserver)
        self.data.refreshdata(self.currentplayer, self.currentserver)

        # Rank 0
        Label(self.serverframe, text="Rank:", anchor=W).grid()
        Label(self.serverframe, textvariable=self.data.rank).grid(column=1)

        # IP 1
        Label(self.serverframe, text="IP:", anchor=W).grid(row=1)
        Label(self.serverframe, textvariable=self.data.ip, anchor=W).grid(row=1, column=1)

        self.serverframe.pack(fill=BOTH, expand=1)
        self.userframe.pack(fill=BOTH, expand=1)

    def changeserver(self, event=None):
        newserver = self.serverbox.get(self.serverbox.current())
        print(self.currentserver)

    def runloop(self):
        self.root.mainloop()
        
    


app = App()

app.runloop()
