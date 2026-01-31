# Level09 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Decrypt a position-based character shift cipher to retrieve the flag09 token.

## Vulnerability
Position-based character shift cipher where each character is encoded by adding its position index.

## Exploitation

The level09 binary reads a token file that is encrypted with a weak cipher. The token file at `/home/user/level09/token` contains encoded data.

**The Cipher:**
- Each character is encoded as: `encoded_char = original_char + position_index`
- Position index starts at 0 and increments for each character
- This is a trivially weak cipher with no key material

**Why it's Vulnerable:**
1. **Predictable Algorithm**: Encoding is deterministic based on position
2. **No Key Required**: Algorithm is known; no secret key needed
3. **Position Index is Sequential**: Attacker knows exactly what values were added
4. **Simple Decryption**: Reverse operation is trivial: `original = (encoded_char - position_index) % 256`

### Exploit Steps

#### Step 1: Connect to level09 and Extract Encoded Token
Use the token from Level08 as the password. Extract the token file in hexadecimal format:

```bash
sshpass -p "quif5eloekouj29ke0vouxean" ssh -o StrictHostKeyChecking=no -p 4242 level09@localhost "od -An -tx1 /home/user/level09/token"
```

**Example Output:**
```
f4 6b 6d 6d 36 70 7c 3d ...
```

Each byte is the encoded character at that position.

#### Step 2: Decode the Extracted Token

Parse the hex output and apply position-based reversal. For each byte at position i, subtract the position index:

```bash
# Convert hex to decimal and apply decoding: original = (encoded_byte - position) % 256
# The decoded token is: f3iji1ju5yuevaus41q1afiuq
```

#### Step 3: Access flag09 Account with Decoded Password
Using the decoded password from above:

```bash
sshpass -p "f3iji1ju5yuevaus41q1afiuq" ssh -o StrictHostKeyChecking=no -p 4242 flag09@localhost getflag
```

#### Step 4: Extract Final Flag
The token from getflag:
```bash
# Output should be:
Check flag.Here is your token : s5cAJpM8ev6XHw998pRWG728z
```

## Security Flaws

1. **Weak Cipher**: Position-based shift is trivially breakable
2. **No Key Material**: Encryption uses only position, no secret key
3. **Deterministic**: Same plaintext always produces same ciphertext
4. **Predictable Pattern**: Position index is sequential (0, 1, 2, 3...) and known
5. **No Authentication**: No integrity checking on decoded data
6. **Insufficient Key Space**: Entire algorithm is public; no randomization

## Answer

- **Flag09 Password**: `f3iji1ju5yuevaus41q1afiuq` (from decoded token)
- **Level09 Flag**: `s5cAJpM8ev6XHw998pRWG728z`
- **Vulnerability Type**: Weak position-based character shift cipher
- **Impact**: Trivial decryption via position index manipulation
