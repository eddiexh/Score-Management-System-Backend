# Main.py
from dotenv import load_dotenv
from fastapi import FastAPI
from web3 import Web3
import web3
from Account import Account_Router
from Function import Function_Router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://traffic-hero.eddie.tw"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # 讀取.env檔案中的變數
    load_dotenv()

# Connect to Ethereum blockchain
    web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    # Check connection status
    if web3.is_connected():
        network_version = web3.net.version
        print(f"Connected to Ethereum node. Network version: {network_version}")
    else:
        print("Failed to connect to Ethereum node.")

app.include_router(Account_Router, prefix="/Account")
app.include_router(Function_Router, prefix="/Function")