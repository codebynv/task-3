"""Phase 4: verify a persisted Phase 3 record and detect tampering."""

import copy
import json
import os
import sys

from dotenv import load_dotenv

from blockchain import connect_to_blockchain, get_canonical_hash, get_verification


def main(artifact_path: str, contract_address: str, identifier: str) -> int:
    load_dotenv(dotenv_path=".env")
    if not os.path.exists(artifact_path):
        print(f"[ERROR] Verification artifact not found: {artifact_path}")
        return 1

    with open(artifact_path, encoding="utf-8") as artifact_file:
        recorded_data = json.load(artifact_file)
    if set(recorded_data) != {"url", "title", "source"}:
        print("[ERROR] Verification artifact does not contain the expected canonical fields.")
        return 1

    try:
        w3 = connect_to_blockchain()
    except Exception as error:
        print(f"[ERROR] Blockchain connection failed: {error}")
        return 1

    read_result = get_verification(identifier, contract_address)
    if not read_result.get("success"):
        print(f"[ERROR] Blockchain read failed: {read_result.get('error')}")
        return 1

    current_hash = get_canonical_hash(recorded_data)
    on_chain_hash = read_result["data_hash"]
    original_verified = current_hash == on_chain_hash

    tampered_data = copy.deepcopy(recorded_data)
    tampered_data["title"] = f"{tampered_data['title']} [tampered]"
    tampered_hash = get_canonical_hash(tampered_data)
    tamper_detected = tampered_hash != on_chain_hash

    print("\n========================================")
    print("PHASE 4 - BLOCKCHAIN VERIFICATION")
    print("========================================")
    print("\nBlockchain:")
    print("Ethereum Sepolia")
    print(f"Chain ID: {w3.eth.chain_id}")
    print(f"\nContract: {contract_address}")
    print("\nTEST 1 - ORIGINAL DATA")
    print(f"Current Hash: {current_hash}")
    print(f"On-chain Hash: {on_chain_hash}")
    print(f"Result: {'VERIFIED' if original_verified else 'NOT VERIFIED'}")
    print("\nTEST 2 - TAMPERED DATA")
    print("Modified Field: title")
    print(f"Tampered Hash: {tampered_hash}")
    print(f"On-chain Hash: {on_chain_hash}")
    print(f"Result: {'TAMPERED / NOT VERIFIED' if tamper_detected else 'VERIFIED'}")
    print("\nBlockchain Modified During Phase 4: NO")
    print(f"\nPhase 4: {'PASS' if original_verified and tamper_detected else 'FAIL'}")
    print("========================================")

    return 0 if original_verified and tamper_detected else 1


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python run_phase4.py <artifact_path> <contract_address> <identifier>")
        sys.exit(1)
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))