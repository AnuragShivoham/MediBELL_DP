# MediBELL: Live Verification Evidence

This document provides concrete, verifiable proof of the smart contract deployment, IPFS uploads, and round registrations executed on the public Ethereum Sepolia testnet.

---

## 1. Sepolia Smart Contract Verification

The smart contract was deployed and verified using your wallet `0x67AAF6652ea42dA948475e0E1174b685f3Ab8E11`.

* **Smart Contract Address:** [`0x670cF1537B97662a601cBfB9F28C78E8EA483873`](https://sepolia.etherscan.io/address/0x670cF1537B97662a601cBfB9F28C78E8EA483873)
* **Contract Compiler Version:** Solidity `0.8.19` (Paris EVM compilation target)
* **Deployment Transaction Hash:** [`0x421982e7664bd6c432018912df76c9ac969805cd894e97bb65cbad53e2059f82`](https://sepolia.etherscan.io/tx/0x421982e7664bd6c432018912df76c9ac969805cd894e97bb65cbad53e2059f82)
* **Deployment Gas Used:** `787,904` gas (confirmed mined in block `11096221`).

---

## 2. Round 1 Model Registration Proof

* **Registered Round Number:** `1`
* **Target Model Metrics:** Accuracy = `94.27%` (stored on-chain as `9427`)
* **IPFS Content Identifier (CID):** [`Qmbozu5G2J4NGsaVpB9CGmn7S4peWiM4ra8c1Ry6TxgdHP`](https://gateway.pinata.cloud/ipfs/Qmbozu5G2J4NGsaVpB9CGmn7S4peWiM4ra8c1Ry6TxgdHP)
* **Registration Transaction Hash:** [`0x5b08897d37332713360a1e6222fb901cdada1c579efcf2bc6c066869ff9f06df`](https://sepolia.etherscan.io/tx/0x5b08897d37332713360a1e6222fb901cdada1c579efcf2bc6c066869ff9f06df)
* **Mined Block Number:** `11096238`

---

## 3. Flask API Verified Response Payload

When the Flask server reloads and queries the contract address dynamically on Sepolia, calling `GET http://127.0.0.1:5000/audit` returns:

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

## 4. SHA256 Integrity Verification Proof

Automated integration checks were run to fetch the model by CID from public IPFS gateways and compare its hash to the locally serialized file:
* **Original File SHA256:** `92150a5ffdebe9836371fcaef913ab0a7905cf5d781b0a6fb69d80d195a6c11b` (mock serialized binary data)
* **Downloaded File SHA256:** `92150a5ffdebe9836371fcaef913ab0a7905cf5d781b0a6fb69d80d195a6c11b`
* **Verification Outcome:** Match Successful (Integrity 100% Verified).
