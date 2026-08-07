import sys
import re
import base64
from Crypto.Cipher import AES

def fix_padding(b64_string):
    """Adds missing padding to a Base64 string if needed."""
    return b64_string + '=' * (-len(b64_string) % 4)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 decrypt.py <path_to_app.js>")
        sys.exit(1)

    # 1. Read the app.js file
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. Automatically find the hex-style variable strings using regex
    # Matches patterns like: _0x16829b = "string" or _0x16829b="string"
    key_match = re.search(r'_0x16829b\s*=\s*["\']([^"\']+)["\']', content)
    iv_match = re.search(r'_0xd4dcec\s*=\s*["\']([^"\']+)["\']', content)
    
    # Try to find the large ciphertext block (either variable _0x5189ce or the raw text block)
    cipher_match = re.search(r'_0x5189ce\s*=\s*["\']([^"\']+)["\']', content)

    if not key_match or not iv_match:
        print("[-] Error: Could not find key (_0x16829b) or IV (_0xd4dcec) in the file.")
        sys.exit(1)

    # 3. Extract and sanitize strings
    key_b64 = fix_padding(key_match.group(1).strip())
    iv_b64 = fix_padding(iv_match.group(1).strip())
    
    if cipher_match:
        ciphertext_b64 = fix_padding(cipher_match.group(1).strip())
    else:
        # Fallback: if the big string pasted is loose in the file, look for any massive string
        large_str_match = re.search(r'["\']([A-Za-z0-9+/]{100,}=*)["\']', content)
        if large_str_match:
            ciphertext_b64 = fix_padding(large_str_match.group(1).strip())
        else:
            print("[-] Error: Could not find the encrypted ciphertext block.")
            sys.exit(1)

    print("[+] Successfully extracted all variables.")

    # 4. Decode base64 layers into raw bytes
    try:
        key = base64.b64decode(key_b64)
        iv = base64.b64decode(iv_b64)
        raw_payload = base64.b64decode(ciphertext_b64)
    except Exception as e:
        print(f"[-] Base64 decoding failed: {e}")
        sys.exit(1)

    # 5. AES-GCM splitting: The last 16 bytes are always the GCM authentication tag
    ciphertext = raw_payload[:-16]
    tag = raw_payload[-16:]

    # 6. Decrypt
    try:
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        print("\n--- DECRYPTED CODE START ---\n")
        print(decrypted_bytes.decode('utf-8'))
        print("\n--- DECRYPTED CODE END ---")
    except Exception as e:
        print(f"[-] AES Decryption failed (bad key/tag/IV): {e}")

if __name__ == "__main__":
    main()
