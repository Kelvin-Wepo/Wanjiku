Blockchain smart contract and deployment
=====================================

This folder contains a minimal smart contract and Hardhat scripts for document verification.

What was added
- `contracts/DocumentVerification.sol` - Solidity contract that notarizes a document hash and optional IPFS CID.
- `scripts/deploy.js` - Hardhat deployment script that writes ABI and address into `blockchain/abi/`.
- `abi/DocumentVerification.json` - ABI for the contract (created here so backend can operate without compiling first).
- `package.json`, `hardhat.config.js` - Hardhat project configuration.

Quick start (local Hardhat)
1. Install dependencies (from the `blockchain` folder):

```bash
cd blockchain
npm install
```

2. Start a local Hardhat node in a separate terminal (or use `npx hardhat node`):

```bash
npx hardhat node
```

3. Deploy the contract to the local node:

```bash
npm run deploy:local
```

This will compile and deploy `DocumentVerification`, then write `abi/DocumentVerification.json` and `abi/contract-address.txt`.

Hooking backend to the deployed contract
1. Set environment variables in your `.env` (or `env.example` values) with the deployed contract address and ABI path:

```
CONTRACT_ADDRESS=0x... # from abi/contract-address.txt
CONTRACT_ABI_PATH=./blockchain/abi/DocumentVerification.json
```

2. Ensure `ETHEREUM_RPC_URL` points to the network where the contract was deployed (e.g., `http://127.0.0.1:8545` for a local Hardhat node) and `PRIVATE_KEY` contains the hex private key of the account that will send transactions.

3. Restart Django. The backend service `blockchain.services.EthereumService` will attempt to load the ABI/address and call `notarizeDocument` when uploading documents and `getDocument` when verifying.

Notes on encrypted file storage
- The smart contract stores only a document hash (bytes32) and an optional IPFS CID. Encrypted file content should be stored off-chain (e.g., IPFS, S3) and the symmetric key encrypted and distributed to authorized parties off-chain. This keeps on-chain gas costs low and still provides tamper-proof verification via the stored hash.

Security
- Never store unencrypted private keys in source control. Use environment variables or a secrets manager.
