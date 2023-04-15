import tkinter as tk
import customtkinter as ctk
from database import DataFormatter, CryptographyHandler
from database import PresistentDatabaseHandler, CryptographyHandler
import uuid
import string
import os






# The frame for creating a new database with a password
class SetPasswordFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.objs = self.parent.getObjs()
        self.iconObj = self.objs['iconObj']
        # configure the rows and columns
        for row in range(4):
            self.grid_rowconfigure(row, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)
        # label to indicate the necessary action
        self.createNewDBLabel = ctk.CTkLabel(self,
                                            text='Create a New Database')
        self.createNewDBLabel.grid(row=0,
                                    column=0,
                                    rowspan=1,
                                    columnspan=2,
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
        self.newPasswordEntry = ctk.CTkEntry(self, 
                                             show='*'
                                             )
        self.newPasswordEntry.grid(row=1,
                                    column=1,
                                    rowspan=1,
                                    columnspan=1,
                                    sticky='we'
                                    )
        # show or hide password button
        self.showOrHidePassButton = ctk.CTkButton(self,
                                          image=self.iconObj.showHiddenImg,
                                          text='',
                                          width=30,
                                          height=20,
                                          fg_color='#0074ff',
                                          hover_color='#002450',
                                          command=self.showOrHidePassAction)
        self.showOrHidePassButton.grid(row=1,
                                      column=2,
                                      rowspan=1,
                                      columnspan=1,
                                      sticky='e'
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
        self.reenterPasswordEntry = ctk.CTkEntry(self,
                                                show='*'
                                                )
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
                                               command=self.createNewDB
                                               )
        self.enterSubmitButton.grid(row=3,
                                    column=1,
                                    rowspan=1,
                                    columnspan=1,
                                    sticky='w'
                                    )

    # creates a new database to store user data
    # after verifying that the new password is upto a 
    # set standard
    def createNewDB(self):
        newPassword = self.newPasswordEntry.get()
        reenteredNewPassword = self.reenterPasswordEntry.get()
        reject, rejectionMsg = self.checkPasswordStandard(newPassword, reenteredNewPassword)
        if reject:
            tk.messagebox.showwarning(title='Password Not Accepted',
                                      message=f"The Password is not accepted for the following reasons:{rejectionMsg}")
        else:
            self.parent.cryptObj = CryptographyHandler(newPassword)
            (
            encryptedKey,
            encryptKeyIV,
            generateKeySalt,
            hashKeySalt,
            hashedKey ) = self.parent.cryptObj.getCryptValues()
            self.parent.presistentDBObj = PresistentDatabaseHandler()
            self.parent.presistentDBObj.addCryptInfoEntry({'encryptedKey': encryptedKey,
                                                            'encryptKeyIV': encryptKeyIV,
                                                            'generateKeySalt': generateKeySalt,
                                                            'hashKeySalt': hashKeySalt,
                                                            'hashedKey': hashedKey
                                                            })
            self.parent.dataFormatterObj = DataFormatter(self.parent.cryptObj)
            self.parent.setPassFrame.grid_forget()
            self.parent.drawContent()
        
    # check to see if the new password fits the password standard
    def checkPasswordStandard(self, newPassword, reenteredNewPassword):
        rejectionMsg = ''
        reject = False
        if len(newPassword) < 9:
            rejectionMsg += "\n* Password Length less than 9 characters!"
            reject = True
        if newPassword != reenteredNewPassword:
            rejectionMsg += "\n* The Re-Entered Password does not Match!"
            reject = True
        upperCaseExist = False
        lowerCaseExist = False
        digitsExist = False
        specialCharExist = False
        for passwordChar in newPassword:
            if passwordChar.isupper():
                upperCaseExist = True
            elif passwordChar.islower():
                lowerCaseExist = True
            elif passwordChar.isdigit():
                digitsExist = True
            elif passwordChar in string.punctuation:
                specialCharExist = True
        if not upperCaseExist:
            rejectionMsg += "\n* No uppercase character(s)!"
            reject = True
        if not lowerCaseExist:
            rejectionMsg += "\n* No lowercase character(s)!"
            reject = True
        if not digitsExist:
            rejectionMsg += "\n* No Digits!"
            reject = True
        if not specialCharExist:
            rejectionMsg += "\n* No special character(s)!"
            reject = True
        return reject, rejectionMsg

    # shows or hides password
    def showOrHidePassAction(self):
        currentShowState = self.newPasswordEntry.cget('show')
        if currentShowState == '*':
            self.newPasswordEntry.configure(show='')
            self.reenterPasswordEntry.configure(show='')
            self.showOrHidePassButton.configure(image=self.iconObj.notShowHiddenImg)
        else:
            self.newPasswordEntry.configure(show='*')
            self.reenterPasswordEntry.configure(show='*')
            self.showOrHidePassButton.configure(image=self.iconObj.showHiddenImg)








# The frame for the password input and authentication
class PasswordAuthFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.objs = self.parent.getObjs()
        self.iconObj = self.objs['iconObj']
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)
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
                                          show='*',
                                          height=10,
                                          width=0
                                          )
        self.passwordEntry.grid(row=0,
                                column=1,
                                rowspan=1,
                                columnspan=1,
                                sticky='we'
                                )
        self.passwordEntry.bind('<Return>', self.submitPassword)
        # show or hide password button
        self.showOrHidePassButton = ctk.CTkButton(self,
                                          image=self.iconObj.showHiddenImg,
                                          text='',
                                          width=30,
                                          height=20,
                                          fg_color='#0074ff',
                                          hover_color='#002450',
                                          command=self.showOrHidePassAction)
        self.showOrHidePassButton.grid(row=0,
                                      column=2,
                                      rowspan=1,
                                      columnspan=1,
                                      sticky='e'
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
    def submitPassword(self, eventInfo=None):
        password = self.passwordEntry.get()
        # get the only row from CryptInfo table
        cryptInfoPrimitive = self.parent.presistentDBObj.getCryptInfoRow()[0]
        if not len(cryptInfoPrimitive):
            tk.messagebox.showwarning(title='Decryption Error',
                                      message='No password or decryption Information found!')
        else:
            # set up the crypt object with the values from the 
            # CryptInfo table row
            self.parent.cryptObj = CryptographyHandler(password,
                                                        cryptInfoPrimitive['encryptedKey'],
                                                        cryptInfoPrimitive['encryptKeyIV'],
                                                        cryptInfoPrimitive['generateKeySalt'],
                                                        cryptInfoPrimitive['hashKeySalt'],
                                                        cryptInfoPrimitive['hashedKey'],
                                                        )
        self.parent.dataFormatterObj = DataFormatter(self.parent.cryptObj)
        # check if the password is the correct password
        # if the password is correnct then get loginInfo column
        # data from UserInfo table and place them after decrypting and
        # decoding into the LoginInfo table in the memory database 
        if not self.parent.cryptObj.getAuthStatus():
            tk.messagebox.showwarning(title='Authentication Failed',
                                      message='Authentication Failed, re-enter password')
        else:
            encryptedLoginInfoPrimitiveS = self.parent.presistentDBObj.getAllLoginInfo()
            for encryptedLoginInfoPrimitive in encryptedLoginInfoPrimitiveS:
                loginInfoPrimitive = self.parent.cryptObj.decrypt(encryptedLoginInfoPrimitive)
                loginInfoEntry = self.parent.dataFormatterObj.convertToPythonType(loginInfoPrimitive['loginInfo'])
                self.parent.memDBObj.addNewEntry(loginInfoEntry)
            self.parent.passwordAuthFrame.grid_forget()
            self.parent.drawContent()

    # sets to show or hide text value in the entry box
    def showOrHidePassAction(self):
        currentShowState = self.passwordEntry.cget('show')
        if currentShowState == '*':
            self.passwordEntry.configure(show='')
            self.showOrHidePassButton.configure(image=self.iconObj.notShowHiddenImg)
        else:
            self.passwordEntry.configure(show='*')
            self.showOrHidePassButton.configure(image=self.iconObj.showHiddenImg)









# Reset Password frame
class ResetPasswordToplevel(ctk.CTkToplevel):
    def __init__(self, parent, objs, **kwargs):
        super().__init__(parent, **kwargs)
        self.geometry("600x200")
        self.resizable(False, False)
        self.title('Set New Password')
        self.grab_set()
        self.objs = objs
        self.iconObj = self.objs['iconObj']
        # configure the rows and columns
        for row in range(4):
            self.grid_rowconfigure(row, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)
        # enter current password label and entry
        self.currentPasswordLabel = ctk.CTkLabel(self,
                                                 text='Enter Current Password: ')
        self.currentPasswordLabel.grid(row=0,
                                      column=0,
                                      rowspan=1,
                                      columnspan=1,
                                      sticky='w'
                                      )
        self.currentPasswordEntry = ctk.CTkEntry(self,
                                                 show='*'
                                                 )
        self.currentPasswordEntry.grid(row=0,
                                      column=1,
                                      rowspan=1,
                                      columnspan=1,
                                      sticky='we'
                                      )
        # show or hide password button
        self.showOrHidePassButton = ctk.CTkButton(self,
                                          image=self.iconObj.showHiddenImg,
                                          text='',
                                          width=30,
                                          height=20,
                                          fg_color='#0074ff',
                                          hover_color='#002450',
                                          command=self.showOrHidePassAction)
        self.showOrHidePassButton.grid(row=0,
                                      column=2,
                                      rowspan=1,
                                      columnspan=1,
                                      sticky='e'
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
        self.newPasswordEntry = ctk.CTkEntry(self,
                                             show='*'
                                             )
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
        self.reenterPasswordEntry = ctk.CTkEntry(self,
                                                 show='*'
                                                 )
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
        currentPassword = self.currentPasswordEntry.get()
        newPassword = self.newPasswordEntry.get()
        reenteredNewPassword = self.reenterPasswordEntry.get()
        reject, rejectionMsg = self.checkPasswordStandard(newPassword, reenteredNewPassword)
        # verify the current password
        currentPasswordVerification = self.objs['cryptObj'].verifyPassword(currentPassword)
        if not currentPasswordVerification:
            tk.messagebox.showwarning(title='Wrong Password',
                                      message='The current password is wrong!')
        if reject:
            tk.messagebox.showwarning(title='Password Not Accepted',
                                      message=f"The Password is not accepted for the following reasons:{rejectionMsg}")
        if currentPasswordVerification and not reject:
            self.copyPersistentDatabase(newPassword)
            self.destroy()

    # creates a temporary database and copies the values from the
    # current database (decrypt with old key and encrypt with new key)
    # into the temporary database. Then deletes the current database and
    # renames the temporary database to the name of the current database.
    def copyPersistentDatabase(self, newPassword):
        # create new cryptObj and presistentDBObj
        presistentDBObj = PresistentDatabaseHandler('userDataTmp')
        cryptObj = CryptographyHandler(newPassword)
        (encryptedKey,
        encryptKeyIV,
        generateKeySalt,
        hashKeySalt,
        hashedKey,
        ) = cryptObj.getCryptValues()
        presistentDBObj.addCryptInfoEntry({
            'encryptedKey': encryptedKey,
            'encryptKeyIV': encryptKeyIV,
            'generateKeySalt': generateKeySalt,
            'hashKeySalt': hashKeySalt,
            'hashedKey': hashedKey
        })
        # get all the rows from the old database and decrypt and 
        # encrypt them with the new credentials.
        encryptedUserInfoPrimitiveS = self.objs['presistentDBObj'].getAllUserInfo()
        for encryptedUserInfoPrimitive in encryptedUserInfoPrimitiveS:
            userInfoPrimitive = self.objs['cryptObj'].decrypt(encryptedUserInfoPrimitive)
            encryptedUserInfoEntry = cryptObj.encrypt(userInfoPrimitive)
            presistentDBObj.addUserInfoEntry(encryptedUserInfoEntry)
        # set the new cryptObj and presistentDBObj object values in
        # the main window.
        self.objs['mainWindow'].cryptObj = cryptObj
        # delete the old database and rename the new database
        presistentDBObj.disconnectDB()
        self.objs['presistentDBObj'].disconnectDB()
        del presistentDBObj
        del self.objs['mainWindow'].presistentDBObj
        del self.objs['presistentDBObj']
        if os.path.exists('userData.db'):
            os.remove('userData.db')
            os.rename('userDataTmp.db', 'userData.db')
        else:
            os.remove('userDataTmp.db')
        presistentDBObj= PresistentDatabaseHandler()
        self.objs['mainWindow'].presistentDBObj = presistentDBObj
        self.objs['mainWindow'].removeAllContent()
        self.objs['mainWindow'].drawContent()

    # check to see if the new password fits the password standard
    def checkPasswordStandard(self, newPassword, reenteredNewPassword):
        rejectionMsg = ''
        reject = False
        if len(newPassword) < 9:
            rejectionMsg += "\n* Password Length less than 9 characters!"
            reject = True
        if newPassword != reenteredNewPassword:
            rejectionMsg += "\n* The Re-Entered Password does not Match!"
            reject = True
        upperCaseExist = False
        lowerCaseExist = False
        digitsExist = False
        specialCharExist = False
        for passwordChar in newPassword:
            if passwordChar.isupper():
                upperCaseExist = True
            elif passwordChar.islower():
                lowerCaseExist = True
            elif passwordChar.isdigit():
                digitsExist = True
            elif passwordChar in string.punctuation:
                specialCharExist = True
        if not upperCaseExist:
            rejectionMsg += "\n* No uppercase character(s)!"
            reject = True
        if not lowerCaseExist:
            rejectionMsg += "\n* No lowercase character(s)!"
            reject = True
        if not digitsExist:
            rejectionMsg += "\n* No Digits!"
            reject = True
        if not specialCharExist:
            rejectionMsg += "\n* No special character(s)!"
            reject = True
        return reject, rejectionMsg

    # sets to show or hide text value in the entry box
    def showOrHidePassAction(self):
        currentShowState = self.currentPasswordEntry.cget('show')
        if currentShowState == '*':
            self.currentPasswordEntry.configure(show='')
            self.newPasswordEntry.configure(show='')
            self.reenterPasswordEntry.configure(show='')
            self.showOrHidePassButton.configure(image=self.iconObj.notShowHiddenImg)
        else:
            self.currentPasswordEntry.configure(show='*')
            self.newPasswordEntry.configure(show='*')
            self.reenterPasswordEntry.configure(show='*')
            self.showOrHidePassButton.configure(image=self.iconObj.showHiddenImg)







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
        self.grid_columnconfigure(2, weight=1)
        for idx in  range(9):
            self.grid_rowconfigure(idx, weight=1)
        self.grid_rowconfigure(6, weight=4)
        self.objs = objs
        self.iconObj = self.objs['iconObj']
        # initialize variables
        self.selectTypeBoxValue = None
        self.file = None
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
                        columnspan=2,
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
                        columnspan=1,
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
                                      column=2,
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
                        columnspan=2,
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
        self.fieldDict['AddButton'] = {'label': None,
                                       'entry': addButton
                                      }

    # choose file to add to the new entry
    def chooseFile(self):
        self.file = ctk.filedialog.askopenfile(parent=self, mode='rb', initialdir='/')
        if self.file:
            self.fieldDict['file']['entry'].configure(text=f"{self.file.name.split('/')[-1][:50]}")

    # the action to create a new database entry (row) based on the entered values
    def addAction(self):
        loginInfoEntry = {}
        loginInfoEntry['uniqueID'] = str(uuid.uuid4())
        for key in self.fieldDict.keys():
            if key != 'notes' and key != 'file' and key != 'AddButton':
                loginInfoEntry[key] = self.fieldDict[key]['entry'].get()
        loginInfoEntry['notes'] = self.fieldDict['notes']['entry'].get('0.0', 'end')
        loginInfoEntry['fileName'] = None
        fileData = None
        if self.file:
            loginInfoEntry['fileName'] = self.file.name.split('/')[-1]
            fileData = self.file.read()
        self.objs['memDBObj'].addNewEntry(loginInfoEntry)
        loginInfoEntryBytes = self.objs['dataFormatterObj'].convertToBytes(loginInfoEntry)
        encryptedUserInfoEntry = self.objs['cryptObj'].encrypt({'uniqueID' : loginInfoEntry['uniqueID'],
                                                                'loginInfo': loginInfoEntryBytes,
                                                                'fileInfo': fileData
                                                                })
        self.objs['presistentDBObj'].addUserInfoEntry(encryptedUserInfoEntry)
        self.destroy()

    # sets to show or hide text value in the entry box
    def showOrHidePassAction(self):
        currentShowState = self.fieldDict['password']['entry'].cget('show')
        if currentShowState == '*':
            self.fieldDict['password']['entry'].configure(show='')
            self.showOrHidePassButton.configure(image=self.iconObj.notShowHiddenImg)
        else:
            self.fieldDict['password']['entry'].configure(show='*')
            self.showOrHidePassButton.configure(image=self.iconObj.showHiddenImg)