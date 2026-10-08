# Man-in-the-Middle Attack on Diffie-Hellman

Alice and Bob chat over a channel encrypted with a Diffie-Hellman key exchange and AES. Because the key exchange is not authenticated, Eve can sit between them, set up a separate "secure" channel with each side, and then read, relay or rewrite every message without either of them noticing.

Course assignment, built with Marwa Chiguer.

## Demo

Bob sends "I love you!". Eve, running with `--break-heart`, rewrites the messages in both directions:

```
$ python eve.py --break-heart
Hi Bob! Welcome to SuperSecureChat!
Established secure channel!
Eve thinks: "Nice, getting there..."
Hi Alice! Welcome to SuperSecureChat!
Established secure channel!
Eve thinks: "Hehe, it's working!"
Bob slurred: "I love you!"
Message sent to Alice!
Alice slurred: "You broke my heart..."
Message sent to Bob!
```

On Alice's side, the message she receives is `Bob said: "I hate you!"`. Both Alice and Bob still see "Established secure channel!".

## How it works

- **The chat:** Alice and Bob agree on a shared secret with Diffie-Hellman over a 2048-bit prime group. They derive a 256-bit AES key from it with SHA-256 and encrypt each message with AES in CTR mode.
- **The weakness:** nothing in the exchange proves who sent a public share. Whoever answers on the channel gets a valid shared key.
- **The attack (`eve.py`):** Eve connects to Alice pretending to be Bob, and opens a new endpoint where the real Bob connects thinking it is Alice. She runs a separate key exchange with each of them, so she holds both keys. Every message is decrypted with one key and re-encrypted with the other.
- **Three modes:**
  - `--relay` forwards messages unchanged (silent eavesdropping).
  - `--break-heart` replaces them with hostile ones.
  - `--custom` lets you type what each side receives.

The fix is to authenticate the key exchange, for example by signing the public shares or using certificates, as TLS does.

## Tech stack

Python, Diffie-Hellman key exchange, AES-256-CTR (`pyaes`), SHA-256, Unix domain sockets.

## How to run

Requires macOS or Linux (the processes talk through a Unix socket in `/tmp`).

```bash
pip install -r requirements.txt
```

Then start each party in its own terminal, in this order:

```bash
python alice.py
python eve.py --break-heart     # or --relay / --custom
python bob.py
```

To see the normal, unattacked conversation, run only `alice.py` and then `bob.py`.

## Files

| File | Role |
|------|------|
| `alice.py`, `bob.py` | The two chat participants |
| `eve.py` | The man-in-the-middle attacker |
| `diffie_hellman.py` | Group parameters and key exchange |
| `symmetric.py` | AES-CTR encryption with SHA-256 key derivation |
| `util.py`, `common.py` | Key exchange, encrypted send/receive, session setup |
| `simple_sockets.py` | Unix socket transport |
| `dialog.py`, `const.py` | Coloured terminal output, messages and settings |
