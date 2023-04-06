import customtkinter as ctk
from functools import partial
from ribbonUIComponents import SyncFrame
from toplevelUIComponents import AddNewEntryToplevel, ResetPasswordToplevel




# The frame that contains the add button, search box and the search button
class SearchFrame(ctk.CTkFrame):
    def __init__(self, parent, objs, **kwargs):
        super().__init__(parent, **kwargs)
        self.objs = objs
        iconObj = self.objs['iconObj']
        self.parent = parent
        # add the search box
        self.searchBox = ctk.CTkEntry(self,
                                      placeholder_text='Search...',
                                      width=0,
                                      height=0)
        self.searchBox.pack(side='left', fill='both', expand=True)
        # add the search button
        '''
        searchImg = ctk.CTkImage(dark_image=Image.open('icons/buttonIcon/search.png'),
                                 size=(20, 20)
                                )
        '''
        self.searchButton = ctk.CTkButton(self,
                                          image=iconObj.searchImg,
                                          text='',
                                          width=50,
                                          height=0,
                                          fg_color='#0074ff',
                                          hover_color='#002450',
                                          command=self.searchAction)
        self.searchButton.pack(side='right', fill='y')

    # get data from the database using the string value in the search box
    def searchAction(self):
        searchText = self.searchBox.get()
        itemList = self.objs['memDBObj'].searchLoginInfo(searchText)
        '''
        itemList = [
                        {'entryName': 'btn1',
                         'entryType': 'bank',
                         'id': 1},
                        {'entryName': 'btn2',
                         'entryType': 'email',
                         'id': 2},
                    ]
        '''
        self.parent.itemListFrame.deleteItemList()
        self.parent.itemListFrame.addItemList(itemList=itemList)










# the frame that contains additional functionality and buttons for the app
class RibbonFrame(ctk.CTkFrame):
    def __init__(self, parent, objs, **kwargs):
        super().__init__(parent, **kwargs)
        # add the add new entry button
        self.objs = objs
        iconObj = self.objs['iconObj']
        self.addButton  = ctk.CTkButton(self,
                                        image=iconObj.addImg,
                                        text='',
                                        width=50,
                                        height=0,
                                        anchor='center',
                                        fg_color='green',
                                        hover_color='#125200',
                                        command=self.addAction)
        self.addButton.pack(side='left', fill='y', expand=True, padx=2, pady=5)
        # add a reset password button
        self.resetPasswordButton = ctk.CTkButton(self,
                                                 image=iconObj.resetImg,
                                                 text='',
                                                 width=50,
                                                 height=0,
                                                 anchor='center',
                                                 fg_color='#585f63',
                                                 hover_color='#353a3d',
                                                 command=self.resetPassword)
        self.resetPasswordButton.pack(side='left', fill='y', expand=True, padx=2, pady=5)
        # the save button to push changes into presistent database
        self.saveButton = ctk.CTkButton(self,
                                        image=iconObj.saveFileImg,
                                        text='',
                                        width=50,
                                        height=0,
                                        anchor='center',
                                        fg_color='#585f63',
                                        hover_color='#353a3d',
                                        command=self.saveDatabase)
        self.saveButton.pack(side='left', fill='y', expand=True, padx=2, pady=5)
        # the sync frame
        self.syncFrame = SyncFrame(parent=self, iconObj=iconObj)
        self.syncFrame.pack(side='left', fill='y', expand=True, padx=2, pady=5, ipadx=20)

    # Create a new top-level windows to enter new entry details
    def addAction(self):
        self.addNewEntry = AddNewEntryToplevel(parent=self, objs=self.objs)

    # resets the password of the sqilte database
    def resetPassword(self):
        print('reset pass')
        self.resetPassFrame = ResetPasswordToplevel(parent=self)

    # save memory database for presistent database action
    def saveDatabase(self):
        print('save database') 









# The frame that contains entries and labels to show the information about an entry.
# Also allows to delete or modify an entry.
class ItemInformationFrame(ctk.CTkFrame):
    def __init__(self, parent, objs, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=7)
        for idx in  range(9):
            self.grid_rowconfigure(idx, weight=1)
        self.grid_rowconfigure(6, weight=4)
        self.objs = objs
        self.uniqueID = None
        # add text entry type widgets and it's labels
        fieldNameList = ['entryName',
                        'userName',
                        'password',
                        'email',
                        'url',
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
                        sticky='ns')
        typeSelectBox = ctk.CTkComboBox(self,
                                        values=self.entryTypeList,
                                        #variable=self.entryTypeValue,
                                        state='readonly',
                                        #command=self.getSelectBoxValue
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
                                    text='Save File as ...',
                                    command=self.saveFile
                                    )
        fileButton.grid(row=7,
                        column=1,
                        rowspan=1,
                        columnspan=1,
                        sticky='w')
        # add the button to submit the modified details into the database
        addButton = ctk.CTkButton(self,
                                  text='Modify',
                                  fg_color='green',
                                  hover_color='#125200',
                                  command=self.modifyAction
                                  )
        addButton.grid(row=8,
                        column=1,
                        rowspan=1,
                        columnspan=1,
                        sticky='w')
        # the button to delete the entry
        addButton = ctk.CTkButton(self,
                                  text='Delete',
                                  fg_color='red',
                                  hover_color='#620000',
                                  command=self.deleteAction
                                  )
        addButton.grid(row=8,
                        column=1,
                        rowspan=1,
                        columnspan=1,
                        sticky='e')
        # add the labels and widgets into a dict data structure; to keep track of them
        self.fieldDict['type'] = {'label': typeLabel,
                                  'entry': typeSelectBox
                                 }
        self.fieldDict['notes'] = {'label': notesLabel,
                                   'entry': notesEntry
                                   }
        self.fieldDict['file'] = {'label': fileLabel,
                                  'entry': fileButton
                                  }
        self.fieldDict['AddButton'] = {'label': None,
                                       'entry': addButton
                                      }

    def saveFile(self):
        filename = 'hello world.txt'
        filedata = b'bytes data'
        filext = '.' + filename.split('.')[-1]
        fileLink = ctk.filedialog.asksaveasfile(parent=self, mode='wb', initialdir='/', defaultextension=filext)
        if fileLink:
            fileLink.write(filedata)
            fileLink.close()

    def setAllEntryValue(self, id):
        loginInfoEntry = self.objs['memDBObj'].getLoginInfoEntryOnID(id)
        #print(loginInfoEntry)
        self.uniqueID = loginInfoEntry['uniqueID']
        for key in self.fieldDict.keys():
            if key != 'AddButton' and\
               key != 'file' and\
               key != 'type' and\
               key != 'notes' and\
               loginInfoEntry[key] != None:
                self.fieldDict[key]['entry'].delete("0","end")
                self.fieldDict[key]['entry'].insert("0", loginInfoEntry[key])
        self.fieldDict['type']['entry'].set(loginInfoEntry['entryType'])
        self.fieldDict['notes']['entry'].delete('0.0','end')
        self.fieldDict['notes']['entry'].insert('0.0', loginInfoEntry['notes'])
        #self.fieldDict['Type']['entry'].set(entryValues['Type'])

    def modifyAction(self):
        print('modify action')

    def deleteAction(self):
        print('delete action')





# A scrollable frame that contains the list of buttons to show the values of a given entry
class ItemListFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, objs, **kwargs):
        super().__init__(parent, **kwargs)
        self.objs = objs
        self.iconObj = self.objs['iconObj']
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
            '''
            img = ctk.CTkImage(dark_image=Image.open(f"icons/entryTypeIcon/{item['type']}.png"),
                               size=(30, 30)
                              )
            '''
            entryTypeImg = self.iconObj.entryTypeImgDict[item['entryType'].lower()]
            buttonCallback = partial(self.getEntryDetail, item['id'])
            button = ctk.CTkButton(self,
                                   text=item['entryName'],
                                   image=entryTypeImg,
                                   compound='left', 
                                   anchor='w', 
                                   fg_color="#4a4a4a", 
                                   corner_radius=10,
                                   command=buttonCallback)
            button.pack(side='top', fill='x', pady=2)
            self.buttonItemList.append(button)

    # when a button in the list is clicked this function get the entry details from the database
    def getEntryDetail(self, id):
        self.parent.itemInfoFrame.setAllEntryValue(id)