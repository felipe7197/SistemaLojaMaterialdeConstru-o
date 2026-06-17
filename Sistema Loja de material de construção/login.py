from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import sys

from dashboard import TBS
from billing import billClass


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de faturamento e gerenciamento de faturas")
        self.root.geometry("1100x700+100+50")
        self.root.config(bg="teal")
        self.root.resizable(False, False)

        title = Label(
            self.root,
            text="Sistema de faturamento e gerenciamento de faturas",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#0f4c5c",
            anchor="w",
            padx=15
        )
        title.place(x=0, y=0, relwidth=1, height=40)

        self.main_img = Image.open(resource_path("imagens/imagem1.png"))
        self.main_img = self.main_img.resize((380, 500), Image.LANCZOS)
        self.main_img = ImageTk.PhotoImage(self.main_img)

        lbl_img = Label(self.root, image=self.main_img, bd=0, bg="teal")
        lbl_img.place(x=180, y=120)

        login_frame = Frame(self.root, bg="white", bd=0, relief=RIDGE)
        login_frame.place(x=650, y=150, width=320, height=380)

        lbl_title = Label(login_frame, text="Sistema de login", font=("Arial", 24, "bold"), bg="white", fg="black")
        lbl_title.place(x=30, y=40)

        lbl_user = Label(login_frame, text="Usuário", font=("Arial", 12), bg="white", fg="gray20")
        lbl_user.place(x=30, y=110)

        self.employeeid = Entry(login_frame, font=("Arial", 12), bg="#f0f0f0", bd=0)
        self.employeeid.place(x=30, y=140, width=220, height=28)

        lbl_pass = Label(login_frame, text="Senha", font=("Arial", 12), bg="white", fg="gray20")
        lbl_pass.place(x=30, y=190)

        self.password = Entry(login_frame, font=("Arial", 12), bg="#f0f0f0", bd=0, show="*")
        self.password.place(x=30, y=220, width=220, height=28)

        btn_login = Button(
            login_frame,
            text="Entrar",
            command=self.login,
            font=("Arial", 11, "bold"),
            bg="black",
            fg="white",
            cursor="hand2",
            bd=0
        )
        btn_login.place(x=30, y=290, width=160, height=35)

    def login(self):
        con = sqlite3.connect(resource_path("tbs.db"))
        cur = con.cursor()
        try:
            if self.employeeid.get() == "" or self.password.get() == "":
                messagebox.showerror("Erro", "TODOS OS CAMPOS SÃO OBRIGATÓRIOS", parent=self.root)
                return

            cur.execute(
                "SELECT utype FROM employee WHERE eid=? AND pass=?",
                (self.employeeid.get(), self.password.get())
            )
            user = cur.fetchone()

            if user is None:
                messagebox.showerror("Erro", "NOME DE USUÁRIO/SENHA INVÁLIDA", parent=self.root)
                return

            self.root.withdraw()

            new_win = Toplevel(self.root)
            if user[0] == "Admin":
                TBS(new_win, self.root)
            else:
                billClass(new_win, self.root)

        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a: {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = Login_System(root)
    root.mainloop()