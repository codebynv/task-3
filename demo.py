"""Judge-friendly Phase 1-4 demo with an explicit read-only verification mode."""

import argparse
import json
import os
import sys

from run_phase4 import main as verify_record
from run_phase3 import main as record_on_chain


def load_record_metadata(path: str) -> dict:
    with open(path, encoding="utf-8") as metadata_file:
        return json.load(metadata_file)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the HH GOA Task 3 demo.")
    parser.add_argument("image", help="Input image path")
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Read the saved Phase 3 record and test tamper detection without a search or transaction",
    )
    parser.add_argument(
        "--artifact",
        default=os.path.join("output", "verification_record.json"),
        help="Persisted canonical verification artifact",
    )
    parser.add_argument(
        "--contract",
        help="Phase 3 contract address; required for verify-only unless metadata exists",
    )
    parser.add_argument(
        "--identifier",
        help="Phase 3 record identifier; required for verify-only unless metadata exists",
    )
    args = parser.parse_args()

    if args.verify_only:
        metadata_path = os.path.join("output", "blockchain_record.json")
        metadata = load_record_metadata(metadata_path) if os.path.exists(metadata_path) else {}
        contract_address = args.contract or metadata.get("contract_address")
        identifier = args.identifier or metadata.get("identifier")
        if not contract_address or not identifier:
            parser.error("verify-only requires --contract and --identifier, or output/blockchain_record.json")
        print("[READ-ONLY] No new Google Lens search or blockchain transaction will be performed.")
        return verify_record(args.artifact, contract_address, identifier)

    print("WARNING: LIVE DEMO - this mode performs a real SerpApi Google Lens search and real Sepolia transactions.")
    print("Use --verify-only to demonstrate verification without new external writes.\n", flush=True)
    print("========================================")
    print("PHASE 1 -> PHASE 3: LIVE PIPELINE")
    print("========================================")
    record_on_chain(args.image)

    metadata_path = os.path.join("output", "blockchain_record.json")
    if not os.path.exists(metadata_path):
        print("[ERROR] Phase 3 completed without producing blockchain_record.json.")
        return 1
    metadata = load_record_metadata(metadata_path)
    print("\n========================================")
    print("PHASE 4: READ-BACK VERIFICATION")
    print("========================================")
    return verify_record(args.artifact, metadata["contract_address"], metadata["identifier"])


if __name__ == "__main__":
    sys.exit(main())