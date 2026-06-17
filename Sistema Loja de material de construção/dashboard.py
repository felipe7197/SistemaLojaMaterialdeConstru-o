from tkinter import *
from PIL import Image, ImageTk
from employeer import employeeClass
from supplier import supplierClass
from stock import StockClass
from sales import salesClass
from billing import billClass
from tkinter import messagebox
from db_config import get_connection, BILL_PATH
import os
import time
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class TBS:
    def __init__(self, root, login_window=None):
        self.root = root
        self.login_window = login_window

        self.width = 1310
        self.height = 720

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)

        self.root.title("Gomes materiais de construção")
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.config(bg="Teal")
        self.root.resizable(False, False)

        self.lbl_clock = None
        self.lbl_employee = None
        self.lbl_supplier = None
        self.lbl_sales = None
        self.lbl_product = None

        self.create_widgets()
        self.update_content()

        self.root.protocol("WM_DELETE_WINDOW", self.logout)

    def create_widgets(self):
        title = Label(self.root, text="GOMES MATERIAIS DE CONSTRUÇÃO", font=("Arial", 26, "bold"), bg="#c96f1a", fg="white", anchor="w", padx=90)
        title.place(x=0, y=0, relwidth=1, height=70)

        logo_box = Label(self.root, text="LOGO", font=("Arial", 14, "bold"), bg="white", fg="gray20", bd=2, relief=RIDGE)
        logo_box.place(x=10, y=10, width=65, height=50)

        btn_exit = Button(self.root, text="Sair", command=self.logout, font=("Arial", 12, "bold"), bg="white", fg="black", cursor="hand2")
        btn_exit.place(x=1210, y=18, width=80, height=32)

        self.lbl_clock = Label(self.root, text="Bem-vindo\t\t Data: DD-MM-YYYY\t\t Hora: HH:MM:SS", font=("Arial", 12), bg="white", fg="black")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        menu_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        menu_frame.place(x=10, y=102, width=200, height=560)

        self.menu_img = Image.open(resource_path("imagens/imagem2.png"))
        self.menu_img = self.menu_img.resize((176, 110), Image.LANCZOS)
        self.menu_img = ImageTk.PhotoImage(self.menu_img)

        lbl_menu_img = Label(menu_frame, image=self.menu_img, bd=2, relief=RIDGE, bg="white")
        lbl_menu_img.place(x=10, y=10, width=176, height=110)

        lbl_menu = Label(menu_frame, text="MENU", font=("Arial", 18, "bold"), bg="#5c1f2d", fg="white")
        lbl_menu.place(x=10, y=130, width=176, height=35)

        btn_user = Button(menu_frame, text="   >>   Usuário", font=("Arial", 14), bg="white", fg="black", bd=0, anchor="w", cursor="hand2", command=self.open_employee)
        btn_user.place(x=10, y=180, width=176, height=40)

        btn_supplier = Button(menu_frame, text="   >>   Fornecedor", command=self.supplier, font=("Arial", 14), bg="white", fg="black", bd=0, anchor="w", cursor="hand2")
        btn_supplier.place(x=10, y=220, width=176, height=40)

        btn_stock = Button(menu_frame, text="   >>   Estoque", font=("Arial", 14), command=self.stock, bg="white", fg="black", bd=0, anchor="w", cursor="hand2")
        btn_stock.place(x=10, y=260, width=176, height=40)

        btn_sales = Button(menu_frame, text="   >>   Vendas", command=self.sales, font=("Arial", 14), bg="white", fg="black", bd=0, anchor="w", cursor="hand2")
        btn_sales.place(x=10, y=300, width=176, height=40)

        btn_billing = Button(menu_frame, text="   >>   Cobrança", command=self.billing, font=("Arial", 14), bg="white", fg="black", bd=0, anchor="w", cursor="hand2")
        btn_billing.place(x=10, y=340, width=176, height=40)

        self.lbl_employee = Label(self.root, text="Funcionários\n[ 0 ]", bd=4, relief=RIDGE, bg="gray", fg="white", font=("Arial", 18, "bold"))
        self.lbl_employee.place(x=260, y=120, width=230, height=120)

        self.lbl_supplier = Label(self.root, text="Fornecedores\n[ 0 ]", bd=4, relief=RIDGE, bg="gray", fg="white", font=("Arial", 18, "bold"))
        self.lbl_supplier.place(x=560, y=120, width=230, height=120)

        self.lbl_sales = Label(self.root, text="Vendas\n[ 0 ]", bd=4, relief=RIDGE, bg="gray", fg="white", font=("Arial", 18, "bold"))
        self.lbl_sales.place(x=260, y=300, width=230, height=120)

        self.lbl_product = Label(self.root, text="Estoque\n[ 0 ]", bd=4, relief=RIDGE, bg="gray", fg="white", font=("Arial", 18, "bold"))
        self.lbl_product.place(x=560, y=300, width=230, height=120)

        footer = Label(self.root, text="Sistema de gerenciamento | Gomes materiais de construção", font=("Arial", 11), bg="#c96f1a", fg="white")
        footer.pack(side=BOTTOM, fill=X)

    def get_count(self, table_name):
        con = None
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            return cur.fetchone()[0]
        except Exception:
            return 0
        finally:
            if con:
                con.close()

    def update_content(self):
        try:
            emp_count = self.get_count("employee")
            sup_count = self.get_count("supplier")
            pro_count = self.get_count("stock")

            if os.path.exists(BILL_PATH):
                bill_count = len(os.listdir(BILL_PATH))
            else:
                bill_count = 0

            self.lbl_employee.config(text=f"Funcionários\n[ {emp_count} ]")
            self.lbl_supplier.config(text=f"Fornecedores\n[ {sup_count} ]")
            self.lbl_product.config(text=f"Estoque\n[ {pro_count} ]")
            self.lbl_sales.config(text=f"Vendas\n[ {bill_count} ]")

            time_ = time.strftime("%H:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Bem-vindo ao sistema\t\t Data: {date_}\t\t Hora: {time_}")

        except Exception as ex:
            messagebox.showerror("Erro", f"ERRO DEVIDO A: {str(ex)}", parent=self.root)

        self.root.after(1000, self.update_content)

    def open_employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def logout(self):
        self.root.destroy()
        if self.login_window:
            self.login_window.deiconify()

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def stock(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = StockClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def billing(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = billClass(self.new_win, self.login_window)


if __name__ == "__main__":
    root = Tk()
    obj = TBS(root)
    root.mainloop()