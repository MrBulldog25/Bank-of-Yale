from base import Base
from bank import Bank
import logging
from decimal import setcontext, BasicContext
from translistframe import TransactionsFrame
from accountlistframe import AccountListFrame
from options import AccountOptions
from exceptions import TransactionSequenceError
from transactiongui import TransactionGUI
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
import tkinter as tk
from tkinter import messagebox
import sys


setcontext(BasicContext)

logging.basicConfig(filename='bank.log', level=logging.DEBUG,
                    format='%(asctime)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')



class BankGUI:
    """Class with everything, the BankCLI equivalent, with a questionable front-end but a front-end nonetheless"""
    def __init__(self):
        """Initializes the class and all of the major elements"""
        self._window = tk.Tk()
        self._window.title("Banking App")
        self._window.geometry("1200x800")
        self._window.configure(bg="white")
        
        self._session = Session()
        self._bank = self._session.query(Bank).first()
        if not self._bank:
            self._bank = Bank()
            self._session.add(self._bank)
        else:
            logging.debug("Loaded from bank.db")
        self._session.commit()
        logging.debug("Saved to bank.db")
        self.selected_account = None

        #Our button style that I adhered to for the main ones, then I got tired
        button_style = {
            'bg':'white',
            'fg':'blue',
            'font': ("Comic Sans", 20),
            'borderwidth': 2,
            'relief': 'groove'
        }

        #sets up the grid where the stuff will be
        self._window.grid_rowconfigure(0, weight=2)
        self._window.grid_rowconfigure(1, weight=3)
        self._window.grid_rowconfigure(2, weight=3)
        self._window.grid_rowconfigure(3, weight=1)
        self._window.grid_rowconfigure(4, weight=50)
        self._window.grid_columnconfigure(0, weight=1)
        self._window.grid_columnconfigure(1, weight=1)
        self._window.grid_columnconfigure(2, weight=1)

        #these are like all of the (mega)widgets pretty much
        self._label = tk.Label(self._window, text="Bank of Yale", font=("Helvetica", 30), fg="blue", bg="white")
        self._label.grid(row=0, column=1, pady=20)

        self._open_account_button = tk.Button(self._window, text="Open Account", command=self._open_account, **button_style)
        self._open_account_button.grid(row=1, column=1, pady=20)

        self._i_and_f_button = tk.Button(self._window, text="Interest and Fees", command=self._apply_i_f, **button_style)
        self._i_and_f_button.grid(row=1, column=0, pady=20, padx=35)

        self._add_trans_button = tk.Button(self._window, text="Add Transaction", command=self._add_trans, **button_style)
        self._add_trans_button.grid(row=1, column=2, pady=20, padx=35)

        self._trans_frame = TransactionsFrame(self._window)
        self._trans_frame.grid(row=4, column=1, sticky="n")

        self._acctoptions = AccountOptions(self._window, self._bank, self._session, button_style, callback=self._alist_update)
        self._acctoptions.grid(row=2, column=1, sticky="n")

        self._acc_list = AccountListFrame(self._window, self._bank, self._session, self._trans_frame)
        self._acc_list.grid(row=4, column=0, sticky="n")

        self._transgui = TransactionGUI(self._window, self._bank, self._acc_list, 
                                        callback=self._acc_list.update_names, callback2=self._add_trans, 
                                        session=self._session)

        self._quit_button = tk.Button(self._window, 
                                     text="Quit?", 
                                     bg="white", 
                                     fg="red", 
                                     font=("Helvetica", 12), 
                                     command=self._quit, 
                                     borderwidth=2)
        self._update_quit_pos()

        #Below makes it so that the quit button is always top right corner
        self._window.bind("<Configure>", self.wresize_actions)
    
    def _open_account(self):
        """Triggered by the open account button.  Just makes the checking/savings buttons available, functionality is in the other class"""
        self._acctoptions.change_visibility()

    def _alist_update(self):
        """helper function that prints/updates the account list and the transaction list at the bottom of the screen"""
        self._acc_list.add_button()
        self._acc_list.update_t_list()

    def _quit(self):
        """safely quits out of the program.  Triggered by quit button"""
        self._session.close()
        sys.exit(0)

    def wresize_actions(self, event):
        """move the quit button with the window"""
        self._update_quit_pos()

    def _apply_i_f(self):
        """triggered by the interest and fees button, this allows for the application of just that"""
        if not self._acc_list.selected_account:
            messagebox.showwarning("Warning",f"Please select an account before using this feature.")
        else:
            if not self._acc_list.selected_account.get_transactions():
                messagebox.showwarning("Warning", "Hi Tim!!! You promised you wouldn't check this but I covered it anyway :)")
                return
            try:
                self._acc_list.selected_account.assess_interest_and_fees(self._session)
                self._session.commit()
                self._acc_list.update_names()
                logging.debug("Triggered interest and fees")
                logging.debug("Saved to bank.db")
            except TransactionSequenceError as e:
                messagebox.showwarning("Warning", 
                                       f"Cannot apply interest and fees again in the month of {e.latest_date.strftime('%B')}.")
            


    def _add_trans(self):
        """triggered by add transaction button, opens the menu for adding stuff if applicable"""
        if not self._acc_list.selected_account:
            messagebox.showerror("Error", "Select an account first to continue")
            return
        self._transgui.currentaccount = self._acc_list.selected_account
        if self._transgui.winfo_ismapped():
            #clicking the button also makes it go away
            self._transgui.grid_forget()
        else:
            self._transgui.grid(row=2,column=2)
        

    def _update_quit_pos(self):
        """moves quit button"""
        x_position = self._window.winfo_width() - self._quit_button.winfo_reqwidth() - 5
        self._quit_button.place(x=x_position, y=5)

    def run(self):
        """runs the program"""
        try:
            self._window.mainloop()
        except Exception as e:
            messagebox.showerror("Error", 
                                 "Something unexpected happened.  If the issue persists please contact the developers.")
            logging.error(str(e.__class__.__name__) + ": " + repr(str(e)))
            self._session.close()
            sys.exit(0)



if __name__ == "__main__":
    engine = create_engine(f"sqlite:///bank.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    gui = BankGUI()
    gui.run()
    