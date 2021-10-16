

import socket
import time
from datetime import datetime
import threading
import tkinter
from tkinter import Scrollbar, Text, Entry, Button, font
from tkinter.constants import END, NS, VERTICAL
import sys
from threading import Thread, ThreadError
from win10toast import ToastNotifier

Notify = ToastNotifier()


class Server():

    def unlock():

        try:
            threading.Thread(target=Server.connection_manager).start()
        except :
            pass

    def update():
        while True:
            Server.change_button(str(len(CONNECTED)) +
                                 ' USERS IN ROOM : ', 'light green')
            time.sleep(5)

    def close_app():
        try:
            for clients_list in CONNECTED:
                try:
                    clients_list.send(
                        bytes('SERVER WAS CLOSED BY THE HOST', 'utf-8'))
                except :
                    sys.exit()
            root.destroy()
            sys.exit()
        except :
            root.destroy()

    def pull_message():

        while len(CONNECTED) > 0:
            time.sleep(1)
            for i in CONNECTED:
                try:
                    rec_messages = (i.recv(110232).decode())
                    print("messahe recived : ", rec_messages)
                    if rec_messages == 'I':
                        continue
                    try:
                        id_to_remove = int(rec_messages)
                        print(id_to_remove)
                        CONNECTED.pop(id_to_remove-1)
                        Server.change_button(str(PARTICIPANTS[id_to_remove-1]) + " left the room", "pink")
                        Notify.show_toast("prichat", str(PARTICIPANTS[id_to_remove-1]) + " left the room", duration=1)
                        PARTICIPANTS.pop(id_to_remove-1)
                    except:
                        pass
                    Notify.show_toast("prichat", rec_messages, duration=1)
                    MessageWindow.insert(END, rec_messages+'')
                except :
                    pass

    def push_message():
        """sending messages to clients"""
        outbox_message = MessageBox.get()
        if outbox_message == '':
            pass
        else:
            MessageBox.delete(0, "end")
            outbox_message = ' : '+outbox_message+"  "+datetime.now().strftime("%H:%M:%S")

            for client_list in CONNECTED:

                MessageWindow.insert(
                    END, 'YOU '+outbox_message, font.Font(weight="bold"))
                client_list.send(bytes(USERNAME+outbox_message+'\n', 'utf-8'))
                time.sleep(1)

    def change_button(button_text, button_color):
        """change status button"""
        try:
            Status['text'] = button_text
            Status.config(bg=button_color)
        except RuntimeError:
            pass

    def connection_manager():
        """manage the server client connections"""
        host_config['state'] = 'disable'
        UserNameEntry['state'] = 'disable'
        global CONNECTED
        global USERNAME
        global PARTICIPANTS
        CONNECTED = []
        try:threading.Thread(target=Server.update).start()
        except :pass

        PARTICIPANTS = []

        port_number = str(host_config.get())[len(Ip)+1:len(Ip)+5]
        USERNAME = UserNameEntry.get()

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            server_socket.bind((Ip, int(port_number)))
            server_socket.listen(3)
            Server.change_button("CONNECTED TO PORT : " +str(port_number), 'light green')
            MessageWindow.config(bg='white')

        except:
            Server.change_button('COULD NOT CONNECT', 'red')

        while True:
            connected_client, addr = server_socket.accept()
            CONNECTED.append(connected_client)

            connected_client.send(bytes(str(str(len(CONNECTED))+str(USERNAME)), 'utf-8'))
            print("DATA SEND")
            PARTICIPANTS.append(connected_client.recv(110232).decode())

            Server.change_button(PARTICIPANTS[len(CONNECTED)-1]+' ENTERED THE ROOM', 'light blue')
            try:threading.Thread(target=Server.pull_message).start()
            except :pass

    def fetch_user_data():
        """get the user hostname and ip"""
        return (socket.gethostname(), socket.gethostbyname(socket.gethostname()))

    def participation_window():
        participants_app = tkinter()
        participants_app.title("Participants")
        text_box = tkinter.Text(
            participants_app, height=13, width=32, font=(12))
        text_box.grid(row=0, column=0)
        text_box.config(bg='#D9D8D7')
        scroll_bar = Scrollbar(participants_app, orient=VERTICAL)
        scroll_bar.grid(row=0, column=1, sticky=NS)
        text_box.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=text_box.yview)
        spacing = 0

        text_box.insert(END, "participants"+'\n')
        text_box.insert(END, " "+'\n')
        for clients_list in PARTICIPANTS:
            text_box.insert(END, clients_list+'\n')
            spacing += 30
        text_box['state'] = 'disable'
        participants_app.mainloop()


if __name__ == "__main__":

    root = tkinter.Tk()
    root.title("server")

    try:root.iconbitmap("./icon_chat_app.ico")
    except :pass

    root.geometry("300x391")
    root.maxsize(300, 391)

    Status = Button(root, text="PRESS TO CONNECT", width=45, height=1,
                    command=Server.unlock, borderwidth=0)
    Status.place(x=0, y=0)

    HostName, Ip = Server.fetch_user_data()

    host_config = Entry(root)
    host_config.place(x=0, y=25, width=150, height=35)
    host_config.insert(END, Ip+':9999')

    UserNameEntry = Entry(root)
    UserNameEntry.place(x=150, y=25, width=151, height=35)
    UserNameEntry.insert(END, HostName)

    MessageWindow = Text(root, width=38, height=17, bg='grey', borderwidth=0)
    MessageWindow.place(y=65, x=0)

    MessageBox = tkinter.Entry(root, borderwidth=1)
    MessageBox.place(x=0, y=340, width=245, height=47)

    SendButton = Button(root, text="send", height=3, width=8,
                        borderwidth=0, bg='light green', command=Server.push_message)
    SendButton.place(x=244, y=340)
    root.bind('<Return>', lambda event: Server.push_message)

    SendButton = Button(root, text="File", height=3, width=8, borderwidth=0,
                        bg='light blue', command=Server.push_message)
    SendButton.place(x=344, y=340)

    root.protocol('WM_DELETE_WINDOW', Server.close_app)

    root.mainloop()
