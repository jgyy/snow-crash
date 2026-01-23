# Level01 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Find the password to access the flag01 account and retrieve the token.

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

### Step 3: Crack the DES Hash

Use dictionary attack to test passwords against the hash:

```bash
for password in wordlist:
    if crypt(password, "42") == "42hDRfypTqqnw":
        print(f"Found: {password}")
```

Alternative tools:
- `john the ripper`: `john --format=crypt hash.txt`
- `hashcat`: `hashcat -m 1500 hash wordlist.txt`
- Python script: `python3 crack_des.py`

### Step 4: The Cracked Password

```
Password: abcdefg
```

### Step 5: Access flag01 Account

```bash
su flag01
# Enter password: abcdefg
```

### Step 6: Retrieve the Flag Token

```bash
flag01@SnowCrash:~$ getflag
Check flag.Here is your token : f2av5il02puano7naaf6adaaf
```

## Security Flaws

1. **Weak Password Hash**: DES crypt with only ~70 bits of key strength
2. **Vulnerable to Dictionary Attacks**: Small password space (8 character limit)
3. **Hash Stored in /etc/passwd**: Traditionally world-readable in older systems

## Answer

- **Flag01 Password**: `abcdefg`
- **Level01 Token**: `f2av5il02puano7naaf6adaaf`
- **Token for Level02**: `f2av5il02puano7naaf6adaaf`
