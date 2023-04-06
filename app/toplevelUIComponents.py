import tkinter as tk
import customtkinter as ctk
from database import DataFormatter, CryptographyHandler
import uuid





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
        self.passwordEntry = ctk.CTkEntry(self,
                                          height=10,
                                          width=0
                                          )
        self.passwordEntry.grid(row=0,
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
        password = self.passwordEntry.get()
        cryptInfoPrimitiveS = self.parent.presistentDBObj.getCryptInfoRow()
        if not len(cryptInfoPrimitiveS):
            self.parent.cryptObj = CryptographyHandler(password)
            (
            encryptedKey,
            encryptKeyIV,
            generateKeySalt,
            hashKeySalt,
            hashedKey ) = self.parent.cryptObj.getCryptValues()
            self.parent.presistentDBObj.addCryptInfoEntry({'encryptedKey': encryptedKey,
                                                            'encryptKeyIV': encryptKeyIV,
                                                            'generateKeySalt': generateKeySalt,
                                                            'hashKeySalt': hashKeySalt,
                                                            'hashedKey': hashedKey
                                                            })
        else:
            cryptInfoPrimitiveS = cryptInfoPrimitiveS[0]
            self.parent.cryptObj = CryptographyHandler(password,
                                                        cryptInfoPrimitiveS['encryptedKey'],
                                                        cryptInfoPrimitiveS['encryptKeyIV'],
                                                        cryptInfoPrimitiveS['generateKeySalt'],
                                                        cryptInfoPrimitiveS['hashKeySalt'],
                                                        cryptInfoPrimitiveS['hashedKey'],
                                                        )
        self.parent.dataFormatterObj = DataFormatter(self.parent.cryptObj)
            
        if not self.parent.cryptObj.getAuthStatus():
            tk.messagebox.showwarning(title='Authentication Failed',
                                      message='Authentication Failed, re-enter password')
        else:
            encryptedLoginInfoPrimitiveS = self.parent.presistentDBObj.getAllLoginInfo()
            for encryptedLoginInfoPrimitive in encryptedLoginInfoPrimitiveS:
                loginInfoPrimitive = self.parent.cryptObj.decrypt(encryptedLoginInfoPrimitive)
                #print(loginInfoPrimitive)
                loginInfoEntry = self.parent.dataFormatterObj.convertToPythonType(loginInfoPrimitive['loginInfo'])
                self.parent.memDBObj.addNewEntry(loginInfoEntry)
            self.parent.passwordAuthFrame.grid_forget()
            self.parent.drawContent()









# Reset Password frame
class ResetPasswordToplevel(ctk.CTkToplevel):
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







# The top-level window to enter the details for a new entry
class AddNewEntryToplevel(ctk.CTkToplevel):
    def __init__(self, parent, objs, **kwargs):
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
        self.objs = objs
        # initialize variables
        self.selectTypeBoxValue = None
        self.file = None
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
                        sticky='n')
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
        self.fieldDict['entryType'] = {'label': typeLabel,
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
    '''
    # gets and sets the current chosen value of the combo box for entry type
    def getSelectBoxValue(self, value):
        self.selectTypeBoxValue = value
    '''

    # choose file to add to the new entry
    def chooseFile(self):
        self.file = ctk.filedialog.askopenfile(parent=self, mode='rb', initialdir='/')
        if self.file:
            self.fieldDict['file']['entry'].configure(text=f"{self.file.name.split('/')[-1][:50]}")
        '''
        if self.file:
            print(self.file.name.split('/')[-1])
            print(self.file.read())
        '''

    # the action to create a new database entry based on the entered values
    def addAction(self):
        #print('add action')
        loginInfoEntry = {}
        loginInfoEntry['uniqueID'] = str(uuid.uuid4())
        for key in self.fieldDict.keys():
            if key != 'notes' and key != 'file' and key != 'AddButton':
                #print(f"{key} : {self.fieldDict[key]['entry'].get()}")
                loginInfoEntry[key] = self.fieldDict[key]['entry'].get()
        loginInfoEntry['notes'] = self.fieldDict['notes']['entry'].get('0.0', 'end')
        loginInfoEntry['fileName'] = None
        fileData = None
        if self.file:
            loginInfoEntry['fileName'] = self.file.name.split('/')[-1]
            fileData = self.file.read()
        #print(loginInfoEntry)
        self.objs['memDBObj'].addNewEntry(loginInfoEntry)
        loginInfoEntryBytes = self.objs['dataFormatterObj'].convertToBytes(loginInfoEntry)
        encryptedUserInfoEntry = self.objs['cryptObj'].encrypt({'uniqueID' : loginInfoEntry['uniqueID'],
                                                                'loginInfo': loginInfoEntryBytes,
                                                                'fileInfo': fileData
                                                                })
        self.objs['presistentDBObj'].addUserInfoEntry(encryptedUserInfoEntry)
        self.destroy()