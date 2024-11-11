"""This is a simple implementation of a blockchain. No proof required lol"""

import datetime as _dt
from zoneinfo import ZoneInfo
import hashlib as _hashlib
import json
from sqlitedict import SqliteDict
import qrcode
import io

# Constants
DATABASE_URL = './data/production.sqlite'


class Blockchain:
    """A simple implementation of a blockchain."""

    def __init__(self, db=DATABASE_URL):
        """
        Use sqlitedict to store blockchain data
        """
        self.chain = SqliteDict(
            db,
            autocommit=True,
            encode=json.dumps,
            decode=json.loads
        )

        if len(self.chain) == 0:
            genesis_block = self._create_block(1, "genesis block", "")
            self.chain[1] = genesis_block

    def mine_block(self, data: dict) -> dict:
        """Mine and append a block with provided data to the blockchain."""

        previous_block = self.get_previous_block()
        new_index = len(self.chain) + 1
        block = self._create_block(
            new_index, data, previous_block["current_hash"]
        )
        self.chain[new_index] = block
        return block

    def _create_block(
        self, index: int, transaction: dict, previous_hash: str
    ) -> dict:
        """Create a new block."""
        new_block = {
            "index": index,
            "previous_hash": previous_hash,
            "timestamp":  str(_dt.datetime.now()),
            "transaction": transaction,
        }
        new_block["current_hash"] = self.calculate_hash(new_block)
        return new_block

    def get_previous_block(self) -> dict:
        """Retrieve the last block in the blockchain."""
        return (list(self.chain.items())[-1])[1]

    def calculate_hash(self, block: dict):
        return _hashlib.sha256(
            (block["previous_hash"] +
             block["timestamp"] +
             json.dumps(block["transaction"])).encode()
        ).hexdigest()

    def get_by_transaction(self, id_transaksi):
        query = """
        SELECT
            json_extract(value, '$.transaction') as value
        FROM unnamed
        WHERE
            json_extract(value, '$.transaction.id_transaksi') = ?
        ORDER BY json_extract(value, '$.timestamp') DESC
        LIMIT 1
        """

        item = self.chain.conn.select_one(query, (id_transaksi,))
        print(self.chain)

        return item

    def get_by_ternak(self, id_ternak):
        query = """
        SELECT
            key,
            json_extract(value, '$.transaction') as value
        FROM unnamed
        WHERE
            json_extract(value, '$.transaction.id_transaksi') = ?
        ORDER BY json_extract(value, '$.timestamp') DESC
        LIMIT 1
        """

        item = self.chain.conn.select_one(query, (id_ternak,))

        return item

    def end_delivery(self, iot_id: int, _from):

        query = """
            SELECT
                json_extract(value, '$.transaction') as value
            FROM unnamed
            WHERE
                json_extract(value, '$.transaction.node') = ?
            AND
                json_extract(value, '$.timestamp') BETWEEN ? and ?;
        """

        result = list(self.chain.conn.select(query, (
            iot_id,
            _from,
            _dt.datetime.now(
                ZoneInfo("Asia/Jakarta")).strftime('%Y-%m-%d %H:%M')
        )))
        return [json.loads(item) for sublist in result for item in sublist]


# qrcode generator
def qr_generator(url):
    """ Returns a qrcode image. """
    img_bytes = io.BytesIO()
    img = qrcode.make(url)
    img.save(img_bytes)
    img_bytes.seek(0)

    return img_bytes.read()
