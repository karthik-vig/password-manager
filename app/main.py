import customtkinter as ctk
from PIL import Image
from database import DataFormatter, PresistentDatabaseHandler, MemoryDatabaseHandler, CryptographyHandler
from mainUIComponents import SearchFrame, ItemListFrame, RibbonFrame, ItemInformationFrame
from toplevelUIComponents import PasswordAuthFrame, SetPasswordFrame
import os
import pathlib





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
        self.saveFileImg = ctk.CTkImage(dark_image=Image.open('icons/buttonIcon/saveFile.png'),
                                        size=(20, 20)
                                        )
        self.syncEntryImg = ctk.CTkImage(dark_image=Image.open('icons/buttonIcon/syncEntry.png'),
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
    def __init__(self):
        super().__init__()
        self.iconObj = Icons()
        self.memDBObj = MemoryDatabaseHandler()
        self.presistentDBObj = None
        self.dataFormatterObj = None
        self.cryptObj = None
        self.title("Password Manager")
        databasePath = pathlib.Path(__file__).parent.resolve()
        databasePath = str(databasePath).replace('\\', '/')
        upOneFolderIdx = databasePath.rfind('/')
        databasePath = databasePath[:upOneFolderIdx]
        dirList = os.listdir(databasePath)
        if 'userData.db' in dirList:
            self.presistentDBObj = PresistentDatabaseHandler()
            self.drawPasswordAuth()
        else:
            self.drawCreateNewDB()

    #
    def getObjs(self):
        return {'iconObj': self.iconObj,
                'memDBObj': self.memDBObj,
                'presistentDBObj': self.presistentDBObj,
                'dataFormatterObj': self.dataFormatterObj,
                'cryptObj': self.cryptObj,
                'mainWindow': self
               }
    # draws the windows to create a new sqlite
    # database if an existing one is not found
    def drawCreateNewDB(self):
        self.geometry("400x150")
        self.resizable(False, False)
        # configure the rows and column sizes
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # place the frames in the grid
        self.setPassFrame = SetPasswordFrame(parent=self, height=150, width=400)
        self.setPassFrame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky='nsew')

    # draws the password input and submission window
    # upon authetication; will draw the content window
    def drawPasswordAuth(self):
        self.geometry("400x150")
        self.resizable(False, False)
        # configure the rows and column sizes
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # place the frames in the grid
        self.passwordAuthFrame = PasswordAuthFrame(parent=self, height=150, width=400)
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
        self.searchFrame = SearchFrame(parent=self, objs=self.getObjs(), height=0, width=0)
        self.searchFrame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky='nsew', padx=5, pady=8)
        self.ribbonFrame = RibbonFrame(parent=self, objs=self.getObjs(), height=0, width=0)
        self.ribbonFrame.grid(row=0, column=1, rowspan=1, columnspan=1, sticky='nsew', padx=5, pady=8)
        self.itemListFrame = ItemListFrame(parent=self, objs=self.getObjs(), height=0, width=0)
        self.itemListFrame.grid(row=1, column=0, rowspan=1, columnspan=1, sticky='nsew', padx=5, pady=8)
        self.itemInfoFrame = ItemInformationFrame(parent=self, objs=self.getObjs(), height=0, width=0)
        self.itemInfoFrame.grid(row=1, column=1, rowspan=1, columnspan=1, sticky='nsew', padx=5, pady=8)

    # removes all the UI elements on the Windows
    def removeAllContent(self):
        self.searchFrame.destroy()
        self.ribbonFrame.destroy()
        self.itemInfoFrame.destroy()
        self.itemListFrame.destroy()

                                        
                                    
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_widget_scaling(1.1)
    ctk.set_window_scaling(1.0)
    app = Window()
    app.mainloop()