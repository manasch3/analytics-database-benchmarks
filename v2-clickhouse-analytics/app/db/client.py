import os
import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()

def get_client():
    return clickhouse_connect.get_client(
        host=os.getenv("CH_HOST"),
        port=int(os.getenv("CH_PORT", 8123)),
        user=os.getenv("CH_USER"),
        password=os.getenv("CH_PASSWORD"),
        database=os.getenv("CH_DATABASE"),
        secure=False
    )  
