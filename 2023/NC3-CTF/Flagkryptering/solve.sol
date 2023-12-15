// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract EncryptFlag {


    constructor() {
    }

    function encrypt(bytes32 key, bytes32 flag) pure  public returns (bytes32) {
        bytes32 ciphertext = key ^ flag;
        return ciphertext;
    }

    function generateKey(int blocknum) pure public returns (bytes32) {
        bytes32 key;
        if (blocknum > 0) {
            key = bytes32(keccak256(abi.encodePacked(uint256(blocknum-1))));

        } else {
            key = bytes32(keccak256(abi.encodePacked(uint256(blocknum))));
        }

        return key;
    }

    function crack() pure public returns (bytes32) {
        bytes32 encrypted = 0xc3523b9a72a40978afbab042b0b5f2d41167c2760491b52925cd727d581ac802;
        bytes32 decrypted = "testing";
        bytes32 prefix = "NC3{";
        bytes32 key = "testkey";
        int i = 0;

        while (decrypted[0] != prefix[0] && decrypted[1] != prefix[1] && decrypted[2] != prefix[2] && decrypted[3] != prefix[3]) {
            key = generateKey(i);
            decrypted = encrypt(key, encrypted);
            i += 1;
        }

        // block number = 16 (for key)
        // decrypted = 0x4E43337B796F755F7265706C6963617465645F7468655F6B65797D0000000000
        // key = 0x8D1108E10BCB7C27DDDFC02ED9D693A074039D026CF4EA4240B40F7D581AC802
		// NC3{you_replicated_the_key}
        return decrypted;
    }

}