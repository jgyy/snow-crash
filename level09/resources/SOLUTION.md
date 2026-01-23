# Level09 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Decrypt a position-based character shift cipher to retrieve the flag09 token.

## Vulnerability
Position-based character shift cipher where each character is encoded by adding its position index to the character value.

## Binary Analysis

The level09 binary reads a token file that is encoded. The token file at `/home/user/level09/token` contains encrypted data.

## The Problem

1. **Character Shift Encoding**: Each character is encoded as `encoded_char = original_char + position_index`
2. **Predictable Cipher**: The encoding is deterministic based on position
3. **No Key Required**: The algorithm is simple substitution without a key
4. **File Protection**: Token file protected but readable via the binary

## Exploitation

### Method: Decode Position-Based Cipher

Read the encoded token file (binary format) and decode each character by subtracting its position index:

```
decoded_char = (encoded_char - position_index) % 256
```

### Decoding Steps

1. Read encoded token file as hex bytes
2. For each byte at position i: `original = (encoded_value - i) % 256`
3. Filter to alphanumeric characters to get the final password
4. SSH as flag09 with decoded password
5. Run getflag to obtain the level flag

### Example Payload

```bash
# Read encoded token (26 bytes in this case)
cat /home/user/level09/token | od -An -tx1

# Decode each byte by position
# Position 0: byte - 0
# Position 1: byte - 1
# Position 2: byte - 2
# etc...

# Result: f3iji1ju5yuevaus41q1afiuq (password for flag09)
```

## Encoded vs Decoded

- **Encoded Token**: `f4kmm6p|=...` (binary data with special characters)
- **Decoded Token**: `f3iji1ju5yuevaus41q1afiuq` (flag09 password)
- **Final Flag**: `s5cAJpM8ev6XHw998pRWG728z` (from getflag)

## Security Flaws

1. **Weak Cipher**: Position-based shift is trivially breakable
2. **No Key Material**: Encryption uses only position, no secret
3. **Deterministic**: Same plaintext always produces same ciphertext
4. **Predictable Pattern**: Position index is sequential and known


## Answer

**Flag09 Password**: `f3iji1ju5yuevaus41q1afiuq` (from decoded token)
**Level09 Flag**: `s5cAJpM8ev6XHw998pRWG728z`
**Vulnerability**: Position-based character shift cipher
**Impact**: Trivial decryption via position index manipulation
