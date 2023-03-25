import tkinter as tk
import customtkinter as ctk
from PIL import Image
from functools import partial


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
        # add the add new entry button
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
        # add the search box
        self.searchBox = ctk.CTkEntry(self,
                                      placeholder_text='Search...',
                                      width=0,
                                      height=0)
        self.searchBox.pack(side='left', fill='both', expand=True)
        # add the search button
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

    # Create a new top-level windows to enter new entry details
    def addAction(self):
        self.addNewEntry = AddNewEntryToplevel(parent=self)

    # get data from the database using the string value in the search box
    def searchAction(self):
        searchText = self.searchBox.get()
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
        
    # deletes all the buttons in the scrollable window
    def deleteItemList(self):
        for buttonItem in self.buttonItemList:
            buttonItem.pack_forget()
            buttonItem.destroy()
        self.buttonItemList = []

    # adds a list of buttons based on the values in itemList
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
                                   corner_radius=10,
                                   command=buttonCallback)
            button.pack(side='top', fill='x', pady=2)
            self.buttonItemList.append(button)

    # when a button in the list is clicked this function get the entry details from the database
    def getEntryDetail(self, id):
        print(id)

# The frame that contains entries and labels to show the information about an entry.
# Also allows to delete or modify an entry.
class ItemInformationFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        pass


# The top-level window to enter the details for a new entry
class AddNewEntryToplevel(ctk.CTkToplevel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.geometry("600x600")
        self.resizable(False, False)
        self.title('Add New Entry')
        self.grab_set()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=7)
        for idx in  range(9):
            self.grid_rowconfigure(idx, weight=1)
        self.grid_rowconfigure(6, weight=4)
        # add text entry type widgets and it's labels
        fieldNameList = ['Entry Name',
                        'Username',
                        'Password',
                        'E-Mail',
                        'URL',
                        ]
        self.fieldDict = {}
        for row, fieldName in enumerate(fieldNameList):
            label = ctk.CTkLabel(self, 
                                text=f"{fieldName}: ",
                                height=40,
                                width=0)
            label.grid(row=row,
                        column=0,
                        rowspan=1,
                        columnspan=1,
                        )
            entry = ctk.CTkEntry(self,
                                height=40,
                                width=0)
            entry.grid(row=row,
                        column=1,
                        rowspan=1,
                        columnspan=1,
                        sticky='ew',
                        padx=5,
                        )
            # add the create label and widget to a dict datastructure to keep track off
            field = {"label": label,
                     "entry": entry
                     }
            self.fieldDict[f"{fieldName}"] = field
        # add label and widget for selecting type of entry
        self.entryTypeList = ['Choose...',
                                'Bank',
                                'Communication',
                                'Email',
                                'Entertainment',
                                'Games',
                                'General',
                                'Government',
                                'Office',
                                'Personal',
                                'Shopping',
                                'Streaming',
                                'Study',
                                'Transport'
                                ]
        typeLabel = ctk.CTkLabel(self, 
                                text='Type: ',
                                height=40,
                                width=0
                                )
        typeLabel.grid(row=5,
                        column=0,
                        rowspan=1,
                        columnspan=1,
                        sticky='n')
        typeSelectBox = ctk.CTkComboBox(self,
                                        values=self.entryTypeList,
                                        #variable=self.entryTypeValue,
                                        state='readonly',
                                        command=self.getSelectBoxValue
                                        )
        typeSelectBox.set('Choose...')
        typeSelectBox.grid(row=5,
                        column=1,
                        rowspan=1,
                        columnspan=1,
                        sticky='w',
                        padx=5,
                        )
        # add label and widget for notes textbox
        notesLabel = ctk.CTkLabel(self, 
                                text='Notes: ',
                                height=40,
                                width=0
                                )
        notesLabel.grid(row=6,
                        column=0,
                        rowspan=1,
                        columnspan=1,
                        sticky='n')
        notesEntry = ctk.CTkTextbox(self)
        notesEntry.grid(row=6,
                        column=1,
                        rowspan=1,
                        columnspan=1,
                        sticky='nsew',
                        padx=5,
                        )
        # add label and widget for choosing file to add with entry
        fileLabel = ctk.CTkLabel(self, 
                                text='File: ',
                                height=40,
                                width=0
                                )
        fileLabel.grid(row=7,
                        column=0,
                        rowspan=1,
                        columnspan=1,
                        )
        fileButton = ctk.CTkButton(self,
                                    text='Choose File...')
        fileButton.grid(row=7,
                        column=1,
                        rowspan=1,
                        columnspan=1,
                        sticky='w')
        # add the button to submit the details into the database
        addButton = ctk.CTkButton(self,
                                  text='Add',
                                  command=self.addAction)
        addButton.grid(row=8,
                        column=1,
                        rowspan=1,
                        columnspan=1)
        # add the labels and widgets into a dict data structure; to keep track of them
        self.fieldDict['Type'] = {'label': typeLabel,
                                  'entry': typeSelectBox
                                 }
        self.fieldDict['Notes'] = {'label': notesLabel,
                                   'entry': notesEntry
                                   }
        self.fieldDict['File'] = {'label': fileLabel,
                                  'entry': fileButton
                                  }
        self.fieldDict['AddButton'] = {'label': None,
                                       'entry': addButton
                                      }

    # gets and sets the current chosen value of the combo box for entry type
    def getSelectBoxValue(self, value):
        print(value)

    # the action to create a new database entry based on the entered values
    def addAction(self):
        print('add action')
        self.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Window()
    app.mainloop()