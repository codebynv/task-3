"""
Phase 3 Execution Script
===================================================
Executes Phase 1 -> Phase 2 -> Phase 3 Pipeline.
1. Phase 1: Face detection and encoding.
2. Phase 2: Genuine reverse image search.
3. Phase 3: Hash canonical data and store on-chain.
"""

import sys
import os
import json
from dotenv import load_dotenv

from face_module import process_face
from reverse_search import search_reverse_image
from blockchain import get_canonical_hash, store_verification, get_verification

def main(image_path):
    print("\n============================================================")
    print("  PHASE 1: FACE DETECTION & ENCODING")
    print("============================================================")
    
    # Run Phase 1
    face_data = process_face(image_path)
    if not face_data.get("face_found"):
        print(f"[ERROR] Phase 1 failed: {face_data.get('error')}")
        sys.exit(1)
        
    print(f"  [OK] Face detected at {face_data['face_location']}")
    print(f"  [OK] {face_data['encoding_dimensions']}D Embedding generated")
    
    # We use the cropped face for the reverse image search for better accuracy
    cropped_face_path = face_data['cropped_face_path']
    
    print("\n============================================================")
    print("  PHASE 2: GENUINE REVERSE IMAGE SEARCH")
    print("============================================================")
    
    # Run Phase 2
    search_results = search_reverse_image(cropped_face_path)
    if not search_results.get("success"):
        print(f"[ERROR] Phase 2 failed: {search_results.get('error')}")
        sys.exit(1)
        
    best_match = search_results["best_match"]
    print(f"  [OK] Found matching post: {best_match['url']}")

    verification_record = {
        "url": best_match.get("url", ""),
        "title": best_match.get("title", ""),
        "source": best_match.get("source", ""),
    }
    artifact_path = os.path.join("output", "verification_record.json")
    os.makedirs("output", exist_ok=True)
    with open(artifact_path, "w", encoding="utf-8") as artifact_file:
        json.dump(verification_record, artifact_file, sort_keys=True, separators=(",", ":"))
    artifact_hash = get_canonical_hash(verification_record)
    
    print("\n============================================================")
    print("  PHASE 3: BLOCKCHAIN RECORDING")
    print("============================================================")
    
    # We need to make sure the environment has blockchain keys
    load_dotenv()
    if not os.getenv("SEPOLIA_RPC_URL") or not os.getenv("PRIVATE_KEY"):
        print("[ERROR] Missing SEPOLIA_RPC_URL or PRIVATE_KEY in .env")
        print("  Please configure your Sepolia testnet credentials in .env to continue.")
        sys.exit(1)
        
    print("  [1/3] Extracting canonical data and hashing...")
    
    # Using the face hash as the unique identifier for the blockchain record
    identifier = face_data["face_hash"]
    
    print("  [2/3] Writing to Ethereum Sepolia Testnet...")
    tx_result = store_verification(best_match, identifier)
    
    if not tx_result.get("success"):
        print(f"  [ERROR] Blockchain write failed: {tx_result.get('error')}")
        sys.exit(1)
        
    print(f"  [OK] Transaction Confirmed: {tx_result['transaction_hash']}")
    
    print("\n  [3/3] Verifying On-Chain Record (Read-back)...")
    read_result = get_verification(identifier, tx_result["contract_address"])
    
    if not read_result.get("success"):
        print(f"  [ERROR] Blockchain read failed: {read_result.get('error')}")
        sys.exit(1)

    if artifact_hash != read_result["data_hash"]:
        print("  [ERROR] Verification artifact hash does not match the on-chain hash.")
        sys.exit(1)

    with open(os.path.join("output", "blockchain_record.json"), "w", encoding="utf-8") as record_file:
        json.dump(
            {
                "contract_address": tx_result["contract_address"],
                "identifier": identifier,
                "transaction_hash": tx_result["transaction_hash"],
                "block_number": tx_result["block_number"],
            },
            record_file,
            sort_keys=True,
            indent=2,
        )
        
    print("\n========================================")
    print("BLOCKCHAIN RECORD CREATED")
    print("========================================")
    print("Source URL:")
    print(f"  {read_result['source_url']}")
    print("\nVerification artifact:")
    print(f"  {artifact_path}")
    print("\nData Hash:")
    print(f"  {read_result['data_hash']}")
    print("\nNetwork:")
    print("  Ethereum Sepolia")
    print("\nWallet:")
    print(f"  {tx_result['wallet_address']}")
    print("\nContract:")
    print(f"  {tx_result['contract_address']}")
    print("\nTransaction:")
    print(f"  {tx_result['transaction_hash']}")
    print("\nBlock:")
    print(f"  {tx_result['block_number']}")
    print("\nOn-chain record:")
    print(f"  {{")
    print(f"    'source_url': '{read_result['source_url']}',")
    print(f"    'data_hash': '{read_result['data_hash']}',")
    print(f"    'timestamp': {read_result['timestamp']},")
    print(f"    'submitter': '{read_result['submitter']}'")
    print(f"  }}")
    print("========================================")
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_phase3.py <image_path>")
        sys.exit(1)
        
    main(sys.argv[1])
