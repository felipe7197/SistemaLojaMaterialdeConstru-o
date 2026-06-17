from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        blank_space = " "
        self.root.title(110 * blank_space + "Sistema de faturamento e gerenciamento de faturas | Desenvolvido por Curso")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_supdate = StringVar()

        self.create_table()
        self.create_widgets()
        self.show()

    def db_connect(self):
        return sqlite3.connect("tbs.db")

    def create_table(self):
        con = self.db_connect()
        cur = con.cursor()
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS supplier (
                    invoice TEXT PRIMARY KEY,
                    name TEXT,
                    contact TEXT,
                    supdate TEXT
                )
            """)
            con.commit()
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao criar tabela: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def create_widgets(self):
        lbl_search = Label(
            self.root,
            text="Numero Fiscal .",
            bg="white",
            font=("goudy old style", 12)
        )
        lbl_search.place(x=690, y=80)

        txt_search = Entry(
            self.root,
            textvariable=self.var_searchtxt,
            font=("goudy old style", 15),
            bg="white",
            bd=1
        )
        txt_search.place(x=800, y=80, width=160)

        btn_search = Button(
            self.root,
            text="Pesquisar",
            command=self.search,
            font=("goudy old style", 15, "bold"),
            bg="#722F37",
            fg="white",
            bd=3,
            cursor="hand2"
        )
        btn_search.place(x=980, y=79, width=100, height=28)

        title = Label(
            self.root,
            text="Detalhes do fornecedor",
            font=("goudy old style", 15, "bold"),
            bg="Teal",
            fg="white",
            bd=3
        )
        title.place(x=50, y=10, width=1000, height=40)

        lbl_supplier_invoice = Label(
            self.root,
            text="Numero Fiscal .",
            font=("goudy old style", 14),
            bg="white"
        )
        lbl_supplier_invoice.place(x=50, y=80)

        txt_supplier_invoice = Entry(
            self.root,
            textvariable=self.var_sup_invoice,
            font=("Arial", 14),
            bg="white"
        )
        txt_supplier_invoice.place(x=180, y=80, width=180)

        lbl_name = Label(
            self.root,
            text="Nome",
            font=("goudy old style", 14),
            bg="white"
        )
        lbl_name.place(x=50, y=120)

        txt_name = Entry(
            self.root,
            textvariable=self.var_name,
            font=("Arial", 14),
            bg="white"
        )
        txt_name.place(x=180, y=120, width=180)

        lbl_contact = Label(
            self.root,
            text="Contato",
            font=("goudy old style", 14),
            bg="white"
        )
        lbl_contact.place(x=50, y=160)

        txt_contact = Entry(
            self.root,
            textvariable=self.var_contact,
            font=("Arial", 14),
            bg="white"
        )
        txt_contact.place(x=180, y=160, width=180)

        lbl_supdate = Label(
            self.root,
            text="Data",
            font=("goudy old style", 14),
            bg="white"
        )
        lbl_supdate.place(x=50, y=200)

        txt_supdate = Entry(
            self.root,
            textvariable=self.var_supdate,
            font=("Arial", 14),
            bg="white"
        )
        txt_supdate.place(x=180, y=200, width=180)

        btn_add = Button(
            self.root,
            text="Salvar",
            command=self.add,
            font=("goudy old style", 15),
            bg="#722F37",
            fg="white",
            cursor="hand2"
        )
        btn_add.place(x=180, y=370, width=100, height=35)

        btn_update = Button(
            self.root,
            text="Atualizar",
            command=self.update,
            font=("goudy old style", 15),
            bg="#722F37",
            fg="white",
            cursor="hand2"
        )
        btn_update.place(x=300, y=370, width=100, height=35)

        btn_delete = Button(
            self.root,
            text="Deletar",
            command=self.delete,
            font=("goudy old style", 15),
            bg="#722F37",
            fg="white",
            cursor="hand2"
        )
        btn_delete.place(x=420, y=370, width=100, height=35)

        btn_clear = Button(
            self.root,
            text="Limpar",
            command=self.clear,
            font=("goudy old style", 15),
            bg="#722F37",
            fg="white",
            cursor="hand2"
        )
        btn_clear.place(x=540, y=370, width=100, height=35)

        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=700, y=120, width=380, height=350)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.supplierTable = ttk.Treeview(
            emp_frame,
            columns=("invoice", "name", "contact", "supdate"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice", text="Nota .")
        self.supplierTable.heading("name", text="Nome")
        self.supplierTable.heading("contact", text="Contato")
        self.supplierTable.heading("supdate", text="Data Atualizacao")

        self.supplierTable["show"] = "headings"

        self.supplierTable.column("invoice", width=90)
        self.supplierTable.column("name", width=100)
        self.supplierTable.column("contact", width=100)
        self.supplierTable.column("supdate", width=120)

        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)

    def add(self):
        con = self.db_connect()
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Erro", "Numero fiscal é obrigatório", parent=self.root)
                return

            cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
            row = cur.fetchone()

            if row is not None:
                messagebox.showerror("Erro", "Este número fiscal já existe", parent=self.root)
            else:
                cur.execute(
                    "INSERT INTO supplier (invoice, name, contact, supdate) VALUES (?, ?, ?, ?)",
                    (
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.var_supdate.get()
                    )
                )
                con.commit()
                messagebox.showinfo("Sucesso", "Fornecedor adicionado com sucesso", parent=self.root)
                self.show()
                self.clear()
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = self.db_connect()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())

            for row in rows:
                self.supplierTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.supplierTable.focus()
        content = self.supplierTable.item(f)
        row = content["values"]

        if not row:
            return

        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.var_supdate.set(row[3])

    def update(self):
        con = self.db_connect()
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Erro", "Selecione um fornecedor para atualizar", parent=self.root)
                return

            cur.execute(
                "UPDATE supplier SET name=?, contact=?, supdate=? WHERE invoice=?",
                (
                    self.var_name.get(),
                    self.var_contact.get(),
                    self.var_supdate.get(),
                    self.var_sup_invoice.get()
                )
            )
            con.commit()
            messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = self.db_connect()
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Erro", "Selecione um fornecedor para deletar", parent=self.root)
                return

            op = messagebox.askyesno("Confirmar", "Deseja realmente deletar este fornecedor?", parent=self.root)
            if op:
                cur.execute("DELETE FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                con.commit()
                messagebox.showinfo("Sucesso", "Fornecedor deletado com sucesso", parent=self.root)
                self.show()
                self.clear()
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_searchtxt.set("")
        self.var_sup_invoice.set("")
        self.var_contact.set("")
        self.var_name.set("")
        self.var_supdate.set("")

    def search(self):
        con = self.db_connect()
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Erro", "Digite o número fiscal para pesquisar", parent=self.root)
                return

            cur.execute(
                "SELECT * FROM supplier WHERE invoice LIKE ?",
                ('%' + self.var_searchtxt.get() + '%',)
            )
            rows = cur.fetchall()

            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert("", END, values=row)

            if len(rows) == 0:
                messagebox.showinfo("Resultado", "Nenhum registro encontrado", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a: {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()