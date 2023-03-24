import tkinter as tk
import customtkinter as ctk
import os


# The main app window
class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Password Manager")
        # configure the rows and column sizes
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=24)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        # place the frames in the grid
        self.searchFrame = SearchAndAddFrame(parent=self, height=0, width=0)
        self.searchFrame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky='nsew', padx=7, pady=7)
        self.itemListFrame = ItemListFrame(parent=self, height=0, width=0)
        self.itemListFrame.grid(row=1, column=0, rowspan=1, columnspan=1, sticky='nsew', padx=7, pady=7)
        self.itemInfoFrame = ItemInformationFrame(parent=self, height=0, width=0)
        self.itemInfoFrame.grid(row=0, column=1, rowspan=2, columnspan=1, sticky='nsew', padx=7, pady=7)


# The frame that contains the add button, search box and the search button
class SearchAndAddFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        addImg = tk.PhotoImage(file='icons/buttonIcon/add.png').subsample(25,40)
        self.addButton  = ctk.CTkButton(self,
                                        image=addImg,
                                        text='',
                                        width=0,
                                        height=0,
                                        anchor='center',
                                        fg_color='transparent',
                                        command=self.addAction)
        self.addButton.pack(side='left',fill='y')
        self.searchBox = ctk.CTkEntry(self,
                                      placeholder_text='Search...',
                                      width=0,
                                      height=0)
        self.searchBox.pack(side='left', fill='both', expand=True)
        searchImg = tk.PhotoImage(file='icons/buttonIcon/search.png').subsample(25,35)
        self.searchButton = ctk.CTkButton(self,
                                          image=searchImg,
                                          text='',
                                          width=0,
                                          height=0,
                                          fg_color='transparent',
                                          command=self.searchAction)
        self.searchButton.pack(side='right', fill='y')

    def addAction(self):
        pass

    def searchAction(self):
        pass


# A scrollable frame that contains the list of buttons to show the values of a given entry
class ItemListFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        pass


# The frame that contains entries and labels to show the information about an entry.
# Also allows to delete or modify an entry.
class ItemInformationFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        pass

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Window()
    app.mainloop()