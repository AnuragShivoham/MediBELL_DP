# MediBELL: Decentralized Audit Layer Architecture

This document details the architecture of the Blockchain & IPFS Audit Trail layer for the MediBELL system, highlighting the model-to-ledger pipeline, design constraints, and data flow.

---

## 1. Architectural System Diagram

Below is the end-to-end data flow showing how federated models are securely persisted, registered, and verified:

```mermaid
graph TD
    subgraph Edge Clients (Hospital Nodes)
        C1[Client 1: MLP Model + LDP Noise] -->|Local Updates| Server[Federated Aggregator Server]
        C2[Client 2: MLP Model + LDP Noise] -->|Local Updates| Server
        C3[Client 3: MLP Model + LDP Noise] -->|Local Updates| Server
    end

    subgraph FL Aggregation & Serialization
        Server -->|FedAvg| GlobalWeights[Compute Global Model Weights]
        GlobalWeights -->|joblib Serialization| PickledModel[models/production_model_round_X.pkl]
    end

    subgraph IPFS Storage Layer
        PickledModel -->|Pinata API Upload| PinataGate[Pinata Cloud Gateway]
        PinataGate -->|Cryptographic Hash| CID[Return IPFS CID]
    end

    subgraph Ledger Auditing Layer
        CID -->|registerRound| Contract[MediBellRegistry Smart Contract]
        Contract -->|EIP-1559 Transaction| Sepolia[Ethereum Sepolia Testnet]
        Sepolia -->|Generate Tx Hash| AuditLog[Local audit_trail.json Cache]
    end

    subgraph Verification Gateway
        User[External Auditor / Judge] -->|GET /audit| Flask[Flask API app.py]
        Flask -->|Web3 call getRound| Contract
        Contract -->|On-Chain Data| Flask
        Flask -->|Verify CID + Accuracy| User
        User -->|Download CID| IPFSNet[Public IPFS Gateway]
        IPFSNet -->|Calculate SHA256| HashVerify[Verify Match to Local Hash]
    end
```

---

## 2. Core Architectural Design Decisions

### A. Non-Invasive Hooks
The blockchain and IPFS managers are designed as a decoupled module (`blockchain/`). They attach to the production federated training loop ([run_production_fl.py](file:///home/dev/Desktop/projects/MediBELL_DP/fl_advanced/run_production_fl.py)) through clean interfaces. If the blockchain network goes down or RPC connections time out, the ML simulation catches the warning and proceeds with training, preventing clinical simulation disruption.

### B. Metadata Storage (Off-Chain Models)
To ensure scalability and minimize gas cost, **raw model weights are never stored on the blockchain**. Instead:
1. The serialized model binary is saved to **IPFS** (returning a cryptographic CID).
2. Only the lightweight metadata (`round_num`, `accuracy`, `cid`, and transaction details) is anchored **on-chain**.

### C. Ledger Tamper-Resistance (Duplicate Prevention)
The smart contract [MediBellRegistry.sol](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/contracts/MediBellRegistry.sol) acts as the single source of truth. It enforces that once a round is registered, its metadata cannot be modified or overridden:
```solidity
require(rounds[_round].timestamp == 0, "Round already registered");
```

---

## 3. Data Schema Specifications

### On-Chain (Smart Contract Struct)
```solidity
struct RoundInfo {
    uint256 round;
    string cid;
    uint256 accuracy; // Stored as scaled integer (e.g. 94.27% -> 9427)
    uint256 timestamp;
}
```

### Local Audit Log (`blockchain/audit_trail.json`)
```json
{
  "round": 1,
  "accuracy": 94.27,
  "cid": "Qmbozu5G2J4NGsaVpB9CGmn7S4peWiM4ra8c1Ry6TxgdHP",
  "tx_hash": "0xc34db71cff3bcba9...",
  "timestamp": 1781896052
}
```
