import tkinter as tk
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
        self.searchBox.bind('<Return>', self.searchAction)
        # add the search button
        self.searchButton = ctk.CTkButton(self,
                                          image=iconObj.searchImg,
                                          text='',
                                          width=50,
                                          height=40,
                                          fg_color='#0074ff',
                                          hover_color='#002450',
                                          command=self.searchAction)
        self.searchButton.pack(side='right', fill='y')

    # get data from the database using the string value in the search box
    def searchAction(self, eventInfo=None):
        searchText = self.searchBox.get()
        itemList = self.objs['memDBObj'].searchLoginInfo(searchText)
        self.parent.itemListFrame.deleteItemList()
        self.parent.itemListFrame.addItemList(itemList=itemList)






# the frame that contains additional functionality and buttons for the app
class RibbonFrame(ctk.CTkFrame):
    def __init__(self, parent, objs, **kwargs):
        super().__init__(parent, **kwargs)
        self.objs = objs
        iconObj = self.objs['iconObj']
        # eats up unnecessary space in the sides
        leftFrame = ctk.CTkFrame(self, height=40, fg_color='#2b2b2b')
        leftFrame.pack(side='left', expand=True, fill='both')
        # add the add new entry button
        self.addButton  = ctk.CTkButton(self,
                                        image=iconObj.addImg,
                                        text='',
                                        width=50,
                                        height=40,
                                        anchor='center',
                                        fg_color='green',
                                        hover_color='#125200',
                                        command=self.addAction)
        self.addButton.pack(side='left', fill='y', expand=False, padx=5, pady=5)
        # add a reset password button
        self.resetPasswordButton = ctk.CTkButton(self,
                                                 image=iconObj.resetImg,
                                                 text='',
                                                 width=50,
                                                 height=40,
                                                 anchor='center',
                                                 fg_color='#585f63',
                                                 hover_color='#353a3d',
                                                 command=self.resetPassword)
        self.resetPasswordButton.pack(side='left', fill='y', expand=False, padx=5, pady=5)
        # the sync frame with options for sync
        self.syncFrame = SyncFrame(parent=self, objs=self.objs, height=40)
        self.syncFrame.pack(side='left', fill='y', expand=False, padx=5, pady=5, ipadx=20)
        # eats up unnecessary space in the sides
        rightFrame = ctk.CTkFrame(self, height=40, width=200, fg_color='#2b2b2b')
        rightFrame.pack(side='left', expand=True, fill='both')

    # Create a new top-level windows to enter new entry details
    def addAction(self):
        self.addNewEntry = AddNewEntryToplevel(parent=self, objs=self.objs)

    # resets the password of the sqilte database
    def resetPassword(self):
        self.resetPassFrame = ResetPasswordToplevel(parent=self, objs=self.objs)






# The frame that contains entries and labels to show the information about an entry.
# Also allows to delete or modify an entry.
class ItemInformationFrame(ctk.CTkFrame):
    def __init__(self, parent, objs, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=9)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        for idx in  range(9):
            self.grid_rowconfigure(idx, weight=1)
        self.grid_rowconfigure(6, weight=4)
        self.objs = objs
        self.iconObj = self.objs['iconObj']
        self.uniqueID = None
        self.file = None
        self.filename = None
        self.filedata = None
        # add text entry type widgets and it's labels
        fieldNameList = ['entryName',
                        'userName',
                        #'password',
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
                        columnspan=3,
                        sticky='ew',
                        padx=5,
                        )
            # add the create label and widget to a dict datastructure to keep track off
            field = {"label": label,
                     "entry": entry
                     }
            self.fieldDict[f"{fieldName}"] = field
        # the label and entry for password
        passwordLabel = ctk.CTkLabel(self, 
                                text="Password: ",
                                height=40,
                                width=0)
        passwordLabel.grid(row=4,
                        column=0,
                        rowspan=1,
                        columnspan=1,
                        )
        passwordEntry = ctk.CTkEntry(self,
                                    show='*',
                                    height=40,
                                    width=0
                                    )
        passwordEntry.grid(row=4,
                        column=1,
                        rowspan=1,
                        columnspan=2,
                        sticky='ew',
                        padx=5,
                        )
        # show or hide password button
        self.showOrHidePassButton = ctk.CTkButton(self,
                                          image=self.iconObj.showHiddenImg,
                                          text='',
                                          width=30,
                                          height=40,
                                          fg_color='#0074ff',
                                          hover_color='#002450',
                                          command=self.showOrHidePassAction)
        self.showOrHidePassButton.grid(row=4,
                                      column=3,
                                      rowspan=1,
                                      columnspan=1,
                                      sticky='we'
                                      )  
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
                        columnspan=3,
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
        # the button to delete the the file
        deleteFileButton = ctk.CTkButton(self,
                                        text='Remove File',
                                        width=100,
                                        fg_color='red',
                                        hover_color='#620000',
                                        command=self.deleteFileAction
                                        )
        deleteFileButton.grid(row=7,
                            column=2,
                            rowspan=1,
                            columnspan=1,
                            sticky='w')
        # button to add a new file
        modifyFileButton = ctk.CTkButton(self,
                                        text='Add New File',
                                        width=100,
                                        command=self.addNewFileAction
                                        )
        modifyFileButton.grid(row=7,
                        column=3,
                        rowspan=1,
                        columnspan=1,
                        sticky='w')
        # add the button to submit the modified details into the database
        modifyButton = ctk.CTkButton(self,
                                  text='Modify',
                                  fg_color='green',
                                  hover_color='#125200',
                                  command=self.modifyAction
                                  )
        modifyButton.grid(row=8,
                        column=1,
                        rowspan=1,
                        columnspan=1,
                        sticky='w')
        # the button to delete the entry
        deleteButton = ctk.CTkButton(self,
                                  text='Delete',
                                  fg_color='red',
                                  hover_color='#620000',
                                  command=self.deleteAction
                                  )
        deleteButton.grid(row=8,
                        column=2,
                        rowspan=1,
                        columnspan=1,
                        sticky='w')
        # add the labels and widgets into a dict data structure; to keep track of them
        self.fieldDict['password'] = {'label': passwordLabel,
                                      'entry': passwordEntry
                                      }
        self.fieldDict['entryType'] = {'label': typeLabel,
                                  'entry': typeSelectBox
                                 }
        self.fieldDict['notes'] = {'label': notesLabel,
                                   'entry': notesEntry
                                   }
        self.fieldDict['file'] = {'label': fileLabel,
                                  'entry': fileButton
                                  }
        self.fieldDict['deleteFileButton'] = {'label': None,
                                              'entry': deleteFileButton   
                                             }
        self.fieldDict['modifyFileButton'] = {'label': None,
                                               'entry': modifyFileButton
                                                }
        self.fieldDict['modifyButton'] = {'label': None,
                                       'entry': modifyButton
                                      }
        self.fieldDict['deleteButton'] = {'label': None,
                                          'entry': deleteButton
                                            }

    # opens the dialog box for getting a new file and reading it's data
    def addNewFileAction(self):
        self.file = ctk.filedialog.askopenfile(parent=self, mode='rb', initialdir='/')
        if self.file:
            self.filename = self.file.name.split('/')[-1][:50]
            self.filedata = self.file.read()
            self.fieldDict['file']['entry'].configure(text=f"{self.filename}")

    # opens dialog box to write file to disk
    def saveFile(self):
        if self.filename != None and self.filedata != None:
            filext = [('All Files', '*.' + self.filename.split('.')[-1]), ]
            fileLink = ctk.filedialog.asksaveasfile(parent=self, 
                                                    mode='wb', 
                                                    initialdir='/', 
                                                    filetypes=filext,
                                                    initialfile=self.filename
                                                    )
            if fileLink:
                fileLink.write(self.filedata)
                fileLink.close()
        else:
            tk.messagebox.showwarning(title='No File',
                                      message='No file was attached to this entry')
    
    # retrieve the values from memory database
    # and file value from presistent database based on uniqueID
    # and set them to the fields in the ItemInformationFrame
    def setAllEntryValue(self, id):
        self.clearAllEntries()
        loginInfoEntry = self.objs['memDBObj'].getLoginInfoEntryOnID(id)
        self.uniqueID = loginInfoEntry['uniqueID']
        encryptedFileInfoPrimitive = self.objs['presistentDBObj'].getFileInfoOnUUID(self.uniqueID)[0]
        fileInfoPrimitive = self.objs['cryptObj'].decrypt(encryptedFileInfoPrimitive)
        entriesToSet = ['entryName', 'userName', 'password', 'email', 'url']
        for key in entriesToSet:
            if loginInfoEntry[key] != None:
                self.fieldDict[key]['entry'].insert("0", loginInfoEntry[key])
        self.fieldDict['entryType']['entry'].set(loginInfoEntry['entryType'])
        self.fieldDict['notes']['entry'].insert('0.0', loginInfoEntry['notes'])
        self.filename = loginInfoEntry['fileName']
        self.fieldDict['file']['entry'].configure(text=f"{self.filename}")
        self.filedata = fileInfoPrimitive['fileInfo']

    # get the values in the ItemInformationFrame entry boxes and files
    # and encrypt and store them in both memory and presistent databases.
    def modifyAction(self):
        if self.uniqueID != None:
            loginInfoEntry = {}
            loginInfoEntry['uniqueID'] = self.uniqueID
            entriesToGet = ['entryName', 'userName', 'password', 'email', 'url', 'entryType']
            for key in entriesToGet:
                loginInfoEntry[key] = self.fieldDict[key]['entry'].get()
            loginInfoEntry['notes'] = self.fieldDict['notes']['entry'].get('0.0', 'end')
            loginInfoEntry['fileName'] = self.filename
            self.objs['memDBObj'].modifyLoginInfoEntry(loginInfoEntry)
            loginInfoEntryBytes = self.objs['dataFormatterObj'].convertToBytes(loginInfoEntry)
            encryptedUserInfoEntry = self.objs['cryptObj'].encrypt({'uniqueID': self.uniqueID,
                                                                    'loginInfo': loginInfoEntryBytes,
                                                                    'fileInfo': self.filedata
                                                                    })
            self.objs['presistentDBObj'].updateUserInfoEntry(encryptedUserInfoEntry)
            self.objs['mainWindow'].searchFrame.searchAction()

    # delete the entry (row) from memory and presistent 
    # database based on uniqueID
    def deleteAction(self):
        self.objs['presistentDBObj'].deleteUserInfoEntry(self.uniqueID)
        self.objs['memDBObj'].deleteEntry(self.uniqueID)
        self.clearAllEntries()
        self.objs['mainWindow'].searchFrame.searchAction()

    # clears all the values already in entry or file fields 
    # in the ItemInformationFrame
    def clearAllEntries(self):
        entriesToDelete = ['entryName', 'userName', 'password', 'email', 'url']
        for key in entriesToDelete:
            self.fieldDict[key]['entry'].delete("0","end")
        self.file = None
        self.filename = None
        self.filedate = None
        self.fieldDict['file']['entry'].configure(text='None')
        self.fieldDict['notes']['entry'].delete('0.0', 'end')
        self.fieldDict['entryType']['entry'].set('Choose...')

    # deletes the entry (row) from both memory and
    # presistent databases based on uniqueID
    def deleteFileAction(self):
        self.file = None
        self.filename = None
        self.filedata = None
        self.fieldDict['file']['entry'].configure(text=f"{self.filename}")

    # show or hide the password entry
    def showOrHidePassAction(self):
        currentShowState = self.fieldDict['password']['entry'].cget('show')
        if currentShowState == '*':
            self.fieldDict['password']['entry'].configure(show='')
            self.showOrHidePassButton.configure(image=self.iconObj.notShowHiddenImg)
        else:
            self.fieldDict['password']['entry'].configure(show='*')
            self.showOrHidePassButton.configure(image=self.iconObj.showHiddenImg)





# A scrollable frame that contains the list of buttons to show the values of a given entry
class ItemListFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, objs, **kwargs):
        super().__init__(parent, **kwargs)
        self.objs = objs
        self.parent = parent
        self.iconObj = self.objs['iconObj']
        self.parent = parent
        self.buttonItemList = []
        
    # deletes all the buttons in the scrollable window
    def deleteItemList(self):
        self.parent.itemListFrame = ItemListFrame(parent=self.parent, objs=self.parent.getObjs(), height=0, width=300)
        self.parent.itemListFrame.grid(row=1, column=0, rowspan=1, columnspan=1, sticky='nsew', padx=5, pady=8)
        self.grid_forget()
        self.destroy()

    # adds a list of buttons based on the values in itemList
    def addItemList(self, itemList):
        for item in itemList:
            entryTypeImg = self.iconObj.entryTypeImgDict[item['entryType'].lower()]
            buttonCallback = partial(self.getEntryDetail, item['id'])
            button = ctk.CTkButton(self,
                                   text=item['entryName'],
                                   image=entryTypeImg,
                                   height=50,
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