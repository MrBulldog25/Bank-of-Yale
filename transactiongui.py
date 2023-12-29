import tkinter as tk
from tkinter import messagebox
from decimal import Decimal
from datetime import datetime, date
from exceptions import TransactionLimitError, TransactionSequenceError
import logging

class TransactionGUI(tk.Frame):
    """where transactions are added"""
    def __init__(self, parent, bank, alf, callback, callback2, session, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="white")
        
        self._bank = bank
        self._alf = alf
        self._callback = callback
        self._callback2 = callback2
        self._session = session

        self._amt = tk.StringVar(self)
        self._amt2 = 0

        self.currentaccount = self._alf.selected_account

        self._amt.trace("w", self._isvalid)

        self._amt_label = tk.Label(self, text="Amount: ", bg="white", fg="blue")
        self._amt_label.pack(anchor="w")
        self._amt_entry = tk.Entry(self, textvariable=self._amt, font=("Times New Roman", 14), bg="white", fg="black", highlightbackground="black")
        self._amt_entry.pack(anchor="w")
        
        self._tdate = tk.StringVar(self)
        self._tdate2 = None
        self._tdate.trace("w", self._isvalid)

        self._date_label = tk.Label(self, text="Date (YYYY-MM-DD): ", bg="white", fg="blue")
        self._date_label.pack(anchor="w")
        self._date_entry = tk.Entry(self, textvariable=self._tdate, font=("Times New Roman", 14), bg="white", fg="black", highlightbackground="black")
        self._date_entry.pack(anchor="w")

        self._execute_transaction = tk.Button(self, text="add transaction", command=self._transaction_add)

    def _upDATE(self):
        """checks the earliest possible transaction date"""
        if self.currentaccount and self.currentaccount.get_transactions():
            t = max(self.currentaccount.get_transactions())
            return t.date
        else:
            return date(1000,1,1)

    def _isvalid(self, a, b, c):
        """every time one of the text boxes is updated this is called, if both fields are valid
        then the button to add the transaction pops up."""
        amt = self._amt.get()
        currentaccount = self.currentaccount
        validamt = False
        try:
            self._amt2 = Decimal(amt)
            balance = currentaccount.get_balance()
            if self._amt2 >= 0:
                validamt = True
                self._amt_entry.configure(bg="lightblue")
            else:
                if balance + self._amt2 >= 0:
                    validamt = True
                    self._amt_entry.configure(bg="lightblue")
                else:
                    validamt = False
                    self._amt_entry.configure(bg="red")
        except Exception:
            validamt = False
            self._amt_entry.configure(bg="red")
        latedate = self._upDATE()
        valiDate = False
        try:
            self._tdate2 = datetime.strptime(self._tdate.get(), '%Y-%m-%d').date()
            if self._tdate2 < latedate:
                valiDate = False
                self._date_entry.configure(bg="red")
            else:
                valiDate = True
                self._date_entry.configure(bg="lightblue")
        except Exception:
            valiDate = False
            self._date_entry.configure(bg="red")

        if valiDate and validamt:
            self._execute_transaction.pack(anchor="w")
        else:
            self._execute_transaction.pack_forget()

    def _transaction_add(self):
        """add a transaction"""
        try:
            self.currentaccount.add_transaction(self._amt2, self._tdate2, self._session, False)
            self._session.commit()
            logging.debug("Saved to bank.db")
            self._callback()
            self._callback2()
        except TransactionLimitError as ex:
            messagebox.showerror("Error",
                f"This transaction could not be completed because this account already has {ex.limit} transactions in this {ex.limit_type}.")
        except TransactionSequenceError as ex:
            messagebox.showerror("Error",
                                 "This transaction is out of sequence.")


        



