from sqlalchemy import create_engine, Column, Integer, String, update, or_, ForeignKey, LargeBinary
from sqlalchemy.orm import Session, registry, relationship
import uuid



# handles all the connection and operation on the encrypted database
# using sqlalchemy
class DatabaseHandler:
    # connect to the database and create registry, base and tables
    def __init__(self, password):
        self.engine = create_engine(f"sqlite+pysqlcipher://:{password}@/test.db?cipher=aes-256-cfb&kdf_iter=64000")
        self.registryMapper = registry()
        self.Base = self.registryMapper.generate_base()
        self.LoginInfo, self.FileInfo = self._createTables()
        self.registryMapper.metadata.create_all(self.engine)

    # create the two tables in the database to store information
    def _createTables(self):
        class LoginInfo(self.Base):
            __tablename__ = "LoginInfo"
            id = Column(Integer, primary_key=True, autoincrement=True)
            entryName = Column(String(50), nullable=False)
            userName = Column(String(100), nullable=True)
            password = Column(String(50), nullable=True)
            email = Column(String(100), nullable=True)
            url = Column(String(500), nullable=True)
            notes = Column(String(20_000), nullable=True)
            entryType = Column(String(20), nullable=False)
            fileName = Column(String(100), nullable=True)
            uniqueID = Column(String(36), nullable=False)
            fileInfo = relationship("FileInfo", back_populates="loginInfo")
            def __repr__(self):
                return f"Table for recording all login entry information"
        
        class FileInfo(self.Base):
            __tablename__ = "FileInfo"
            id = Column(Integer, ForeignKey("LoginInfo.id"), primary_key=True)
            fileData = Column(LargeBinary, nullable=True)
            loginInfo = relationship("LoginInfo", back_populates="fileInfo")
            def __repr__(self):
                return f"Table for recording all file binary information"

        return LoginInfo, FileInfo

    # add a new entry into the LoginInfo table and FileInfo table
    def addNewEntry(self, loginInfoRowDict, fileInfoRowDict):
        with Session(self.engine) as session:
            loginInfoRow = self.LoginInfo(entryName=loginInfoRowDict['entryName'],
                                        userName=loginInfoRowDict['userName'],
                                        password=loginInfoRowDict['password'],
                                        email=loginInfoRowDict['email'],
                                        url=loginInfoRowDict['url'],
                                        notes=loginInfoRowDict['notes'],
                                        entryType=loginInfoRowDict['entryType'],
                                        fileName=loginInfoRowDict['fileName'],
                                        uniqueID=str( uuid.uuid4() )
                                        )
            fileInfoRow = self.FileInfo(fileData=fileInfoRowDict['fileData'],
                                        loginInfo=loginInfoRow
                                        )
            session.add(loginInfoRow)
            session.commit()
            session.add(fileInfoRow)
            session.commit()

    # delete a row from LoginInfo table and FileInfo 
    # table for a specific id
    def deleteEntry(self, id):
        with Session(self.engine) as session:
            session.query(self.LoginInfo).filter(self.LoginInfo.id == id).delete()
            session.query(self.FileInfo).filter(self.FileInfo.id == id).delete()
            session.commit()    

    # modify a row in LoginInfo table using row id '
    # and dict structure with information
    def modifyLoginInfoEntry(self,  id, loginInfoRowDict):
        if loginInfoRowDict == None:
            return
        with Session(self.engine) as session:
            loginInfoUpdateStatement = update(self.LoginInfo)\
                                       .where(self.LoginInfo.id == id)\
                                       .values(entryName=loginInfoRowDict['entryName'],
                                                userName=loginInfoRowDict['userName'],
                                                password=loginInfoRowDict['password'],
                                                email=loginInfoRowDict['email'],
                                                url=loginInfoRowDict['url'],
                                                notes=loginInfoRowDict['notes'],
                                                entryType=loginInfoRowDict['entryType'],
                                                fileName=loginInfoRowDict['fileName']
                                              )
            session.execute(loginInfoUpdateStatement)
            session.commit()

    # modify a row in FileInfo table using id and a dict structure
    def modifyFileInfoEntry(self, id, fileInfoRowDict):
        if fileInfoRowDict == None:
            return
        with Session(self.engine) as session:
            fileInfoUpdateStatement = update(self.FileInfo)\
                                      .where(self.FileInfo.id == id)\
                                      .values(fileData=fileInfoRowDict['fileData'])
            session.execute(fileInfoUpdateStatement)
            session.commit()

    # get a row from LoginInfo table using a id
    def getLoginInfoEntryOnID(self, id):
        with Session(self.engine) as session:
            queryStatement = session.query(self.LoginInfo)\
                             .filter(self.LoginInfo.id == id)
            loginInfoRow = session.execute(queryStatement).first()[0]
        return loginInfoRow.mappings()

    # get a row from FileInfo table using a id
    def getFileInfoEntryOnID(self, id):
        with Session(self.engine) as session:
            queryStatement = session.query(self.FileInfo)\
                             .filter(self.FileInfo.id == id)
            fileInfoRow = session.execute(queryStatement).first()[0]
        return fileInfoRow.mappings()

    # searches data in login info table to 
    # get id, entryName and entryType
    def searchLoginInfo(self, searchText):
        loginInfoResultList = []
        with Session(self.engine) as session:
            queryStatement = session.query(self.LoginInfo.id, 
                                           self.LoginInfo.entryName, 
                                           self.LoginInfo.entryType
                                           ).filter( or_ (
                                            self.LoginInfo.entryName.like(f"{searchText}"),
                                            self.LoginInfo.userName.like(f"{searchText}"),
                                            self.LoginInfo.email.like(f"{searchText}"),
                                            self.LoginInfo.url.like(f"{searchText}"),
                                            self.LoginInfo.notes.like(f"{searchText}")
                                           ) )
            LoginInfoResult = session.execute(queryStatement)
            for row in LoginInfoResult:
                loginInfoResultList.append(
                    {
                        'id': row[0],
                        'entryName': row[1],
                        'entryType': row[2]
                    }
                )
        return loginInfoResultList
