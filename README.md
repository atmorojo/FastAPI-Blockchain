# Blockchain + FastAPI

This project implements a simple blockchain system using Python, combined with the power of the FastAPI framework to interact with the blockchain via RESTful endpoints.

## Features

- Mine a New Block:
  Allows users to mine new blocks and add them to the chain.

- Retrieve the Entire Blockchain:
  Provides the capability to fetch the entire current state of the blockchain.

- Get the Last Mined Block:
  Offers a quick view to see the most recently added block in the chain.

- Validate the Blockchain:
  A utility to check and ensure the integrity and validity of the current state of the blockchain.

## Endpoints

Mine a Block: POST /mine_block/

Input: Data for the new block
Output: Details of the newly mined block
Get Entire Blockchain: GET /blockchain/

Output: A list containing all the blocks in the current blockchain
Get the Last Mined Block: GET /blockchain/last/

Output: Details of the last block in the chain
Validate the Blockchain: GET /validate/

Output: A boolean indicating whether the blockchain is valid

## Setup and Run:

Install the required libraries:

```
pip install fastapi[all] uvicorn
```

Navigate to the project directory and start the server:

```
cd path/to/your/directory
uvicorn main:app --reload
```

Access the application at http://127.0.0.1:8000/ and the interactive API documentation at http://127.0.0.1:8000/docs.

## Contributor

Erik Williams
