import tkinter as tk

class TransactionsFrame(tk.Frame):
    """class that contains all transaction labels"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="white")
        self._transaction_labels = []

    def update_transactions(self, transactions=False, empty=False):
        """Updates the visual of the translistframe
        the two optional variables are symbolic, transactions means the list,
        empty is whether we have selected an account."""
        for tl in self._transaction_labels:
            tl.destroy()
        self._transaction_labels = []

        if empty:
            return
        
        if not transactions:
            tl = tk.Label(self, text="No transactions yet.  Make a deposit!", bg="white", fg="blue")
            tl.pack(anchor="w")
            self._transaction_labels.append(tl)

        else:
            title = tk.Label(self, text="Transactions:", bg="white", fg="blue")
            title.pack(anchor="w")
            self._transaction_labels.append(title)

        for trans in transactions:
            tl = tk.Label(self, text=str(trans), bg="white", fg="red")
            if trans.check_balance(0):
                tl.configure(fg="blue")
            if trans.is_exempt():
                tl.configure(font=("italic"))
            tl.pack(anchor='w')
            self._transaction_labels.append(tl)