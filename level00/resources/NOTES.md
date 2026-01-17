# Level00 Investigation Notes

## Challenge Summary
Level00 teaches about information disclosure and weak encryption. The solution requires:
1. Finding a readable file containing encoded credentials
2. Decrypting the encoded password using cryptanalysis
3. Using the decrypted password to access the target account

## Key Findings

### Discovery Phase
The critical file is `/usr/sbin/john`:
- Owner: flag00
- Permissions: ----r--r-- (readable by group and others, NOT by owner)
- Size: 15 bytes
- Content: `cdiiddwpgswtgt` (encoded string)

### Decryption Phase
The encoded string uses a **Caesar cipher with shift 15**.

**Decryption Process:**
1. Recognize the string as potentially encrypted text
2. Try multiple decryption methods:
   - ROT13: `pqvvqqjctfjgtg` (gibberish)
   - Reversed: `tgtwsgpwddiidc` (gibberish)
   - Caesar shifts 0-25: Found shift 15!
3. **Shift 15 produces:** `nottoohardhere` (readable English!)

**Verification:**
The decoded text "nottoohardhere" (split as "not too hard here") makes sense as a hint and works as the actual password.

## Solution Summary
```
Encoded: cdiiddwpgswtgt
Caesar Shift: 15
Decoded: nottoohardhere
Usage: su flag00 (password: nottoohardhere)
Token: x24ti5gi3x0ol2eh4esiuxias
```

## Security Vulnerabilities Demonstrated
1. **Information Disclosure**: Sensitive credentials stored in readable files
2. **Weak Encryption**: Caesar cipher is trivial to break via brute force (26 possibilities)
3. **Poor Access Control**: File readable by all users but owned by privileged account

## Investigation Methods Used
- File permission enumeration
- Pattern matching and frequency analysis
- Brute force Caesar cipher (26 shifts)
- Caesar cipher implementation verification via Python

## Next Level
Token for level01: `x24ti5gi3x0ol2eh4esiuxias`

## Learning Outcomes
- Understanding file permissions and security implications
- Basic cryptanalysis of simple substitution ciphers
- Caesar cipher weaknesses
- Importance of strong encryption vs. obscurity
