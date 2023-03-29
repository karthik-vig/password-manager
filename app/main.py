import tkinter as tk
import customtkinter as ctk
from PIL import Image
from functools import partial



# the class with all the icons
class Icons:
    def __init__(self):
        self.getButtonIcons()
        self.getEntryTypeIcons()

    # gets and sets the button icons
    def getButtonIcons(self):
        self.addImg = ctk.CTkImage(dark_image=Image.open('icons/buttonIcon/add.png'),
                                    size=(20, 20)
                                    )
        self.searchImg = ctk.CTkImage(dark_image=Image.open('icons/buttonIcon/search.png'),
                                    size=(20, 20)
                                    )
        self.resetImg = ctk.CTkImage(dark_image=Image.open('icons/buttonIcon/reset.png'),
                                    size=(20, 20)
                                    )
        self.newEntryImg = ctk.CTkImage(dark_image=Image.open('icons/buttonIcon/newEntry.png'),
                                        size=(20, 20)
                                        )
        self.deleteEntryImg = ctk.CTkImage(dark_image=Image.open('icons/buttonIcon/deleteEntry.png'),
                                            size=(20, 20)
                                            )
        self.updateEntryImg = ctk.CTkImage(dark_image=Image.open('icons/buttonIcon/updateEntry.png'),
                                           size=(20, 20)
                                           )

    # gets and sets the entry type icons
    def getEntryTypeIcons(self):
        entryTypeList = ['bank',
                        'communication',
                        'email',
                        'entertainment',
                        'games',
                        'general',
                        'government',
                        'office',
                        'personal',
                        'shopping',
                        'streaming',
                        'study',
                        'transport'
                        ]
        self.entryTypeImgDict = {}
        for entryType in entryTypeList:
            entryTypeImg = ctk.CTkImage(dark_image=Image.open(f"icons/entryTypeIcon/{entryType}.png"),
                                        size=(20, 20)
                                        )
            self.entryTypeImgDict[entryType] = entryTypeImg


# The main app window
class Window(ctk.CTk):
    def __init__(self, iconObj):
        super().__init__()
        self.iconObj = iconObj
        self.title("Password Manager")
        self.drawPasswordAuth()

    # draws the windows to create a new sqlite
    # database if an existing one is not found
    def drawCreateNewDB(self):
        pass

    # draws the password input and submission window
    # upon authetication; will draw the content window
    def drawPasswordAuth(self):
        self.geometry("400x150")
        self.resizable(False, False)
        # configure the rows and column sizes
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # place the frames in the grid
        self.passwordAuthFrame = PasswordAuthFrame(parent=self, height=100, width=200)
        self.passwordAuthFrame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky='nsew')

    # draws the content window with search options and other operations
    def drawContent(self):
        self.resizable(True, True)
        self.geometry("1200x800")
        # configure the rows and column sizes
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=24)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        # place the frames in the grid
        self.searchFrame = SearchFrame(parent=self, iconObj=self.iconObj, height=0, width=0)
        self.searchFrame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky='nsew', padx=5, pady=8)
        self.ribbonFrame = RibbonFrame(parent=self, iconObj=self.iconObj, height=0, width=0)
        self.ribbonFrame.grid(row=0, column=1, rowspan=1, columnspan=1, sticky='nsew', padx=5, pady=8)
        self.itemListFrame = ItemListFrame(parent=self, iconObj=self.iconObj, height=0, width=0)
        self.itemListFrame.grid(row=1, column=0, rowspan=1, columnspan=1, sticky='nsew', padx=5, pady=8)
        self.itemInfoFrame = ItemInformationFrame(parent=self, height=0, width=0)
        self.itemInfoFrame.grid(row=1, column=1, rowspan=1, columnspan=1, sticky='nsew', padx=5, pady=8)


# The frame for the password input and authentication
class PasswordAuthFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        # create and place the label in the grid
        self.passwordLabel = ctk.CTkLabel(self,
                                          text="Enter Password: "
                                          )
        self.passwordLabel.grid(row=0,
                                column=0,
                                rowspan=1,
                                columnspan=1,
                                sticky='nsew'
                                )
        # create and place the password entry box in the grid
        self.passwrodEntry = ctk.CTkEntry(self,
                                          height=10,
                                          width=0
                                          )
        self.passwrodEntry.grid(row=0,
                                column=1,
                                rowspan=1,
                                columnspan=1,
                                sticky='we'
                                )
        # create and place the password submit button in the grid
        self.enterPasswordButton = ctk.CTkButton(self,
                                                 text='Submit',
                                                 anchor='center',
                                                fg_color='green',
                                                hover_color='#125200',
                                                command=self.submitPassword
                                                )
        self.enterPasswordButton.grid(row=1,
                                      column=1,
                                      rowspan=1,
                                      columnspan=1,
                                      sticky='w'
                                      )
    # Authenticates the password and then draws the content window
    def submitPassword(self):
        print(self.passwrodEntry.get())
        self.parent.passwordAuthFrame.grid_forget()
        self.parent.drawContent()
                                        



# The frame that contains the add button, search box and the search button
class SearchFrame(ctk.CTkFrame):
    def __init__(self, parent, iconObj, **kwargs):
        super().__init__(parent, **kwargs)
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



# the frame that contains additional functionality and buttons for the app
class RibbonFrame(ctk.CTkFrame):
    def __init__(self, parent, iconObj, **kwargs):
        super().__init__(parent, **kwargs)
        # add the add new entry button
        '''
        addImg = ctk.CTkImage(dark_image=Image.open('icons/buttonIcon/add.png'),
                              size=(20, 20)
                              )
        '''
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
        '''
        resetImg = ctk.CTkImage(dark_image=Image.open('icons/buttonIcon/reset.png'),
                                size=(20, 20)
                                )
        '''
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
        # add the frame for push sync
        self.pushSyncFrame = PushSyncFrame(parent=self, iconObj=iconObj)
        self.pushSyncFrame.pack(side='left', fill='y', expand=True, padx=2, pady=5, ipadx=20)
        # add the frame for pull sync
        self.pullSyncFrame = PullSyncFrame(parent=self, iconObj=iconObj)
        self.pullSyncFrame.pack(side='left', fill='y', expand=True, padx=2, pady=5, ipadx=20)

    # Create a new top-level windows to enter new entry details
    def addAction(self):
        self.addNewEntry = AddNewEntryToplevel(parent=self)

    # resets the password of the sqilte database
    def resetPassword(self):
        print('reset pass')
        self.resetPassFrame = ResetPasswordFrame(parent=self)




# push sync class, used to push the current state
# of the internal database onto the external database
class PushSyncFrame(ctk.CTkFrame):
    def __init__(self, parent, iconObj, **kwargs):
        super().__init__(parent, **kwargs)
        # the label frame
        self.pushSyncLable = ctk.CTkLabel(self,
                                          text='Push-Sync: ')
        self.pushSyncLable.pack(side='left')
        # the new entry button
        self.newEntryButton = ctk.CTkButton(self,
                                            text='',
                                            image=iconObj.newEntryImg,
                                            anchor='center',
                                            width=50,
                                            height=0,
                                            command=self.setNewEntry
                                            )
        self.newEntryButton.pack(side='left', fill='y', expand=True)
        # the delte entry button
        self.newEntryButton = ctk.CTkButton(self,
                                            text='',
                                            image=iconObj.deleteEntryImg,
                                            anchor='center',
                                            width=50,
                                            height=0,
                                            command=self.deleteExternalDBEntry
                                            )
        self.newEntryButton.pack(side='left', fill='y', expand=True)
        # the update modifications button
        self.newEntryButton = ctk.CTkButton(self,
                                            text='',
                                            image=iconObj.updateEntryImg,
                                            anchor='center',
                                            width=50,
                                            height=0,
                                            command=self.updateExternalDatabaseEntry
                                            )
        self.newEntryButton.pack(side='left', fill='y', expand=True)

    # the action to set new entries in the internal database 
    # onto the external database
    def setNewEntry(self):
        print('setting new entries in the external database')
    
    # the action to delete new entries in the external database 
    # not in the internal database
    def deleteExternalDBEntry(self):
        print('deletting external db entry not in the internal database')
    
    # the action to make the rows in the external database conform
    # according to the internal database
    def updateExternalDatabaseEntry(self):
        print('updating external database to conform to internal database')


    
# pull sync class, used to pull the current state
# of the external database onto the internal database
class PullSyncFrame(ctk.CTkFrame):
    def __init__(self, parent, iconObj, **kwargs):
        super().__init__(parent, **kwargs)
        # the label frame
        self.pushSyncLable = ctk.CTkLabel(self,
                                          text='Pull-Sync: ')
        self.pushSyncLable.pack(side='left')
        # the new entry button
        self.newEntryButton = ctk.CTkButton(self,
                                            text='',
                                            image=iconObj.newEntryImg,
                                            anchor='center',
                                            width=50,
                                            height=0,
                                            command=self.setNewEntry
                                            )
        self.newEntryButton.pack(side='left', fill='y', expand=True)
        # the delte entry button
        self.newEntryButton = ctk.CTkButton(self,
                                            text='',
                                            image=iconObj.deleteEntryImg,
                                            anchor='center',
                                            width=50,
                                            height=0,
                                            command=self.deleteInternalDBEntry
                                            )
        self.newEntryButton.pack(side='left', fill='y', expand=True)
        # the update modifications button
        self.newEntryButton = ctk.CTkButton(self,
                                            text='',
                                            image=iconObj.updateEntryImg,
                                            anchor='center',
                                            width=50,
                                            height=0,
                                            command=self.updateInternalDatabaseEntry
                                            )
        self.newEntryButton.pack(side='left', fill='y', expand=True)

    # the action to set new entries in the external database 
    # onto the internal database
    def setNewEntry(self):
        print('setting new entries in the internal database')
    
    # the action to delete new entries in the internal database 
    # not in the external database
    def deleteInternalDBEntry(self):
        print('deletting internal db entry not in the exteranl database')
    
    # the action to make the rows in the internal database conform
    # according to the external database
    def updateInternalDatabaseEntry(self):
        print('updating internal database to conform to external database')



# Reset Password frame
class ResetPasswordFrame(ctk.CTkToplevel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.geometry("600x200")
        self.resizable(False, False)
        self.title('Set New Password')
        self.grab_set()
        # configure the rows and columns
        for row in range(4):
            self.grid_rowconfigure(row, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        # enter current password label and entry
        self.currentPasswordLabel = ctk.CTkLabel(self,
                                                 text='Enter Current Password: ')
        self.currentPasswordLabel.grid(row=0,
                                      column=0,
                                      rowspan=1,
                                      columnspan=1,
                                      sticky='w'
                                      )
        self.currentPasswordEntry = ctk.CTkEntry(self)
        self.currentPasswordEntry.grid(row=0,
                                      column=1,
                                      rowspan=1,
                                      columnspan=1,
                                      sticky='we'
                                      )
        # enter new password label and entry
        self.newPasswordLabel = ctk.CTkLabel(self,
                                             text='Enter the New Password: ')
        self.newPasswordLabel.grid(row=1,
                                    column=0,
                                    rowspan=1,
                                    columnspan=1,
                                    sticky='w'
                                    )
        self.newPasswordEntry = ctk.CTkEntry(self)
        self.newPasswordEntry.grid(row=1,
                                    column=1,
                                    rowspan=1,
                                    columnspan=1,
                                    sticky='we'
                                    )
        # re-enter new password label and entry
        self.reenterPasswordLabel = ctk.CTkLabel(self,
                                                 text='Re-Enter the New Password: ')
        self.reenterPasswordLabel.grid(row=2,
                                      column=0,
                                      rowspan=1,
                                      columnspan=1,
                                      sticky='w'
                                      )
        self.reenterPasswordEntry = ctk.CTkEntry(self)
        self.reenterPasswordEntry.grid(row=2,
                                      column=1,
                                      rowspan=1,
                                      columnspan=1,
                                      sticky='we'
                                      )
        # the submit button
        self.enterSubmitButton = ctk.CTkButton(self,
                                               text='Submit',
                                               anchor='center',
                                               fg_color='green',
                                               hover_color='#125200',
                                               command=self.resetPassword
                                               )
        self.enterSubmitButton.grid(row=3,
                                    column=1,
                                    rowspan=1,
                                    columnspan=1,
                                    sticky='w'
                                    )

    # the action for reset the password
    def resetPassword(self):
        print('resetting password')
        self.destroy()



# A scrollable frame that contains the list of buttons to show the values of a given entry
class ItemListFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, iconObj, **kwargs):
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
            '''
            img = ctk.CTkImage(dark_image=Image.open(f"icons/entryTypeIcon/{item['type']}.png"),
                               size=(30, 30)
                              )
            '''
            entryTypeImg = iconObj.entryTypeImgDict[item['type'].lower()]
            buttonCallback = partial(self.getEntryDetail, item['id'])
            button = ctk.CTkButton(self,
                                   text=item['text'],
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
        print(id)



# The frame that contains entries and labels to show the information about an entry.
# Also allows to delete or modify an entry.
class ItemInformationFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
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

    def saveFile(self):
        filename = 'hello world.txt'
        filedata = b'bytes data'
        filext = '.' + filename.split('.')[-1]
        fileLink = ctk.filedialog.asksaveasfile(parent=self, mode='wb', initialdir='/', defaultextension=filext)
        if fileLink:
            fileLink.write(filedata)
            fileLink.close()

    def setAllEntryValue(self, entryValues):
        self.fieldDict['Type']['entry'].set(entryValues['Type'])

    def modifyAction(self):
        print('modify action')

    def deleteAction(self):
        print('delete action')



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
                                    text='Choose File...',
                                    command=self.chooseFile)
        fileButton.grid(row=7,
                        column=1,
                        rowspan=1,
                        columnspan=1,
                        sticky='w')
        # add the button to submit the details into the database
        addButton = ctk.CTkButton(self,
                                  text='Add',
                                  fg_color='green',
                                  hover_color='#125200',
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

    # choose file to add to the new entry
    def chooseFile(self):
        file = ctk.filedialog.askopenfile(parent=self, mode='rb', initialdir='/')
        if file:
            print(file.name.split('/')[-1])
            print(file.read())

    # the action to create a new database entry based on the entered values
    def addAction(self):
        print('add action')
        self.destroy()



if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_widget_scaling(1.1)
    ctk.set_window_scaling(1.0)
    iconObj = Icons()
    app = Window(iconObj  = iconObj)
    app.mainloop()