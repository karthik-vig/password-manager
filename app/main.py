import tkinter as tk
import customtkinter as ctk
from PIL import Image
from functools import partial
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
        self.parent = parent
        #addImg = tk.PhotoImage(file='icons/buttonIcon/add.png').subsample(25,40)
        addImg = ctk.CTkImage(dark_image=Image.open('icons/buttonIcon/add.png'),
                              size=(20, 20)
                              )
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
        #searchImg = tk.PhotoImage(file='icons/buttonIcon/search.png').subsample(25,35)
        searchImg = ctk.CTkImage(dark_image=Image.open('icons/buttonIcon/search.png'),
                                 size=(20, 20)
                                )
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
        itemList = [
                        {'text': 'btn1',
                         'type': 'bank',
                         'id': 1},
                        {'text': 'btn2',
                         'type': 'email',
                         'id': 2},
                    ]
        self.parent.itemListFrame.deleteItemList()
        self.parent.itemListFrame.addItemList(itemList=itemList)


# A scrollable frame that contains the list of buttons to show the values of a given entry
class ItemListFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.buttonItemList = []
        
    def deleteItemList(self):
        for buttonItem in self.buttonItemList:
            buttonItem.pack_forget()
            #buttonItem.destory()
        self.buttonItemList = []

    def addItemList(self, itemList):
        for item in itemList:
            img = ctk.CTkImage(dark_image=Image.open(f"icons/entryTypeIcon/{item['type']}.png"),
                               size=(30, 30)
                              )
            buttonCallback = partial(self.getEntryDetail, item['id'])
            button = ctk.CTkButton(self,
                                   text=item['text'],
                                   image=img,
                                   compound='left', 
                                   anchor='w', 
                                   fg_color="#4a4a4a", 
                                   corner_radius=0,
                                   command=buttonCallback)
            button.pack(side='top', fill='x')
            self.buttonItemList.append(button)

    def getEntryDetail(self, id):
        print(id)

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