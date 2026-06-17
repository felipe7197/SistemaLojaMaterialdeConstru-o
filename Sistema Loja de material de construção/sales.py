from tkinter import *
from tkinter import messagebox
import os

import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1190x500+220+130")
        blank_space = " "
        self.root.title(110 * blank_space + "Sistema de faturamento e gerenciamento de faturas | Desenvolvido por Curso")
        self.root.focus_force()
        self.root.config(bg="#F5F5F5")

        self.bill_dir = "bill"
        self.bill_list = []
        self.var_invoice = StringVar()

        lbl_title = Label(
            self.root,
            text="Ver contas de clientes",
            font=("goudy old style", 16, "bold"),
            bg="#F5F5F5",
            fg="black",
            bd=0,
            relief=RIDGE
        )
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_invoice = Label(
            self.root,
            text="Numero Nota .",
            font=("goudy old style", 12),
            bg="#F5F5F5"
        )
        lbl_invoice.place(x=50, y=100)

        txt_invoice = Entry(
            self.root,
            textvariable=self.var_invoice,
            font=("goudy old style", 15),
            bg="white"
        )
        txt_invoice.place(x=160, y=100, width=180, height=28)

        btn_search = Button(
            self.root,
            text="Pesquisar",
            command=self.search,
            font=("goudy old style", 15, "bold"),
            bg="#722F37",
            fg="white",
            cursor="hand2"
        )
        btn_search.place(x=360, y=100, width=120, height=28)

        btn_clear = Button(
            self.root,
            text="Limpar",
            command=self.clear,
            font=("goudy old style", 15, "bold"),
            bg="#722F37",
            fg="white",
            cursor="hand2"
        )
        btn_clear.place(x=490, y=100, width=120, height=28)

        sales_frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_frame.place(x=50, y=140, width=200, height=300)

        scrolly = Scrollbar(sales_frame, orient=VERTICAL)

        self.sales_list = Listbox(
            sales_frame,
            font=("goudy old style", 15),
            bg="white",
            yscrollcommand=scrolly.set
        )
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH, expand=True)
        self.sales_list.bind("<ButtonRelease-1>", self.get_data)

        bill_frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_frame.place(x=280, y=140, width=600, height=300)

        lbl_title2 = Label(
            bill_frame,
            text="Área de fatura do cliente",
            font=("goudy old style", 20),
            bg="#722F37",
            fg="white",
            bd=3,
            relief=RIDGE
        )
        lbl_title2.pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(bill_frame, orient=VERTICAL)

        self.bill_area = Text(
            bill_frame,
            bg="white",
            yscrollcommand=scrolly2.set,
            font=("Courier New", 11)
        )
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        self.show()

    def show(self):
        self.sales_list.delete(0, END)
        self.bill_list.clear()

        try:
            if not os.path.exists(self.bill_dir):
                os.makedirs(self.bill_dir)

            for file in os.listdir(self.bill_dir):
                if file.endswith(".txt"):
                    self.bill_list.append(file)

            self.bill_list.sort(reverse=True)

            for item in self.bill_list:
                self.sales_list.insert(END, item)

        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao carregar faturas: {str(ex)}", parent=self.root)

    def get_data(self, ev=None):
        index_ = self.sales_list.curselection()
        if not index_:
            return

        file_name = self.sales_list.get(index_[0])
        self.bill_area.delete("1.0", END)

        try:
            file_path = os.path.join(self.bill_dir, file_name)
            with open(file_path, "r", encoding="utf-8") as fp:
                for line in fp:
                    self.bill_area.insert(END, line)
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a: {str(ex)}", parent=self.root)

    def search(self):
        invoice_no = self.var_invoice.get().strip()
        self.sales_list.delete(0, END)
        self.bill_area.delete("1.0", END)

        if invoice_no == "":
            self.show()
            return

        found = False
        try:
            if not os.path.exists(self.bill_dir):
                os.makedirs(self.bill_dir)

            for file in os.listdir(self.bill_dir):
                if file.endswith(".txt") and invoice_no in file:
                    self.sales_list.insert(END, file)
                    found = True

            if not found:
                messagebox.showinfo("Resultado", "Nenhuma fatura encontrada.", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao pesquisar: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_invoice.set("")
        self.bill_area.delete("1.0", END)
        self.show()


if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()