#!/usr/bin/env python3
"""Firma client/custom.json y genera custom.txt para el cliente Esmeralab.

Formato esperado por RustDesk (src/common.rs read_custom_client):
base64( firma_ed25519(64 bytes) + json ), el mismo "signed message" de libsodium.

Uso: sign_custom.py [custom.json] [custom.txt]
Llave privada: variable CLIENT_SIGNING_KEY (base64 de la semilla de 32 bytes) o
el archivo ~/.config/esmeralab-rustdesk/client-signing.key. Nunca va al repo.
"""
import base64, json, os, sys
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "custom.json")
dst = sys.argv[2] if len(sys.argv) > 2 else "custom.txt"
seed_b64 = os.environ.get("CLIENT_SIGNING_KEY") or open(
    os.path.expanduser("~/.config/esmeralab-rustdesk/client-signing.key")).read()
key = Ed25519PrivateKey.from_private_bytes(base64.b64decode(seed_b64.strip()))
msg = json.dumps(json.load(open(src, encoding="utf-8")), separators=(",", ":")).encode()
open(dst, "w").write(base64.b64encode(key.sign(msg) + msg).decode())
print("escrito", dst)
