import sys
import zlib
import base64
import random
import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def generate_loader_code(fragments, encoding_type):
    loader_template = r'''import zlib
import base64
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def reconstruct(fragments, encoding_type):
    try:
        data = ''.join(fragments)
        
        if encoding_type == 'base85':
            decoded = base64.b85decode(data)
        elif encoding_type == 'base64':
            decoded = base64.b64decode(data)
        elif encoding_type == 'hex':
            decoded = bytes.fromhex(data)
        
        if len(decoded) < 48:
            raise ValueError("Datos insuficientes")
            
        key = decoded[:32]
        iv = decoded[32:48]
        encrypted = decoded[48:]
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        return zlib.decompress(decrypted).decode('utf-8')
    
    except Exception as e:
        print(f"[!] Error: {{str(e)}}", file=sys.stderr)
        return None

if __name__ == '__main__':
    fragments = [
''' + ',\n        '.join(f"        '{chunk}'" for chunk in fragments) + '''
    ]
    encoding_type = ''' + f"'{encoding_type}'" + '''
    
    code = reconstruct(fragments, encoding_type)
    if code:
        try:
            exec(code)
        except Exception as e:
            print(f"[!] Error de ejecución: {{str(e)}}", file=sys.stderr)
'''
    return loader_template

def obfuscate_payload(payload):
    # 1. Compresión
    compressed = zlib.compress(payload.encode('utf-8'))
    
    # 2. Generar claves AES
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(compressed, AES.block_size))
    
    # 3. Codificación (selección aleatoria)
    encoding_type = random.choice(['base85', 'base64', 'hex'])
    combined = key + iv + encrypted
    
    if encoding_type == 'base85':
        encoded = base64.b85encode(combined).decode('ascii')
    elif encoding_type == 'base64':
        encoded = base64.b64encode(combined).decode('ascii')
    else:
        encoded = combined.hex()
    
    # 4. Fragmentación
    chunk_size = random.randint(40, 60)
    chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]
    
    return chunks, encoding_type

def process_file(input_file, output_file=None):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            payload = f.read()
        
        chunks, encoding_type = obfuscate_payload(payload)
        loader_code = generate_loader_code(chunks, encoding_type)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(loader_code)
            print(f"[+] Archivo cifrado generado: {output_file}")
        else:
            print(loader_code)
            
    except Exception as e:
        print(f"[!] Error procesando archivo: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Herramienta de ofuscación de código Python')
    parser.add_argument('-e', '--encrypt', metavar='FILE', help='Archivo Python a ofuscar')
    parser.add_argument('-o', '--output', metavar='OUTPUT', help='Archivo de salida (opcional)')
    
    args = parser.parse_args()
    
    if not args.encrypt:
        parser.print_help()
        sys.exit(1)
    
    process_file(args.encrypt, args.output)

if __name__ == '__main__':
    main()
