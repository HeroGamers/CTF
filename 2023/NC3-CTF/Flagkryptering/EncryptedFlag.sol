// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract EncryptFlag {


    constructor() {
    }

    function encrypt(bytes32 key, bytes32 flag) pure  public returns (bytes32) {
        bytes32 ciphertext = key ^ flag;
        return ciphertext;
    }

    function generateKey() view public returns (bytes32) {
        bytes32 key;
        if (block.number > 0) {
            key = bytes32(keccak256(abi.encodePacked(uint256(block.number-1))));
        
        } else {
            key = bytes32(keccak256(abi.encodePacked(uint256(block.number))));           
        }

        return key;
    }

}