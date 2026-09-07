"""
Phase 3: Blockchain Recording Module
===================================================
Connects to Ethereum Sepolia to deploy and interact with the Verifier smart contract.
Stores a canonical hash of the discovered data.
"""

import os
import json
import hashlib
from web3 import Web3
from dotenv import load_dotenv

def get_canonical_hash(post_data: dict) -> str:
    """
    Generates a deterministic SHA-256 hash from the canonical post data.
    """
    # Select minimum useful canonical fields
    canonical_data = {
        "url": post_data.get("url", ""),
        "title": post_data.get("title", ""),
        "source": post_data.get("source", ""),
    }
    
    # Deterministic JSON string: sorted keys, no spaces
    canonical_string = json.dumps(canonical_data, sort_keys=True, separators=(',', ':'))
    
    # SHA-256
    return hashlib.sha256(canonical_string.encode('utf-8')).hexdigest()

def connect_to_blockchain():
    """Connects to the blockchain using RPC URL from .env"""
    load_dotenv()
    rpc_url = os.getenv("SEPOLIA_RPC_URL")
    
    if not rpc_url:
        raise ValueError("SEPOLIA_RPC_URL not found in .env")
        
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to Ethereum network")
    if w3.eth.chain_id != 11155111:
        raise ConnectionError(
            f"Connected to chain ID {w3.eth.chain_id}; expected Ethereum Sepolia (11155111)"
        )
        
    return w3

def get_wallet(w3):
    """Retrieves and configures the wallet from .env"""
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        raise ValueError("PRIVATE_KEY not found in .env")
        
    # Ensure it starts with 0x for web3.py
    if not private_key.startswith('0x'):
        private_key = '0x' + private_key
        
    account = w3.eth.account.from_key(private_key)
    return account

def compile_contract():
    """Compiles the Verifier.sol contract"""
    import solcx
    
    print("  [INFO] Compiling Solidity contract...")
    try:
        solcx.install_solc("0.8.19")
    except Exception as e:
        print(f"  [WARN] Failed to install solc: {e}")
        
    solcx.set_solc_version("0.8.19")
    
    contract_path = os.path.join(os.path.dirname(__file__), "contracts", "Verifier.sol")
    if not os.path.exists(contract_path):
        raise FileNotFoundError(f"Contract not found at {contract_path}")
        
    with open(contract_path, "r") as f:
        source = f.read()
        
    compiled_sol = solcx.compile_source(
        source,
        output_values=["abi", "bin"]
    )
    
    contract_id, contract_interface = compiled_sol.popitem()
    return contract_interface['abi'], contract_interface['bin']

def deploy_contract(w3, account):
    """Deploys the Verifier contract to the blockchain"""
    abi, bytecode = compile_contract()
    
    VerifierContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Build transaction
    nonce = w3.eth.get_transaction_count(account.address)
    tx = VerifierContract.constructor().build_transaction({
        'chainId': w3.eth.chain_id,
        'gasPrice': w3.eth.gas_price,
        'from': account.address,
        'nonce': nonce
    })
    
    # Sign and send
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=account.key)
    print("  [INFO] Broadcasting deployment transaction...")
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"  [INFO] Waiting for deployment receipt... (Tx: {tx_hash.hex()})")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    contract_address = tx_receipt.contractAddress
    
    # Save the ABI for later use
    with open("verifier_abi.json", "w") as f:
        json.dump(abi, f)
        
    return contract_address, abi

def load_contract(w3, contract_address):
    """Loads an existing deployed contract"""
    # Try to load ABI from file, or compile it
    try:
        with open("verifier_abi.json", "r") as f:
            abi = json.load(f)
    except FileNotFoundError:
        abi, _ = compile_contract()
        with open("verifier_abi.json", "w") as f:
            json.dump(abi, f)
            
    return w3.eth.contract(address=contract_address, abi=abi)

def store_verification(post_data: dict, identifier: str = None) -> dict:
    """
    Fingerprints post data and stores it on the blockchain.
    """
    try:
        w3 = connect_to_blockchain()
        account = get_wallet(w3)
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Blockchain connection failed: {e}"}

    data_hash = get_canonical_hash(post_data)
    source_url = post_data.get("url", "UNKNOWN")
    
    if not identifier:
        identifier = data_hash # Use hash as identifier if none provided

    contract_address = os.getenv("CONTRACT_ADDRESS")
    
    if not contract_address:
        print("  [INFO] CONTRACT_ADDRESS not found in .env. Deploying new contract...")
        try:
            contract_address, abi = deploy_contract(w3, account)
            print(f"  [OK] Contract deployed at: {contract_address}")
            print(f"  [WARN] IMPORTANT: Add this to your .env file: CONTRACT_ADDRESS={contract_address}")
        except Exception as e:
            return {"success": False, "error": f"Failed to deploy contract: {e}"}
            
    contract = load_contract(w3, contract_address)
    
    # Check if record already exists
    try:
        _, _, _, _, exists = contract.functions.getVerification(identifier).call()
        if exists:
            return {"success": False, "error": f"Record already exists on-chain for identifier {identifier}"}
    except Exception as e:
        print(f"  [WARN] Failed to check existing record: {e}")

    # Build transaction
    try:
        nonce = w3.eth.get_transaction_count(account.address)
        tx = contract.functions.storeVerification(
            identifier, 
            source_url, 
            data_hash
        ).build_transaction({
            'chainId': w3.eth.chain_id,
            'gasPrice': w3.eth.gas_price,
            'from': account.address,
            'nonce': nonce
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"  [INFO] Broadcasting record transaction... (Tx: {tx_hash.hex()})")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if tx_receipt.status != 1:
            return {"success": False, "error": "Transaction reverted by the EVM."}
            
        return {
            "success": True,
            "transaction_hash": tx_receipt.transactionHash.hex(),
            "block_number": tx_receipt.blockNumber,
            "contract_address": contract_address,
            "wallet_address": account.address,
            "data_hash": data_hash,
            "source_url": source_url,
            "identifier": identifier
        }
    except Exception as e:
        return {"success": False, "error": f"Transaction failed: {e}"}

def get_verification(identifier: str, contract_address: str = None) -> dict:
    """
    Reads a record back from the blockchain.
    """
    try:
        w3 = connect_to_blockchain()
        contract_address = contract_address or os.getenv("CONTRACT_ADDRESS")
        if not contract_address:
            return {"success": False, "error": "CONTRACT_ADDRESS not configured."}
            
        contract = load_contract(w3, contract_address)
        
        sourceUrl, dataHash, timestamp, submitter, exists = contract.functions.getVerification(identifier).call()
        
        if not exists:
            return {"success": False, "error": "Record does not exist."}
            
        return {
            "success": True,
            "source_url": sourceUrl,
            "data_hash": dataHash,
            "timestamp": timestamp,
            "submitter": submitter
        }
    except Exception as e:
        return {"success": False, "error": f"Failed to read from blockchain: {e}"}
