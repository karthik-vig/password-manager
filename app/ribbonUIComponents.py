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
                                        height=0,
                                        command=self.syncAction
                                        )
        self.syncButton.pack(side='left', fill='y', expand=True)

    #
    def unckeckImportRadioButton(self):
        self.importRadioButton.deselect()
        self.operationMode = 'export'
 
    def unckeckExportRadioButton(self):
        self.exportRadioButton.deselect()
        self.operationMode = 'import'

    def setOperationMode(self, operation):
        self.operation = operation

    def syncAction(self):
        print('called the sync action')
        if self.operation == 'Choose...' or self.operation == None:
            tk.messagebox.showwarning(title = 'Invalid Operation',
                                      message = 'Please Choose an option from the drop-down box.'
                                     )
            return
        externalDBLocation = tk.filedialog.askopenfilename()
        if not externalDBLocation:
            return
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
        if self.operation == 'Add New Entries':
            self.copyNewEntries(fromDBHandler, toDBHandler)
        elif self.operation == 'Delete Missing Entries':
            self.deleteEntries(fromDBHandler, toDBHandler)
        elif self.operation == 'Conform Modified Entries':
            self.updateEntries(fromDBHandler, toDBHandler, fromDBCryptObj, toDBCryptObj)
        tk.messagebox.showwarning(title = 'Success',
                                  message = 'The Sync Action was successful'
                                 )

    # copies new entries in fromDB to toDB
    def copyNewEntries(self, fromDBHandler, toDBHandler):
        fromDBAllUniqueIDS = self.getUniqueIDS(fromDBHandler)
        toDBAllUniqueIDS = self.getUniqueIDS(toDBHandler)
        newEntriesUniqueIDS = fromDBAllUniqueIDS - toDBAllUniqueIDS
        for uniqueID in newEntriesUniqueIDS:
            encryptedUserInfoPrimitive = fromDBHandler.getUserInfoOnUniqueID(uniqueID)[0]
            toDBHandler.addUserInfoEntry(encryptedUserInfoPrimitive)

    # entries in toDB but not in fromDB are deleted from toDB        
    def deleteEntries(self, fromDBHandler, toDBHandler):
        fromDBAllUniqueIDS = self.getUniqueIDS(fromDBHandler)
        toDBAllUniqueIDS = self.getUniqueIDS(toDBHandler)
        deleteEntriesUniqueIDS = toDBAllUniqueIDS - fromDBAllUniqueIDS
        for uniqueID in deleteEntriesUniqueIDS:
            toDBHandler.deleteUserInfoEntry(uniqueID)

    # if toDB has entries with same uniqueID as the fromDB but their 
    # values don't match; then the values of the fromDB are copied to
    # the toDB
    def updateEntries(self, fromDBHandler, toDBHandler, fromDBCryptObj, toDBCryptObj):
        fromDBAllUniqueIDS = self.getUniqueIDS(fromDBHandler)
        toDBAllUniqueIDS = self.getUniqueIDS(toDBHandler)
        commonUniqueIDS = fromDBAllUniqueIDS.intersection(toDBAllUniqueIDS)
        for uniqueID in commonUniqueIDS:
            fromDBUserInfoPrimitive = self.decryptRow(fromDBCryptObj, fromDBHandler, uniqueID)
            toDBUserInfoPrimitive = self.decryptRow(toDBCryptObj, toDBHandler, uniqueID)
            if fromDBUserInfoPrimitive != toDBUserInfoPrimitive:
                toDBHandler.addUserInfoEntry({'uniqueID': uniqueID,
                                              'loginInfo': toDBCryptObj.encrypt(fromDBUserInfoPrimitive['loginInfo']),
                                              'fileInfo': toDBCryptObj.encrypt(fromDBUserInfoPrimitive['fileInfo'])
                                              })

    def getUniqueIDS(self, dbHandler):
        allUniqueIDPrimitiveS = dbHandler.getAllUniqueID()
        allUniqueIDS = []
        for allUniqueIDPrimitive in allUniqueIDPrimitiveS:
            allUniqueIDS.append(allUniqueIDPrimitive['uniqueID'])
        return set(allUniqueIDS)

    def decryptRow(self, cryptObj, dbHandler, uniqueID):
        encryptedUserInfoPrimitive = dbHandler.getUserInfoOnUniqueID(uniqueID)[0]
        userInfoPrimitive = cryptObj.decrypt(encryptedUserInfoPrimitive)
        return userInfoPrimitive