from tkinter import *
from tkinter import ttk, messagebox
import tkinter.ttk as ttk
import sqlite3

import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        blank_space = " "
        self.root.title(110 * blank_space + "Sistema de faturamento e gerenciamento de faturas")
        self.root.config(bg="Teal")
        self.root.focus_force()

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()

        SearchFrame = LabelFrame(
            self.root,
            text="Pesquisar Funcionarios",
            font=("goudy old style", 12),
            bg="Teal",
            fg="white"
        )
        SearchFrame.place(x=250, y=20, width=600, height=70)

        cmb_search = ttk.Combobox(
            SearchFrame,
            textvariable=self.var_searchby,
            values=("Selecione", "Email", "Nome", "Contato"),
            state="readonly",
            justify=CENTER,
            font=("goudy old style", 12)
        )
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        self.search_map = {
            "Email": "email",
            "Nome": "name",
            "Contato": "contact"
        }

        txt_search = Entry(
            SearchFrame,
            textvariable=self.var_searchtxt,
            font=("goudy old style", 15),
            bg="white",
            bd=3
        )
        txt_search.place(x=200, y=10, width=220)

        btn_search = Button(
            SearchFrame,
            text="Pesquisar",
            font=("goudy old style", 15, "bold"),
            bg="Green",
            fg="white",
            cursor="hand2"
        )
        btn_search.place(x=440, y=10, width=150, height=30)

        title = Label(
            self.root,
            text="Detalhes do funcionario",
            font=("goudy old style", 15, "bold"),
            bg="peru",
            fg="white",
            bd=3
        )
        title.place(x=50, y=100, width=1000)

        Label(self.root, text="Emp ID", font=("goudy old style", 14), bg="Teal", fg="white").place(x=50, y=150)
        Label(self.root, text="Sexo", font=("goudy old style", 14), bg="Teal", fg="white").place(x=370, y=150)
        Label(self.root, text="Contato", font=("goudy old style", 14), bg="Teal", fg="white").place(x=750, y=150)

        Entry(self.root, textvariable=self.var_emp_id, font=("ARIEL", 14), bg="white").place(x=150, y=150, width=180)
        Entry(self.root, textvariable=self.var_gender, font=("ARIEL", 14), bg="white").place(x=450, y=150, width=180)
        Entry(self.root, textvariable=self.var_contact, font=("ARIEL", 14), bg="white").place(x=850, y=150, width=180)

        Label(self.root, text="Nome", font=("goudy old style", 14), bg="Teal", fg="white").place(x=50, y=190)
        Label(self.root, text="D_Nac", font=("goudy old style", 14), bg="Teal", fg="white").place(x=370, y=190)
        Label(self.root, text="D_Emp", font=("goudy old style", 14), bg="Teal", fg="white").place(x=750, y=190)

        Entry(self.root, textvariable=self.var_name, font=("ARIEL", 14), bg="white").place(x=150, y=190, width=180)
        Entry(self.root, textvariable=self.var_dob, font=("ARIEL", 14), bg="white").place(x=450, y=190, width=180)
        Entry(self.root, textvariable=self.var_doj, font=("ARIEL", 14), bg="white").place(x=850, y=190, width=180)

        Label(self.root, text="Email", font=("goudy old style", 14), bg="Teal", fg="white").place(x=50, y=230)
        Label(self.root, text="Senha", font=("goudy old style", 14), bg="Teal", fg="white").place(x=370, y=230)
        Label(self.root, text="Usuario", font=("goudy old style", 14), bg="Teal", fg="white").place(x=750, y=230)

        Entry(self.root, textvariable=self.var_email, font=("ARIEL", 14), bg="white").place(x=150, y=230, width=180)
        Entry(self.root, textvariable=self.var_pass, font=("ARIEL", 14), bg="white").place(x=450, y=230, width=180)

        cmb_utype = ttk.Combobox(
            self.root,
            textvariable=self.var_utype,
            values=("Admin", "Funcionario"),
            state="readonly",
            justify=CENTER,
            font=("goudy old style", 12)
        )
        cmb_utype.place(x=850, y=230, width=180)
        cmb_utype.current(0)

        Label(self.root, text="Address", font=("goudy old style", 14), bg="Teal", fg="white").place(x=50, y=270)

        self.txt_address = Text(self.root, font=("ARIEL", 14), bg="white")
        self.txt_address.place(x=150, y=280, width=300, height=60)

        Button(self.root, text="Salvar", command=self.add, font=("goudy old style", 15), bg="#722F37", fg="white", bd=0, cursor="hand2").place(x=500, y=330, width=110, height=28)

        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=380, relwidth=1, height=120)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(
            emp_frame,
            columns=("eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address"),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("eid", text="EMP ID")
        self.EmployeeTable.heading("name", text="Nome")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Sexo")
        self.EmployeeTable.heading("contact", text="Contato")
        self.EmployeeTable.heading("dob", text="Data Nasc")
        self.EmployeeTable.heading("doj", text="Data Contrato")
        self.EmployeeTable.heading("pass", text="Senha")
        self.EmployeeTable.heading("utype", text="Tipo Usuario")
        self.EmployeeTable.heading("address", text="Endereco")

        self.EmployeeTable["show"] = "headings"
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def add(self):
        con = sqlite3.connect(database=r"tbs.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Erro", "ID do funcionário necessária", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()

                if row is not None:
                    messagebox.showerror("Erro", "Esta ID de funcionário já foi atribuída, tente uma ID diferente", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO employee (eid, name, email, gender, contact, dob, doj, pass, utype, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            self.var_emp_id.get(),
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_pass.get(),
                            self.var_utype.get(),
                            self.txt_address.get('1.0', END).strip()
                        )
                    )
                    con.commit()
                    messagebox.showinfo("Sucesso", "Funcionário adicionado com sucesso", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r"tbs.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        content = self.EmployeeTable.item(f)
        row = content['values']

        if not row:
            return

        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END, row[9])


if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()