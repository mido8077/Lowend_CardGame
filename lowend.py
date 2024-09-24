import random
import socket


class Lowend:

    listarr = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    players = [[], [], []]
    names = []

    leftover = []
    cards = {
        "1": 4,
        "2": 4,
        "3": 4,
        "4": 4,
        "5": 4,
        "6": 4,
        "7": 4,
        "8": 4,
        "9": 4,
        "10": 4,
        "11": 2,
        "12": 2,
        "13": 2,
        "14": 2,
        "15": 2,
        "16": 2,
        "17": 2,
    }
    cardsscore = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 20, 0, 25, -1, 10]

    def __init__(self):
        while True:
            x = int(input("Welcome to Lowend\n 1:Create Game       2:Join Game\n"))
            if x == 1:
                self.creategame()
            elif x == 2:
                self.joingame()
            else:
                print("wrong input")

    def joingame(self):

        Host = input("enter the ip :\n")
        Name = input("enter your name\n")
        Port = 5050
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((Host, Port))
        while True:
            x = s.recv(1024)
            x = x.decode()
            response = input(x)
            y = s.send(response.encode())

    def creategame(self):

        host = self.ip_gen()
        port = 5050
        ADDR = (host, port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        server.listen()
        print(f"connect at {host} {port}")

        for i in range(len(self.players)):
            conn, addr = server.accept()
            self.players[i].append(conn)
            self.players[i].append(addr)
            print(f"active connections {i+2}")

        for i in range(len(self.listarr)):
            for j in range(len(self.listarr[i])):
                num = self.randomcardgen()
                self.listarr[i][j] = num

        num = self.randomcardgen()
        self.leftover.append(num)

        Lowend = False
        count = 0
        while True:

            for i in range(len(self.listarr)):
                turn_msg = (
                    str(self.cards)
                    + "\n"
                    + str(self.listarr)
                    + "your -------turn "
                    + "the leftover card is :  "
                    + str(self.leftover)
                    + "\n1: pick a card       2:swap card     3:match card       4:lowend\n"
                )

                if Lowend == True:
                    count += 1
                    if count > 3:
                        self.results()
                        exit()

                if i > 0:

                    self.players[i - 1][0].send(turn_msg.encode())
                    rec_msg = self.players[i - 1][0].recv(1024)
                    rec_msg = rec_msg.decode()
                    act = int(rec_msg)

                    if act == 1:
                        num = self.randomcardgen()
                        turn_msg = (
                            "you picked " + str(num) + " \n 1:swap       2:return"
                        )
                        self.players[i - 1][0].send(turn_msg.encode())
                        rec_msg = self.players[i - 1][0].recv(1024)
                        rec_msg = rec_msg.decode()
                        act = int(rec_msg)

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
                        turn_msg = "lowend"

                        Lowend = True

                else:

                    print(f"your-------turn")
                    print("the leftover card is :", self.leftover[-1])
                    act = int(
                        input(
                            "1: pick a card       2:swap card     3:match card       4:lowend\n"
                        )
                    )

                    if act == 1:
                        num = self.randomcardgen()
                        act = int(input(f"you picked {num} \n 1:swap       2:return"))
                        if act == 1:
                            self.swap2(i, num)
                        elif act == 2:
                            if num in [1, 2, 3, 4, 5, 6, 13, 14, 15, 16]:
                                self.leftover.append(num)
                                print(self.leftover)
                            else:
                                self.special_Cards(i, num)
                    elif act == 2:
                        self.swap1(i)
                    elif act == 3:
                        self.match(i)
                    elif act == 4:
                        print("lowend")
                        Lowend = True

    def special_Cards(self, i, num):
        self.leftover.append(num)
        if num in [7, 8]:
            if i > 0:
                ranger = range(1, len(self.listarr[i]))
                turn_msg = "enter a num form " + str(ranger)
                self.players[i - 1][0].send(turn_msg.encode())
                rec_msg = self.players[i - 1][0].recv(1024)
                rec_msg = rec_msg.decode()
                picked = int(rec_msg)
                print(self.listarr[i][picked])
            else:
                ranger = range(1, len(self.listarr[i]))
                picked = int(input(f"enter a num from {ranger}")) - 1
                print(self.listarr[i][picked])
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

    def swap3(self, i):
        if i > 0:
            turn_msg = "choose a player"
            self.players[i - 1][0].send(turn_msg.encode())
            rec_msg = self.players[i - 1][0].recv(1024)
            rec_msg = rec_msg.decode()
            pickplayer = int(rec_msg) - 1

            ranger = range(1, len(self.listarr[i]))
            turn_msg = "enter a num from (your card)" + str(ranger)
            self.players[i - 1][0].send(turn_msg.encode())
            rec_msg = self.players[i - 1][0].recv(1024)
            rec_msg = rec_msg.decode()
            urcard = int(rec_msg) - 1

            ranger = range(1, len(self.listarr[pickplayer]))
            turn_msg = "enter a num from (their card)" + str(ranger)
            self.players[i - 1][0].send(turn_msg.encode())
            rec_msg = self.players[i - 1][0].recv(1024)
            rec_msg = rec_msg.decode()
            theircard = int(rec_msg) - 1

            temp = self.listarr[i][urcard]
            self.listarr[i][urcard] = self.listarr[pickplayer][theircard]
            self.listarr[pickplayer][theircard] = temp
        else:
            pickplayer = int(input("choose the player")) - 1
            ranger = range(1, len(self.listarr[i]))
            print("enter a num from ", ranger)
            urcard = int(input()) - 1
            ranger = range(1, len(self.listarr[pickplayer]))
            theircard = int(input()) - 1
            temp = self.listarr[i][urcard]
            self.listarr[i][urcard] = self.listarr[pickplayer][theircard]
            self.listarr[pickplayer][theircard] = temp

    def seeothcard(self, i):
        if i > 0:
            turn_msg = "choose a player" + str(ranger)
            self.players[i - 1][0].send(turn_msg.encode())
            rec_msg = self.players[i - 1][0].recv(1024)
            rec_msg = rec_msg.decode()
            pickplayer = int(rec_msg) - 1

            ranger = range(1, len(self.listarr[pickplayer]))
            turn_msg = "enter a num from " + str(ranger)
            self.players[i - 1][0].send(turn_msg.encode())
            rec_msg = self.players[i - 1][0].recv(1024)
            rec_msg = rec_msg.decode()
            picked = int(rec_msg) - 1
            print(f"player {pickplayer} card is : {self.listarr[pickplayer][picked]}")
        else:
            pickplayer = int(input("choose the player"))
            ranger = range(1, len(self.listarr[pickplayer]))
            picked = int(input(f"enter a num from {ranger}")) - 1
            print(f"player {pickplayer} card is : {self.listarr[pickplayer][picked]}")

    def match(self, i):
        if i > 0:
            ranger = range(1, len(self.listarr[i]))
            turn_msg = "enter a num form " + str(ranger)
            self.players[i - 1][0].send(turn_msg.encode())
            rec_msg = self.players[i - 1][0].recv(1024)
            rec_msg = rec_msg.decode()
            picked = int(rec_msg) - 1
            if self.listarr[i][picked] == self.leftover[-1] or self.leftover[-1] == 12:
                self.listarr[1].pop(picked)
                print("match done")
            else:
                self.listarr[i].append(self.leftover[-1])
                self.leftover.pop(-1)
                print("match failed")
        else:
            ranger = range(1, len(self.listarr[i]))
            picked = int(input(f"enter a num from {ranger}")) - 1
            if self.listarr[i][picked] == self.leftover[-1] or self.leftover[-1] == 12:
                self.listarr[1].pop(picked)
                print("done")
            else:
                self.listarr[i].append(self.leftover[-1])
                self.leftover.pop(-1)
                print("match failed")

    def swap1(self, i):
        if i > 0:
            ranger = range(1, len(self.listarr[i]))
            turn_msg = "enter a num form " + str(ranger)
            self.players[i - 1][0].send(turn_msg.encode())
            rec_msg = self.players[i - 1][0].recv(1024)
            rec_msg = rec_msg.decode()
            picked = int(rec_msg) - 1
            temp = self.leftover[-1]
            self.leftover[-1] = self.listarr[i][picked]
            self.listarr[i][picked] = temp
        else:
            ranger = range(1, len(self.listarr[i]))
            picked = int(input(f"enter a num from {ranger}")) - 1
            temp = self.leftover[-1]
            self.leftover[-1] = self.listarr[i][picked]
            self.listarr[i][picked] = temp

    def swap2(self, i, num):
        if i > 0:
            ranger = range(1, len(self.listarr[i]))
            turn_msg = "enter a num form " + str(ranger)
            self.players[i - 1][0].send(turn_msg.encode())
            rec_msg = self.players[i - 1][0].recv(1024)
            rec_msg = rec_msg.decode()
            picked = int(rec_msg) - 1
            self.leftover.append(self.listarr[i][picked])
            self.listarr[i][picked] = num
        else:
            ranger = range(1, len(self.listarr[i]))
            picked = int(input(f"enter a num from {ranger}")) - 1
            self.leftover.append(self.listarr[i][picked])
            self.listarr[i][picked] = num

    def lookaround(self, i):
        if i > 0:
            for j in len(range(self.listarr)):
                ranger = range(1, len(self.listarr[i]))
                turn_msg = "enter a num form " + str(ranger)
                self.players[i - 1][0].send(turn_msg.encode())
                rec_msg = self.players[i - 1][0].recv(1024)
                rec_msg = rec_msg.decode()
                picked = int(rec_msg) - 1
                self.players[i - 1][0].send(self.listarr[j][picked].encode())

        else:
            for j in len(range(self.listarr)):
                ranger = range(1, len(self.listarr[i]))
                picked = int(input("enter a num from ", ranger)) - 1
                print(self.listarr[j][picked])

    def results(self):
        best = 100
        bestid = 0
        for num in range(len(self.listarr)):
            sum = 0
            for i in self.listarr[num]:
                sum += self.cardsscore[i - 1]
            print(f"{self.names[num]} score is {sum}")
            if sum < best:
                best = sum
                bestid = num
        print(f"the winner is {self.names[bestid]} with the score {best}")


def main():

    instance = Lowend()


main()
