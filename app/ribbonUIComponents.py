import customtkinter as ctk






# the frame for syncing with external database
class SyncFrame(ctk.CTkFrame):
    def __init__(self, parent, iconObj, **kwargs):
        super().__init__(parent, **kwargs)
        # the variable that records the current selected operation
        self.operation = 'export'
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
        self.operation = 'export'
 
    def unckeckExportRadioButton(self):
        self.exportRadioButton.deselect()
        self.operation = 'import'

    def setOperationMode(self, operationMode):
        print(operationMode)

    def syncAction(self):
        print('called the sync action')