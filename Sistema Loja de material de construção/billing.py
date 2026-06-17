import os
import sys
import time
from time import strftime
from tkinter import *
from tkinter import messagebox, ttk
from db_config import get_connection, BILL_PATH, init_db


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


BILL_DIR = BILL_PATH


class billClass:
    def __init__(self, root, login_window=None):
        self.root = root
        self.login_window = login_window

        self.width = 1510
        self.height = 710
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)

        self.root.title("Sistema de Faturamento e Gerenciamento de Faturas")
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.config(bg="Teal")

        self.cart_list = []
        self.chk_print = 0
        self.last_bill_txt = ""

        self.var_search = StringVar()
        self.var_cname = StringVar()
        self.var_contact = StringVar()
        self.var_cal_input = StringVar()
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_hsncode = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar(value="1")
        self.var_stock = StringVar()
        self.var_discount = StringVar()

        self.total_sales = 0.0
        self.total_sgst = 0.0
        self.total_cgst = 0.0
        self.total_gst = 0.0
        self.total_invoice_amount = 0.0
        self.invoice = 0

        try:
            self.icon_title = PhotoImage(file=resource_path("imagens/tool.png"))
            self.compound_mod = LEFT
        except Exception:
            self.icon_title = None
            self.compound_mod = NONE

        os.makedirs(BILL_DIR, exist_ok=True)
        init_db()
        self.create_header()
        self.create_widgets()
        self.show()
        self.update_date_time()

    def create_header(self):
        title = Label(
            self.root,
            text="FLUXO DE CAIXA | VENDAS",
            image=self.icon_title,
            compound=self.compound_mod,
            font=("ARIEL", 40, "bold"),
            bg="chocolate",
            fg="white",
            anchor="w",
            padx=20,
        )
        title.place(x=0, y=0, relwidth=1, height=120)

        btn_logout = Button(
            self.root,
            text="Sair",
            command=self.logout,
            font=("ARIEL", 15, "bold"),
            bg="white",
            cursor="hand2",
        )
        btn_logout.place(x=1400, y=30, height=50, width=100)

        self.lbl_clock = Label(
            self.root,
            text="Bem-vindo...!!\t Data: DD-MM-YYYY\t\t Horas: HH:MM:SS",
            font=("ARIEL", 10, "bold"),
            bg="Teal",
            fg="yellow",
            borderwidth=1,
            relief="solid",
        )
        self.lbl_clock.place(x=0, y=120, relwidth=1, height=30)

    def safe_int(self, value, default=0):
        try:
            txt = str(value).strip().replace(",", ".")
            if txt == "":
                return default
            return int(float(txt))
        except Exception:
            return default

    def safe_float(self, value, default=0.0):
        try:
            txt = str(value).strip()
            txt = txt.replace("R$", "").replace("Rs.", "").replace("rs.", "")
            txt = txt.replace(",", ".").strip()
            if txt == "":
                return default
            return float(txt)
        except Exception:
            return default

    def create_widgets(self):
        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=155, width=410, height=545)

        pTitle = Label(ProductFrame1, text="Todos Produtos", font=("ARIEL", 15, "bold"), bg="black", fg="white")
        pTitle.pack(side=TOP, fill=X)

        SearchFrame = Frame(ProductFrame1, bg="white")
        SearchFrame.pack(side=TOP, fill=X, padx=5, pady=5)

        lbl_search_title = Label(SearchFrame, text="Pesquisar Produto por nome", font=("ARIEL", 11, "bold"), fg="green", bg="white")
        lbl_search_title.grid(row=0, column=0, sticky="w", pady=2)

        btn_show_all = Button(SearchFrame, text="Todos", command=self.show, font=("ARIEL", 10, "bold"), bg="black", fg="white", width=8)
        btn_show_all.grid(row=0, column=1, padx=5)

        lbl_prod_name = Label(SearchFrame, text="Prod nome", font=("ARIEL", 11, "bold"), fg="green", bg="white")
        lbl_prod_name.grid(row=1, column=0, sticky="w", pady=5)

        txt_search = Entry(SearchFrame, textvariable=self.var_search, font=("ARIEL", 11), bg="mistyrose", width=15)
        txt_search.grid(row=1, column=1, padx=2)

        btn_search = Button(SearchFrame, text="Pesquisar", command=self.search_product, font=("ARIEL", 10, "bold"), bg="black", fg="white", width=9)
        btn_search.grid(row=1, column=2, padx=2)

        TableFrame = Frame(ProductFrame1, bd=2, relief=RIDGE)
        TableFrame.pack(fill=BOTH, expand=1, padx=5, pady=5)

        scrollx = Scrollbar(TableFrame, orient=HORIZONTAL)
        scrolly = Scrollbar(TableFrame, orient=VERTICAL)

        self.product_Table = ttk.Treeview(
            TableFrame,
            columns=("pid", "itemname", "hsncode", "price", "qty", "discount"),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set,
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid", text="ID")
        self.product_Table.heading("itemname", text="Prod_Nome")
        self.product_Table.heading("hsncode", text="HSN")
        self.product_Table.heading("price", text="Preço")
        self.product_Table.heading("qty", text="Qtda")
        self.product_Table.heading("discount", text="Desc")
        self.product_Table["show"] = "headings"

        self.product_Table.column("pid", width=40, anchor="center")
        self.product_Table.column("itemname", width=120)
        self.product_Table.column("hsncode", width=70, anchor="center")
        self.product_Table.column("price", width=70, anchor="center")
        self.product_Table.column("qty", width=50, anchor="center")
        self.product_Table.column("discount", width=50, anchor="center")
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<<TreeviewSelect>>", self.get_data)

        lbl_note = Label(
            ProductFrame1,
            text="Nota: Insira 0 Quantidade para remover o produto do carrinho",
            font=("ARIEL", 8, "bold"),
            fg="red",
            bg="white",
            anchor="w",
        )
        lbl_note.pack(side=BOTTOM, fill=X, padx=5)

        MiddleFrame = Frame(self.root, bg="Teal")
        MiddleFrame.place(x=425, y=155, width=520, height=545)

        ClientFrame = Frame(MiddleFrame, bd=3, relief=RIDGE, bg="white")
        ClientFrame.place(x=0, y=0, width=520, height=75)

        cTitle = Label(ClientFrame, text="Detalhes Cliente", font=("ARIEL", 12, "bold"), bg="maroon", fg="white")
        cTitle.pack(side=TOP, fill=X)

        lbl_cname = Label(ClientFrame, text="Nome", font=("ARIEL", 11, "bold"), bg="white")
        lbl_cname.place(x=5, y=35)

        txt_cname = Entry(ClientFrame, textvariable=self.var_cname, font=("ARIEL", 11), bg="mistyrose", width=20)
        txt_cname.place(x=60, y=35)

        lbl_contact = Label(ClientFrame, text="Contato", font=("ARIEL", 11, "bold"), bg="white")
        lbl_contact.place(x=250, y=35)

        txt_contact = Entry(ClientFrame, textvariable=self.var_contact, font=("ARIEL", 11), bg="mistyrose", width=18)
        txt_contact.place(x=330, y=35)

        CalcCartFrame = Frame(MiddleFrame, bg="Teal")
        CalcCartFrame.place(x=0, y=80, width=520, height=340)

        CalcFrame = Frame(CalcCartFrame, bd=3, relief=RIDGE, bg="white")
        CalcFrame.place(x=0, y=0, width=245, height=335)

        txt_cal_input = Entry(
            CalcFrame,
            textvariable=self.var_cal_input,
            font=("ARIEL", 16, "bold"),
            width=14,
            bd=5,
            relief=GROOVE,
            justify=RIGHT,
        )
        txt_cal_input.grid(row=0, column=0, columnspan=4, padx=4, pady=5)

        btn_list = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("+", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("*", 3, 3),
            ("0", 4, 0), ("c", 4, 1), ("=", 4, 2), ("/", 4, 3),
        ]

        for text, row, col in btn_list:
            if text == "c":
                cmd = self.clear_cal
            elif text == "=":
                cmd = self.perform_cal
            else:
                cmd = lambda x=text: self.get_input(x)

            Button(
                CalcFrame,
                text=text,
                font=("ARIEL", 12, "bold"),
                command=cmd,
                width=4,
                height=2,
                bd=2,
                relief=RAISED,
            ).grid(row=row, column=col, padx=2, pady=2)

        CartFrame = Frame(CalcCartFrame, bd=3, relief=RIDGE, bg="white")
        CartFrame.place(x=250, y=0, width=270, height=335)

        self.cartTitle = Label(CartFrame, text="Carrinho  Total Produtos: [0]", font=("ARIEL", 10, "bold"), bg="maroon", fg="white")
        self.cartTitle.pack(side=TOP, fill=X)

        cart_scrollx = Scrollbar(CartFrame, orient=HORIZONTAL)
        cart_scrolly = Scrollbar(CartFrame, orient=VERTICAL)

        self.cart_Table = ttk.Treeview(
            CartFrame,
            columns=("pid", "itemname", "hsncode"),
            xscrollcommand=cart_scrollx.set,
            yscrollcommand=cart_scrolly.set,
        )

        cart_scrollx.pack(side=BOTTOM, fill=X)
        cart_scrolly.pack(side=RIGHT, fill=Y)
        cart_scrollx.config(command=self.cart_Table.xview)
        cart_scrolly.config(command=self.cart_Table.yview)

        self.cart_Table.heading("pid", text="ID")
        self.cart_Table.heading("itemname", text="Prod_Nome")
        self.cart_Table.heading("hsncode", text="HSN")
        self.cart_Table["show"] = "headings"

        self.cart_Table.column("pid", width=30, anchor="center")
        self.cart_Table.column("itemname", width=120)
        self.cart_Table.column("hsncode", width=60, anchor="center")
        self.cart_Table.pack(fill=BOTH, expand=1)
        self.cart_Table.bind("<<TreeviewSelect>>", self.get_cart_data)

        ItemEditFrame = Frame(MiddleFrame, bd=2, relief=RIDGE, bg="white")
        ItemEditFrame.place(x=0, y=420, width=520, height=125)

        lbl_pname = Label(ItemEditFrame, text="Pro_Nome", font=("ARIEL", 10, "bold"), bg="white")
        lbl_pname.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.txt_pname = Entry(ItemEditFrame, textvariable=self.var_pname, font=("ARIEL", 10), bg="mistyrose", width=20)
        self.txt_pname.grid(row=1, column=0, padx=5, pady=2)

        lbl_price = Label(ItemEditFrame, text="Preço Unidade", font=("ARIEL", 10, "bold"), bg="white")
        lbl_price.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.txt_price = Entry(ItemEditFrame, textvariable=self.var_price, font=("ARIEL", 10), bg="mistyrose", width=15)
        self.txt_price.grid(row=1, column=1, padx=5, pady=2)

        lbl_qty = Label(ItemEditFrame, text="Qtde", font=("ARIEL", 10, "bold"), bg="white")
        lbl_qty.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.txt_qty = Entry(ItemEditFrame, textvariable=self.var_qty, font=("ARIEL", 10), bg="mistyrose", width=10)
        self.txt_qty.grid(row=1, column=2, padx=5, pady=2)

        btn_clear_cart_item = Button(ItemEditFrame, text="Limpar", command=self.clear_cart, font=("ARIEL", 11, "bold"), bg="maroon", fg="white", width=12)
        btn_clear_cart_item.grid(row=2, column=0, padx=5, pady=10)

        btn_update_cart = Button(ItemEditFrame, text="+ | Atualizar carrinho", command=self.add_update_cart, font=("ARIEL", 11, "bold"), bg="maroon", fg="white", width=22)
        btn_update_cart.grid(row=2, column=1, columnspan=2, padx=5, pady=10)

        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billFrame.place(x=953, y=155, width=550, height=410)

        btitle = Label(billFrame, text="Área de fatura do cliente", font=("ARIEL", 15, "bold"), bg="Olive", fg="white")
        btitle.pack(side=TOP, fill=X)

        bill_scrolly = Scrollbar(billFrame, orient=VERTICAL)
        bill_scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=bill_scrolly.set, font=("Courier", 10))
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        bill_scrolly.config(command=self.txt_bill_area.yview)

        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billMenuFrame.place(x=953, y=565, width=550, height=135)

        Button(billMenuFrame, text="Gerar/Fatura", command=self.generate_bill, font=("ARIEL", 14, "bold"), bg="Olive", fg="white").place(x=15, y=10, width=200, height=45)
        Button(billMenuFrame, text="Limpar tudo", command=self.clear_all, font=("ARIEL", 14, "bold"), bg="Olive", fg="white").place(x=330, y=10, width=200, height=45)
        Button(billMenuFrame, text="Imprimir fatura", command=self.print_bill, font=("ARIEL", 14, "bold"), bg="Olive", fg="white").place(x=15, y=65, width=515, height=45)

    def get_input(self, num):
        self.var_cal_input.set(self.var_cal_input.get() + str(num))

    def clear_cal(self):
        self.var_cal_input.set("")

    def perform_cal(self):
        try:
            result = eval(self.var_cal_input.get())
            self.var_cal_input.set(str(result))
        except Exception:
            self.var_cal_input.set("Erro")

    def show(self):
        con = None
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute("SELECT pid, itemname, hsncode, price, qty, discount FROM stock ORDER BY pid DESC")
            rows = cur.fetchall()

            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert("", END, values=row)

        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao carregar produtos: {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()

    def search_product(self):
        con = None
        try:
            termo = self.var_search.get().strip()
            if termo == "":
                messagebox.showerror("Erro", "Digite o nome do produto para pesquisar", parent=self.root)
                return

            con = get_connection()
            cur = con.cursor()
            cur.execute(
                "SELECT pid, itemname, hsncode, price, qty, discount FROM stock WHERE itemname LIKE ? ORDER BY pid DESC",
                (f"%{termo}%",),
            )
            rows = cur.fetchall()

            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert("", END, values=row)

            if not rows:
                messagebox.showinfo("Não encontrado", "Nenhum produto correspondente!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a: {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()

    def get_data(self, ev=None):
        selected = self.product_Table.selection()
        if not selected:
            return

        item_id = selected[0]
        row = self.product_Table.item(item_id, "values")
        if not row:
            return

        self.var_pid.set(str(row[0]))
        self.var_pname.set("" if row[1] is None else str(row[1]))
        self.var_hsncode.set("" if row[2] is None else str(row[2]))
        self.var_price.set(str(row[3] if row[3] is not None else 0))
        self.var_stock.set(str(row[4] if row[4] is not None else 0))
        self.var_discount.set(str(row[5] if row[5] is not None else 0))
        self.var_qty.set("1")

    def get_cart_data(self, ev=None):
        selected = self.cart_Table.selection()
        if not selected:
            return

        item_id = selected[0]
        row = self.cart_Table.item(item_id, "values")
        if not row:
            return

        for item in self.cart_list:
            if str(item["pid"]) == str(row[0]):
                self.var_pid.set(str(item["pid"]))
                self.var_pname.set(str(item["itemname"]))
                self.var_hsncode.set(str(item["hsncode"]))
                self.var_price.set(f"{item['price']:.2f}")
                self.var_qty.set(str(item["qty"]))
                self.var_discount.set(str(item["discount"]))
                self.var_stock.set(str(item["stock"]))
                break

    def add_update_cart(self):
        if self.var_pid.get().strip() == "":
            messagebox.showerror("Erro", "Por favor selecione um produto", parent=self.root)
            return

        qty_input = self.safe_int(self.var_qty.get(), -1)
        price_input = self.safe_float(self.var_price.get(), -1)

        if qty_input < 0:
            messagebox.showerror("Erro", "Quantidade inválida", parent=self.root)
            return

        if price_input < 0:
            messagebox.showerror("Erro", "Preço inválido", parent=self.root)
            return

        con = None
        try:
            pid = self.safe_int(self.var_pid.get(), 0)

            con = get_connection()
            cur = con.cursor()
            cur.execute("SELECT qty, discount FROM stock WHERE pid=?", (pid,))
            db_data = cur.fetchone()

            if not db_data:
                messagebox.showerror("Erro", "Produto não encontrado no banco", parent=self.root)
                return

            stock_qty = self.safe_int(db_data[0], 0)
            discount = self.safe_float(db_data[1], 0.0)

            if qty_input > stock_qty:
                messagebox.showerror("Erro", "Quantidade indisponível no estoque", parent=self.root)
                return

            item_data = {
                "pid": pid,
                "itemname": self.var_pname.get().strip(),
                "hsncode": self.var_hsncode.get().strip(),
                "price": price_input,
                "qty": qty_input,
                "discount": discount,
                "stock": stock_qty,
            }

            index_ = -1
            for i, item in enumerate(self.cart_list):
                if item["pid"] == pid:
                    index_ = i
                    break

            if index_ != -1:
                if qty_input == 0:
                    del self.cart_list[index_]
                else:
                    self.cart_list[index_] = item_data
            else:
                if qty_input > 0:
                    self.cart_list.append(item_data)

            self.show_cart()
            self.refresh_bill_preview()
            self.clear_cart()

        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao adicionar item: {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()

    def show_cart(self):
        self.cart_Table.delete(*self.cart_Table.get_children())
        for row in self.cart_list:
            self.cart_Table.insert("", END, values=(row["pid"], row["itemname"], row["hsncode"]))
        self.cartTitle.config(text=f"Carrinho \t Total Produtos: [{len(self.cart_list)}]")

    def refresh_bill_preview(self):
        self.txt_bill_area.delete("1.0", END)
        self.txt_bill_area.insert(END, "\t\tPRÉVIA DA FATURA\n")
        self.txt_bill_area.insert(END, "*" * 60 + "\n")

        if self.var_cname.get().strip():
            self.txt_bill_area.insert(END, f"Cliente: {self.var_cname.get().strip()}\n")
        if self.var_contact.get().strip():
            self.txt_bill_area.insert(END, f"Contato: {self.var_contact.get().strip()}\n")

        self.txt_bill_area.insert(END, "*" * 60 + "\n")
        self.txt_bill_area.insert(END, "Nome_Prod\tHSN\tQtd\tPreço\tDesc\n")
        self.txt_bill_area.insert(END, "*" * 60 + "\n")

        total_preview = 0.0
        for row in self.cart_list:
            line_total = row["price"] * row["qty"]
            total_preview += line_total
            self.txt_bill_area.insert(
                END,
                f"{row['itemname'][:12]:12}\t{row['hsncode'][:8]:8}\t{row['qty']}\tR$ {line_total:.2f}\t{row['discount']:.0f}%\n"
            )

        self.txt_bill_area.insert(END, "*" * 60 + "\n")
        self.txt_bill_area.insert(END, f"Total parcial: R$ {total_preview:.2f}\n")

    def generate_bill(self):
        if not self.var_cname.get().strip() or not self.var_contact.get().strip():
            messagebox.showerror("Erro", "Detalhes do cliente são obrigatórios", parent=self.root)
            return

        if not self.cart_list:
            messagebox.showerror("Erro", "Adicione produtos ao carrinho", parent=self.root)
            return

        self.total_sales = 0.0
        for row in self.cart_list:
            self.total_sales += row["price"] * row["qty"]

        self.total_sgst = self.total_sales * 0.09
        self.total_cgst = self.total_sales * 0.09
        self.total_gst = self.total_sgst + self.total_cgst
        self.total_invoice_amount = self.total_sales + self.total_gst

        con = None
        try:
            con = get_connection()
            cur = con.cursor()

            self.bill_top()

            for row in self.cart_list:
                pid = row["pid"]
                name = row["itemname"]
                hsn = row["hsncode"]
                unit_price = row["price"]
                qty_sold = row["qty"]
                discount = row["discount"]

                cur.execute("SELECT qty FROM stock WHERE pid=?", (pid,))
                stock_row = cur.fetchone()

                if not stock_row:
                    raise Exception(f"Produto ID {pid} não encontrado no estoque")

                current_stock = self.safe_int(stock_row[0], 0)

                if qty_sold > current_stock:
                    raise Exception(f"Estoque insuficiente para o produto {name}")

                line_total = unit_price * qty_sold
                new_stock = current_stock - qty_sold

                self.txt_bill_area.insert(
                    END,
                    f"\n{name[:12]:12}\t{hsn[:8]:8}\t{qty_sold}\tR$ {line_total:.2f}\t{discount:.0f}%"
                )

                cur.execute("UPDATE stock SET qty=? WHERE pid=?", (new_stock, pid))

                cur.execute("""
                    INSERT INTO sales (
                        invoice_no, pid, itemname, hsncode, qty, unit_price, discount,
                        total, customer_name, customer_contact, sale_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(self.invoice),
                    pid,
                    name,
                    hsn,
                    qty_sold,
                    unit_price,
                    discount,
                    line_total,
                    self.var_cname.get().strip(),
                    self.var_contact.get().strip(),
                    time.strftime("%d/%m/%Y %H:%M:%S")
                ))

            self.bill_bottom()
            con.commit()

            txt_path = os.path.join(BILL_DIR, f"{self.invoice}.txt")
            with open(txt_path, "w", encoding="utf-8") as fp:
                fp.write(self.txt_bill_area.get("1.0", END))

            self.last_bill_txt = txt_path
            self.chk_print = 1

            messagebox.showinfo("Salvo", "A fatura foi gerada e a venda foi registrada com sucesso!", parent=self.root)

            self.cart_list.clear()
            self.show_cart()
            self.clear_cart()
            self.show()

        except Exception as ex:
            if con:
                con.rollback()
            messagebox.showerror("Erro", f"Erro ao gerar fatura: {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f"""
\t\tGOMES MATERIAIS DE CONSTRUÇÃO
\tRua sao joao da barra numero 312
\tTelefone: 464646465654
\tEmail: atendimento@gomes.com
{"*" * 60}
Nome Cliente: {self.var_cname.get()}
Tel No: {self.var_contact.get()}
Nota No: {self.invoice}\t\tData: {time.strftime("%d/%m/%Y")}
{"*" * 60}
Nome_Prod\t\tHSN\tQtd\tPreco\tDesconto
{"*" * 60}
        """
        self.txt_bill_area.delete("1.0", END)
        self.txt_bill_area.insert("1.0", bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp = f"""

{"*" * 60}
Total Vendas(A)\t\tR$ {self.total_sales:.2f}
Total Taxa(9%)\t\tR$ {self.total_sgst:.2f}
Total Servico(9%)\t\tR$ {self.total_cgst:.2f}
Total Bens_ser(18%)(B)\t\tR$ {self.total_gst:.2f}
Valor da Fatura(A+B)\t\tR$ {self.total_invoice_amount:.2f}
{"*" * 60}
        """
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_hsncode.set("")
        self.var_price.set("")
        self.var_qty.set("1")
        self.var_stock.set("")
        self.var_discount.set("")

    def clear_all(self):
        self.cart_list.clear()
        self.var_cname.set("")
        self.var_contact.set("")
        self.txt_bill_area.delete("1.0", END)
        self.cartTitle.config(text="Carrinho \t Total de produtos: [0]")
        self.var_search.set("")
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print = 0
        self.last_bill_txt = ""

    def update_date_time(self):
        time_time = strftime("%H:%M:%S")
        date_time = strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Bem-vindo...!!!\t Data: {date_time}\t Horas: {time_time}")
        self.lbl_clock.after(200, self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            try:
                if self.last_bill_txt and os.path.exists(self.last_bill_txt):
                    os.startfile(self.last_bill_txt)
                else:
                    messagebox.showerror("Erro", "Arquivo da fatura não encontrado!", parent=self.root)
            except Exception as ex:
                messagebox.showerror("Erro", f"Erro ao abrir impressão: {str(ex)}", parent=self.root)
        else:
            messagebox.showinfo("Imprimir", "Por favor, gere a fatura primeiro!", parent=self.root)

    def logout(self):
        self.root.destroy()
        if self.login_window:
            self.login_window.deiconify()


if __name__ == "__main__":
    root = Tk()
    obj = billClass(root)
    root.mainloop()