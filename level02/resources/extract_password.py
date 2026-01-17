"""Level02 PCAP Telnet Password Extractor"""

import struct
import os


def parse_pcap(pcap_file):
    """Parse PCAP file and extract TCP payloads"""
    with open(pcap_file, 'rb') as f:
        data = f.read()

    packets_data = []
    pos = 24

    while pos < len(data) - 16:
        if pos + 16 > len(data):
            break

        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[pos:pos+16])
        pos += 16

        if incl_len == 0 or incl_len > 65535 or pos + incl_len > len(data):
            break

        packet = data[pos:pos+incl_len]
        pos += incl_len

        if len(packet) < 34:
            continue

        ip_version_ihl = packet[14]
        ihl = (ip_version_ihl & 0x0f) * 4

        if len(packet) < 14 + ihl + 20:
            continue

        tcp_start = 14 + ihl
        data_offset_res = packet[tcp_start + 12]
        tcp_header_len = ((data_offset_res >> 4) & 0xf) * 4

        payload_start = tcp_start + tcp_header_len
        if len(packet) > payload_start:
            payload = packet[payload_start:]
            if payload:
                packets_data.append(payload)

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
