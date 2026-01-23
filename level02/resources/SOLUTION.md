# Level02 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Extract password from network traffic and access the flag02 account.

### Step 1: Discover the PCAP File

The flag02-owned file is in the level02 home directory:

```bash
ls -la ~/
# Output: level02.pcap (owned by flag02, readable by group)
```

### Step 2: Analyze the PCAP File

The `level02.pcap` contains a telnet session with login credentials:

```bash
# Extract telnet traffic
tcpdump -r level02.pcap -A | grep -i password
```

### Step 3: Decode the Telnet Session

The PCAP shows a telnet login with password typed character-by-character:
- Keystroke data includes telnet protocol codes (0xff bytes)
- **Backspace character**: `7f` in hex (DEL key)
- **Enter key**: `0d` in hex (CR)

The raw sequence shows:
- Type: `ft_wandr`
- Backspace 3 times: `7f 7f 7f` (removes "dra")
- Type: `NDRel`
- Backspace 1 time: `7f` (removes "l")
- Type: `L0L`
- Enter: `0d`

### Step 4: Reconstruct the Password

After applying backspaces to the typed characters:

```
ft_wandr -> [backspace x3] -> ft_w
ft_w + NDRel -> ft_wNDRel
ft_wNDRel -> [backspace x1] -> ft_wNDRe
ft_wNDRe + L0L -> ft_wNDReL0L
```

**Password:** `ft_waNDReL0L`

### Step 5: Access flag02 Account

```bash
su flag02
# Enter password: ft_waNDReL0L
```

### Step 6: Retrieve the Flag Token

```bash
flag02@SnowCrash:~$ getflag
Check flag.Here is your token : kooda2puivaav1idi4f57q8iq
```


## Security Flaws

1. **Plain-text Protocol**: Telnet transmits all data unencrypted
2. **Network Sniffing**: Captured traffic reveals complete login credentials
3. **No Encryption**: Password visible in packet capture

## Answer

- **Flag02 Password**: `ft_waNDReL0L`
- **Level02 Token**: `kooda2puivaav1idi4f57q8iq`
- **Token for Level03**: `kooda2puivaav1idi4f57q8iq`
