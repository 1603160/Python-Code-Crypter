# Python Code Crypter
![image](https://github.com/user-attachments/assets/f2fa80b0-679d-4ab9-a87c-4ba23c5e5248)


A sophisticated Python code obfuscation tool that combines compression, AES encryption, and multiple encoding techniques to protect your Python scripts.

## Features

- **Multi-layer obfuscation**: Compression + AES-256 encryption + encoding
- **Multiple encoding options**: Base85, Base64, or Hex encoding
- **Payload fragmentation**: Splits payload into randomized chunks
- **Standalone output**: Generates self-contained loader files
- **Cross-platform**: Works on any system with Python 3.6+

## Installation

No installation required. Just ensure you have the dependencies:

```bash
pip install pycryptodome
```

## Usage

### Basic Obfuscation

```bash
python crypter.py -e input.py -o output.py
```

### Command Line Options

| Option        | Description                          |
|---------------|--------------------------------------|
| `-e`, `--encrypt` | Input Python file to obfuscate (required) |
| `-o`, `--output`  | Output file name (optional)          |

### Advanced Examples

1. **Obfuscate and display in console:**
   ```bash
   python crypter.py -e myscript.py
   ```

2. **Obfuscate and save to file:**
   ```bash
   python crypter.py -e myscript.py -o protected.py
   ```

## Technical Details

### Obfuscation Process

1. **Compression**: Uses zlib to compress the source code
2. **Encryption**:
   - Generates random 256-bit AES key
   - Uses CBC mode with random IV
   - PKCS7 padding
3. **Encoding** (randomly selected):
   - Base85 (ASCII85)
   - Base64
   - Hexadecimal
4. **Fragmentation**:
   - Splits payload into chunks (40-60 chars each)
   - Randomizes chunk sizes

### Loader Structure

The generated loader contains:
- Decoding logic for all supported formats
- AES decryption routine
- Decompression function
- Error handling
- Automatic execution

## Disclaimer

**IMPORTANT LEGAL NOTICE**

1. **Intended Use**: This tool is designed for legitimate code protection purposes only, such as:
   - Protecting intellectual property
   - Securing sensitive configuration data
   - Anti-tampering mechanisms for authorized software

2. **Prohibited Uses**: Strictly forbidden to use this tool for:
   - Malware creation or distribution
   - Bypassing license controls of commercial software
   - Any illegal or unethical activities
   - Obfuscating malicious scripts or payloads

3. **No Warranty**: This software is provided "as-is" without any warranties of any kind, express or implied.

4. **Legal Compliance**: Users are solely responsible for ensuring their use complies with all applicable laws in their jurisdiction, including:
   - Copyright laws
   - Digital Millennium Copyright Act (DMCA)
   - Computer Fraud and Abuse Act (CFAA)
   - Local cybersecurity regulations

5. **Ethical Considerations**: By using this tool, you agree to:
   - Use it only on code you own or have permission to modify
   - Not use it to hide malicious behavior
   - Assume all liability for improper use

6. **Security Researchers**: If using for defensive security research, ensure you have proper authorization before testing on systems you don't own.

## Security Notes

- Uses cryptographically strong random numbers
- Proper IV usage for AES-CBC
- Includes integrity checks
- Not immune to reverse engineering - consider this as obfuscation, not true encryption

## Limitations

- Increases code size significantly
- Not compatible with compiled Python (py2exe, PyInstaller)
- May trigger AV scanners due to encryption patterns

## License

MIT License - Free for personal and commercial use

## Contributing

Pull requests welcome. For major changes, please open an issue first to discuss proposed changes.
