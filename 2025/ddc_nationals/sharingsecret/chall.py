from Crypto.Util.number import long_to_bytes, bytes_to_long
# https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing#Python_code
from ss import make_random_shares, recover_secret
from ast import literal_eval

yes_flag = b'Flag out ok'
no_flag = b'Dont give flag'


cached_shares = {}
# Network level cache
def cache_share(share):
    x,y = share
    assert x.bit_length() <= 4, "packet field limit size"
    if x in cached_shares:
        return (x, cached_shares[x])
    else:
        cached_shares[x] = y
        return (x,y)

original_shares = make_random_shares(bytes_to_long(no_flag), minimum=7, shares=12)

print(f"Intercepted secret shares: ")

for share in original_shares:
    print(share)
    _ = cache_share(share)

# Only 6 shares corrupted, not enough to control output 
corrupt_shares = original_shares[:6]
honest_shares = original_shares[6:]

corrupt_shares = []
for i in range(6):
    try:
        new_share = input(f'party {i+1} new share ({i+1},share): ')
        corrupt_shares.append(literal_eval(new_share))

    except:
        print(f"keeping original share for party {i+1}")
        corrupt_shares.append(original_shares[i])


from random import sample

# All 64 evaluators check the shares to see if flag should be released
evaluated_shares = corrupt_shares + honest_shares


for i in range(64):
    check_shares = sample(evaluated_shares, 7)
    from_network = [cache_share(x) for x in check_shares]
    result = recover_secret(from_network)
    if long_to_bytes(result) == yes_flag:
        print(f'evaluator {i} accepts!')
    else:
        print(f'evaluator {i} recovered {result}, and will not send you the flag')
        exit()


with open("flag.txt", "rb") as f:
    flag = f.read()
    print(flag)