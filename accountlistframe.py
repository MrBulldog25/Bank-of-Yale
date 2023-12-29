import tkinter as tk
import logging

class AccountListFrame(tk.Frame):
    """includes the list of all accounts."""
    def __init__(self, parent, bank, session, tlframe, **kwargs):
        super().__init__(parent, **kwargs)
        self._bank = bank
        self._session = session
        self.selected_account = None
        self._tlframe = tlframe
        self.configure(bg="white")

        title_label = tk.Label(self, text="List of accounts:", font=("Comic Sans", 14), bg="white", fg="blue")
        title_label.pack(pady=10)

        self._buttons = []
        self.alist_maker()

    def alist_maker(self):
        """makes the list of accounts."""
        for rad in self._buttons:
            rad.destroy()
        self._buttons = []
        accounts = self._bank.show_accounts()

        for account in accounts:
            rad = tk.Radiobutton(self, text=str(account), variable=self.selected_account, value=account,
                                 command=lambda acct=account: self.aupdate(acct), bg="white", fg="black")
            rad.pack(anchor='w')
            self._buttons.append(rad)

        logging.debug("Account list created")

    def update_names(self):
        """updates the names of the accounts."""
        for rad, account in zip(self._buttons, self._bank.show_accounts()):
            rad.configure(text=str(account))

    def aupdate(self, acc):
        """updates the transaction list based on the selected account."""
        self.selected_account = acc
        self.update_t_list()

    def add_button(self):
        """adds a button when additional account is created"""
        account = self._bank.show_accounts()[-1]
        rad = tk.Radiobutton(self, text=str(account), variable=self.selected_account, value=account,
                                 command=lambda acct=account: self.aupdate(acct), bg="white", fg="black")
        rad.pack(anchor='w')
        self._buttons.append(rad)

    def update_t_list(self):
        """updates the transaction list."""
        if self.selected_account:
            self._tlframe.update_transactions(transactions=self.selected_account.get_transactions())
        else:
            self._tlframe.update_transactions(empty=True) #empty = True means we want it to be empty.