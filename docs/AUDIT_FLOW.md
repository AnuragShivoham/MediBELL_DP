# MediBELL: Model Audit & Verification Flow

This guide describes how to verify the integrity and provenance of trained federated learning models in the MediBELL system, either programmatically via the Flask API or manually using block explorers and IPFS gateways.

---

## 1. Programmatic Verification Flow (Flask API)

The Flask server provides automated, dynamic verification against the Ethereum ledger.

```
 Auditor GET /audit
        │
        ▼
 Reads Local audit_trail.json Cache
        │
        ▼
 Connects to Sepolia Node (via Alchemy URL)
        │
        ▼
 Queries MediBellRegistry Contract (getRound)
        │
        ▼
 Compares on-chain CID/Accuracy to cached values
        │
        ├──► Matches: Appends "on_chain_verified": true
        └──► Mismatch: Appends "on_chain_verified": false
```

### Response Example:
```json
[
  {
    "round": 1,
    "accuracy": 94.27,
    "cid": "Qmbozu5G2J4NGsaVpB9CGmn7S4peWiM4ra8c1Ry6TxgdHP",
    "tx_hash": "0x5b08897d37332713360a1e6222fb901cdada1c579efcf2bc6c066869ff9f06df",
    "timestamp": 1781896052,
    "on_chain_accuracy": 94.27,
    "on_chain_timestamp": 1781896056,
    "on_chain_verified": true
  }
]
```

---

## 2. Manual Verification Walkthrough

An external auditor or judge can verify any model round independently without running the MediBELL application.

### Step 1: Look up transaction details on Etherscan
1. Go to [Sepolia Etherscan](https://sepolia.etherscan.io/).
2. Search the contract address `0x670cF1537B97662a601cBfB9F28C78E8EA483873` (or the current address in `deployed_address.txt`).
3. Click the **Contract** tab and choose **Read Contract**.
4. Expand `getRound` and enter the round number (e.g., `1`).
5. Click **Query**. You will see:
   - The round number
   - The IPFS Content Identifier (CID) (e.g., `Qmbozu5G2J4NGsaVpB9CGmn7S4peWiM4ra8c1Ry6TxgdHP`)
   - The aggregated round accuracy scaled by 100 (e.g., `9427` for `94.27%`)
   - The transaction confirmation timestamp.

### Step 2: Retrieve the Model Binary from IPFS
Using the retrieved CID, download the raw joblib model file from a public IPFS gateway:
* Pinata gateway: `https://gateway.pinata.cloud/ipfs/Qmbozu5G2J4NGsaVpB9CGmn7S4peWiM4ra8c1Ry6TxgdHP`
* Cloudflare gateway: `https://cloudflare-ipfs.com/ipfs/Qmbozu5G2J4NGsaVpB9CGmn7S4peWiM4ra8c1Ry6TxgdHP`

Save the file as `downloaded_model.pkl`.

### Step 3: Verify the File Hash
Calculate the SHA256 checksum of your downloaded file and compare it to the expected checksum:
- **Linux/macOS:**
  ```bash
  sha256sum downloaded_model.pkl
  ```
- **Windows (PowerShell):**
  ```powershell
  Get-FileHash downloaded_model.pkl -Algorithm SHA256
  ```

Because IPFS CIDs are cryptographically generated from the file content, any tampering or modification to the model weights will change the CID, causing the integrity check to fail. This guarantees that the model used in production predictions is exactly the same one verified during federated training.
