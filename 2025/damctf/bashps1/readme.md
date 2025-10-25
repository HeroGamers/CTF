wget 35.87.165.65:31337/key

openssl enc -aes-256-cbc -pass file:key -d -in enc -out dec