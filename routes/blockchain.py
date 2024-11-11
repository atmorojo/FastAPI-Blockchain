from pydantic import BaseModel
import src.blockchain as _blockchain
from src.security import get_current_user
import json
import qrcode
import io
from templates import blockchain as tpl_bc
from templates import base_template
from fastapi import (
    APIRouter,
    Response,
    Request,
    Depends,
)
from fastapi.responses import HTMLResponse


routes = APIRouter(prefix="/blockchain")


class BlockData(BaseModel):
    """Model for block data input."""
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


@routes.get("/")
def get_blockchain_route(
        blockchain: _blockchain.Blockchain = Depends(get_blockchain)
):
    """Returns the entire blockchain."""
    return blockchain.chain.items()


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


@routes.get("/{transaksi_id}", response_class=HTMLResponse)
def read_blockchain(
    transaksi_id: int,
    blockchain: _blockchain.Blockchain = Depends(get_blockchain),
    user = Depends(get_current_user)
):
    """ Returns a specific block from the blockchain. """
    logged_in = False

    if user:
        logged_in = user.role.role == 4

    data = blockchain.get_by_transaction(transaksi_id)[0]
    if data:
        data = json.loads(data)
        return str(base_template.base_page(
            page_title="Keterangan Daging",
            content=tpl_bc.bc_detail(data, logged_in)
        ))
    else:
        return { "error:" "Not Available" }
