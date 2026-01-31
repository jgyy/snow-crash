# Level01 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Find the password to access the flag01 account and retrieve the token.

## Vulnerability
Weak DES crypt hash vulnerable to dictionary attacks.

## Exploitation

### Step 1: Examine /etc/passwd for flag01

The flag01 account has a password hash stored directly in `/etc/passwd`:

```bash
getent passwd | grep flag01
# Output: flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

### Step 2: Analyze the Password Hash

The hash `42hDRfypTqqnw` is a **DES crypt hash**:
- **Format**: Traditional Unix DES-based crypt (13 characters)
- **Salt**: `42` (first 2 characters)
- **Algorithm**: DES (Data Encryption Standard)
- **Maximum password length**: 8 characters
- **Key strength**: ~70 bits (vulnerable to dictionary attacks)

### Step 3: Crack the DES Hash via Dictionary Attack

**Method 1: Using `john` the Ripper (Fastest Manual Method)**

Create a file with the hash in john format and crack it:
snow-crash vm does not have the proper john binary, so have to do outside vm

```bash
echo "flag01:42hDRfypTqqnw" > /tmp/hashes.txt
john --show /tmp/hashes.txt
```

**Result:** The password `abcdefg` matches the hash.

### Step 4: Access flag01 Account via SSH

```bash
sshpass -p "abcdefg" ssh -o StrictHostKeyChecking=no -p 4242 flag01@localhost getflag
```

### Step 5: Retrieve the Flag Token

```
Check flag.Here is your token : f2av5il02puano7naaf6adaaf
```

## Security Flaws

1. **Weak Password Hash**: DES crypt with only ~70 bits of key strength
2. **Vulnerable to Dictionary Attacks**: Small password space (8 character limit)
3. **Hash Stored in /etc/passwd**: Publicly readable file contains password hash
4. **No salting protection**: Salt is only 2 characters (standard DES behavior)

## Answer

- **Flag01 Password**: `abcdefg`
- **Level01 Token**: `f2av5il02puano7naaf6adaaf`
- **Vulnerability Type:** Weak cryptographic hash (DES) with dictionary attack
