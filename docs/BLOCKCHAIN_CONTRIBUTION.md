# MediBELL: Blockchain & IPFS Contribution Scope

This document defines the contribution boundary of the Blockchain and IPFS audit trial extension layer added to the MediBELL repository, clarifying what existed previously and what was introduced.

---

## 1. Project Context

**MediBELL** was originally developed as a privacy-preserving IoT healthcare prediction system utilizing **Local Differential Privacy (LDP)** and **Federated Learning (FL)**. The original project successfully trained models across distributed client nodes but lacked any public verifiability, provenance recording, or model integrity proofs.

This contribution (developed by **Pranjal Yadav**) introduces a secure, decentralized auditing layer that hashes model weights per round, uploads them to IPFS, and anchors their CIDs to the Ethereum blockchain.

---

## 2. Contribution Scope Boundaries

```
┌──────────────────────────────────────┐     ┌──────────────────────────────────────┐
│       ORIGINAL MEDIBELL SCOPE        │     │       NEW CONTRIBUTION SCOPE         │
├──────────────────────────────────────┤     ├──────────────────────────────────────┤
│  • Differential Privacy (LDP)        │     │  • Solidity Smart Contract           │
│  • Disease Prediction Pipelines      │     │  • EIP-1559 Transaction Manager      │
│  • Multi-hospital Client Aggregation  │     │  • IPFS Model Pinning & Retrieval    │
│  • Dataset Generation Scripts         │     │  • SHA256 Model Integrity Check      │
│  • Vitals Preprocessing Utilities    │     │  • verified Flask /audit Endpoint   │
└──────────────────────────────────────┘     └──────────────────────────────────────┘
```

---

## 3. Files Created or Modified

### 🆕 Files Created
The entire blockchain audit infrastructure was isolated to a dedicated module to preserve system modularity:
* [blockchain/contracts/MediBellRegistry.sol](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/contracts/MediBellRegistry.sol) — Solidity registry contract.
* [blockchain/deploy.py](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/deploy.py) — Solidity compiler and EIP-1559 deployer.
* [blockchain/chain_manager.py](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/chain_manager.py) — Web3 interaction manager.
* [blockchain/ipfs_manager.py](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/ipfs_manager.py) — Pinata API pinning and public gateway retrieval/validation.
* [blockchain/config.py](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/config.py) — Config loader parsing `.env`.
* [blockchain/simulation.py](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/simulation.py) — Mock simulation test.
* [tests/test_audit_api.py](file:///home/dev/Desktop/projects/MediBELL_DP/tests/test_audit_api.py) — Flask audit endpoint unit tests.
* [tests/test_ipfs_integrity.py](file:///home/dev/Desktop/projects/MediBELL_DP/tests/test_ipfs_integrity.py) — IPFS verification tests.
* [docs/ARCHITECTURE.md](file:///home/dev/Desktop/projects/MediBELL_DP/docs/ARCHITECTURE.md) — System diagram and schemas.
* [docs/DEPLOYMENT.md](file:///home/dev/Desktop/projects/MediBELL_DP/docs/DEPLOYMENT.md) — Sepolia / Pinata deployment guide.
* [docs/AUDIT_FLOW.md](file:///home/dev/Desktop/projects/MediBELL_DP/docs/AUDIT_FLOW.md) — Dynamic / manual verification walkthroughs.
* [docs/MILESTONES.md](file:///home/dev/Desktop/projects/MediBELL_DP/docs/MILESTONES.md) — Phase roadmaps.
* [docs/VERIFICATION.md](file:///home/dev/Desktop/projects/MediBELL_DP/docs/VERIFICATION.md) — Live transaction hashes and output screenshots/evidence.

### 🔧 Existing Files Modified
We integrated our modules into the existing FL training pipelines and REST endpoints:
* [fl_advanced/run_production_fl.py](file:///home/dev/Desktop/projects/MediBELL_DP/fl_advanced/run_production_fl.py) — Injected intermediate model exports (`production_model_round_X.pkl`), IPFS uploads, and blockchain registration hooks inside the global aggregation loop.
* [app.py](file:///home/dev/Desktop/projects/MediBELL_DP/app.py) — Exposed `GET /audit` endpoint calling Web3 contract states dynamically.
* [README.md](file:///home/dev/Desktop/projects/MediBELL_DP/README.md) — Added blockchain deployment guides near the top of the system description.
* [requirements.txt](file:///home/dev/Desktop/projects/MediBELL_DP/requirements.txt) — Appended `web3` and `python-dotenv` dependencies.
* [.gitignore](file:///home/dev/Desktop/projects/MediBELL_DP/.gitignore) — Ignored local private keys, deployment outputs, and transaction cache (`.env`, `deployed_address.txt`, `audit_trail.json`).

### 🔒 Files Left Untouched
All core medical logic remains intact to avoid regulatory or prediction accuracy drift:
* `dp/` — Unchanged. Core Laplace and Randomized Response DP mechanisms remain unmodified.
* `fl/` — Unchanged. Standard federated classifier loops remain unmodified.
* `utils/` — Unchanged. Preprocessing and feature alignment pipelines remain unmodified.
* `predict_dp_interactive.py` — Unchanged. The interactive GUI predictions remain unmodified.
* `train_dp.py` — Unchanged. Individual local training remains unmodified.
