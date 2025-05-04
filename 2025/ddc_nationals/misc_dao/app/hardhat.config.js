require("@nomicfoundation/hardhat-toolbox");
require("web3");

module.exports = {
    solidity: "0.8.18",
    networks: {
        hardhat: {
            chainId: 1337,
        },
        local: {
            url: "http://dao.blockchain.hkn:8545", // Blockchain RPC address
            chainId: 1337,
            accounts: [
                "0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6", // Account private key
            ],
        },
    },
};
