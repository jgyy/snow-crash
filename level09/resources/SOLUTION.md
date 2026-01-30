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

#### Step 1: Extract Encoded Token File from Remote Host
Read the encoded token file in hexadecimal format:

```bash
ssh -p 4242 level09@localhost "od -An -tx1 /home/user/level09/token"
```

**Example Output:**
```
f4 6b 6d 6d 36 70 7c 3d ...
```

Each byte is the encoded character at that position.

#### Step 2: Manually Extract and Decode the Token

**Manual Multi-Step Extraction:**

```bash
# Step 2a: Get the hex dump as a continuous string
HEX_OUTPUT=$(ssh -p 4242 level09@localhost "od -An -tx1 /home/user/level09/token" | tr -d ' ' | tr -d '\n')
echo "$HEX_OUTPUT"

# Step 2b: Convert hex to raw bytes
echo "$HEX_OUTPUT" | xxd -r -p > /tmp/encoded_token.bin

# Step 2c: Display as binary to see the encoded characters
od -A x -t x1z /tmp/encoded_token.bin
```

#### Step 3: Decode Using Python Script
Create a Python script to decode the position-based cipher:

```bash
cat > /tmp/decode_level09.py << 'PYTHON_EOF'
import sys

def decode_token(token):
    """Decode position-based character shift cipher."""
    decoded = "".join(chr((ord(c) - i) % 256) for i, c in enumerate(token))
    # Filter to alphanumeric characters only
    return "".join(c for c in decoded if c in "abcdefghijklmnopqrstuvwxyz0123456789")

# Read from file or stdin
with open('/tmp/encoded_token.bin', 'rb') as f:
    encoded_bytes = f.read()

# Decode the token
encoded_token = encoded_bytes.decode('latin-1')
decoded_token = decode_token(encoded_token)
print(f"Decoded Token: {decoded_token}")
PYTHON_EOF

python /tmp/decode_level09.py
# Output: f3iji1ju5yuevaus41q1afiuq
```

**Alternative: Direct Bash/AWK Decoding (Without Python)**

```bash
# Extract hex and convert to ASCII, then apply position-based shift
HEX=$(ssh -p 4242 level09@localhost "od -An -tx1 /home/user/level09/token" | tr -d ' ' | tr -d '\n')
echo "$HEX" | xxd -r -p | od -An -t dC | awk '{
    for(i=1;i<=NF;i++) {
        val = $i - (i-1);
        if (val < 0) val += 256;
        if ((val >= 97 && val <= 122) || (val >= 48 && val <= 57)) {
            printf "%c", val;
        }
    }
}' ; echo
```

#### Step 4: Access flag09 Account with Decoded Password
Using the decoded password from above:

```bash
sshpass -p "f3iji1ju5yuevaus41q1afiuq" ssh -o StrictHostKeyChecking=no -p 4242 flag09@localhost getflag
```

#### Step 5: Extract Final Flag
The token from getflag:
```bash
# Output should be:
Check flag.Here is your token : s5cAJpM8ev6XHw998pRWG728z
```

## Decryption Analysis

**Encoded vs Decoded:**
- **Encoded Token**: Binary data with values shifted by position (f4 6b 6d 6d...)
- **Decoded Token**: `f3iji1ju5yuevaus41q1afiuq` (password for flag09)
- **Final Flag**: `s5cAJpM8ev6XHw998pRWG728z` (from getflag)

**Algorithm Verification:**
- Each byte at position i was incremented by i during encoding
- Reversing: subtract position index from each byte
- Filter to alphanumeric characters to extract the password

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
