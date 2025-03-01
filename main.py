import os
from web3 import Web3
from dotenv import load_dotenv
import requests
import json

load_dotenv()


# RPC_URL = os.getenv("RPC_URL")
RPC_URL = os.getenv("QUICK_URL")
DEX_ROUTER_ADDRESS = os.getenv("DEX_ROUTER_ADDRESS")

# Load necessary ABIs
# with open("router_abi.json", "r") as f:
#    router_abi = json.load(f)


w3 = Web3(Web3.HTTPProvider(RPC_URL))
# print(w3.is_connected())
# print(w3.eth.get_block("latest"))
print("---" * 20)


if __name__ == "__main__":
    # router_contract = w3.eth.contract(address=DEX_ROUTER_ADDRESS, abi=router_abi)
    # print(router_contract)
    pending_tx_filter = w3.eth.filter("pending")
    print(pending_tx_filter)
    new_transactions = pending_tx_filter.get_new_entries()
    print(new_transactions)

    # payload = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}

#    headers = {"content-type": "application/json"}

#    response = requests.post(RPC_URL, data=json.dumps(payload), headers=headers).json()

#    print(response)
