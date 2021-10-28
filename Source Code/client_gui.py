"""All the Important pakages"""
import socket
import threading

import tkinter as tk
from tkinter import Entry, Text, Button
from tkinter.constants import END

import time
import sys


class Client():
    """methods realted to client side"""

    def unlock():
        """startup funtctions """
        try:
            threading.Thread(target=Client.connection_manager).start()
        except threading.ThreadError:
            pass
        try:
            threading.Thread(target=Client.push_message).start()
        except threading.ThreadError:
            pass
        try:
            threading.Thread(target=Client.spam_message).start()
        except threading.ThreadError:
            pass

    def spam_message():
        """spams text to avoid being idel"""
        time.sleep(10)
        while True:
            time.sleep(5)
            try:
                CLIENT.send(bytes('I', 'utf-8'))
            except:
                continue

    def close_app():
        """task before shuting client side"""
        try:
            try:
                CLIENT.send(bytes(str(USER_ID), 'utf-8'))
            except ConnectionRefusedError:
                pass
            root.destroy()
            sys.exit()
        except SystemExit:
            print("in axcept")
            sys.exit()

    def push_message():
        print("pushing")
        message = message_.get()
        if message == '':
            pass
        else:
            message_.delete(0, "end")
            send_template = str(username.get()) + ' : '+message+'\n'
            time.sleep(1)
            CLIENT.send(bytes(send_template, 'utf-8'))
            template = 'YOU : '+message+'\n'
            ChatBox.insert(END, template)

    def change_button(button_text, button_color):
        """change statuts button color """
        StatusButton['text'] = button_text
        StatusButton.config(bg=button_color)

    def connection_manager():

        global CLIENT
        global USER_ID

        server_ip = str(HostIpAndPort.get()[0:-5])
        server_port = int(HostIpAndPort.get()[
                          len(server_ip)+1:len(server_ip)+5])
        try:
            CLIENT = socket.socket()
            CLIENT.connect((server_ip, server_port))
            Client.change_button('CONNECTED TO PORT : ' +
                                 str(server_port), 'light green')
        except ConnectionRefusedError :
            Client.change_button('COULD NOT CONNECT TRY AGAIN', 'red')

        ChatBox.config(bg='white')

        server_data = (CLIENT.recv(10232).decode())
        USER_ID = server_data[0:1]
        server_data = server_data[1:]
        Client.change_button("You Entered : "+str(server_data), 'light blue')
        CLIENT.send(bytes(str(str(username.get())), 'utf-8'))
        StatusButton['state'] = 'disable'

        while True:
            try:
                rec_messages = (CLIENT.recv(10232).decode())+'\n'
                ChatBox.insert(END, rec_messages)
            except TimeoutError:
                continue

    def fetch_user_data():
        """fetching users host name"""
        return socket.gethostname()


if __name__ == "__main__":

    root = tk.Tk()

    root.title("client")
    try:
        root.iconbitmap("./icon_chat_app.ico")
    except :pass

    root.config(bg="white")

    root.geometry("300x391")
    root.minsize(300, 391)
    root.maxsize(300, 391)

    StatusButton = Button(root, text="PRESS TO CONNECT", width=45,
                          height=1, command=Client.unlock, borderwidth=0)
    StatusButton.place(x=0, y=0)

    Hostname = Client.fetch_user_data()

    HostIpAndPort = Entry(root)
    HostIpAndPort.place(x=0, y=25, width=150, height=35)
    HostIpAndPort.insert(END, "localhost"+':9999')

    username = Entry(root)
    username.place(x=150, y=28, width=151, height=35)
    username.insert(END, Hostname)

    ChatBox = Text(root, width=38, height=17, bg='grey', borderwidth=0)
    ChatBox.place(y=65, x=0)

    message_ = tk.Entry(root, borderwidth=1)
    message_.place(x=0, y=340, width=245, height=47)

    send_button = Button(root, text="send", height=3, width=8,
                         borderwidth=0, bg='light green', command=Client.push_message)
    send_button.place(x=244, y=340)
    root.bind('<Return>', lambda event: Client.push_message())

    root.protocol('WM_DELETE_WINDOW', Client.close_app)

    root.mainloop()
