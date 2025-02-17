import customtkinter as ctk
import tkinter as tk
from database import PresistentDatabaseHandler, CryptographyHandler






# the frame for syncing with external database
class SyncFrame(ctk.CTkFrame):
    def __init__(self, parent, objs, **kwargs):
        super().__init__(parent, **kwargs)
        self.objs = objs
        iconObj = self.objs['iconObj']
        # the variable that records the current selected operation
        self.operationMode = 'export'
        self.operation = None
        # the radio button to choose export sync option
        self.exportRadioButton = ctk.CTkRadioButton(self,
                                                    text='Export',
                                                    command=self.unckeckImportRadioButton)
        self.exportRadioButton.select()
        self.exportRadioButton.pack(side='left')
        # the radio button to choose import sync option
        self.importRadioButton = ctk.CTkRadioButton(self,
                                                    text='Import',
                                                    command=self.unckeckExportRadioButton)
        self.importRadioButton.deselect()
        self.importRadioButton.pack(side='left')
        # combo box to select the operaton mode
        self.operationModes = ['Choose...', 
                                'Add New Entries', 
                                'Delete Missing Entries', 
                                'Conform Modified Entries'
                                ]
        self.selectOperationMode = ctk.CTkComboBox(self,
                                                    values=self.operationModes,
                                                    state='readonly',
                                                    width=200,
                                                    command=self.setOperationMode
                                                    )
        self.selectOperationMode.set('Choose...')
        self.selectOperationMode.pack(side='left')
        # button to call on the sync operation
        self.syncButton = ctk.CTkButton(self,
                                        text='',
                                        image=iconObj.syncEntryImg,
                                        anchor='center',
                                        width=50,
                                        height=30,
                                        command=self.syncAction
                                        )
        self.syncButton.pack(side='left', fill='y', expand=True)

    # sets the operationMode to export and deselects the 
    # other operationMode radio button
    def unckeckImportRadioButton(self):
        self.importRadioButton.deselect()
        self.operationMode = 'export'
 
    # sets the operationMode to import and deselects the 
    # other operationMode radio button
    def unckeckExportRadioButton(self):
        self.exportRadioButton.deselect()
        self.operationMode = 'import'

    # sets the operation mode for new entry, delete entry
    # or to update entries between two databases.
    def setOperationMode(self, operation):
        self.operation = operation

    # this method uses the operation and operationMode variables
    # to perform sync operation between two different databases.
    def syncAction(self):
        if self.operation == 'Choose...' or self.operation == None:
            tk.messagebox.showwarning(title = 'Invalid Operation',
                                      message = 'Please Choose an option from the drop-down box.'
                                     )
            return
        externalDBLocation = tk.filedialog.askopenfilename()
        if not externalDBLocation:
            return
        else:
            externalDBLocation = externalDBLocation[0:-3]
        # based on operationMode, set the fromDB and toDB
        # along with their CryptObjs
        if self.operationMode == 'export':
            fromDBHandler = self.objs['presistentDBObj']
            fromDBCryptObj = self.objs['cryptObj'] 
            toDBHandler = PresistentDatabaseHandler(externalDBLocation.split('.')[0])
            cryptInfoPrimitive = toDBHandler.getCryptInfoRow()[0]
            toDBCryptObj = CryptographyHandler(self.objs['cryptObj'].getPassword(),
                                                cryptInfoPrimitive['encryptedKey'],
                                                cryptInfoPrimitive['encryptKeyIV'],
                                                cryptInfoPrimitive['generateKeySalt'],
                                                cryptInfoPrimitive['hashKeySalt'],
                                                cryptInfoPrimitive['hashedKey'],
                                                )
            if not toDBCryptObj.getAuthStatus():
                tk.messagebox.showwarning(title = 'Password Mismatch',
                                          message = 'The password of the current database did not match the external database; cannot decrypt!'
                                          )
                return
        elif self.operationMode == 'import':
            toDBHandler = self.objs['presistentDBObj']
            toDBCryptObj = self.objs['cryptObj']
            fromDBHandler = PresistentDatabaseHandler(externalDBLocation)
            cryptInfoPrimitive = fromDBHandler.getCryptInfoRow()[0]
            fromDBCryptObj = CryptographyHandler(self.objs['cryptObj'].getPassword(),
                                                cryptInfoPrimitive['encryptedKey'],
                                                cryptInfoPrimitive['encryptKeyIV'],
                                                cryptInfoPrimitive['generateKeySalt'],
                                                cryptInfoPrimitive['hashKeySalt'],
                                                cryptInfoPrimitive['hashedKey'],
                                                )
            if not fromDBCryptObj.getAuthStatus():
                tk.messagebox.showwarning(title= 'Password Mismatch',
                                          message= 'The password of the current database did not match the external database; cannot decrypt!'
                                          )
                return
        # call the necessary sync action as per selection
        if self.operation == 'Add New Entries':
            self.copyNewEntries(fromDBHandler, 
                                toDBHandler, 
                                fromDBCryptObj, 
                                toDBCryptObj
                                )
        elif self.operation == 'Delete Missing Entries':
            self.deleteEntries(fromDBHandler, toDBHandler)
        elif self.operation == 'Conform Modified Entries':
            self.updateEntries(fromDBHandler, 
                               toDBHandler, 
                               fromDBCryptObj, 
                               toDBCryptObj
                               )
        tk.messagebox.showwarning(title = 'Success',
                                  message = 'The Sync Action was successful'
                                 )
        self.objs['mainWindow'].searchFrame.searchAction()

    # copies new entries in fromDB to toDB
    def copyNewEntries(self, fromDBHandler, toDBHandler, fromDBCryptObj, toDBCryptObj):
        fromDBAllUniqueIDS = self.getUniqueIDS(fromDBHandler)
        toDBAllUniqueIDS = self.getUniqueIDS(toDBHandler)
        newEntriesUniqueIDS = fromDBAllUniqueIDS - toDBAllUniqueIDS
        insertIntoMemDB = True if toDBHandler == self.objs['presistentDBObj'] else False
        for uniqueID in newEntriesUniqueIDS:
            #encryptedUserInfoPrimitive = fromDBHandler.getUserInfoOnUniqueID(uniqueID)[0]
            userInfoPrimitive = self.decryptRow(fromDBCryptObj, fromDBHandler, uniqueID)
            if insertIntoMemDB:
                loginInfoEntry = self.objs['dataFormatterObj'].convertToPythonType(userInfoPrimitive['loginInfo'])
                self.objs['memDBObj'].addNewEntry(loginInfoEntry)
            encryptedUserInfoPrimitive = toDBCryptObj.encrypt(userInfoPrimitive)
            toDBHandler.addUserInfoEntry(encryptedUserInfoPrimitive)

    # entries in toDB but not in fromDB are deleted from toDB        
    def deleteEntries(self, fromDBHandler, toDBHandler):
        fromDBAllUniqueIDS = self.getUniqueIDS(fromDBHandler)
        toDBAllUniqueIDS = self.getUniqueIDS(toDBHandler)
        deleteEntriesUniqueIDS = toDBAllUniqueIDS - fromDBAllUniqueIDS
        deleteFromMemDB = True if toDBHandler == self.objs['presistentDBObj'] else False
        for uniqueID in deleteEntriesUniqueIDS:
            toDBHandler.deleteUserInfoEntry(uniqueID)
            if deleteFromMemDB:
                self.objs['memDBObj'].deleteEntry(uniqueID)

    # if toDB has entries with same uniqueID as the fromDB but their 
    # values don't match; then the values of the fromDB are copied to
    # the toDB
    def updateEntries(self, fromDBHandler, toDBHandler, fromDBCryptObj, toDBCryptObj):
        fromDBAllUniqueIDS = self.getUniqueIDS(fromDBHandler)
        toDBAllUniqueIDS = self.getUniqueIDS(toDBHandler)
        commonUniqueIDS = fromDBAllUniqueIDS.intersection(toDBAllUniqueIDS)
        updateMemDB = True if toDBHandler == self.objs['presistentDBObj'] else False
        for uniqueID in commonUniqueIDS:
            fromDBUserInfoPrimitive = self.decryptRow(fromDBCryptObj, fromDBHandler, uniqueID)
            toDBUserInfoPrimitive = self.decryptRow(toDBCryptObj, toDBHandler, uniqueID)
            if fromDBUserInfoPrimitive != toDBUserInfoPrimitive:
                if updateMemDB:
                    loginInfoEntry = self.objs['dataFormatterObj'].convertToPythonType(fromDBUserInfoPrimitive['loginInfo'])
                    self.objs['memDBObj'].modifyLoginInfoEntry(loginInfoEntry)
                encryptedFromDBUserInfoPrimitive = toDBCryptObj.encrypt(fromDBUserInfoPrimitive)
                toDBHandler.updateUserInfoEntry({'uniqueID': uniqueID,
                                                 'loginInfo': encryptedFromDBUserInfoPrimitive['loginInfo'],
                                                 'fileInfo': encryptedFromDBUserInfoPrimitive['fileInfo']
                                                })

    # get a set of UUID4 based uniqueID for a given database
    def getUniqueIDS(self, dbHandler):
        allUniqueIDPrimitiveS = dbHandler.getAllUniqueID()
        allUniqueIDS = []
        for allUniqueIDPrimitive in allUniqueIDPrimitiveS:
            allUniqueIDS.append(allUniqueIDPrimitive['uniqueID'])
        return set(allUniqueIDS)

    # for a database get a row baed on uniqueID and 
    # decrypt it
    def decryptRow(self, cryptObj, dbHandler, uniqueID):
        encryptedUserInfoPrimitive = dbHandler.getUserInfoOnUniqueID(uniqueID)[0]
        userInfoPrimitive = cryptObj.decrypt(encryptedUserInfoPrimitive)
        return userInfoPrimitive
