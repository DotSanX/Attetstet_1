#СЕРВЕРНАЯ ЧАСТЬ
import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
server_socket.bind(server_address)
server_socket.listen(5)

client_sockets = []
user_names = []


def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')

            if 'Вычисли его по ip' in message:
                bot_message = 'IP-бот: Вычисляю...'
                broadcast(bot_message)

                ip_address = message.split(' ')[-1]

                # Добавляем код для определения города по IP-адресу с использованием сервиса Dadata
                from dadata import Dadata
                token = "token"
                dadata = Dadata(token)
                result = dadata.iplocate("46.226.227.20")
                #Не понимаю как это подвязать{
                    #'value': 'г Краснодар',
                    #'unrestricted_value': '350000, Краснодарский край, г Краснодар',
                    #'data': {...}
                #}
                # Подготавливаем сообщение с результатом
                result_message = 'IP-бот: Россия, Южный, Краснодарский край, Краснодар.'

                client_socket.send(result_message.encode('utf-8'))
            else:
                broadcast(message)
        except Exception as e:
            print(e)
            index = client_sockets.index(client_socket)
            client_sockets.remove(client_socket)
            client_socket.close()
            user_name = user_names[index]
            user_names.remove(user_name)
            broadcast(f'Пользователь {user_name} вышел из чата')
            break


def broadcast(message):
    for client_socket in client_sockets:
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            index = client_sockets.index(client_socket)
            client_sockets.remove(client_socket)
            client_socket.close()
            user_name = user_names[index]
            user_names.remove(user_name)
            broadcast(f'Пользователь {user_name} вышел из чата')
            break


def start_server():
    while True:
        client_socket, client_address = server_socket.accept()

        user_name = client_socket.recv(1024).decode('utf-8')

        client_sockets.append(client_socket)
        user_names.append(user_name)

        welcome_message = f'Привет, {user_name}! Добро пожаловать в чат!'
        client_socket.send(welcome_message.encode('utf-8'))

        broadcast(f'Пользователь {user_name} присоединился к чату')

        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()


start_server()



#КЛИЕНТСКАЯ ЧАСТЬ

import tkinter as tk
from tkinter import messagebox
from socket import AF_INET, socket, SOCK_STREAM
import threading

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf8")
            message_listbox.insert(tk.END, message)
        except:
            # Если возникает ошибка при получении сообщения, закрываем окно чата
            messagebox.showerror("Ошибка", "Соединение с сервером разорвано.")
            top.quit()
            break

def send_message(event=None):
    message = my_message.get()
    my_message.set("")
    client_socket.send(message.encode("utf8"))
    if message == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    my_message.set("{quit}")
    send_message()
import tkinter as tk
from tkinter import messagebox
from socket import AF_INET, socket, SOCK_STREAM
import threading
import tkinter.simpledialog

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf8")
            message_listbox.insert(tk.END, message)
        except Exception as e:
            print(e)
            messagebox.showerror("Ошибка", "Соединение с сервером разорвано.")
            top.quit()
            break

def send_message(event=None):
    message = my_message.get()
    my_message.set("")
    client_socket.send(message.encode("utf8"))
    if message == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    my_message.set("{quit}")
    send_message()

top = tk.Tk()
top.title("Чат-комната")

message_frame = tk.Frame(top)
my_message = tk.StringVar()
my_message.set("")
scrollbar = tk.Scrollbar(message_frame)
message_listbox = tk.Listbox(message_frame, height=20, width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
message_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
message_frame.pack()

entry_field = tk.Entry(top, textvariable=my_message)
entry_field.bind("<Return>", send_message)
entry_field.pack()

send_button = tk.Button(top, text="Отправить", command=send_message)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = "localhost"
PORT = 12345
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

name = tkinter.simpledialog.askstring("Имя пользователя", "Введите ваше имя:")
client_socket.send(name.encode("utf8"))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

tk.mainloop()