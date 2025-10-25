msg1 = "d55860b8bd9fb5da012f7d153627e5f0e28dd3536b5648eaa33d563955c59b7a984f14cd0e3f8c7488917f5ab83fbea8ad79c01ab4e2b957097e6fa5eea6de302e82db2b86fbd55ae8c2f8944eb210699ae5162968e973ec94c283c84436dfaaa732c14f2f98963885ae9a49dd64b79daba95b1c95081bac0223abdd4e10eada3cdceae39c0538550b03f2f9fbd0c997aca6e199b5e9cba354248757db"
msg2 = "d1527eb1bf9fb1d3523c625c3726edbeb0e4804d700345e3e6251372538a8166dd5805c4166a873b9cd5770aa229beb3a66acc5face3a85b596c79b2b9adc3746b82dd78ccd3e439dfeed7a16d94172ed4c7133e6ead72ea85c298d91c2e9ea5ad33d70e2d899615caa3981bcb21b498a5a95d1c8d0b07fd002be9913b06af9f1edaf5a6904151481118f6b4bdc9ded9b3a2fedcf3f1ddab536d865686e03eddc7000c5317e332f6f8ef2c1d3128cc161f311481ce1d272b0bcaeb88438aef5e89ccbe4ec7c42f68554acd5b5714e27ca39b5f55e9b9a20f658961c654f2978794e10132fb167ba40ea2c8cb04b77d76bd104caaf68f8d3fadfba160bd4efdf6794ff6659b93063b8e1ef128d73ae3ac1daa1eaf49f56a8dd377f96292eef14c64b14e05878b69d5067894e06d2b07c9d539e485c759b21467952f6305b2224e75b9d76c92435549446bd74d916857796a9786ff71725c00f8bab66532dd9cb93338b48f68d540fc76d9b09083b926fb23243e44907f7ca84f82003a2516e5fff0a3fa9198833af58a488da752c46edc2001910b1b0ed6de7a68ce6e87159db284b31b6c7864843ff654e9ab49276e4a481bb1beec6dfc708fe2fd444a"

known_plaintext = "Hello my friend!".encode()
msg1_bytes = bytes.fromhex(msg1)
msg2_bytes = bytes.fromhex(msg2)

# Extract the keystream from the known plaintext and the first message
keystream_block1 = bytes([msg1_bytes[i] ^ known_plaintext[i] for i in range(len(known_plaintext))])
print(f"First keystream block (16 bytes): {keystream_block1.hex()}")

# Let's try decrypting the first message to assert getting the correct output
partial_msg1_decrypt = bytes([msg1_bytes[i] ^ keystream_block1[i] for i in range(len(keystream_block1))])
print(f"First message decrypted: {partial_msg1_decrypt}")
assert partial_msg1_decrypt == known_plaintext

# Decrypt the beginning of the second message using the extracted keystream
decrypted_msg2_start = bytes([msg2_bytes[i] ^ keystream_block1[i] for i in range(len(keystream_block1))])
print(f"Decrypted start of msg2: {decrypted_msg2_start}") # Lorem ipsum dolo

# That gave us the beginning of Lorem ipsum, we can get the full common lorem ipsum text online, and use it to get the full keystream for msg2
# Full lorem ipsum
lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

# Get keystream from msg2
lorem_bytes = lorem_ipsum.encode()
keystream_from_msg2 = bytes([msg2_bytes[i] ^ lorem_bytes[i] for i in range(len(lorem_bytes))])
print(f"Keystream from msg2: {keystream_from_msg2.hex()}")

# Now decrypt msg1 using the keystream from msg2
decrypted_msg1 = bytes([msg1_bytes[i] ^ keystream_from_msg2[i] for i in range(len(msg1_bytes))])
print(f"Decrypted msg1: {decrypted_msg1}")
# Hello my friend! I would like to tell you a secret, the password is 'GUCCIBELT'. Also the next message I am sending you will be Lorem Ipsum for verification.