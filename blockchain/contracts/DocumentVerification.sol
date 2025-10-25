// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract DocumentVerification {
    struct Doc {
        address owner;
        uint256 timestamp;
        string ipfsCid;
        bool exists;
    }

    mapping(bytes32 => Doc) private docs;

    event DocumentNotarized(bytes32 indexed docHash, address indexed owner, uint256 timestamp, string ipfsCid);

    /**
     * @dev Notarize a document by its SHA-256 hash and optional IPFS CID.
     * The docHash should be a 32-byte value (sha256).
     */
    function notarizeDocument(bytes32 docHash, string memory ipfsCid) public returns (bool) {
        require(docHash != bytes32(0), "Invalid document hash");
        require(!docs[docHash].exists, "Document already notarized");

        docs[docHash] = Doc({
            owner: msg.sender,
            timestamp: block.timestamp,
            ipfsCid: ipfsCid,
            exists: true
        });

        emit DocumentNotarized(docHash, msg.sender, block.timestamp, ipfsCid);
        return true;
    }

    function getDocument(bytes32 docHash) public view returns (address owner, uint256 timestamp, string memory ipfsCid, bool exists) {
        Doc memory d = docs[docHash];
        return (d.owner, d.timestamp, d.ipfsCid, d.exists);
    }

    function isNotarized(bytes32 docHash) public view returns (bool) {
        return docs[docHash].exists;
    }
}
