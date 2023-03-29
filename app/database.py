from sqlalchemy import create_engine, Column, Integer, String, Date, Table, func, update, select, or_, and_, ForeignKey, LargeBinary
from sqlalchemy.orm import Session, registry, relationship, aliased
import datetime
import uuid

class DatabaseHandler:
    # 
    def __init__(self, password):
        self.engine = create_engine(f"sqlite+pysqlcipher://:{password}@/test.db?cipher=aes-256-cfb&kdf_iter=64000")
        self.registryMapper = registry()
        self.Base = self.registryMapper.generate_base()
        self.LoginInfo, self.FileInfo = self._createTables()
        self.registryMapper.metadata.create_all(self.engine)

    # 
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
        
        class FileInfo(self.Base):
            __tablename__ = "FileInfo"
            id = Column(Integer, ForeignKey("LoginInfo.id"), primary_key=True)
            fileData = Column(LargeBinary, nullable=True)
            loginInfo = relationship("LoginInfo", back_populates="fileInfo")

        return LoginInfo, FileInfo

    #
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

    #
    def deleteEntry(self, id):
        with Session(self.engine) as session:
            session.query(self.LoginInfo).filter(self.LoginInfo.id == id).delete()
            session.query(self.FileInfo).filter(self.FileInfo.id == id).delete()
            session.commit()

    #
    def modifyEntry(self):
        pass
