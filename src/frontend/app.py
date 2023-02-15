import datetime
import sys, os.path
be_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/backend/')
sys.path.append(be_dir)
from rc4 import rc4

# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Checkbutton, filedialog, messagebox
import tkinter as tk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../img")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def App(screen=None):
    if (screen != None):
        screen.destroy()
    global window
    window = Tk()
    window.title("My Own Stream Cipher")
    window.geometry("900x600")
    window.configure(bg = "#F8EFD3")

    # true ketika encrypt file selain txt
    global is_file, byte_file, file_path
    is_file = False

    canvas = Canvas(
        window,
        bg = "#F8EFD3",
        height = 600,
        width = 900,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    # judul
    canvas.place(x = 0, y = 0)
    image_title = PhotoImage(
        file=relative_to_assets("title.png"))
    title = canvas.create_image(
        449.0,
        43.0,
        image=image_title
    )

    # navigation bar
    image_bar = PhotoImage(
        file=relative_to_assets("bar.png"))
    bar = canvas.create_image(
        95.0,
        305.0,
        image=image_bar
    )

    # input label
    image_input = PhotoImage(
        file=relative_to_assets("input.png"))
    input = canvas.create_image(
        105.0,
        100.0,
        image=image_input
    )

    def select_plain_file():
        global is_file, file_path
        file_path = filedialog.askopenfilename(initialdir = Path(__file__),)
        ext = file_path.split(".")[-1]
        content = file_path
        if ext == "txt":
            is_file = False
            with open(file_path, "r") as file:
                content = file.read()
        else:
            is_file = True
        entry_input.delete("1.0", tk.END)
        entry_input.insert("1.0", content)

    # choose file button
    button_choose = PhotoImage(
        file=relative_to_assets("choose.png"))
    choose = Button(
        image=button_choose,
        borderwidth=0,
        highlightthickness=0,
        command=select_plain_file,
        relief="flat"
    )
    # posisi tombol choose file
    choose.place(
        x=147.0,
        y=80.0,
        width=140.0,
        height=40.0
    )

    # kolom input
    entry_input_column = PhotoImage(
        file=relative_to_assets("input_column.png"))
    entry_bg_input_column = canvas.create_image(
        497.0,
        165.0,
        image=entry_input_column
    )
    # format kolom input
    entry_input = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    # posisi kolom input
    entry_input.place(
        x=147.0,
        y=130.0,
        width=700.0,
        height=68.0
    )

    # key label
    image_key = PhotoImage(
        file=relative_to_assets("key.png"))
    key = canvas.create_image(
        113.0,
        245.0,
        image=image_key
    )

    # key column
    entry_key_column = PhotoImage(
        file=relative_to_assets("key_column.png"))
    entry_bg_key_column = canvas.create_image(
        497.0,
        265.0,
        image=entry_key_column
    )
    # format kolom key
    entry_key = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    # posisi kolom key
    entry_key.place(
        x=147.0,
        y=230.0,
        width=700.0,
        height=68.0
    )

    # checkbox string format
    is_string_format = tk.IntVar()
    check = Checkbutton(
            window,
            anchor = "nw",
            bg = "#F8EFD3",
            variable=is_string_format
        )
    # posisi checkbox
    check.pack()
    check.place(
        x = 155.0,
        y = 311.0
    )

    # string format check
    image_string_format = PhotoImage(
        file=relative_to_assets("string_format.png"))
    string_foramt = canvas.create_image(
        268.0,
        324.0,
        image=image_string_format
    )

    def encrypt():
        global byte_file, is_file
        # plain teks
        plain_teks = entry_input.get('1.0', 'end')
        key = entry_key.get('1.0', 'end')
        if key == '\n':
            tk.messagebox.showwarning(message="Keynya jangan kosong, hadeh")
            return
        if is_string_format.get():
            tk.messagebox.showwarning(message="RC4 encryption does not support string output")
            return
        # case kalau dia sudah pilih file
        # dan yang diencrypt bukan file tersebut
        if is_file and plain_teks.replace("\n", "") != file_path:
            is_file = False
        r = rc4()
        if is_file:
            if "/" in plain_teks:
                split = plain_teks.split("/")
            elif "\\" in plain_teks:
                split = plain_teks.split("\\")
            filename_with_ext = split[-1]
            split_plain_filename = filename_with_ext.split(".")
            split_plain_filename[0] += "-e"
            split[-1] = ".".join(split_plain_filename)
            if "/" in plain_teks:
                fileout = "/".join(split)
            elif "\\" in plain_teks:
                fileout = "\\".join(split)
            plain_teks = plain_teks.replace("\n", "")
            fileout = fileout.replace("\n", "")
            byte_file = r.encrypt_file(plain_teks, key)
            result = fileout
        else:
            result = r.encrypt(plain_teks, key)
        entry_output.delete("1.0", tk.END)
        entry_output.insert("1.0", result)

    # encrypt button
    button_encrypt = PhotoImage(
        file=relative_to_assets("encrypt.png"))
    encrypt = Button(
        image=button_encrypt,
        borderwidth=0,
        highlightthickness=0,
        command=encrypt,
        relief="flat"
    )
    # posisi tombol encrypt
    encrypt.place(
        x=147.0,
        y=350.0,
        width=140.0,
        height=40.0
    )

    def decrypt():
        global byte_file, is_file
        # plain teks
        plain_teks = entry_input.get('1.0', 'end')
        key = entry_key.get('1.0', 'end')
        if key == '\n':
            tk.messagebox.showwarning(message="Keynya jangan kosong, hadeh")
            return
        # case kalau dia sudah pilih file
        # dan yang diencrypt bukan file tersebut
        if is_file and plain_teks.replace("\n", "") != file_path:
            is_file = False
        r = rc4()
        try:
            if is_file:
                if "/" in plain_teks:
                    split = plain_teks.split("/")
                elif "\\" in plain_teks:
                    split = plain_teks.split("\\")
                filename_with_ext = split[-1]
                split_plain_filename = filename_with_ext.split(".")
                split_plain_filename[0] += "-d"
                split[-1] = ".".join(split_plain_filename)
                if "/" in plain_teks:
                    fileout = "/".join(split)
                elif "\\" in plain_teks:
                    fileout = "\\".join(split)
                plain_teks = plain_teks.replace("\n", "")
                fileout = fileout.replace("\n", "")
                byte_file = r.decrypt_file(plain_teks, key)
                result = fileout
            else:
                result = r.decrypt(plain_teks, key, is_string_format.get())
        except:
            tk.messagebox.showwarning(message="Invalid base64 string")
            return
        entry_output.delete("1.0", tk.END)
        entry_output.insert("1.0", result)

    # decrypt button
    button_decrypt = PhotoImage(
        file=relative_to_assets("decrypt.png"))
    decrypt = Button(
        image=button_decrypt,
        borderwidth=0,
        highlightthickness=0,
        command=decrypt,
        relief="flat"
    )
    # posisi tombol decrypt
    decrypt.place(
        x=324.0,
        y=350.0,
        width=140.0,
        height=40.0
    )

    # default message
    image_default_message = PhotoImage(
        file=relative_to_assets("default_message.png"))
    default_message = canvas.create_image(
        261.0,
        420.0,
        image=image_default_message
    )

    # output label
    image_output = PhotoImage(
        file=relative_to_assets("output.png"))
    output = canvas.create_image(
        96.0,
        445.0,
        image=image_output
    )

    # kolom output
    entry_output_column = PhotoImage(
        file=relative_to_assets("output_column.png"))
    entry_bg_output_column = canvas.create_image(
        497.0,
        465.0,
        image=entry_output_column
    )
    entry_output = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_output.place(
        x=147.0,
        y=430.0,
        width=700.0,
        height=68.0
    )

    def save_file():
        file_content = entry_output.get('1.0', 'end').replace("\n", "")
        if is_file:
            with open(file_content, "wb") as file:
                file.write(bytes(byte_file))
        else:
            filename = "rc4-" + datetime.datetime.now().strftime("%H%M%S-%Y%m%d") + ".txt"
            with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/download/' + filename, "w") as file:
                file.write(file_content)

    # download button
    button_download = PhotoImage(
        file=relative_to_assets("download.png"))
    download = Button(
        image=button_download,
        borderwidth=0,
        highlightthickness=0,
        command=save_file,
        relief="flat"
    )
    download.place(
        x=147.0,
        y=510.0,
        width=140.0,
        height=40.0
    )

    image_credit = PhotoImage(
        file=relative_to_assets("credit.png"))
    credit = canvas.create_image(
        778.0,
        580.0,
        image=image_credit
    )
    window.resizable(False, False)
    window.mainloop()
if __name__ == "__main__":
    App()
