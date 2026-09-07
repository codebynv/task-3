# HH GOA 2026 Task 3: Face Identification and Blockchain Verification

This project demonstrates a five-step evidence pipeline for Hacker House Goa 2026 Task 3:

1. Detect and encode a face from an input image.
2. Search the cropped face with SerpApi's Google Lens engine.
3. Canonicalize the runtime result, fingerprint it with SHA-256, and record the fingerprint on Ethereum Sepolia.
4. Read the exact saved result back and verify it against the on-chain hash.
5. Modify a copy in memory and demonstrate tamper detection without writing to the blockchain.

The system stores a compact fingerprint and reference data, not the complete image.

## Architecture

```text
Input image
  -> DeepFace FaceNet embedding with RetinaFace
  -> SerpApi Google Lens runtime search
  -> dynamically selected result
  -> canonical {url, title, source}
  -> SHA-256 fingerprint
  -> Verifier contract on Ethereum Sepolia
  -> read-back comparison
  -> in-memory tamper test
```

## Phases

### Phase 1: Face identification

`face_module.py` uses DeepFace with the RetinaFace detector and FaceNet embeddings. It handles missing files, unreadable images, and images with no detectable face. It writes diagnostic images under `output/` and returns a deterministic face hash used as the blockchain record identifier.

### Phase 2: Reverse image search

`reverse_search.py` uploads the local crop to SerpApi and uses the Google Lens engine. Results are discovered at runtime. The selected result is never hardcoded or pre-selected by URL. Social results are preferred when present, otherwise the first valid web result is used.

Search results depend on the external SerpApi/Google Lens service. A reverse-image match is evidence of visual similarity or source linkage; it does not establish a person's real-world identity.

### Phase 3: Blockchain storage

`run_phase3.py` takes the runtime `url`, `title`, and `source` fields, applies the shared canonicalization function in `blockchain.py`, and computes a SHA-256 fingerprint. It deploys or uses the `Verifier.sol` contract on Ethereum Sepolia, stores the fingerprint and source URL, waits for confirmation, reads the record back, and writes:

- `output/verification_record.json`: exact canonical data used for hashing
- `output/blockchain_record.json`: non-secret contract, identifier, transaction, and block metadata

The previous records remain on-chain. A new deployment is used when `CONTRACT_ADDRESS` is blank.

### Phase 4: Verification and tamper detection

`run_phase4.py` reads `output/verification_record.json` rather than performing a new search. It recomputes the hash with the same `get_canonical_hash()` function, reads the specified Sepolia record, and reports `VERIFIED` only when the hashes match. It then changes only the title in an in-memory copy and expects `TAMPERED / NOT VERIFIED`. No tampered value is submitted.

### Phase 5: Demo preparation

`demo.py` is the presentation entry point. Its default mode runs the real pipeline and then verifies the newly created record. Its `--verify-only` mode is read-only and is the recommended mode for repeated demos.

## Technologies

- Python 3.10+
- DeepFace, FaceNet, RetinaFace
- OpenCV and Pillow
- SerpApi Google Lens
- Web3.py
- Solidity 0.8.x and `py-solc-x`
- Ethereum Sepolia testnet

## Project structure

```text
blockchain.py                 Shared hashing, Sepolia, contract, and read/write logic
face_module.py                Phase 1 face detection and embedding
reverse_search.py             Phase 2 SerpApi Google Lens search
run_phase3.py                 Phase 3 runtime record creation
run_phase4.py                 Phase 4 read-only verification and tamper test
demo.py                       Presentation entry point
contracts/Verifier.sol        Minimal on-chain record contract
test_images/                  Demo and negative test images
output/                       Ignored runtime artifacts
requirements.txt              Python dependencies
.env.example                  Secret-free environment template
```

## Installation

Create a virtual environment and install the pinned-compatible dependency ranges:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`py-solc-x` downloads Solidity compiler `0.8.19` on the first blockchain deployment if it is not already installed.

## Environment

Copy `.env.example` to `.env` and fill in local values:

```text
SERPAPI_API_KEY=
SEPOLIA_RPC_URL=
PRIVATE_KEY=
CONTRACT_ADDRESS=
```

Use a dedicated wallet private key funded only with Sepolia test ETH. Never use mainnet credentials, commit `.env`, print a private key, or print an API key. `.env` is excluded by `.gitignore`.

`CONTRACT_ADDRESS` may be left blank for a new deployment. After a Phase 3 run, the generated `output/blockchain_record.json` contains the actual contract address and identifier for the demo chain.

## Commands

Run the complete live pipeline. This performs a real Google Lens search and real Sepolia transactions, so use it deliberately:

```powershell
python demo.py test_images/einstein.jpg
```

Run Phase 3 directly:

```powershell
python run_phase3.py test_images/einstein.jpg
```

Verify the latest successful record without a new search or transaction:

```powershell
python demo.py --verify-only test_images/einstein.jpg --contract 0x2383A3a4801dDfc9befabAE29164fd1e4EFa8697 --identifier 6739e46750097892e3003f1d22e4214fa707494937a201370ecd58dc574907b8
```

Once `output/blockchain_record.json` exists, the shorter read-only command is:

```powershell
python demo.py --verify-only test_images/einstein.jpg
```

The image argument is retained for a consistent demo interface; verify-only mode does not process it, search, or write to the chain.

Run Phase 4 directly:

```powershell
python run_phase4.py output/verification_record.json <contract_address> <identifier>
```

## Example output

```text
========================================
PHASE 4 - BLOCKCHAIN VERIFICATION
========================================
Blockchain:
Ethereum Sepolia
Chain ID: 11155111
TEST 1 - ORIGINAL DATA
Result: VERIFIED
TEST 2 - TAMPERED DATA
Result: TAMPERED / NOT VERIFIED
Blockchain Modified During Phase 4: NO
Phase 4: PASS
========================================
```

Runtime search titles, URLs, hashes, transaction hashes, blocks, and contract addresses vary by run and are not hardcoded.

## Limitations and security

- Google Lens and SerpApi results are external and can change between searches.
- Visual similarity does not prove identity, ownership, authorship, or authenticity.
- The contract stores a URL and hash but does not validate the external page.
- The current contract intentionally keeps on-chain data minimal; exact canonical fields are preserved in the ignored local artifact for later verification.
- Sepolia is a testnet. Transactions are public and irreversible even though the ETH has no production value.
- Do not expose or commit `SERPAPI_API_KEY`, `PRIVATE_KEY`, RPC credentials, or seed phrases.
- Generated images, artifacts, ABI files, caches, and local environments are ignored by Git.

## Submission status

Phase 1 through Phase 4 have been exercised successfully. Phase 5 provides the final integration wrapper, reproducible setup instructions, read-only verification demo, and submission cleanup for Hacker House Goa 2026 Task 3.
