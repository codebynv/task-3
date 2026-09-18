<div align="center">

# HACKER HOUSE GOA '26

### OPEN TRIAL · TASK #3

# FACE IDENTIFICATION & BLOCKCHAIN VERIFICATION

**FACE → DISCOVERY → PROOF**

[![HH Goa](https://img.shields.io/badge/HACKER%20HOUSE-GOA%20'26-0B6B3A?style=for-the-badge&labelColor=FFE500)](https://hhgoa.com/)
[![Open Trial](https://img.shields.io/badge/OPEN%20TRIAL-TASK%20%233-FF2A8A?style=for-the-badge)](https://hhgoa.com/)
[![Python](https://img.shields.io/badge/PYTHON-3.10%2B-0B6B3A?style=for-the-badge&logo=python&logoColor=FFE500)](https://www.python.org/)
[![Blockchain](https://img.shields.io/badge/BLOCKCHAIN-ETHEREUM%20SEPOLIA-FF2A8A?style=for-the-badge&logo=ethereum&logoColor=F7F0D0)](https://sepolia.etherscan.io/)

</div>

---

> **HACKER HOUSE GOA 2026 · OPEN TRIAL**  
> Task #3 turns a face scan into a discoverable source and then anchors the discovered data into a verifiable blockchain record.

---

## 01 · THE BRIEF

Task #3 asks for an end-to-end pipeline that takes a face scan, finds matching content on the web/social media, creates a blockchain record, and demonstrates re-verification against that record.

### THE PIPELINE

```text
FACE SCAN
   ↓
FACE IDENTIFICATION
   ↓
REAL WEB / SOCIAL SEARCH
   ↓
MATCHING RESULT
   ↓
CANONICAL DATA
   ↓
SHA-256 FINGERPRINT
   ↓
ETHEREUM SEPOLIA
   ↓
READ-BACK VERIFICATION
   ↓
TAMPER TEST
```

---

## 02 · WHAT I BUILT

This repository implements the pipeline as a Python-based CLI workflow.

### PHASE 1 · FACE IDENTIFICATION

**DeepFace + FaceNet + RetinaFace**

- Loads and validates the input image.
- Detects a face with RetinaFace.
- Generates a FaceNet embedding.
- Saves a cropped face.
- Saves an annotated image.
- Generates a SHA-256 hash of the embedding.
- Handles missing, unreadable, and face-less images.

```text
INPUT IMAGE
    ↓
RETINAFACE
    ↓
FACE DETECTED
    ↓
FACENET EMBEDDING
    ↓
FACE HASH
```

---

### PHASE 2 · GENUINE REVERSE SEARCH

**SerpApi + Google Lens**

The cropped face is sent to a real runtime reverse-image search.

There is **no hardcoded matching URL**.

```text
FACE CROP
   ↓
SERPAPI
   ↓
GOOGLE LENS
   ↓
VISUAL MATCHES
   ↓
SOCIAL / WEB CLASSIFICATION
   ↓
BEST AVAILABLE RESULT
```

The implementation collects visual matches, classifies social-media domains, prefers a social result when available, and otherwise uses a valid web result.

A reverse-image match is treated as **visual/source evidence**, not as proof of a person's real-world identity.

---

### PHASE 3 · ON-CHAIN RECORD

**Ethereum Sepolia**

The selected result is reduced to canonical fields:

```json
{
  "url": "...",
  "title": "...",
  "source": "..."
}
```

The fields are serialized deterministically and hashed with **SHA-256**.

The fingerprint is then stored through the Solidity `Verifier` contract on Ethereum Sepolia.

The on-chain record contains:

- Identifier
- Source URL
- Data hash
- Timestamp
- Submitter address

The full image is **not** stored on-chain.

---

### PHASE 4 · READ-BACK + TAMPER TEST

The persisted canonical artifact is loaded and hashed again.

```text
LOCAL RECORD
     ↓
RECOMPUTE SHA-256
     ↓
READ ON-CHAIN HASH
     ↓
COMPARE
     ↓
VERIFIED / NOT VERIFIED
```

A separate in-memory copy is then modified by changing the title.

```text
ORIGINAL DATA
     ↓
HASH MATCHES CHAIN
     ↓
VERIFIED

TAMPERED COPY
     ↓
HASH CHANGES
     ↓
NOT VERIFIED

BLOCKCHAIN
     ↓
UNCHANGED
```

No tampered value is written to the blockchain.

---

## 03 · THE TRUST MODEL

The key design choice is separating **discovery** from **verification**.

| LAYER | PURPOSE | EVIDENCE |
|---|---|---|
| Face processing | Create a reproducible face representation | Embedding + face hash |
| Web search | Discover external matching content | Runtime Google Lens result |
| Canonicalization | Define the exact data being verified | URL + title + source |
| SHA-256 | Create deterministic fingerprint | Data hash |
| Blockchain | Anchor the fingerprint | Ethereum Sepolia record |
| Read-back | Re-check the original data | Hash comparison |
| Tamper test | Demonstrate integrity failure | Modified in-memory copy |

> **DISCOVERY ≠ PROOF**  
> The search step discovers a possible source. The blockchain step anchors a fingerprint of the canonical record so it can be checked later.

---

## 04 · ARCHITECTURE

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
                    FACE EMBEDDING
                           │
                           ▼
              ┌──────────────────────────┐
              │ SerpApi / Google Lens    │
              │ Genuine Runtime Search   │
              └────────────┬─────────────┘
                           │
                     MATCHING RESULT
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
                     READ-BACK RECORD
                           │
                           ▼
              ┌──────────────────────────┐
              │ VERIFY + TAMPER TEST     │
              └──────────────────────────┘
```

---

## 05 · TECH STACK

| TECHNOLOGY | ROLE |
|---|---|
| **Python 3.10+** | Pipeline and CLI |
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

## 06 · PROJECT STRUCTURE

```text
task-3/
├── blockchain.py          # Hashing + Sepolia interaction
├── face_module.py         # Face detection + encoding
├── reverse_search.py      # Google Lens reverse search
├── run_phase3.py          # On-chain record creation
├── run_phase4.py          # Verification + tamper test
├── demo.py                # Judge-friendly integration entry point
│
├── contracts/
│   └── Verifier.sol       # Minimal verification contract
│
├── test_images/           # Demo / negative-test images
├── requirements.txt
├── .env.example
└── README.md
```

Runtime artifacts under `output/` are intentionally ignored by Git.

---

## 07 · RUN THE PIPELINE

### CLONE

```powershell
git clone https://github.com/codebynv/task-3.git
cd task-3
```

### ENVIRONMENT

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### CONFIGURE

Create `.env` from `.env.example`:

```text
SERPAPI_API_KEY=
SEPOLIA_RPC_URL=
PRIVATE_KEY=
CONTRACT_ADDRESS=
```

Keep credentials out of Git.

### LIVE RUN

```powershell
python demo.py test_images/einstein.jpg
```

This runs the reverse search and creates a real Sepolia transaction.

### READ-ONLY VERIFICATION

```powershell
python demo.py --verify-only test_images/einstein.jpg
```

This mode reads the saved record and performs verification/tamper testing without another search or blockchain transaction.

---

## 08 · DEMO OUTPUT

A successful verification stage follows this structure:

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

Runtime URLs, hashes, transaction hashes, block numbers and contract addresses vary by run.

---

## 09 · HH GOA VISUAL LANGUAGE

The HH Goa treatment is carried through the entire README, not only the header.

### OPEN-TRIAL / EVENT-PASS LANGUAGE

- **Goa green** → structure
- **Electric yellow** → primary event accent
- **Hot pink** → task and contrast accents
- **Cream** → softer typography/surfaces
- Bold uppercase labels
- Numbered trial sections
- Compact metadata tables
- Task callouts
- Arrow-based pipeline diagrams
- Poster / event-pass hierarchy

### THE CORE IDEA

```text
FACE
 ↓
DISCOVER
 ↓
FINGERPRINT
 ↓
ANCHOR
 ↓
VERIFY
```

---

## 10 · SECURITY & LIMITATIONS

- Google Lens / SerpApi results are external and can change between searches.
- Visual similarity does not prove real-world identity, ownership, authorship, or authenticity.
- The contract stores a URL and fingerprint; it does not validate the external page itself.
- Ethereum Sepolia is a public testnet; transactions are publicly visible and irreversible.
- The complete source image is not written to the blockchain.
- API keys, private keys, RPC credentials and seed phrases must never be committed.
- Local artifacts and generated outputs are kept outside tracked source where configured.

---

## 11 · OPEN TRIAL SUBMISSION

**TASK #3 · FACE IDENTIFICATION & BLOCKCHAIN VERIFICATION**

| | |
|---|---|
| **STATUS** | SHIPPED |
| **REPOSITORY** | [github.com/codebynv/task-3](https://github.com/codebynv/task-3) |
| **STAGE** | Open Trials |
| **NETWORK** | Ethereum Sepolia |
| **PIPELINE** | Face → Search → Hash → Chain → Verify |

The selection framework describes **Proof of building**, **Task performance**, **Clear thinking**, and **Drive to be there** as selection signals. fileciteturn43file3

---

> ### BUILD · SHIP · LAUNCH
>
> **HACKER HOUSE GOA '26**  
> Goa, India · 28–31 October 2026
>
> [hhgoa.com](https://hhgoa.com/) · [@codebynv](https://github.com/codebynv)

<div align="center">

**TASK #3 · FACE → DISCOVERY → PROOF**

</div>
