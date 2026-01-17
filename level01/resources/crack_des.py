"""Level01 DES Password Hash Cracker"""

import subprocess


def hash_password_des(password, salt):
    """Hash password using DES crypt via system Perl"""
    try:
        perl_code = f"print crypt('{password}', '{salt}')"
        result = subprocess.run(
            ['perl', '-e', perl_code],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return None


def crack_des_hash(target_hash, wordlist_file=None):
    """Attempt to crack a DES crypt hash using dictionary attack"""
    salt = target_hash[:2]

    common_passwords = [
        "abcdefg", "password", "123456", "admin", "test", "user", "root",
        "flag01", "level01", "level", "flag", "snowcrash", "crash", "snow",
        "password123", "admin123", "test123", "qwerty", "abc123",
        "login", "access", "welcome", "letmein", "monkey", "dragon",
        "master", "shadow", "iloveyou", "superman", "batman",
        "bonnie", "clyde", "nottoohardhere",
    ]

    print("[*] Attempting DES hash cracking")
    print(f"[*] Target hash: {target_hash}")
    print(f"[*] Salt: {salt}\n")

    print("[*] Phase 1: Testing common passwords...")
    for pwd in common_passwords:
        pwd_truncated = pwd[:8]
        hashed = hash_password_des(pwd_truncated, salt)

        if hashed == target_hash:
            print(f"[+] PASSWORD FOUND: {pwd}")
            return pwd

        print(f"  [-] Trying: {pwd}")

    if wordlist_file:
        print(f"\n[*] Phase 2: Testing wordlist from {wordlist_file}...")
        try:
            with open(wordlist_file, 'r') as f:
                count = 0
                for line in f:
                    word = line.strip()

                    if len(word) > 8:
                        word = word[:8]

                    hashed = hash_password_des(word, salt)

                    if hashed == target_hash:
                        print(f"\n[+] PASSWORD FOUND: {word}")
                        return word

                    count += 1
                    if count % 10000 == 0:
                        print(f"  [-] Tested {count} passwords...")

                print(f"[-] Password not found (tested {count} words)")

        except FileNotFoundError:
            print(f"[-] Wordlist file not found: {wordlist_file}")

    return None


def analyze_hash(hash_string):
    """Analyze a DES crypt hash"""
    print("DES Crypt Hash Analysis")
    print(f"Hash: {hash_string}")
    print(f"Length: {len(hash_string)} characters")
    print(f"Salt: {hash_string[:2]}")
    print(f"Hash part: {hash_string[2:]}")
    print("\nHash Format Details:")
    print("- Algorithm: DES (Data Encryption Standard)")
    print("- Format: Traditional Unix crypt")
    print("- Max password length: 8 characters")
    print("- Effective key strength: ~70 bits (with salt)")
    print("- Security: WEAK - easily cracked with modern hardware")


def main():
    flag01_hash = "42hDRfypTqqnw"

    analyze_hash(flag01_hash)

    print("[*] Starting dictionary attack...\n")

    password = crack_des_hash(
        flag01_hash,
        wordlist_file="/usr/share/dict/words"
    )

    if password:
        print("SUCCESS!")
        print(f"Hash: {flag01_hash}")
        print(f"Password: {password}")
        print("\nNext steps:")
        print(f"  su flag01")
        print(f"  Password: {password}")
        print(f"  getflag")
    else:
        print("\n[-] Password not found in common passwords or wordlist")
        print("[*] Try expanding the wordlist or using specialized tools:")
        print("    - john the ripper: john --format=crypt hash.txt")
        print("    - hashcat: hashcat -m 1500 hash wordlist.txt")


if __name__ == "__main__":
    main()
