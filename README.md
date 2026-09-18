<div align="center">

# HACKER HOUSE GOA '26

### TASK #3 · FACE IDENTIFICATION & BLOCKCHAIN VERIFICATION

**FACE → DISCOVERY → PROOF**

[![HH Goa 2026](https://img.shields.io/badge/HACKER%20HOUSE-GOA%20'26-0B6B3A?style=for-the-badge&labelColor=FFE500)](https://hhgoa.com/)
[![Open Trial](https://img.shields.io/badge/OPEN%20TRIAL-TASK%20%233-FF2A8A?style=for-the-badge)](https://hhgoa.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-0B6B3A?style=for-the-badge&logo=python&logoColor=FFE500)](https://www.python.org/)
[![Ethereum Sepolia](https://img.shields.io/badge/BLOCKCHAIN-ETHEREUM%20SEPOLIA-FF2A8A?style=for-the-badge&logo=ethereum&logoColor=F7F0D0)](https://sepolia.etherscan.io/)

</div>

---

## THE TASK

Build an end-to-end pipeline that takes a face scan, finds matching content on the web/social media, and creates a verifiable, tamper-evident blockchain record.

```text
FACE SCAN
   ↓
FACE IDENTIFICATION
   ↓
REAL WEB / SOCIAL SEARCH
   ↓
MATCHING POST
   ↓
CANONICAL DATA + SHA-256
   ↓
ETHEREUM SEPOLIA
   ↓
READ-BACK VERIFICATION
   ↓
TAMPER TEST
```

The project follows the Task #3 flow: **face scan input → web/social media search → matching post → blockchain upload/verification**.

---

## WHAT I BUILT

### 01 · FACE IDENTIFICATION

**DeepFace + FaceNet + RetinaFace**

- Detects a face from the input image.
- Generates a FaceNet embedding.
- Saves a cropped face and annotated image for inspection.
- Produces a deterministic SHA-256 face hash.
- Handles missing, unreadable, and face-less inputs.

### 02 · GENUINE REVERSE IMAGE SEARCH

**SerpApi + Google Lens**

The face crop is searched at runtime. The matching result is **not hardcoded**.

- Results are discovered dynamically.
- Social-media domains are preferred when available.
- A valid web result is used when no social result is available.
- The selected result is reduced to canonical `URL + Title + Source` data.

```text
URL + Title + Source
        ↓
Canonical representation
        ↓
SHA-256 fingerprint
```

A reverse-image match is treated as visual/source evidence, not as proof of a person's real-world identity.

### 03 · ON-CHAIN RECORD

**Ethereum Sepolia**

The canonical result is fingerprinted and recorded on-chain.

The stored record is intentionally compact:

- Record identifier
- SHA-256 fingerprint
- Source URL
- Contract address
- Transaction metadata
- Block metadata

The complete image is not stored on-chain.

### 04 · READ-BACK VERIFICATION

The saved canonical result is hashed again and compared with the blockchain record.

```text
LOCAL CANONICAL DATA
        ↓
RECOMPUTE HASH
        ↓
READ BLOCKCHAIN RECORD
        ↓
COMPARE
        ↓
VERIFIED / NOT VERIFIED
```

### 05 · TAMPER DETECTION

A copy of the verified data is changed **only in memory**. The altered fingerprint is then checked against the original on-chain fingerprint.

```text
ORIGINAL DATA  → VERIFIED
TAMPERED COPY  → TAMPERED / NOT VERIFIED
CHAIN          → NOT MODIFIED
```

No tampered value is submitted to the blockchain.

---

## ARCHITECTURE

```text
                    ┌──────────────────┐
                    │    INPUT IMAGE   │
                    └────────┬─────────┘
                             │
                             ▼
              ┌──────────────────────────┐
              │ DeepFace / FaceNet       │
              │ RetinaFace Detection     │
              └────────────┬─────────────┘
                           │
                    Face embedding
                           │
                           ▼
              ┌──────────────────────────┐
              │ SerpApi / Google Lens    │
              │ Genuine runtime search   │
              └────────────┬─────────────┘
                           │
                     Matching result
                           │
                           ▼
              ┌──────────────────────────┐
              │ Canonicalize             │
              │ URL / Title / Source     │
              └────────────┬─────────────┘
                           │
                         SHA-256
                           │
                           ▼
              ┌──────────────────────────┐
              │ Ethereum Sepolia         │
              │ Verifier.sol             │
              └────────────┬─────────────┘
                           │
                     Read exact record
                           │
                           ▼
              ┌──────────────────────────┐
              │ Verification +           │
              │ In-memory Tamper Test    │
              └──────────────────────────┘
```

---

## WHY THE PIPELINE IS AUDITABLE

| Layer | What happens | Evidence |
|---|---|---|
| Face processing | Detect and encode | Face embedding + face hash |
| Web search | Discover matching content | Runtime Google Lens result |
| Canonicalization | Define the exact data being verified | URL + title + source |
| Blockchain | Anchor the fingerprint | Ethereum Sepolia record |
| Verification | Recompute and compare | Hash comparison |
| Tamper test | Change a copy and verify failure | In-memory modified record |

---

## TECH STACK

| Technology | Role |
|---|---|
| **Python 3.10+** | Pipeline |
| **DeepFace** | Face processing |
| **FaceNet** | Face embeddings |
| **RetinaFace** | Face detection |
| **OpenCV / Pillow** | Image processing |
| **SerpApi / Google Lens** | Genuine reverse-image search |
| **Web3.py** | Ethereum interaction |
| **Solidity 0.8.x** | Verification contract |
| **py-solc-x** | Contract compilation |
| **Ethereum Sepolia** | Public testnet record |

---

## PROJECT STRUCTURE

```text
task-3/
├── blockchain.py          # Hashing + Sepolia contract logic
├── face_module.py         # Face detection and encoding
├── reverse_search.py      # Google Lens reverse search
├── run_phase3.py          # Create on-chain record
├── run_phase4.py          # Verification + tamper test
├── demo.py                # Integration / presentation entry point
│
├── contracts/
│   └── Verifier.sol       # Minimal verification contract
│
├── test_images/           # Demo / negative-test images
├── requirements.txt
├── .env.example
└── README.md
```

Runtime artifacts in `output/` are intentionally ignored by Git.

---

## RUN LOCALLY

### 1. Clone

```powershell
git clone https://github.com/codebynv/task-3.git
cd task-3
```

### 2. Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configure

Copy `.env.example` to `.env`:

```text
SERPAPI_API_KEY=
SEPOLIA_RPC_URL=
PRIVATE_KEY=
CONTRACT_ADDRESS=
```

Use a dedicated testnet wallet. Never commit `.env`, API keys, private keys, seed phrases, or production credentials.

### 4. Run the live pipeline

```powershell
python demo.py test_images/einstein.jpg
```

This performs a genuine Google Lens search and a Sepolia transaction.

### 5. Verify without a new transaction

```powershell
python demo.py --verify-only test_images/einstein.jpg
```

Verify-only mode is read-only: no new search and no blockchain write.

---

## DEMO RESULT

A successful verification run follows this pattern:

```text
PHASE 4 - BLOCKCHAIN VERIFICATION

Blockchain:
Ethereum Sepolia
Chain ID: 11155111

TEST 1 - ORIGINAL DATA
Result: VERIFIED

TEST 2 - TAMPERED DATA
Result: TAMPERED / NOT VERIFIED

Blockchain Modified During Phase 4: NO
Phase 4: PASS
```

Runtime URLs, hashes, transaction hashes, block numbers, and contract addresses vary by run.

---

## SECURITY & LIMITATIONS

- Google Lens / SerpApi results are external and can change between searches.
- Visual similarity does not prove real-world identity, ownership, authorship, or authenticity.
- The contract stores a URL and fingerprint; it does not validate the external page.
- Sepolia is a public testnet. Transactions are public and irreversible.
- Secrets remain outside Git through `.env` and `.gitignore`.
- The complete source image is not written to the blockchain.

---

## HH GOA 2026 · OPEN TRIAL

**Task #3 — Face Identification & Blockchain Verification**

This repository contains the implementation, setup instructions, live verification flow, and tamper-detection demonstration for the Open Trial.

The Hacker House Goa 2026 selection framework describes **Proof of building**, **Task performance**, **Clear thinking**, and **Drive to be there** as selection signals. This repository keeps the build and task execution directly inspectable.

---

<div align="center">

### BUILD · SHIP · LAUNCH

**HACKER HOUSE GOA 2026**

[hhgoa.com](https://hhgoa.com/) · [GitHub](https://github.com/codebynv/task-3)

</div>
