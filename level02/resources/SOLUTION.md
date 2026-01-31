# Level02 Solution

## Starting VM

```bash
qemu-system-x86_64 -m 2048 -cdrom ./SnowCrash.iso -boot d -net nic,model=virtio -net user,hostfwd=tcp::4242-:4242
```

## Objective
Extract password from network traffic and access the flag02 account.

## Vulnerability
Plain-text telnet traffic in PCAP file allows extraction of login credentials.

## Exploitation

### Step 1: Retrieve the PCAP File

The flag02-owned PCAP file can be copied from the VM:

```bash
sshpass -p "f2av5il02puano7naaf6adaaf" scp -P 4242 level02@localhost:/home/user/level02/level02.pcap .
```

### Step 2: Parse PCAP to Extract TCP Payloads

**Method 1: Using `scapy` Python library**

Extract telnet packets directly from PCAP:

```bash
python3 << 'EOF'
from scapy.all import rdpcap, TCP
pkts = rdpcap('level02.pcap')
for pkt in pkts:
    if TCP in pkt and pkt[TCP].payload:
        print(pkt[TCP].payload.load)
EOF
```

Or use Wireshark to view telnet follow stream (GUI method):
```bash
wireshark level02.pcap
# Follow TCP Stream (right-click on packet) to view telnet session
```

**Method 2: Using `tcpdump` to Extract Packets**

```bash
tcpdump -r level02.pcap -A | grep -E '[a-zA-Z0-9]' | head -30
# Look for telnet session data with login attempts
```

### Step 3: Decode Telnet Session with Backspace Handling

The PCAP contains a telnet login sequence with backspace characters (0x7F).

**Telnet Packet Structure:**
- `0xFF` = telnet control code prefix (skip)
- `0x7F` = backspace character (DEL)
- `0x0A`, `0x0D` = newline characters

**Decode Algorithm:**
1. Remove telnet control sequences (0xFF bytes)
2. Process backspace: when 0x7F is encountered, remove the previous character
3. Extract printable ASCII characters

**Reconstructed Password from PCAP:**
```
ft_wandr -> [backspace x3] -> ft_w
ft_w + NDRel -> ft_wNDRel
ft_wNDRel -> [backspace x1] -> ft_wNDRe
ft_wNDRe + L0L -> ft_wNDReL0L
```

**Password:** `ft_waNDReL0L`

### Step 4: Access flag02 Account via SSH

```bash
sshpass -p "ft_waNDReL0L" ssh -o StrictHostKeyChecking=no -p 4242 flag02@localhost getflag
```

### Step 5: Retrieve the Flag Token

```
Check flag.Here is your token : kooda2puivaav1idi4f57q8iq
```

## Security Flaws

1. **Plain-text Protocol**: Telnet transmits all data unencrypted
2. **Network Sniffing**: Captured traffic reveals complete login credentials
3. **No Encryption**: Password fully visible in packet capture
4. **Backspace Handling**: Keystroke data includes timing and editing information

## Answer

- **Flag02 Password**: `ft_waNDReL0L`
- **Level02 Token**: `kooda2puivaav1idi4f57q8iq`
- **Vulnerability Type**: Network traffic interception via unencrypted protocol
