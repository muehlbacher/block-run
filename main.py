import os
from web3 import Web3
from dotenv import load_dotenv
import time
import requests
import json

load_dotenv()


# RPC_URL = os.getenv("RPC_URL")
RPC_URL = os.getenv("QUICK_URL")
DEX_ROUTER_ADDRESS = str(os.getenv("DEX_ROUTER_ADDRESS"))
MIN_ETH_AMOUNT = 0.1

# Load necessary ABIs
# with open("router_abi.json", "r") as f:
#    router_abi = json.load(f)


w3 = Web3(Web3.HTTPProvider(RPC_URL))
# print(w3.is_connected())
# print(w3.eth.get_block("latest"))
print("---" * 20)


def decode_swap_token(tx):
    """Decode the transaction to extract the target token address"""
    try:
        # This is a simplified example - actual decoding requires full ABI parsing
        # In real implementation, you would decode the full transaction input
        # For demonstration, we're assuming the last address in the path is the target token
        input_data = tx.input
        # Extract the path parameter (this is heavily simplified)
        # Real implementation would properly decode the function parameters
        return "0x" + input_data[-40:]  # Last 20 bytes as hex string
    except Exception as e:
        print(f"Error decoding: {e}")
        return None


def is_swap_transaction(tx):
    """Check if the transaction is a token swap"""
    # Checking function signature for swapExactETHForTokens or similar functions
    print("check if swap transaction...")
    print(tx)
    tx_input = tx.input.hex()
    print("Input: ", tx_input)
    if not tx_input.startswith("0x7ff36ab5"):  # swapExactETHForTokens signature
        return False
    return True


if __name__ == "__main__":
    # router_contract = w3.eth.contract(address=DEX_ROUTER_ADDRESS, abi=router_abi)
    # print(router_contract)
    pending_tx_filter = w3.eth.filter("pending")
    print(pending_tx_filter)

    while True:
        try:
            new_transactions = pending_tx_filter.get_new_entries()
            print("New token fetch...")
            print(new_transactions)
            for tx_hash in new_transactions:
                # Get the full transaction
                try:
                    tx = w3.eth.get_transaction(tx_hash)
                    # print(tx)

                    # Check if it's a transaction to the DEX router
                    if tx.to and tx.to.lower() == DEX_ROUTER_ADDRESS.lower():
                        print("Transaction to dex router")
                        print(tx_hash)
                        print(tx)
                        print("Block number: ", tx.blockNumber)
                        print("Block hash: ", tx.blockHash)
                        # Analyze the transaction to see if it's a swap
                        if is_swap_transaction(tx):
                            print(f"Potential swap detected: {tx_hash.hex()}")

                            # Check if the transaction meets our criteria
                            if tx.value >= w3.to_wei(MIN_ETH_AMOUNT, "ether"):
                                token_address = decode_swap_token(tx)
                                if token_address:
                                    print(
                                        f"Large swap for token {token_address} detected"
                                    )
                except Exception as e:
                    # Some transactions may fail to decode
                    continue
            print("----" * 20)
            time.sleep(1)
        except Exception as e:
            print(f"Error in monitoring: {e}")
            time.sleep(1)

    # payload = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}

#    headers = {"content-type": "application/json"}

#    response = requests.post(RPC_URL, data=json.dumps(payload), headers=headers).json()

#    print(response)
