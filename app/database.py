from sqlalchemy import create_engine, Column, Integer, String, update, or_, ForeignKey, LargeBinary
from sqlalchemy.orm import Session, registry, relationship
import os
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
import cryptography
import pathlib



# handles all data formatting
class DataFormatter:
    def __init__(self, cryptObj):
        self.cryptObj = cryptObj

    # converts a python dict/list of dict structure to bytes
    def convertToBytes(self, data):
        return bytes( json.dumps(data), encoding='utf-16' )

    # converts bytes back into python dict/list of dict
    def convertToPythonType(self, data):
        return json.loads( data.decode('utf-16') )

    # converts sqlalchemy result to python datatype,
    # where a row is a dict and multiple rows are given as
    # a list of dicts
    def convertRowsToListOfDict(self, rows):
        primitiveRows = []
        for row in rows:
            if str(type(row)) == "<class 'sqlalchemy.engine.row.Row'>":
                dictFormat = dict(row._mapping)
            else:
                dictFormat = row.__dict__
                del dictFormat['_sa_instance_state']
            primitiveRows.append(dictFormat)
        return primitiveRows





# handles all cryptographic functionalities
class CryptographyHandler:
    def __init__(self, 
                 password, 
                 encryptedKey= None,
                 encryptKeyIV = None,
                 generateKeySalt = None,
                 hashKeySalt = None,
                 hashedKey = None
                 ):
        self.password = password
        self.encryptKeyIV = encryptKeyIV
        self.generateKeySalt = generateKeySalt
        self.hashKeySalt = hashKeySalt
        self.hashedKey = hashedKey
        self.encryptedKey = encryptedKey
        self.mainAESKey = self.getMainAESKey(encryptedKey)

    # get the authentication status of the password
    # input using the constructor
    def getAuthStatus(self):
        if self.mainAESKey == None:
            return False
        return True

    # get the key to decrypt the presistent database
    def getMainAESKey(self, encryptedKey):
        if encryptedKey is None:
            (key, 
            self.encryptedKey,
            self.encryptKeyIV,
            self.generateKeySalt,
            self.hashKeySalt,
            self.hashedKey
            ) = self._createNewKey()
        else:
            key = self._decryptAESKey(encryptedKey)
        return key

    # creates a new key and sets up the verification 
    # values
    def _createNewKey(self):
        mainAESKey = os.urandom(32)

        firstSalt = os.urandom(16)
        kdf1 = self._setupPBKDF2(firstSalt)
        keyForMainAESKey = kdf1.derive(bytes(self.password, encoding='utf-16'))

        initVecForMainAESKey = os.urandom(16)
        encryForKey, decryForKey = self._setupAESAlg(keyForMainAESKey,
                                                initVecForMainAESKey)                                    
        encrypAESKeyVal = encryForKey.update(mainAESKey) + encryForKey.finalize()

        secondSalt = os.urandom(16)
        kdf2 = self._setupPBKDF2(secondSalt)
        hashedKey = kdf2.derive(keyForMainAESKey)

        return ( mainAESKey,
                 encrypAESKeyVal,
                 initVecForMainAESKey,
                 firstSalt,
                 secondSalt,
                 hashedKey
                )

    # get the current state of the encryption/decryption values
    def getCryptValues(self):
        return (self.encryptedKey,
                self.encryptKeyIV,
                self.generateKeySalt,
                self.hashKeySalt,
                self.hashedKey,
                )

    # get the password
    def getPassword(self):
        return self.password

    # using the password verify it, and decrypt and get the actually
    # key to decrypt the database.
    def _decryptAESKey(self, encryptedKey):
        kdf1 = self._setupPBKDF2(self.generateKeySalt)
        kdf2 = self._setupPBKDF2(self.hashKeySalt)
        keyToDecryptKey = kdf1.derive(bytes(self.password, encoding='utf-16'))
        try:
            kdf2.verify(keyToDecryptKey,
                       self.hashedKey)
            encryptor, decryptor = self._setupAESAlg(keyToDecryptKey,
                                                     self.encryptKeyIV
                                                    )
            key = decryptor.update(encryptedKey) + decryptor.finalize()
        except cryptography.exceptions.InvalidKey as e:
            key = None
        return key

    # given a password verify if it can decrypt the database
    def verifyPassword(self, password):
        kdf1 = self._setupPBKDF2(self.generateKeySalt)
        kdf2 = self._setupPBKDF2(self.hashKeySalt)
        keyToDecryptKey = kdf1.derive(bytes(password, encoding='utf-16'))
        try:
            kdf2.verify(keyToDecryptKey,
                       self.hashedKey)
            return True
        except cryptography.exceptions.InvalidKey as e:
            return False

    # factory to setup the AES256 algorithm
    def _setupAESAlg(self, key, initVec): 
        cipher = Cipher(algorithms.AES256( key ), 
                        modes.CBC(initVec)
                        )
        encryptor = cipher.encryptor()
        decryptor = cipher.decryptor()
        return encryptor, decryptor

    # factory to setup the hashing algorithm of PBKDF2
    def _setupPBKDF2(self, salt):
        return PBKDF2HMAC(
                        algorithm=hashes.SHA512,
                        length=32,
                        salt=salt,
                        iterations=480000
                        )

    # takes in a dictionary and encrypts the value for each of its keys 
    # except uuid
    def encrypt(self, data):
        encryptIV = os.urandom(16) 
        encryptor, decryptor = self._setupAESAlg(self.mainAESKey,
                                                 encryptIV
                                                )
        for key in data.keys():
            if key != 'uniqueID' and data[key] != None:
                padder = padding.PKCS7(128).padder()
                paddedData = padder.update(data[key]) + padder.finalize()
                data[key] = encryptor.update(paddedData)
                data[key] = encryptIV + data[key]
        return data

    # takes in a dictionary and decrypts the value for each of its keys
    # except uuid
    def decrypt(self, data):
        for key in data.keys():
            if key != 'uniqueID' and data[key] != None:
                encryptor , decryptor = self._setupAESAlg(self.mainAESKey,
                                                          data[key][0:16]
                                                        )
                paddedData = decryptor.update(data[key][16:])
                unpadder = padding.PKCS7(128).unpadder()
                data[key] = unpadder.update(paddedData) + unpadder.finalize()
        return data




# handles connection and operation with presistent database
class PresistentDatabaseHandler:
    # connect with the presistent database
    def __init__(self, databaseName=None):
        if not databaseName:
            databaseName = 'userData'
            databasePath = pathlib.Path(__file__).parent.resolve()
            databasePath = str(databasePath).replace('\\', '/')
            upOneFolderIdx = databasePath.rfind('/')
            databasePath = databasePath[:upOneFolderIdx] + '/' + databaseName
        else:
            databasePath = databaseName
        self.engine = create_engine(f"sqlite+pysqlite:///{databasePath}.db")
        self.registryMapper = registry()
        self.Base = self.registryMapper.generate_base()
        self.UserInfo, self.CryptInfo = self._createTables()
        self.registryMapper.metadata.create_all(self.engine)
        self.dataFormatterObj = DataFormatter(None)

    # creates the tables in the presistent database
    def _createTables(self):
        # the table contains the encrypted entries 
        class UserInfo(self.Base):
            __tablename__ = "UserInfo"
            uniqueID = Column(String(36), primary_key=True)
            loginInfo = Column(LargeBinary, nullable=False)
            fileInfo = Column(LargeBinary, nullable=True)
            def __repr__(self):
                return f"The Table that contains the encrypted binary info."

        # this table only contains one row; used for encryption and decryption
        class CryptInfo(self.Base):
            __tablename__ = "CryptInfo"
            encryptedKey = Column(LargeBinary, primary_key=True)
            encryptKeyIV = Column(LargeBinary, nullable=False)
            generateKeySalt = Column(LargeBinary, nullable=False)
            hashKeySalt = Column(LargeBinary, nullable=False)
            hashedKey = Column(LargeBinary, nullable=False)
        return UserInfo, CryptInfo

    # disconnects the link to the database
    def disconnectDB(self):
        self.engine.dispose()

    # get the only row in CryptInfo table
    def getCryptInfoRow(self):
        with Session(self.engine) as session:
            cryptInfoResult = session.query(self.CryptInfo).all()
        return self.dataFormatterObj.convertRowsToListOfDict(cryptInfoResult)

    # add a new row to the CryptInfo table
    def addCryptInfoEntry(self, cryptInfoEntry):
        with Session(self.engine) as session:
            session.add(self.CryptInfo(encryptedKey=cryptInfoEntry['encryptedKey'],
                                        encryptKeyIV=cryptInfoEntry['encryptKeyIV'],
                                        generateKeySalt=cryptInfoEntry['generateKeySalt'],
                                        hashKeySalt=cryptInfoEntry['hashKeySalt'],
                                        hashedKey=cryptInfoEntry['hashedKey']
                                       )
                            )
            session.commit()

    # delete the only row in CryptInfo table
    def deleteCryptInfoEntry(self):
        with Session(self.engine) as session:
            session.query(self.CryptInfo).delete()
            session.commit()

    # adds a new entry into the database
    def addUserInfoEntry(self, encryptedUserInfoEntry):
        #encryptedUserInfoEntry = self.cryptObj.encrypt(userInfoEntry)
        with Session(self.engine) as session:
            userInfoRow = self.UserInfo(uniqueID=encryptedUserInfoEntry['uniqueID'],
                                        loginInfo = encryptedUserInfoEntry['loginInfo'],
                                        fileInfo = encryptedUserInfoEntry['fileInfo']
                                        )
            session.add(userInfoRow)
            session.commit()

    # delets an entry from the database based on uuid
    def deleteUserInfoEntry(self, uniqueID):
        with Session(self.engine) as session:
            session.query(self.UserInfo).filter(self.UserInfo.uniqueID == uniqueID).delete()
            session.commit()

    # modifies the value for a given uuid
    def updateUserInfoEntry(self, encryptedUserInfoEntry):
        #encryptedUserInfoEntry = self.cryptObj.encrypt(userInfoEntry)
        with Session(self.engine) as session:
            session.execute(
                            update(self.UserInfo)\
                            .where(self.UserInfo.uniqueID == encryptedUserInfoEntry['uniqueID'])\
                            .values(loginInfo = encryptedUserInfoEntry['loginInfo'],
                                    fileInfo = encryptedUserInfoEntry['fileInfo']
                                    )
            )
            session.commit()

    # gets all the loginInfo in the decrypted form
    def getAllLoginInfo(self):
        with Session(self.engine) as session:
            encryptedLoginInfoResult = session.query(self.UserInfo.loginInfo).all()
        # need to process ecrypted result to a list of dicts
        encryptedLoginInfoPrimitiveS = self.dataFormatterObj.convertRowsToListOfDict(encryptedLoginInfoResult)
        return encryptedLoginInfoPrimitiveS

    # the value from the fileInfo column in UserInfo table for a specific UUID4 primary key value
    def getFileInfoOnUUID(self, uniqueID):
        with Session(self.engine) as session:
            encryptedFileInfoResult = session.query(self.UserInfo.fileInfo)\
                                      .filter(self.UserInfo.uniqueID == uniqueID).all()
        # need to conver the result in a dict first
        encryptedFileInfoPrimitiveS = self.dataFormatterObj.convertRowsToListOfDict(encryptedFileInfoResult)
        return encryptedFileInfoPrimitiveS

    # get a row from the UserInfo table based on the UUID4 primary key value
    def getUserInfoOnUniqueID(self, uniqueID):
        with Session(self.engine) as session:
            encryptedUserInfoResult = session.query(self.UserInfo)\
                                        .filter(self.UserInfo.uniqueID == uniqueID).all()
            encryptedUserInfoPrimitiveS = self.dataFormatterObj.convertRowsToListOfDict(encryptedUserInfoResult)
        return encryptedUserInfoPrimitiveS

    # get all the rows fo the UserInfo table
    def getAllUserInfo(self):
        with Session(self.engine) as session:
            encryptedUserInfoResult = session.query(self.UserInfo).all()
            encryptedUserInfoPrimitiveS = self.dataFormatterObj.convertRowsToListOfDict(encryptedUserInfoResult)
        return encryptedUserInfoPrimitiveS

    # get all the UUID4 primary key value from the UserInfo table
    def getAllUniqueID(self):
        with Session(self.engine) as session:
            allUniqueIDResult = session.query(self.UserInfo.uniqueID).all()
            allUniqueIDPrimitiveS = self.dataFormatterObj.convertRowsToListOfDict(allUniqueIDResult)
        return allUniqueIDPrimitiveS






# the in memory database handler
class MemoryDatabaseHandler:
    def __init__(self):
        self.engine = create_engine('sqlite+pysqlite:///:memory:')
        self.registryMapper = registry()
        self.Base = self.registryMapper.generate_base()
        self.LoginInfo = self._createTable()
        self.registryMapper.metadata.create_all(self.engine)
        self.dataFormatterObj = DataFormatter(None)

    # create and/or initializes the necessary table(s)
    def _createTable(self):
        class LoginInfo(self.Base):
            __tablename__ = "LoginInfo"
            uniqueID = Column(String(36), primary_key=True)
            entryName = Column(String(50), nullable=False)
            userName = Column(String(100), nullable=True)
            password = Column(String(50), nullable=True)
            email = Column(String(100), nullable=True)
            url = Column(String(500), nullable=True)
            notes = Column(String(20_000), nullable=True)
            entryType = Column(String(20), nullable=False)
            fileName = Column(String(100), nullable=True)
        return LoginInfo

    # add a new entry into the LoginInfo table and FileInfo table
    def addNewEntry(self, loginInfoEntry):
        with Session(self.engine) as session:
            session.add( self.LoginInfo(uniqueID=loginInfoEntry['uniqueID'],
                                        entryName=loginInfoEntry['entryName'],
                                        userName=loginInfoEntry['userName'],
                                        password=loginInfoEntry['password'],
                                        email=loginInfoEntry['email'],
                                        url=loginInfoEntry['url'],
                                        notes=loginInfoEntry['notes'],
                                        entryType=loginInfoEntry['entryType'],
                                        fileName=loginInfoEntry['fileName']
                                        )
                        )
            session.commit()

    # delete a row from LoginInfo table
    # table for a specific uniqueID
    def deleteEntry(self, uniqueID):
        with Session(self.engine) as session:
            session.query(self.LoginInfo).filter(self.LoginInfo.uniqueID == uniqueID).delete()
            session.commit()    

    # modify a row in LoginInfo table using row uniqueID
    # and dict structure with information
    def modifyLoginInfoEntry(self, loginInfoEntry):
        if loginInfoEntry == None:
            return
        with Session(self.engine) as session:
            session.execute( update(self.LoginInfo)\
                                    .where(self.LoginInfo.uniqueID == loginInfoEntry['uniqueID'])\
                                    .values(entryName=loginInfoEntry['entryName'],
                                            userName=loginInfoEntry['userName'],
                                            password=loginInfoEntry['password'],
                                            email=loginInfoEntry['email'],
                                            url=loginInfoEntry['url'],
                                            notes=loginInfoEntry['notes'],
                                            entryType=loginInfoEntry['entryType'],
                                            fileName=loginInfoEntry['fileName']
                                            )
                            )
            session.commit()

    # get a row from LoginInfo table using a id
    def getLoginInfoEntryOnID(self, uniqueID):
        with Session(self.engine) as session:
            loginInfoRow = session.query(self.LoginInfo)\
                             .filter(self.LoginInfo.uniqueID == uniqueID).all()
            loginInfoEntry = self.dataFormatterObj.convertRowsToListOfDict(loginInfoRow)[0]
        return loginInfoEntry

    # searches data in login info table to 
    # get id, entryName and entryType
    def searchLoginInfo(self, searchText):
        searchText = f"%{searchText}%"
        loginInfoResultList = []
        with Session(self.engine) as session:
            loginInfoResult = session.query(self.LoginInfo.uniqueID, 
                                           self.LoginInfo.entryName, 
                                           self.LoginInfo.entryType
                                           ).filter( or_ (
                                            self.LoginInfo.entryName.like(searchText),
                                            self.LoginInfo.userName.like(searchText),
                                            self.LoginInfo.email.like(searchText),
                                            self.LoginInfo.url.like(searchText),
                                            self.LoginInfo.notes.like(searchText)
                                            ) ).all()
            for row in loginInfoResult:
                loginInfoResultList.append(
                    {
                        'id': row[0],
                        'entryName': row[1],
                        'entryType': row[2]
                    }
                )
        return loginInfoResultList