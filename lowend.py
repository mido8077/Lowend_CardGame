import random
import socket
import os
import time



class Lowend:

    cards = {"1": 4,"2": 4,"3": 4,"4": 4,"5": 4,"6": 4,"7": 4,"8": 4,"9": 4,"10": 4,"11": 2,"12": 2,"13": 2,"14": 2,"15": 2,"16": 2,"17": 2}
    cardsscore = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 20, 0, 25, -1, 10]
    listarr = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    players = [[], [], []]
    leftover = []
    names = []
    Totals=[]
    def __init__(self):
        self.clear(0)
        while True:
            x = input("Welcome to Lowend\n 1:Create Game       2:Join Game\n")
            if x == "1":
                self.creategame()
                
            elif x == "2":
                self.joingame()
            else:
                print("wrong input")
            self.clear(0)    
                    
    def creategame(self):
        self.names.append(input("Enter your name\n"))
        HOST = self.ip_gen()
        PORT = 5050
        ADDR = (HOST, PORT)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        server.listen()
        print(f"connect at {HOST} {PORT}")

        for i in range(len(self.listarr)-1):
            conn, addr = server.accept()
            self.players[i].append(conn)
            self.players[i].append(addr)
            name=self.players[i][0].recv(1024)
            name=name.decode()
            self.names.append(name)
            print(f"{name} connected")
        
        for i in range(len(self.listarr)):
            for j in range(len(self.listarr[i])):
                num = self.randomcardgen()
                self.listarr[i][j] = num

        num = self.randomcardgen()
        self.leftover.append(num)
        Endgame = False
        count = 0
        self.clear(0)

        while True:

            for i in range(len(self.listarr)):

                if len(self.leftover)==38:
                     for i in range(len(self.leftover)):
                          card =str(self.leftover[i])
                          self.cards[card]+=1
                          self.leftover.pop(i)

                if Endgame == True:
                    count += 1
                    if count > 3:
                        self.results()
                        exit()
                turn_msg = (str(self.names[i])+" turn (player-"
                    +str(i+1)
                    + ") the leftover card is :  "
                    + str(self.leftover[-1])
                )
                for j in range(len(self.listarr)):
                            if j >0 and j!=i:
                                self.players[j-1][0].send((turn_msg).encode())
                            if j==0 and j!=i:
                                 print(turn_msg)

                turn_msg=turn_msg+"\n1: pick a card       2:swap a card     3:match a card       4:Endgame\n"
                
                if i >0:
                        act = int(self.input2(i,turn_msg))
                else:
                        act = int(input(turn_msg))

                if act == 1:
                        num = self.randomcardgen()
                        if i>0:
                            act = int(self.input2(i,("you picked " + str(num) + " \n 1:swap       2:return\n")))
                        else:
                            act = int(input(("you picked " + str(num) + " \n 1:swap       2:return\n")))
                        if act == 1:
                            self.swap2(i, num)
                        elif act == 2:
                            if num in [1, 2, 3, 4, 5, 6, 13, 14, 15, 16]:
                                self.leftover.append(num)
                            else:
                                self.special_Cards(i, num)
                elif act == 2:
                        self.swap1(i)
                elif act == 3:
                        self.match(i)
                elif act == 4:
                        Endgame = True
                        print("Endgame")
                        for j in range(len(self.listarr)):
                            if j >0:
                                self.players[j-1][0].send(("Endgame\n").encode())

                self.clear(1)

    def joingame(self):
        HOST = input("enter the ip :\n")
        NAME = input("enter your name\n")
        PORT = 5050
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.1.2", PORT))
        x=s.send(NAME.encode())
        self.clear(0)
        while True:
            x = s.recv(1024)
            self.clear(0)
            x = x.decode()
            if x.split()[-1] not in ["2:return","4:Endgame",":"]:
                print(x)
            else:
                response = input(x)
                s.send(response.encode())
        
    def special_Cards(self, i, num):
        self.leftover.append(num)
        if num in [7, 8]:
            self.seeurcard(i)
        elif num in [9, 10]:
            self.seeothcard(i)
        elif num == 11:
            self.lookaround(i)
        elif num == 12:
            self.match(i)
        elif num == 17:
            self.swap3(i)

    def randomcardgen(self):
        num = random.randint(1, 17)
        while self.cards[str(num)] == 0:
            num = random.randint(1, 17)
        cardname = str(num)
        self.cards[cardname] -= 1
        return num
    
    def ip_gen(self):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(("8.8.8.8", 80))
                ip_address = s.getsockname()[0]
            finally:
                s.close()
            return ip_address
    
    def swap1(self, i):
        ranger = range(1, len(self.listarr[i]))
        if i > 0:
            picked = int(self.input2(i,("enter a num form " + str(ranger)+" :\n"))) - 1
        else:
            picked = int(input(f"enter a num from {ranger} :\n")) - 1
        temp = self.leftover[-1]
        self.leftover[-1] = self.listarr[i][picked]
        self.listarr[i][picked] = temp

    def swap2(self, i, num):
        ranger = range(1, len(self.listarr[i]))
        if i > 0:
            picked = int(self.input2(i,("enter a num form " + str(ranger)+" :\n"))) - 1
        else:
            picked = int(input(f"enter a num from {ranger}")) - 1
        self.leftover.append(self.listarr[i][picked])
        self.listarr[i][picked] = num

    def swap3(self, i):
        if i > 0:
            pickplayer = int(self.input2(i,"choose a player :\n")) - 1
            ranger = range(1, len(self.listarr[i]))
            urcard = int(self.input2(i,("enter a num from "+ str(ranger)+" (your card) :"))) - 1
            ranger = range(1, len(self.listarr[pickplayer]))
            theircard = int(self.input2(i,("enter a num from " + str(ranger)+" (their card) :"))) - 1
        else:
            pickplayer = int(input("choose the player :\n")) - 1
            ranger = range(1, len(self.listarr[i]))
            urcard = int(input(f"enter a num from {ranger} (your card) :\n")) - 1
            ranger = range(1, len(self.listarr[pickplayer]))
            theircard = int(input(f"enter a num from {ranger} (your card) :\n")) - 1
        temp = self.listarr[i][urcard]
        self.listarr[i][urcard] = self.listarr[pickplayer][theircard]
        self.listarr[pickplayer][theircard] = temp 

    def seeurcard(self,i):
            ranger = range(1, len(self.listarr[i]))
            if i > 0:
                picked = + int(self.input2(i,("enter a num form " + str(ranger)+" :\n")))-1
                self.players[i-1][0].send(("card is : "+str(self.listarr[i][picked])).encode())
            else:
                picked = int(input(f"enter a num from {ranger}")) - 1
                print(self.listarr[i][picked])

    def seeothcard(self, i):
        if i > 0:
            pickplayer = int(self.input2(i,"choose a player :\n")) - 1
            ranger = range(1, len(self.listarr[pickplayer]))
            picked = int(self.input2(i,("enter a num from " + str(ranger)+" :\n"))) - 1
            self.players[i-1][0].send(("player "+str(pickplayer+1)+" card is :"+ str(self.listarr[pickplayer][picked])).encode())
        else:
            pickplayer = int(input("choose the player :\n"))-1
            ranger = range(1, len(self.listarr[pickplayer]))
            picked = int(input(f"enter a num from {ranger} :\n")) - 1
            print(f"player {pickplayer+1} card is : {self.listarr[pickplayer][picked]}")

    def lookaround(self, i):
        if i > 0:
            for j in range(len(self.listarr)):
                ranger = range(1, len(self.listarr[i]))
                picked = int(self.input2(i,("enter a num form " + str(ranger)+ " :\n"))) - 1
                self.players[i - 1][0].send(self.listarr[j][picked].encode())
        else:
            for j in range(len(self.listarr)):
                ranger = range(1, len(self.listarr[i]))
                picked = int(input("enter a num from ", ranger," :\n")) - 1
                print(self.listarr[j][picked])
                
    def match(self, i):
        ranger = range(1, len(self.listarr[i]))
        if i > 0:
            picked =int(self.input2(i,("enter a num form " + str(ranger)+" :\n")))-1  
        else:
            picked = int(input(f"enter a num from {ranger} :\n")) - 1

        if self.listarr[i][picked] == self.leftover[-1] or self.leftover[-1] == 12:
                self.listarr[i].pop(picked)
                if i>0:
                     self.players[i-1][0].send("done".encode())
                else:
                    print("done")
        else:
                self.listarr[i].append(self.leftover[-1])
                self.leftover.pop(-1)
                if i>0:
                     self.players[i-1][0].send("match failed".encode())
                else:
                    print("match failed")

    def results(self):
        for num in range(len(self.listarr)):
            sum = 0
            for i in self.listarr[num]:
                sum += self.cardsscore[i - 1]
            Total=str(self.names[num])+" score is : "+str(sum)
            self.Totals.append(Total)
        for i in range(len(self.listarr)):
            if i>0:
                self.players[i-1][0].send(str(self.Totals).encode())
                self.players[i-1][0].close()
            else:
                print(self.Totals)

    def input2(self,i,msg):
                self.players[i - 1][0].send(msg.encode())
                rec_msg = self.players[i - 1][0].recv(1024)
                rec_msg = rec_msg.decode()
                return rec_msg
            
    def clear(self,t):
        time.sleep(t)
        os.system('cls' if os.name == 'nt' else 'clear')
        
instance = Lowend()


