#pakages 

# connection modules 
import socket

# achive random values 
import random

# gui module 
import tkinter as tk
from tkinter import *

# module to improve modules 
import threading


# class 

class client_():

    # fuctions 

    #this fuction unlocks threading to run things multiple

    def unlock():
        t1 = threading.Thread(target=client_.port_cheak, args=())
        t1.start()
        t2 = threading.Thread(target=client_.push, args=())
        t2.start()





    def doSomething():
        try:
            client.send(bytes(str(id),'utf-8'))
            print("network closed")
            root.destroy()
        except:
            root.destroy()

    def push():
        message=message_.get()
        if message=='':
            pass
        else:
            print("message typed : ",message)
            message_.delete(0,"end")
            send_template=username +' : '+message+'\n'
            client.send(bytes(send_template,'utf-8'))
            template='YOU : '+message+'\n'
            view_window.insert(END,template) 
            return message


    # this fuction connect you with your port 

    def port_cheak():
        config_button['text'] = 'TRYING TO CONNECT.....'
        #vars 

        global client
        reconnect=0  #this var limits reconnecting attempt
        global connected
        global port
        global id
        port=host_config.get()
        port=int(port[len_ip+1:len_ip+5])  #port number
        port_text=str(port)
        ip=host_config.get()
        ip=ip[0:len_ip]
        print("ip conneting to : ",ip)
        print("port conneting to : ",port)
     
        global username
        username=username_config.get()

        try:

            hostname = socket.gethostname()
            ip=socket.gethostbyname(hostname)
            config_button['text'] = 'IP SET : '+ip

            try: 

                # creating socket 
                try:
                    client=socket.socket()
                    print("socket created")
                except socket.error as msg:
                    client=None
                    client_.port_cheak()

                # generating a random port number so that it wont show any occupied the next time using the same one 
                # binding the socket
                client.connect((ip,port)) 

                # this is a update to status menu in gui 
                config_button['text'] = 'CONNECTED TO PORT : '+port_text
                config_button.config(bg='light green')

            except:

                reconnect=reconnect+1

                #this is update to status menu in gui
                config_button['text'] = 'PROBLEM CONNECTING TRY AGAIN'+port_text
                config_button.config(bg='red')

                if reconnect>4:
                    client_.port_cheak()

        except: 
            config_button['text'] = 'COULD NOT CONNECT TRY AGAIN'
            config_button.config(bg='red')
            if reconnect>4:
                client_.port_cheak()

        config_button['text'] = 'CONNECTED: '+port_text

        #all the connection work is handel here 




        while True:
            view_window.config(bg='white')
            id=rec_messages=(client.recv(10232).decode())
            print(id)
            try:
                rec_messages=(client.recv(10232).decode())
                template= rec_messages+'\n'
                view_window.insert(END,template) 
            except:
                continue
    



                   
    
#programs     

# gui code 
   
root = tk.Tk()

#TITLE
root.title("client")

try:
    root.iconbitmap('media//icon_chat_app.ico')
except:
    print("cant load icon")

#color of background
root.config(bg="white")

#SCREENSIZE
root.geometry("300x391")
root.minsize(300,400)
root.maxsize(300,400)

 
# status bar 

config_button = Button(root, text ="PRESS TO CONNECT",width=45,height=1, command=client_.unlock,borderwidth=0) 
config_button.place(x=0, y=0)

# details section 

# getting the users ip and hostname
fetch_hostname = socket.gethostname()
print("fetch hostname : ",fetch_hostname)
fetch_ip=socket.gethostbyname(fetch_hostname)

len_ip=len(fetch_ip)
print("ip_lenght : ",len_ip)

# Generator of username 
fetch_hostname='username'+str(random.randint(100,9999))


# PRINTING DETAILS 
print("generated username : ",fetch_hostname)
print("fetch_ip : ",fetch_ip)

# HOST_IP ENTRY 
host_config = Entry(root)
host_config.place(x =0,y =25,width=150,height=35)
host_config.insert(END,fetch_ip+':9999')

# username ENTRY 
username_config = Entry(root)
username_config.place(x =150,y =28,width=151,height=35)
username_config.insert(END,fetch_hostname)

#message window
view_window= Text(root, width=38,height=19,bg='grey',borderwidth=0)
view_window.place(y=65,x=0)

# text message section   
message_ = tk.Entry(root,borderwidth=1)
message_.place(x =0,y = 345,width=245,height=47)

# message sending 
send_button = Button(root, text ="send",height=3,width=8,borderwidth=0,bg='light green',command=client_.push) 
send_button.place(x=244, y=346)
root.bind('<Return>',lambda event:client_.push())

root.protocol('WM_DELETE_WINDOW', client_.doSomething)  

root.mainloop()