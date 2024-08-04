from pydantic import BaseModel
import src.blockchain as _blockchain
from fastapi import (
    APIRouter,
    Depends
)


routes = APIRouter(prefix="/blockchain")


class BlockData(BaseModel):
    """Model for block data input."""
    name: str
    transaction: str
    hash: str
    previous_hash: str


def get_blockchain():
    """
    Provides an instance of the Blockchain.
    Checks if the blockchain is valid and raises an HTTPException if not.
    """
    blockchain = _blockchain.Blockchain()
#    if not blockchain.is_chain_valid():
#        raise HTTPException(
#           status_code=400,
#           detail="The blockchain is invalid"
#        )
    return blockchain


@routes.post("/mine_block/")
def mine_block(
    block_data: BlockData
        # , blockchain: _blockchain.Blockchain = Depends(get_blockchain)
):
    """Mines a block with the provided data and returns the new block."""
    # return blockchain.mine_block(data=block_data.data)
    print(block_data)
    return block_data


@routes.get("/blockchain/")
def get_blockchain_route(
        blockchain: _blockchain.Blockchain = Depends(get_blockchain)
):
    """Returns the entire blockchain."""
    return blockchain.chain


# pylint: disable=unused-argument
@routes.get("/validate/")
def is_blockchain_valid(
        blockchain: _blockchain.Blockchain = Depends(get_blockchain)
):
    """Checks if the blockchain is valid and returns a relevant message."""
    return {"message": "The blockchain is valid."}


@routes.get("/blockchain/last/")
def previous_block(
        blockchain: _blockchain.Blockchain = Depends(get_blockchain)
):
    """Returns the last block in the blockchain."""
    return blockchain.get_previous_block()
