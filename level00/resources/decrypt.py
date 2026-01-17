"""Level00 Caesar Cipher Decoder"""

def caesar_decrypt(text, shift):
    """Decrypt text using Caesar cipher with given shift"""
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')

            shifted = (ord(char) - base - shift) % 26
            result += chr(base + shifted)
        else:
            result += char

    return result


def brute_force_caesar(encrypted_text):
    """Try all 26 possible Caesar cipher shifts"""
    results = {}
    for shift in range(26):
        decrypted = caesar_decrypt(encrypted_text, shift)
        results[shift] = decrypted
    return results


def main():
    encoded_password = "cdiiddwpgswtgt"

    print("Level00 - Caesar Cipher Decoder")
    print(f"\nEncoded password: {encoded_password}\n")

    print("Method 1: Direct decryption with shift 15")
    known_shift = 15
    decrypted = caesar_decrypt(encoded_password, known_shift)
    print(f"Shift: {known_shift}")
    print(f"Decrypted: {decrypted}")

    print("\n\nMethod 2: Brute force all possible shifts")
    all_attempts = brute_force_caesar(encoded_password)

    for shift in range(26):
        result = all_attempts[shift]
        marker = " <-- CORRECT PASSWORD" if shift == 15 else ""
        print(f"Shift {shift:2d}: {result}{marker}")

    print(f"Caesar Cipher Shift: 15")
    print(f"Encrypted: {encoded_password}")
    print(f"Decrypted: {decrypted}")
    print(f"\nPassword for flag00: {decrypted}")


if __name__ == "__main__":
    main()
