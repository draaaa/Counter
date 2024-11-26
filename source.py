# This code, upon execution, will create 3 folders/files - counter_main, counter_main/data, counter_main/config, and counter_main/config/config.txt
# (The directory should look like this - C:\Users\Username\counter_main)
# It can also save the results of your recorded intervals, also in .txt format.
# Also note that executing this code for the first time will throw an error. I might add a workaround so you aren't thrown an unnecessary error later.  
# Should work without error after you have executed it for the second time. If not, post an issue on the repo or something.

# If you do not feel comfortable with this, you are free to use previous versions of the code. The most recent version without file saving can be found via the link below
# https://raw.githubusercontent.com/draaaa/counter/801492f8cfbe1cc4e572335a3a46d806950040c5/source
# Simply paste the raw code into your preferred IDE/Editor, save, and execute as you normally would.

# Lastly, please ensure that you have the keyboard module installed. Unlike other modules that come with python, you must download the keyboard module manually.
# The link below is a relatively easy guide on how to install the keyboard module that I had created.
# https://github.com/draaaa/counter/wiki/Installing-the-Keyboard-Module
# If you need further clarification, your favorite AI/LLM will do you wonders.


# import modules
import keyboard
import tkinter as tk
import tkinter.messagebox
import os
import time

# define variables
count, etime, avg, sec, mnt, hr = 0, 0, 0, 0, 0, 0
timer_running = True  # flag to control timer
timer_started = False  # flag to prevent premature label updates

# hotkeys that are changeable based on the user's preference
startkey = None
endkey = None
try:
    file_path = os.path.expanduser('~/counter_main/config/config.txt')
    with open(file_path, 'r') as f:
        cfg_contents = f.readlines()
        for line in cfg_contents:
            if line.startswith('startkey'):
                startkey = line.split('=')[1].strip()
            if line.startswith('endkey'):
                endkey = line.split('=')[1].strip()
except FileNotFoundError:
    tkinter.messagebox.showinfo(
        'counter',
        'Config file not found - re-execute code')
    pass


# function to save data
def save_data():
    global count
    data_file = time.strftime('%Y-%m-%d %H_%M_%S') + '.txt'
    data = os.path.join(os.path.expanduser('~'), 'counter_main', 'data')
    with open(os.path.join(data, data_file), 'a') as file:
        file.write(
            f"{count} presses\ntotal time elapsed: {hr:02}:{mnt:02}:{sec:02}\naverage units per minute: {avg}"
        )
    tkinter.messagebox.showinfo(
        f"counter",
        f"{data_file} saved successfully"
    )


# function to update label
def update_label():
    (label.config(
        text=f"count: {count}\nTime: {hr:02}:{mnt:02}:{sec:02}"
    ))
    label.pack(pady=20)


# function to create the end label
def update_endlabel():
    global avg, count, etime, sec, mnt, hr
    etime = hr * 60 + mnt + sec / 60  # calculates elapsed time
    if etime > 0:
        avg = count / etime
    else:
        avg = 0
    label.config(
        text=f"{count} presses\ntotal time elapsed: {hr:02}:{mnt:02}:{sec:02}\naverage units per minute: {avg}"
    )
    save_prompt = tkinter.messagebox.askyesno(title=f"counter",
                                              message=f"Wanna save the results?")
    if save_prompt:
        save_data()
    else:
        pass


# function to structure timer
def update_time():
    global sec, mnt, hr
    if timer_running and timer_started:  # only update recorded time if timer is running
        sec += 1
        if sec == 60:
            sec = 0
            mnt += 1
        if mnt == 60:
            mnt = 0
            hr += 1
        # update label as time passes
        label.config(
            text=f"count: {count}\nTime: {hr:02}:{mnt:02}:{sec:02}")
    # function called again after 1000 ms
    root.after(1000,
               update_time)


# function to add to count upon key
def on_start_press(event):
    global count, timer_started
    count += 1
    timer_started = True  # timer starts when startkey is pressed
    update_label()


# function to end time interval and show endlabel
def on_end_press(event):
    global timer_running
    timer_running = False  # timer stops when endkey is pressed
    update_endlabel()


# ui window
root = tk.Tk()
root.title("counter")
root.geometry("350x135")  # ui resolution

# initial ui label, states key, creates folders
label = tk.Label(root,
                 text=f"press {startkey} to begin\npress {endkey} to end interval",
                 font=("Comic Sans MS", 14))  # creates beginning ui label
label.pack(pady=20)
user_directory = os.path.expanduser('~')
main_folder = os.path.join(user_directory, 'counter_main')
cfg_folder = os.path.join(main_folder, 'config')
data_folder = os.path.join(main_folder, 'data')
if not os.path.isdir(main_folder):
    os.makedirs(main_folder)  # creates main folder
    os.makedirs(cfg_folder)  # creates config folder
    os.makedirs(data_folder)  # creates data folder
    data_file = 'config.txt'  # creates config
    data = os.path.join(os.path.expanduser('~'), 'counter_main', 'config')
    with open(os.path.join(data, data_file), 'a') as file:
        file.write(
            f"startkey = insert\nendkey = escape"
            # creates the default config, modifiable through counter_main/config/config.txt
        )

# timer
root.after(1000,
           update_time)  # timer that begins upon startkey, shows in active label

# keypress handling
keyboard.on_press_key(startkey, on_start_press)
keyboard.on_press_key(endkey, on_end_press)

# ui main loop
root.mainloop()
