# Level01 Solution

## Objective
Find the password to access the flag01 account and retrieve the token.

## Solution

### Step 1: Examine /etc/passwd for flag01

The flag01 account has a password hash stored directly in `/etc/passwd` (rather than in `/etc/shadow`):

```bash
getent passwd | grep flag01
# Output: flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

### Step 2: Analyze the Password Hash

The hash `42hDRfypTqqnw` is a **DES crypt hash**:
- **Format**: Traditional Unix DES-based crypt (13 characters)
- **Salt**: `42` (first 2 characters)
- **Algorithm**: DES (Data Encryption Standard)

Key characteristics:
- Maximum password length: 8 characters
- Only 70-bit effective key strength
- Highly vulnerable to dictionary attacks

### Step 3: Crack the DES Hash

Using dictionary attack with crypt():

```bash
# Using python program with crypt() function:
for password in wordlist.txt:
    if crypt(password, "42") == "42hDRfypTqqnw":
        print(f"Found: {password}")
```

The password can also be cracked with:
- **john the ripper**: `john --format=crypt hash.txt`
- **hashcat**: `hashcat -m 1500 hash.txt wordlist.txt`
- **Custom C/Python program** using crypt() function

### Step 4: The Cracked Password

```
Password: abcdefg
```

This simple password demonstrates the weakness of:
1. **Weak password selection**: Common, simple passwords
2. **Weak algorithm**: DES is no longer considered secure
3. **Obsolete storage**: Password hashes readable in /etc/passwd

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

## Key Points

1. **Information Disclosure**: Password hash visible in `/etc/passwd` (should be in `/etc/shadow`)
2. **Weak Encryption**: DES is deprecated and easily cracked
3. **Weak Authentication**: Simple password "abcdefg" is trivial
4. **Privilege Escalation**: Access to flag01 allows running getflag to proceed

## Final Answer

**Flag01 Password:** `abcdefg`
**Level01 Token:** `f2av5il02puano7naaf6adaaf`
**Token for Level02:** `f2av5il02puano7naaf6adaaf`

## Security Lessons

### What was vulnerable:
- DES-based password hashing (deprecated since 1990s)
- Passwords stored in world-readable file
- Weak password policy (allowing simple 7-letter passwords)
- No password complexity requirements

### Modern solutions:
- Use `/etc/shadow` (readable only by root)
- Use strong algorithms: SHA-256/512, bcrypt, scrypt, or Argon2
- Enforce password policies (minimum length, complexity, etc.)
- Use rate-limiting and account lockout after failed attempts
- Monitor for unauthorized password cracking attempts

## Cracking Tools Used

For educational purposes, password hashes can be cracked with:
1. **john the ripper** - Rule-based dictionary attacks
2. **hashcat** - GPU-accelerated cracking
3. **Custom programs** - Using `crypt()` function with wordlists
4. **Rainbow tables** - Pre-computed hash tables (for weak algorithms like DES)

## References

- Unix crypt() function documentation
- DES algorithm security analysis
- Modern password hashing standards (NIST SP 800-63)
