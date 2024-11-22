import datetime as _dt
import hashlib as _hashlib


class Node:
    def __init__(self, name: str):
        """Initialize new node"""
        self.name = name

    def create_block(
        self, index: int, transaction: str, previous_hash: str = ""
    ) -> dict:
        """Create a new block."""
        timestamp = str(_dt.datetime.now())
        new_block = {
            "index": index,
            "previous_hash": previous_hash,
            "timestamp": timestamp,
            "transaction": transaction,
            "block_author": self.name,
            "validator": None,
        }
        new_block["current_hash"] = self.calculate_hash(new_block)
        return new_block

    def calculate_hash(self, block: dict):
        return (
            _hashlib.sha256(
                block["previous_hash"]
                + block["timestamp"]
                + block["transaction"]
                + block["name"]
            ).hexdigest(),
        )

    def validate_block(self, block: dict):
        validity = block["current_hash"] == self.calculate_hash(block)
        return validity
