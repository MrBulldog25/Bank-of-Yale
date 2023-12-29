import tkinter as tk

class AccountOptions(tk.Frame):
    """Class for the buttons that choose which type of account to add."""
    def __init__(self, parent, bank, session, button_style, callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="white")
        self.checking_button = tk.Button(self, text="checking", command=lambda: self._account_add(acctype="checking"),
                                         **button_style)
        self.savings_button = tk.Button(self, text="savings", command=lambda: self._account_add(acctype="savings"),
                                         **button_style)
        self._bank = bank
        self._session = session
        self._callback = callback

    def change_visibility(self):
        """change the visibility"""
        if self.checking_button.winfo_ismapped():
            self.checking_button.grid_forget()
            self.savings_button.grid_forget()
        else:
            self.checking_button.grid(row=0, column=0)
            self.savings_button.grid(row=0, column=1)

    def _account_add(self, acctype):
        """adds the new account and essentially disables the buttons"""
        self._bank.add_account(acctype, self._session)
        self.checking_button.grid_forget()
        self.savings_button.grid_forget()
        self._session.commit()
        #below -- callback to main to update list
        self._callback()

