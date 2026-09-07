// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Verifier {
    struct Record {
        string sourceUrl;
        string dataHash;
        uint256 timestamp;
        address submitter;
        bool exists;
    }

    // Mapping from a unique identifier (like the image hash or data hash itself) to the Record
    mapping(string => Record) public records;

    event RecordStored(string indexed identifier, string sourceUrl, string dataHash, uint256 timestamp, address submitter);

    function storeVerification(string memory identifier, string memory sourceUrl, string memory dataHash) public {
        require(!records[identifier].exists, "Record already exists for this identifier");
        
        records[identifier] = Record({
            sourceUrl: sourceUrl,
            dataHash: dataHash,
            timestamp: block.timestamp,
            submitter: msg.sender,
            exists: true
        });

        emit RecordStored(identifier, sourceUrl, dataHash, block.timestamp, msg.sender);
    }

    function getVerification(string memory identifier) public view returns (string memory, string memory, uint256, address, bool) {
        Record memory rec = records[identifier];
        return (rec.sourceUrl, rec.dataHash, rec.timestamp, rec.submitter, rec.exists);
    }
}
