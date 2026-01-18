"""Level02 PCAP Telnet Password Extractor"""

import os

try:
    import dpkt
    HAS_DPKT = True
except ImportError:
    HAS_DPKT = False


def parse_pcap(pcap_file):
    """Parse PCAP file and extract TCP payloads using dpkt"""
    if not HAS_DPKT:
        raise ImportError("dpkt library required. Install with: pip install dpkt")

    packets_data = []
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            try:
                eth = dpkt.ethernet.Ethernet(buf)
                if isinstance(eth.data, dpkt.ip.IP):
                    ip = eth.data
                    if isinstance(ip.data, dpkt.tcp.TCP):
                        tcp = ip.data
                        if tcp.data:
                            packets_data.append(tcp.data)
            except (dpkt.UnpackError, AttributeError):
                continue

    return packets_data


def extract_password(payloads):
    """Extract password from telnet session"""
    stream = b''.join(payloads)

    clean_stream = bytearray()
    i = 0
    while i < len(stream):
        if stream[i] == 0xff and i + 1 < len(stream):
            i += 2
            continue
        clean_stream.append(stream[i])
        i += 1

    text = []
    for byte in clean_stream:
        if byte == 0x7f:
            if text:
                text.pop()
        elif byte >= 0x20 and byte < 0x7f:
            text.append(chr(byte))
        elif byte in (0x0a, 0x0d):
            if text:
                text.append('\n')

    result = ''.join(text)
    return result


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pcap_file = os.path.join(script_dir, 'level02.pcap')

    print("Level02 - PCAP Telnet Password Extractor")
    print(f"\n[*] Analyzing PCAP file: {pcap_file}\n")

    try:
        payloads = parse_pcap(pcap_file)
        print(f"[+] Extracted {len(payloads)} TCP payloads")

        result = extract_password(payloads)

        print("Extracted Telnet Session:")
        print(result)

        lines = result.split('\n')
        for i, line in enumerate(lines):
            if 'Password:' in line:
                password = line.split('Password:')[-1].strip()
                if password:
                    print(f"[+] EXTRACTED PASSWORD: {password}")
                    break

    except FileNotFoundError:
        print(f"[-] File not found: {pcap_file}")
    except Exception as e:
        print(f"[-] Error: {e}")


if __name__ == "__main__":
    main()
