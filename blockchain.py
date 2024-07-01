"""This is a simple implementation of a blockchain."""

import datetime as _dt
import hashlib as _hashlib
import json as _json
from sqlitedict import SqliteDict

# Constants
POW_PREFIX = "0000"

class Blockchain:
    """A simple implementation of a blockchain."""

    def __init__(self):
        """
        Use sqlitedict to store blockchain data
        """
        self.chain = SqliteDict("data.sqlite", autocommit=True)

        if len(self.chain) == 0:
            genesis_block = self._create_block(
                "genesis block", 1, "0", 1)
            self.chain[1] = genesis_block

    def mine_block(self, data: str) -> dict:
        """Mine and append a block with provided data to the blockchain."""
        previous_block = self.get_previous_block()
        proof = self._proof_of_work(previous_block, data)
        new_index = len(self.chain) + 1
        block = self._create_block(
            data, proof, self._hash(previous_block), new_index
        )
        self.chain[new_index] = block
        return block

    def _create_block(
        self, data: str, proof: int, previous_hash: str, index: int
    ) -> dict:
        """Create a new block."""
        return {
            "index": index,
            "timestamp": str(_dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash,
        }

    def get_previous_block(self) -> dict:
        """Retrieve the last block in the blockchain."""
        return (list(self.chain.items())[-1])[1]

    def _proof_of_work(self, previous_block: dict, data: str) -> int:
        """Find a proof that when hashed has a specific prefix."""
        previous_proof = previous_block["proof"]
        new_proof = 1
        while not self._valid_proof(
            new_proof, previous_proof, len(self.chain) + 1, data
        ):
            new_proof += 1
        return new_proof

    def _valid_proof(
        self, proof: int, previous_proof: int, index: int, data: str
    ) -> bool:
        """Check if the proof is valid."""
        guess = f"{proof**2 - previous_proof**2 + index}{data}".encode()
        guess_hash = _hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == POW_PREFIX

    def _hash(self, block: dict) -> str:
        """Hash a block."""
        block_string = _json.dumps(block, sort_keys=True).encode()
        return _hashlib.sha256(block_string).hexdigest()

    def is_chain_valid(self) -> bool:
        """Validate the blockchain's integrity."""
        previous_block = self.chain[1]
        for idx in range(2, len(self.chain)):
            block = self.chain[idx]
            if block["previous_hash"] != self._hash(previous_block):
                return False
            if not self._valid_proof(
                block["proof"], previous_block["proof"], block["index"], block["data"]
            ):
                return False
            previous_block = block
        return True
