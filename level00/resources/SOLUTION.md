# Level00 Solution

## Starting VM

```bash
wget https://cdn.intra.42.fr/isos/SnowCrash.iso
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Find the password to access the flag00 account and retrieve the token.

## Vulnerability
Weak Caesar cipher encryption storing a password in a publicly readable file.

## Exploitation

### Step 1: Discover the Encoded Password
The password hint is hidden in a file with unusual permissions: `/usr/sbin/john`

```bash
cat /usr/sbin/john
# Output: cdiiddwpgswtgt
```

### Step 2: Decode the Password
The string `cdiiddwpgswtgt` is encoded using a Caesar cipher with shift 15.

**Decryption Method:**
Apply Caesar cipher shift 15 to decrypt:
- Input: `cdiiddwpgswtgt`
- Output: `nottoohardhere`

**Algorithm (Caesar Cipher):**
For each character, subtract the shift value from its position in the alphabet:
```
Original: n o t t o o h a r d h e r e
Encoded:  c d i i d d w p g w t g t g (shift +15)
```

### Step 3: Access flag00 Account via SSH
Connect via SSH and run getflag:

```bash
sshpass -p "nottoohardhere" ssh -o StrictHostKeyChecking=no -p 4242 flag00@localhost getflag
```

### Step 4: Get the Flag Token
Output from getflag:
```
Check flag.Here is your token : x24ti5gi3x0ol2eh4esiuxias
```

## Security Flaws
1. **Information Disclosure**: The encoded password is stored in a readable file (`/usr/sbin/john`) owned by flag00
2. **Weak Encryption**: Caesar cipher is easily breakable (only 26 possible shifts)
3. **No access controls**: File is world-readable despite containing encoded credentials

## Answer
- **Flag00 Password:** `nottoohardhere`
- **Level00 Token:** `x24ti5gi3x0ol2eh4esiuxias`
- **Vulnerability Type:** Weak encryption with information disclosure

