"""
Main module for handling FastAPI endpoints and dependencies related to the blockchain.
"""

from typing import Annotated, Union

from fastapi import FastAPI, Depends, Request  # HTTPException (?)
# from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import src.blockchain as _blockchain
import templates.base_template as temp

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# CORS --
# origins = [
#     "http://localhost:5173"
# ]
# 
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


class BlockData(BaseModel):
    """Model for block data input."""
    name: str
    transaction: str
    hash: str
    previous_hash: str


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


def get_blockchain():
    """
    Provides an instance of the Blockchain.
    Checks if the blockchain is valid and raises an HTTPException if not.
    """
    blockchain = _blockchain.Blockchain()
#    if not blockchain.is_chain_valid():
#        raise HTTPException(status_code=400, detail="The blockchain is invalid")
    return blockchain


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    return str(temp.base_page(page_title="APDH App"))


@app.post("/mine_block/")
def mine_block(
    block_data: BlockData
        # , blockchain: _blockchain.Blockchain = Depends(get_blockchain)
):
    """Mines a block with the provided data and returns the new block."""
    # return blockchain.mine_block(data=block_data.data)
    print(block_data)
    return block_data


@app.get("/blockchain/")
def get_blockchain_route(blockchain: _blockchain.Blockchain = Depends(get_blockchain)):
    """Returns the entire blockchain."""
    return blockchain.chain

# pylint: disable=unused-argument
@app.get("/validate/")
def is_blockchain_valid(blockchain: _blockchain.Blockchain = Depends(get_blockchain)):
    """Checks if the blockchain is valid and returns a relevant message."""
    return {"message": "The blockchain is valid."}


@app.get("/blockchain/last/")
def previous_block(blockchain: _blockchain.Blockchain = Depends(get_blockchain)):
    """Returns the last block in the blockchain."""
    return blockchain.get_previous_block()
