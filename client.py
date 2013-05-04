from Tkinter import *
from ttk import *
import socket
import sys
import datetime

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
    def close(self):
        self.sock.close
        
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
    def getcommands(self, player):
        if len(player) > 2:
            prep = self.secukey + "getcommands:" + player
            self.sock.send(prep.encode())
            data = self.sock.recv(10240)
            return eval(data)
    def getchat(self, player):
        if len(player) > 2:
            prep = self.secukey + "getchat:" + player
            self.sock.send(prep.encode())
            data = self.sock.recv(10240)
            if data == "no data":
                return
            else:
                return ("No data")

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
    commands = None
    chat = None
    notes = {}
    playerfull = {}

    def __init__(self, server):
        self.server = server
        
    def refreshfulldata(self, player):
        server = 'survival'
        self.playerfull = self.server.getinfo(player)
        self.rank.set(self.playerfull['rank'])
        self.ip.set(self.playerfull['servers']['survival']['ipAddress'])
        self.coordinates.set(self.playerfull['servers'][server]['lastlocation']['world'] + ", " + self.playerfull['servers'][server]['lastlocation']['x'] + ", " + self.playerfull['servers'][server]['lastlocation']['y'] + ", " + self.playerfull['servers'][server]['lastlocation']['z'])
        self.lastlogin.set(datetime.datetime.utcfromtimestamp(self.playerfull['servers'][server]['timestamps']['login'] // 1000).strftime('%H:%M:%S %m-%d-%Y'))
        self.lasttp.set(datetime.datetime.utcfromtimestamp(self.playerfull['servers'][server]['timestamps']['lastteleport'] // 1000).strftime('%H:%M:%S %m-%d-%Y'))
        self.lastlogout.set(datetime.datetime.utcfromtimestamp(self.playerfull['servers'][server]['timestamps']['logout'] // 1000).strftime('%H:%M:%S %m-%d-%Y'))
        try:
            if(self.playerfull['servers'][server]['muted']):
                self.muted.set("Yes")
            else:
                self.muted.set("No")
        except:
            self.muted.set("No")
        try:
            self.banreason.set(self.playerfull['servers'][server]['ban']['reason'])
            self.banned.set("Yes")
        except:
            self.banned.set("No")
            self.banreason.set("-")
        self.chat = self.server.getchat(player)
        self.commands = self.server.getcommands(player)
        print self.commands
    def changedata(self, server):
        try:
            self.coordinates.set(self.playerfull['servers'][server]['lastlocation']['world'] + ", " + self.playerfull['servers'][server]['lastlocation']['x'] + ", " + self.playerfull['servers'][server]['lastlocation']['y'] + ", " + self.playerfull['servers'][server]['lastlocation']['z'])
        except:
            self.coordinates.set("-")
        try:
            self.lastlogin.set(datetime.datetime.utcfromtimestamp(self.playerfull['servers'][server]['timestamps']['login'] // 1000).strftime('%H:%M:%S %m-%d-%Y'))
        except:
            self.lastlogin.set("-")
        try:
            self.lasttp.set(datetime.datetime.utcfromtimestamp(self.playerfull['servers'][server]['timestamps']['lastteleport'] // 1000).strftime('%H:%M:%S %m-%d-%Y'))
        except:
            self.lasttp.set("-")
        try:
            self.lastlogout.set(datetime.datetime.utcfromtimestamp(self.playerfull['servers'][server]['timestamps']['logout'] // 1000).strftime('%H:%M:%S %m-%d-%Y'))
        except:
            self.lastlogout.set("-")
        try:
            if(self.playerfull['servers'][server]['muted']):
                self.muted.set("Yes")
            else:
                self.muted.set("No")
        except:
            self.muted.set("No")
        try:
            self.banreason.set(self.playerfull['servers'][server]['ban']['reason'])
            self.banned.set("Yes")
        except:
            self.banned.set("No")
            self.banreason.set("-")
        
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
    userframe = None
    serverbox = None
    serverselection = None
    serverframe = None
    historyframe = Frame(userframe)
    onuser = 0

    def __init__(self):
        self.root = self.data.root
        self.root.geometry("300x500")
        self.root.resizable(width=FALSE, height=FALSE)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
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
        
    def dologin(self, event=None):
        login = self.server.login(self.userentry.get(), self.passentry.get())
        if login:
            self.loginframe.pack_forget()
            self.loginframe.destroy()
            self.opensearchframe()

    def playerHistories(self):
        player = self.currentplayer.get()
        

    def opensearchframe(self):
        self.searchstr.set("Search for player...")
        if self.firstsearch:
            self.searchstr.trace("w", lambda name, index, mode, sv=self.searchstr: self.dosearch(sv))
            self.searchentry.pack(fill=X)
            self.searchresults.bind("<<ListboxSelect>>", self.selectplayer)
            self.searchentry.focus()
        self.searchresults.pack(fill=BOTH, expand=1)

        self.searchframe.pack(fill=BOTH, expand=1)

    def dosearch(self, stringvar):
        if self.firstsearch:
                self.searchstr.set("")
                self.firstsearch = 0
        search = self.server.search(stringvar.get())
        if not search == None:
            if self.onuser:
                self.userframe.pack_forget()
                self.userframe.destroy()
                self.searchframe.pack(fill=BOTH, expand=1)
            self.searchresults.delete(0, END)
            for user in search:
                self.searchresults.insert(END, user)
                self.searchentry.focus()
            self.searchscroll.config(command=self.searchresults.yview)
        else:
            self.searchresults.delete(0, END)

    def ipclick(self, event):
        self.searchstr.set(self.data.ip.get())
        self.dosearch(self.searchstr)

    def selectplayer(self, event):
        self.currentplayer = self.searchresults.get(self.searchresults.curselection()[0])
        self.searchframe.pack_forget()
        count = 1
        self.onuser = 1
        serverselect = {}
        self.userframe = Frame(self.root)
        self.serverframe = Frame(self.userframe)
        self.serverselection = Frame(self.userframe)
        self.serverselection.pack(side=TOP)
        self.serverframe.pack(fill=BOTH, expand=1)
        self.userframe.pack(fill=BOTH, expand=1)
        self.currentserver = 'survival'
        self.serverbox = Combobox(self.serverselection, values="Survival HG PVP Hub", width=295)
        self.serverbox.pack(fill=X, expand=1)
        self.serverbox.current(newindex=0)
        self.serverbox.bind('<<ComboboxSelected>>', self.changeserver)
        self.data.refreshfulldata(self.currentplayer)
        self.serverframe.columnconfigure(1, weight=1)

        # Rank 0
        Label(self.serverframe, text="Rank:", anchor=W).grid()
        Label(self.serverframe, textvariable=self.data.rank).grid(column=1)

        # IP 1
        Label(self.serverframe, text="IP:", anchor=W).grid(row=1)
        ip = Label(self.serverframe, textvariable=self.data.ip)
        ip.grid(row=1, column=1)
        ip.bind("<Button-1>", self.ipclick)

        # Coords 2
        Label(self.serverframe, text="Last Location:", anchor=W).grid(row=2)
        Label(self.serverframe, textvariable=self.data.coordinates).grid(row=2, column=1)

        # Last Login 3
        Label(self.serverframe, text="Last Login:", anchor=W).grid(row=3)
        Label(self.serverframe, textvariable=self.data.lastlogin).grid(row=3, column=1)

        # Last Logout 4
        Label(self.serverframe, text="Last Logout:", anchor=W).grid(row=4)
        Label(self.serverframe, textvariable=self.data.lastlogout).grid(row=4, column=1)

        # Last teleport 5
        Label(self.serverframe, text="Last Teleport:", anchor=W).grid(row=5)
        Label(self.serverframe, textvariable=self.data.lasttp).grid(row=5, column=1)

        # Muted 6
        Label(self.serverframe, text="Muted:", anchor=W).grid(row=6)
        Label(self.serverframe, textvariable=self.data.muted).grid(row=6, column=1)

        # Banned 7
        Label(self.serverframe, text="Banned:", anchor=W).grid(row=7)
        Label(self.serverframe, textvariable=self.data.banned).grid(row=7, column=1)

        Button(self.serverframe, text="Chat", command=self.server.getchat(self.currentplayer)).grid(row=8)
        Button(self.serverframe, text="History", command=self.historywindow).grid(row=9)

    def changeserver(self, event=None):
        self.currentserver = self.serverbox.get().lower()
        self.data.changedata(self.currentserver)

    def historywindow(self):
        self.serverframe.pack_forget()
        self.historyframe.pack(fill=BOTH, expand=1)
        Label(self.historyframe, text="Command History").pack()
        commandbox = Listbox(self.historyframe, height=10)
        for i in self.data.commands:
            commandbox.insert(END, i['date'] + " " + i['data'])
        commandbox.pack(fill=X, expand=1)

    def runloop(self):
        self.root.mainloop()

    def close(self):
        self.server.close()
        self.root.destroy()

app = App()

app.runloop()
