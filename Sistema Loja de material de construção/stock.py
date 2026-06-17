from tkinter import *
from tkinter import messagebox, ttk
from db_config import get_connection, init_db


class StockClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Sistema de faturamento e gerenciamento de faturas | Desenvolvido por Felipe Gomes")
        self.root.config(bg="Teal")
        self.root.focus_force()

        self.selected_pid = None

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_pid = StringVar()
        self.var_hsncode = StringVar()
        self.var_discount = StringVar()
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()

        self.sup_list = ["Selecione"]

        init_db()
        self.fetch_supplier()
        self.create_widgets()
        self.show_products()

    def create_tables(self):
        pass

    def fetch_supplier(self):
        con = None
        try:
            con = get_connection()
            cur = con.cursor()
            self.sup_list = ["Selecione"]
            cur.execute("SELECT name FROM supplier ORDER BY name")
            rows = cur.fetchall()
            for row in rows:
                self.sup_list.append(row[0])
        except Exception:
            pass
        finally:
            if con:
                con.close()

    def create_widgets(self):
        stock_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        stock_Frame.place(x=10, y=10, width=450, height=480)

        title = Label(
            stock_Frame,
            text="Detalhes do estoque",
            font=("goudy old style", 18, "bold"),
            bg="Teal",
            fg="white",
        )
        title.pack(side=TOP, fill=X)

        Label(stock_Frame, text="ID", font=("goudy old style", 15, "bold"), bg="white").place(x=30, y=60)
        Label(stock_Frame, text="Fornecedor", font=("goudy old style", 15, "bold"), bg="white").place(x=30, y=110)
        Label(stock_Frame, text="Produto", font=("goudy old style", 15, "bold"), bg="white").place(x=30, y=160)
        Label(stock_Frame, text="HSN", font=("goudy old style", 15, "bold"), bg="white").place(x=30, y=210)
        Label(stock_Frame, text="Preço", font=("goudy old style", 15, "bold"), bg="white").place(x=30, y=260)
        Label(stock_Frame, text="Quantidade", font=("goudy old style", 15, "bold"), bg="white").place(x=30, y=310)
        Label(stock_Frame, text="Desconto", font=("goudy old style", 15, "bold"), bg="white").place(x=30, y=360)

        Entry(stock_Frame, textvariable=self.var_pid, font=("goudy old style", 12), bg="white").place(x=150, y=60, width=280)

        self.cmb_sup = ttk.Combobox(
            stock_Frame,
            textvariable=self.var_sup,
            values=self.sup_list,
            state="readonly",
            justify=CENTER,
            font=("goudy old style", 12),
        )
        self.cmb_sup.place(x=150, y=110, width=280)
        self.cmb_sup.current(0)

        Entry(stock_Frame, textvariable=self.var_name, font=("goudy old style", 12), bg="white").place(x=150, y=160, width=280)
        Entry(stock_Frame, textvariable=self.var_hsncode, font=("goudy old style", 12), bg="white").place(x=150, y=210, width=280)
        Entry(stock_Frame, textvariable=self.var_price, font=("goudy old style", 12), bg="white").place(x=150, y=260, width=280)
        Entry(stock_Frame, textvariable=self.var_qty, font=("goudy old style", 12), bg="white").place(x=150, y=310, width=280)
        Entry(stock_Frame, textvariable=self.var_discount, font=("goudy old style", 12), bg="white").place(x=150, y=360, width=280)

        Button(stock_Frame, text="Salvar", command=self.add_product, font=("goudy old style", 15), bg="Olive", fg="white", bd=0, cursor="hand2").place(x=40, y=420, width=90, height=30)
        Button(stock_Frame, text="Atualizar", command=self.update_product, font=("goudy old style", 15), bg="Olive", fg="white", bd=0, cursor="hand2").place(x=140, y=420, width=90, height=30)
        Button(stock_Frame, text="Deletar", command=self.delete_product, font=("goudy old style", 15), bg="Olive", fg="white", bd=0, cursor="hand2").place(x=240, y=420, width=90, height=30)
        Button(stock_Frame, text="Limpar", command=self.clear_fields, font=("goudy old style", 15), bg="Olive", fg="white", bd=0, cursor="hand2").place(x=340, y=420, width=90, height=30)

        SearchFrame = LabelFrame(
            self.root,
            text="Pesquisar Produto",
            font=("goudy old style", 12),
            bg="Teal",
            bd=3,
            fg="white",
        )
        SearchFrame.place(x=480, y=10, width=600, height=80)

        self.cmb_search = ttk.Combobox(
            SearchFrame,
            textvariable=self.var_searchby,
            values=("Selecione", "Fornecedor", "Prod_Nome"),
            state="readonly",
            justify=CENTER,
            font=("goudy old style", 12),
        )
        self.cmb_search.place(x=10, y=10, width=180)
        self.cmb_search.current(0)

        self.search_map = {"Fornecedor": "Supplier", "Prod_Nome": "itemname"}

        Entry(
            SearchFrame,
            textvariable=self.var_searchtxt,
            font=("goudy old style", 15),
            bg="white",
            bd=1,
        ).place(x=200, y=10, width=180)

        Button(
            SearchFrame,
            text="Pesquisar",
            command=self.search_product,
            font=("goudy old style", 15, "bold"),
            bg="black",
            fg="white",
            bd=0,
            cursor="hand2",
        ).place(x=400, y=10, width=180, height=30)

        self.table_frame = Frame(self.root, bd=3, relief=RIDGE)
        self.table_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(self.table_frame, orient=VERTICAL)
        scrollx = Scrollbar(self.table_frame, orient=HORIZONTAL)

        self.StockTable = ttk.Treeview(
            self.table_frame,
            columns=("pid", "supplier", "itemname", "hsncode", "price", "qty", "discount"),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set,
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.StockTable.xview)
        scrolly.config(command=self.StockTable.yview)

        self.StockTable.heading("pid", text="ID")
        self.StockTable.heading("supplier", text="Fornecedor")
        self.StockTable.heading("itemname", text="Nome Prod")
        self.StockTable.heading("hsncode", text="HSN")
        self.StockTable.heading("price", text="Preço")
        self.StockTable.heading("qty", text="Quantidade")
        self.StockTable.heading("discount", text="Desconto")

        self.StockTable["show"] = "headings"

        self.StockTable.column("pid", width=90)
        self.StockTable.column("supplier", width=100)
        self.StockTable.column("itemname", width=120)
        self.StockTable.column("hsncode", width=100)
        self.StockTable.column("price", width=100)
        self.StockTable.column("qty", width=100)
        self.StockTable.column("discount", width=100)

        self.StockTable.pack(fill=BOTH, expand=1)
        self.StockTable.bind("<<TreeviewSelect>>", self.get_data)

    def show_products(self):
        con = None
        try:
            con = get_connection()
            cur = con.cursor()
            self.StockTable.delete(*self.StockTable.get_children())
            cur.execute("SELECT pid, Supplier, itemname, hsncode, price, qty, discount FROM stock ORDER BY pid")
            rows = cur.fetchall()

            for row in rows:
                self.StockTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao listar produtos: {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()

    def get_data(self, event=None):
        selected = self.StockTable.focus()
        if not selected:
            return

        values = self.StockTable.item(selected, "values")
        if not values:
            return

        self.selected_pid = values[0]
        self.var_pid.set(values[0])
        self.var_sup.set(values[1])
        self.var_name.set(values[2])
        self.var_hsncode.set(values[3])
        self.var_price.set(values[4])
        self.var_qty.set(values[5])
        self.var_discount.set(values[6])

    def validate_fields(self):
        if self.var_pid.get().strip() == "":
            messagebox.showerror("Erro", "O campo ID é obrigatório", parent=self.root)
            return False

        if self.var_sup.get().strip() == "" or self.var_sup.get().strip() == "Selecione":
            messagebox.showerror("Erro", "Selecione um fornecedor", parent=self.root)
            return False

        if self.var_name.get().strip() == "":
            messagebox.showerror("Erro", "O campo Produto é obrigatório", parent=self.root)
            return False

        return True

    def add_product(self):
        if not self.validate_fields():
            return

        con = None
        try:
            con = get_connection()
            cur = con.cursor()
            pid = self.var_pid.get().strip()

            cur.execute("SELECT pid FROM stock WHERE pid=?", (pid,))
            if cur.fetchone():
                messagebox.showerror("Erro", "ID do produto já existe", parent=self.root)
                return

            cur.execute(
                """
                INSERT INTO stock (pid, Supplier, itemname, hsncode, price, qty, discount)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.var_pid.get().strip(),
                    self.var_sup.get().strip(),
                    self.var_name.get().strip(),
                    self.var_hsncode.get().strip(),
                    self.var_price.get().strip(),
                    self.var_qty.get().strip(),
                    self.var_discount.get().strip(),
                ),
            )
            con.commit()

            messagebox.showinfo("Sucesso", "Produto salvo com sucesso", parent=self.root)
            self.show_products()
            self.clear_fields()

        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao salvar produto: {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()

    def update_product(self):
        if self.selected_pid is None:
            messagebox.showerror("Erro", "Selecione um produto na listagem para atualizar", parent=self.root)
            return

        if not self.validate_fields():
            return

        con = None
        try:
            con = get_connection()
            cur = con.cursor()
            new_pid = self.var_pid.get().strip()

            if new_pid != self.selected_pid:
                cur.execute("SELECT pid FROM stock WHERE pid=?", (new_pid,))
                if cur.fetchone():
                    messagebox.showerror("Erro", "Já existe outro produto com esse ID", parent=self.root)
                    return

            cur.execute(
                """
                UPDATE stock
                SET pid=?, Supplier=?, itemname=?, hsncode=?, price=?, qty=?, discount=?
                WHERE pid=?
                """,
                (
                    self.var_pid.get().strip(),
                    self.var_sup.get().strip(),
                    self.var_name.get().strip(),
                    self.var_hsncode.get().strip(),
                    self.var_price.get().strip(),
                    self.var_qty.get().strip(),
                    self.var_discount.get().strip(),
                    self.selected_pid,
                ),
            )
            con.commit()

            if cur.rowcount == 0:
                messagebox.showerror("Erro", "Nenhum produto foi atualizado", parent=self.root)
                return

            messagebox.showinfo("Sucesso", "Produto actualizado com sucesso", parent=self.root)
            self.show_products()
            self.selected_pid = new_pid

        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao atualizar produto: {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()

    def delete_product(self):
        if self.selected_pid is None:
            messagebox.showerror("Erro", "Selecione um produto na listagem para deletar", parent=self.root)
            return

        op = messagebox.askyesno("Confirmar", "Deseja realmente deletar este produto?", parent=self.root)
        if not op:
            return

        con = None
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute("DELETE FROM stock WHERE pid=?", (self.selected_pid,))
            con.commit()

            if cur.rowcount == 0:
                messagebox.showerror("Erro", "Nenhum produto foi deletado", parent=self.root)
                return

            messagebox.showinfo("Sucesso", "Produto deletado com sucesso", parent=self.root)
            self.show_products()
            self.clear_fields()

        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao deletar produto: {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()

    def clear_fields(self):
        self.var_pid.set("")
        self.var_sup.set("Selecione")
        self.var_name.set("")
        self.var_hsncode.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_discount.set("")
        self.var_searchby.set("Selecione")
        self.var_searchtxt.set("")
        self.selected_pid = None

        for item in self.StockTable.selection():
            self.StockTable.selection_remove(item)

    def search_product(self):
        if self.var_searchby.get() == "Selecione":
            messagebox.showerror("Erro", "Selecione o tipo de pesquisa", parent=self.root)
            return

        if self.var_searchtxt.get().strip() == "":
            messagebox.showerror("Erro", "Digite algo para pesquisar", parent=self.root)
            return

        con = None
        try:
            con = get_connection()
            cur = con.cursor()

            column_name = self.search_map.get(self.var_searchby.get())
            search_text = self.var_searchtxt.get().strip()

            self.StockTable.delete(*self.StockTable.get_children())

            query = f"""
                SELECT pid, Supplier, itemname, hsncode, price, qty, discount
                FROM stock
                WHERE {column_name} LIKE ?
                ORDER BY pid
            """
            cur.execute(query, ("%" + search_text + "%",))
            rows = cur.fetchall()

            for row in rows:
                self.StockTable.insert("", END, values=row)

            if len(rows) == 0:
                messagebox.showinfo("Resultado", "Nenhum registro encontrado", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Erro", f"Erro na pesquisa: {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()


if __name__ == "__main__":
    root = Tk()
    obj = StockClass(root)
    root.mainloop()