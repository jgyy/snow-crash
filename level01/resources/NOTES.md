# Level01 Investigation Notes

## Challenge Summary

Level01 teaches about **weak password hashing** and the security implications of using deprecated cryptographic algorithms. The challenge requires:
1. Discovering a password hash in an insecure location
2. Cracking the DES-based hash using dictionary attack
3. Using the cracked password to escalate privileges

## Key Findings

### Initial Reconnaissance

```bash
# Check if flag01 account exists
getent passwd | grep flag01
```

Output reveals:
```
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

### Critical Vulnerability: Password Hash in /etc/passwd

Normal Unix systems store:
- **Usernames and UIDs**: `/etc/passwd` (world readable)
- **Password hashes**: `/etc/shadow` (readable only by root)

This system violates this basic principle by storing the DES hash in `/etc/passwd`.

### Hash Analysis

**Hash:** `42hDRfypTqqnw`

Breaking down the hash:
- **Characters 1-2**: `42` = DES salt
- **Characters 3-13**: `hDRfypTqqnw` = DES encrypted password

**Hash format**: Traditional Unix crypt format (not salted bcrypt or SHA-512)

**Algorithm**: DES (Data Encryption Standard)
- Designed in 1977
- Uses only 56-bit keys (effective security: 70 bits with salt)
- Thoroughly broken by modern standards
- Crackable on modern hardware in seconds to minutes

## Investigation Process

### Step 1: File System Reconnaissance
```bash
find / -user flag01 2>/dev/null          # No files found
ls -la /home/flag01                       # Directory doesn't exist
getent passwd | grep flag01               # Found the hash!
```

### Step 2: Hash Recognition
The format `username:hash:uid:gid::...` with `42hDRfypTqqnw` clearly indicates:
- DES crypt hash (13 characters, starts with salt)
- Not a modern format like bcrypt ($2a$) or SHA-512 ($6$)

### Step 3: Attack Vector Selection

**Options considered:**
1. Rainbow tables - DES is simple enough that pre-computed tables exist
2. Brute force - 56-bit key space is small (though still ~72 quadrillion combinations)
3. Dictionary attack - Most likely approach (fast and effective)
4. Specialized tools - john the ripper, hashcat

**Chosen approach:** Dictionary attack using `crypt()` function

### Step 4: Password Cracking

Testing simple passwords with `crypt()`:
```c
for each word in dictionary:
    if crypt(word, "42") == "42hDRfypTqqnw":
        password_found = word
```

Testing started with common passwords:
- "password" - NO
- "123456" - NO
- "admin" - NO
- "flag01" - NO
- ...
- "abcdefg" - **MATCH!**

The password "abcdefg" hashes to "42hDRfypTqqnw" when using salt "42".

## Solution Summary

```
Hash: 42hDRfypTqqnw
Salt: 42
Algorithm: DES crypt
Password: abcdefg
Token: f2av5il02puano7naaf6adaaf
```

## Security Vulnerabilities Demonstrated

### 1. Weak Password Storage Location
- **Issue**: Hash in world-readable `/etc/passwd`
- **Impact**: Any user can read and attack password hashes
- **Fix**: Use `/etc/shadow` (readable only by root)

### 2. Deprecated Hash Algorithm
- **Issue**: DES-based crypt is outdated (40+ years old)
- **Impact**: Modern GPUs can crack it in milliseconds
- **Fix**: Use bcrypt, scrypt, PBKDF2, or Argon2

### 3. Weak Password Policy
- **Issue**: Simple 7-character password is allowed
- **Impact**: Easily guessable, appears in common password lists
- **Fix**: Enforce minimum 12+ characters, complexity requirements

### 4. No Rate Limiting
- **Issue**: No protection against repeated login attempts
- **Impact**: Enables brute force attacks
- **Fix**: Account lockout after N failed attempts

## Investigation Methods Used

1. **File system enumeration** - Located password hash in /etc/passwd
2. **Pattern analysis** - Recognized DES crypt format
3. **Dictionary attack** - Tested passwords from wordlists
4. **Hash verification** - Confirmed match of cracked password

## Comparative Analysis: Level00 vs Level01

| Aspect | Level00 | Level01 |
|--------|---------|---------|
| **Vulnerability** | Information Disclosure + Weak Encryption | Weak Hash Algorithm + Bad Storage |
| **Secret Location** | Encoded file in /usr/sbin/john | Hash in /etc/passwd |
| **Encryption** | Caesar cipher (shift 15) | DES crypt hash |
| **Attack Type** | Cryptanalysis | Dictionary Attack |
| **Time to Crack** | Seconds (26 possibilities) | Seconds (dictionary lookup) |
| **Password Format** | Readable encoding | Hashed |

## Advanced Techniques Not Required

- Rainbow tables (not necessary, too much storage)
- GPU-accelerated cracking (overkill for DES)
- Specialized dictionaries (standard wordlists sufficient)
- Timing attacks (not applicable to hash verification)

## Tools That Would Work

1. **john the ripper**: `john --format=crypt passwd_file`
2. **hashcat**: `hashcat -m 1500 hash wordlist.txt`
3. **unshadow + john**: `unshadow passwd shadow | john`
4. **Custom Python/C programs**: Using crypt() and wordlists

## Next Level

Token for level02: `f2av5il02puano7naaf6adaaf`

## Learning Outcomes

1. Understanding Unix password storage mechanisms
2. Recognition of DES crypt hash format
3. Dictionary attack methodology
4. Why deprecated algorithms are dangerous
5. Importance of proper file permissions (/etc/shadow)
6. Password policy enforcement requirements
7. Modern password hashing best practices
