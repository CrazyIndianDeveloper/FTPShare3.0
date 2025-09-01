# Author: Crazy Indian Developer (Vijay Mahajan)
# Date: 2025-09-01
# Description: GUI FTP server script using pyftpdlib for file sharing in local network
# Version: 3.0

import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
import threading
import socket

cwd = os.getcwd()


def update_textarea(message, color):
    def callback():
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, message)
        text_area.config(fg=color)
        text_area.config(state=tk.DISABLED)
        text_area.see(tk.END)

    root.after(0, callback)


def start_server():
    start_button.config(state=tk.DISABLED, fg="green")  # Change text color to green and disable start button
    stop_button.config(state=tk.NORMAL, fg="red")  # Enable stop button and change text color to red
    update_textarea("Server Started\n", "green")

    User = username.get()
    Upass = password.get()
    Uport = port_no.get()
    Udirectory = directory.get()

    authorizer = DummyAuthorizer()
    # adding User
    authorizer.add_user(User, Upass, Udirectory, perm="elradfmw")

    # Set up FTP handler
    handler = FTPHandler
    handler.authorizer = authorizer

    # Create FTP server
    root.server = FTPServer(("0.0.0.0", Uport), handler)

    # Starting server in separate thread
    def run_server():
        root.server.serve_forever()

    root.server_thread = threading.Thread(target=run_server)
    root.server_thread.start()
    root.running = True

    ip_list = []
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if not ip.startswith("127."):
            ip_list.append(ip)

    for ip in ip_list:
        # Update the text area
        update_textarea("FTPShare3.0 Server Started on ftp://" + ip + ":" + Uport + "\n", "green")


# Function to stop the FTP server
def stop_server():
    stop_button.config(state=tk.DISABLED, fg="red")  # Change text color to red and disable stop button
    start_button.config(state=tk.NORMAL, fg="green")  # Enable start button and reset text color to black
    update_textarea("Server Stopped\n", "red")

    if root.server:
        # Set running flag to False to stop the server
        root.running = False
        root.server.close_all()

        # root.server_thread.join() # <------ This Line Cause Trouble in Linux | taking too much time to close thread and freeze the application
        # Wait for the thread to finish
        # In Windows it works fine


# Function to browse for FTP folder
def browse_directory():
    folder_selected = filedialog.askdirectory()
    directory.config(state=tk.NORMAL)  # Enable the entry to insert the folder
    directory.delete(0, tk.END)
    directory.insert(0, folder_selected)
    directory.config(state=tk.DISABLED)


def on_closing():
    if messagebox.askokcancel("FTPShare 3.0", "Do you want to quit?"):
        root.destroy()
        root.running = False
        root.server.close_all()

        # stop_server()
        # exit()


root = tk.Tk()
root.title("FTPShare 3.0")
root.geometry("350x400")
root.resizable(False, False)

# Menubar
menubar = tk.Menu(root)

# Menu and commands
file = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='More Free Tools', menu=file)


def open_youtube():
    webbrowser.open(
        "https://www.youtube.com/channel/UCnij5U2Ic3PtpzCWmmydP7g?sub_confirmation=1")  # Opens YouTube in the default browser


def open_github():
    webbrowser.open("https://github.com/CrazyIndianDeveloper")  # Opens GitHub in the default browser


def open_instagram():
    webbrowser.open("https://www.instagram.com/crazy_indian_developer/")  # Opens Instagram in the default browser


def open_x():
    webbrowser.open("https://x.com/mahajan__vijay")  # Opens Twitter in the default browser


file.add_command(label='YouTube', command=open_youtube)
file.add_command(label='GitHub', command=open_github)
file.add_command(label='Instagram', command=open_instagram)
file.add_command(label='Twitter ( X )', command=open_x)
file.add_separator()
file.add_command(label='Crazy Indian Developer ( Vijay Mahajan )', command=None)

username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
username = tk.Entry(root, width=30)
username.grid(row=0, column=1, padx=10, pady=5)
username.insert(0, "user")  # Insert the default username here

password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
password = tk.Entry(root, show="*", width=30)
password.grid(row=1, column=1, padx=10, pady=5)
password.insert(0, "0000")  # default password

port_label = tk.Label(root, text="Port:")
port_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
port_no = tk.Entry(root, width=30)
port_no.grid(row=2, column=1, padx=10, pady=5)
port_no.insert(0, "2121")  # default port

# Create labels and entry widgets for FTP folder and log file
ftp_folder_label = tk.Label(root, text="FTP Folder:")
ftp_folder_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
directory = tk.Entry(root, width=30)
directory.grid(row=3, column=1, padx=10, pady=5)
directory.insert(0, cwd)  # default directory path
directory.config(state=tk.DISABLED)

browse_ftp_button = tk.Button(root, text="Browse Folder", command=browse_directory)
browse_ftp_button.grid(row=4, column=1, padx=10, pady=5)

#  Buttons
start_button = tk.Button(root, text="Start FTP Server", command=start_server, fg="green")
start_button.grid(row=5, column=0, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop FTP Server", command=stop_server, state=tk.DISABLED, fg="black")
stop_button.grid(row=5, column=1, padx=10, pady=10)

text_area = tk.Text(root, width=40, height=6, wrap=tk.WORD)
text_area.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

icon = tk.PhotoImage(file='ftp.png')
root.iconphoto(True, icon)
root.config(menu=menubar)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
