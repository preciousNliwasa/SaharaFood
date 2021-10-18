from fastapi import FastAPI,Depends,Form,Response,status
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from passlib.context import CryptContext

pwd_co = CryptContext(schemes = ['bcrypt'],deprecated = 'auto')

class Hashed():
    
    def cryp(password:str):
        hashed = pwd_co.hash(password)
        return hashed
    
    def verify(password:str,enc:str):
        verified = pwd_co.verify(password,enc)
        return verified

## connecting to a database

engine = create_engine('sqlite:///./SaharaFD.db',connect_args = {"check_same_thread":False})

Sessionlocal = sessionmaker(autocommit = False,autoflush = False,bind = engine)
Base = declarative_base()

def get_db():
    db = Sessionlocal()
    
    try:
        yield db
    finally: 
        db.close()
        
from sqlalchemy import Column,Integer,String

## creating Tables in the  Database

#customer Table
class Customerr(Base):
    __tablename__ = 'customerr'
    
    id = Column(Integer,primary_key = True,index = True)
    Customer_Name = Column(String,primary_key = True)
    Sex = Column(String)
    Phone_Number = Column(String,primary_key = True)
    PrePaid = Column(String)
    Amount = Column(Integer)

#operator Table    
class Operatorr(Base):
    __tablename__ = 'operatorr'
    
    id = Column(Integer,primary_key = True,index = True)
    Operator_Name = Column(String,primary_key = True)
    Sex = Column(String)
    Place_Of_Stay = Column(String)
    Phone_Number = Column(String,primary_key = True)
    Places_Of_Operation = Column(String)

#sahara Table    
class Sahara(Base):
    __tablename__ = 'Sahara_Key'
    
    id = Column(Integer,primary_key = True)
    Admin = Column(String)
    Sahara_Key = Column(String)

Base.metadata.create_all(bind = engine)

app = FastAPI(title = 'SAHARA FOOD DELIVERY API')

# Home
@app.get('/',tags = ['HOME'])
async def Vision_and_Mission():
    return {'Bringing You Standard and Quality Products'}


# Inserting customer details in the customer Table
@app.post('/customer',tags = ['customer'])
async def Create_Customer(response:Response,Admin:str,Sahara_Key:str,Customer_Name:str = Form(...),Sex:str = Form(...),Phone_Number:str = Form(...),PrePaid:bool = Form(...),Amount:int = Form(...),db : Session = Depends(get_db)):
    
    admin = db.query(Sahara).filter(Sahara.Admin == Admin).first()
    
    if not  admin:
        return "Wrong Admin Name"
    
    if  admin.Admin == 'sahara':
        if Hashed.verify(Sahara_Key,admin.Sahara_Key) == True:
            
            customer = Customerr(Customer_Name = Customer_Name,Sex = Sex,Phone_Number = Phone_Number,PrePaid = PrePaid,Amount = Amount)
            db.add(customer)
            db.commit()
            db.refresh(customer)
            return {'created'}
        
        else:
            return {'wrong sahara key'}
 
# Getting All Customers details from the customer table       
@app.get('/customer/{PrePaid}',tags = ['customer'])
async def Get_ALL_Customers(response:Response,Admin:str,Sahara_Key:str,PrePaid:bool,db : Session = Depends(get_db)):
    
    admin = db.query(Sahara).filter(Sahara.Admin == Admin).first()
    
    if not  admin:
        return "Wrong Admin Name"
    
    if  admin.Admin == 'sahara':
        if Hashed.verify(Sahara_Key,admin.Sahara_Key) == True:
            custommer = db.query(Customerr).filter(Customerr.PrePaid == PrePaid).first()
            
            if not custommer:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"Customer Not Available"}
            
            return custommer
        
        else:
            return {'wrong sahara key'}


# Getting a specific customer details from the customer table
@app.get('/customer',tags = ['customer'])
async def Get_Customer_Details(response:Response,Admin:str,Sahara_Key:str,Customer_Name:str,db : Session = Depends(get_db)):
    
    admin = db.query(Sahara).filter(Sahara.Admin == Admin).first()
    
    if not  admin:
        return "Wrong Admin Name"
    
    if  admin.Admin == 'sahara':
        if Hashed.verify(Sahara_Key,admin.Sahara_Key) == True:
            custommer2 = db.query(Customerr).filter(Customerr.Customer_Name == Customer_Name).first()
            
            if not custommer2:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"Customer Not Available"}
            
            return custommer2
        
        else:
            return {'wrong sahara key'}


# Updating a specific customer details in the customer table
@app.put('/customer',tags = ['customer'])
async def Update_Customers_details(response:Response,Admin:str,Sahara_Key:str,CustomerName:str,Customer_Name:str = Form(...),Sex:str = Form(...),Phone_Number:str = Form(...),PrePaid:bool = Form(...),Amount:int = Form(...),db : Session = Depends(get_db)):
    
    admin = db.query(Sahara).filter(Sahara.Admin == Admin).first()
    
    if not  admin:
        return "Wrong Admin Name"
    
    if  admin.Admin == 'sahara':
        if Hashed.verify(Sahara_Key,admin.Sahara_Key) == True:
            custommer3 = db.query(Customerr).filter(Customerr.Customer_Name == CustomerName)
            
            if not custommer3.first():
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"Customer Not Available"}
            
            custommer3.update(dict(Customer_Name = Customer_Name,Sex = Sex,Phone_Number = Phone_Number,PrePaid = PrePaid,Amount = Amount))
            db.commit()
            return 'updated'
        
        else:
            return {'wrong sahara key'}
        

# Deleting a customer in the customer table
@app.delete('/customer/{Customer_Name}',tags = ['customer'])
async def Delete_Customer_Details(response:Response,Admin:str,Sahara_Key:str,Customer_Name:str,db : Session = Depends(get_db)):
    
    admin = db.query(Sahara).filter(Sahara.Admin == Admin).first()
    
    if not  admin:
        return "Wrong Admin Name"
    
    if  admin.Admin == 'sahara':
        if Hashed.verify(Sahara_Key,admin.Sahara_Key) == True:
            db.query(Customerr).filter(Customerr.Customer_Name == Customer_Name).delete(synchronize_session = False)
            db.commit()
            return {'Row Removed'}
        
        else:
            return {'wrong sahara key'}
        
# Inserting an operator in the operator table
@app.post('/operator',tags = ['operator'])
async def Create_Operator(Admin:str,Sahara_Key:str,Operator_Name:str = Form(...),Sex:str = Form(...),Place_Of_Stay:str = Form(...),Phone_Number:str = Form(...),Places_Of_Operation:str = Form(...),db : Session = Depends(get_db)):
    
    admin = db.query(Sahara).filter(Sahara.Admin == Admin).first()
    
    if not  admin:
        return "Wrong Admin Name"
    
    if  admin.Admin == 'sahara':
        if Hashed.verify(Sahara_Key,admin.Sahara_Key) == True:
            
            operator = Operatorr(Operator_Name = Operator_Name,Sex = Sex,Place_Of_Stay = Place_Of_Stay,Phone_Number = Phone_Number,Places_Of_Operation = Places_Of_Operation)
            db.add(operator)
            db.commit()
            db.refresh(operator)
            return {'created'}
        
        else:
            return {'wrong sahara key'}


# Getting operators from the operator table
@app.get('/operator',tags = ['operator'])
async def Get_ALL_Operators(Admin:str,Sahara_Key:str,db : Session = Depends(get_db)):
    
    admin = db.query(Sahara).filter(Sahara.Admin == Admin).first()
    
    if not  admin:
        return "Wrong Admin Name"
    
    if  admin.Admin == 'sahara':
        if Hashed.verify(Sahara_Key,admin.Sahara_Key) == True:
            operatorr2 = db.query(Operatorr).all()
            
            return operatorr2
        
        else:
            return {'wrong sahara key'}
 
# Getting a specific operator from the operator table       
@app.get('/operator/{Operator_Name}',tags = ['operator'])
async def Get_Specific_Operator_Details(response:Response,Admin:str,Sahara_Key:str,Operator_Name:str,db : Session = Depends(get_db)):
    
    admin = db.query(Sahara).filter(Sahara.Admin == Admin).first()
    
    if not  admin:
        return "Wrong Admin Name"
    
    if  admin.Admin == 'sahara':
        if Hashed.verify(Sahara_Key,admin.Sahara_Key) == True:
            operatorr5 = db.query(Operatorr).filter(Operatorr.Operator_Name == Operator_Name).first()
            
            if not operatorr5:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"Operator Not Available"}
            
            return operatorr5
        
        else:
            return {'wrong sahara key'}
        
    
# Updating an operator details in the Operator Table
@app.put('/operator',tags = ['operator'])
async def Update_Operator_Details(response:Response,Admin:str,Sahara_Key:str,OperatorName:str,Operator_Name:str = Form(...),Sex:str = Form(...),Place_Of_Stay:str = Form(...),Phone_Number:str = Form(...),Places_Of_Operation:str = Form(...),db : Session = Depends(get_db)):
    
    admin = db.query(Sahara).filter(Sahara.Admin == Admin).first()
    
    if not  admin:
        return "Wrong Admin Name"
    
    if  admin.Admin == 'sahara':
        if Hashed.verify(Sahara_Key,admin.Sahara_Key) == True:
            operator3 = db.query(Operatorr).filter(Operatorr.Operator_Name == OperatorName)
            
            if not operator3.first():
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"Operator Not Available"}
            
            operator3.update(dict(Operator_Name = Operator_Name,Sex = Sex,Place_Of_Stay = Place_Of_Stay,Phone_Number = Phone_Number,Places_Of_Operation = Places_Of_Operation))
            db.commit()
            return 'updated'
        
        else:
            return {'wrong sahara key'}


# Deleting an operator in the operator table
@app.delete('/operator/{Customer_Name}',tags = ['operator'])
async def Delete_Operator_Details(Admin:str,Sahara_Key:str,Operator_Name:str,db : Session = Depends(get_db)):
    
    admin = db.query(Sahara).filter(Sahara.Admin == Admin).first()
    
    if not  admin:
        return "Wrong Admin Name"
    
    if  admin.Admin == 'sahara':
        if Hashed.verify(Sahara_Key,admin.Sahara_Key) == True:
                db.query(Operatorr).filter(Operatorr.Operator_Name == Operator_Name).delete(synchronize_session = False)
                db.commit()
                return {'Row Removed'}
        
        else:
            return {'wrong sahara key'}


'''# Sahara Key
@app.post('/sahara',status_code = 201,tags = ['sahara key'])
async def Sahara_Key(Admin:str = Form(...),Sahara_Key:str = Form(...),db : Session = Depends(get_db)):
    key = Hashed.cryp(Sahara_Key)
    sahara_key = Sahara(Admin = Admin,Sahara_Key = key)
    db.add(sahara_key)
    db.commit()
    db.refresh(sahara_key)
    return sahara_key'''
    
