from sqlmodel import SQLModel, create_engine
from supabase import Client, create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase: Client = create_client(os.getenv('SP_URL'), os.getenv('SP_KEY'))
DB_URL = f'postgresql://postgres.toilpobeddzjriuvfktg:{os.getenv('SP_PWD')}@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres'

engine = create_engine(DB_URL, echo=True)
print('Server Running . . .') 

def create_tables():
    SQLModel.metadata.create_all(engine)
    print('creating all tables . . .')