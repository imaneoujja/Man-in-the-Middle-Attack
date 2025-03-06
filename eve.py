from sys import argv
from common import *
from const import *
import os

flags = {'--relay', '--break-heart', '--custom'}
if len(argv) > 1 and argv[1] in flags:
    alt_buffer = 'aliceAltBuffer'
    dlg = Dialog('print')

    # Connect to Alice's socket as "Bob"
    fake_bob = 'bob'
    alice_socket, alice_aes = setup(fake_bob, BUFFER_DIR, BUFFER_FILE_NAME)
    os.rename(BUFFER_DIR + BUFFER_FILE_NAME, BUFFER_DIR + alt_buffer)
    dlg.think("Eve thinks: \"Nice, getting there...\"")

    # Connect to Bob's socket as "Alice"
    fake_alice = 'alice'
    bob_socket, bob_aes = setup(fake_alice, BUFFER_DIR, BUFFER_FILE_NAME)
    dlg.think("Eve thinks: \"Hehe, it's working!\"")

    # Receive and handle message from Bob
    msg_from_bob = receive_and_decrypt(bob_aes, bob_socket)
    dlg.chat(f'Bob slurred: "{msg_from_bob}"')

    if argv[1] == '--relay':
        to_send = msg_from_bob
    elif argv[1] == '--break-heart':
        to_send = "I hate you!"
    elif argv[1] == '--custom':
        dlg.prompt("Input what you would like Bob to say to Alice")
        to_send = input()

    # Send to Alice
    encrypt_and_send(to_send, alice_aes, alice_socket)
    dlg.info("Message sent to Alice!")

    # Receive and handle message from Alice
    msg_from_alice = receive_and_decrypt(alice_aes, alice_socket)
    dlg.chat(f'Alice slurred: "{msg_from_alice}"')

    if argv[1] == '--relay':
        to_send = msg_from_alice
    elif argv[1] == '--break-heart':
        to_send = "You broke my heart..."
    elif argv[1] == '--custom':
        dlg.prompt("Input what you would like Alice to say to Bob")
        to_send = input()

    # Send to Bob
    encrypt_and_send(to_send, bob_aes, bob_socket)
    dlg.info("Message sent to Bob!")

    # Close connections
    tear_down(bob_socket, BUFFER_DIR, BUFFER_FILE_NAME)
    tear_down(alice_socket, BUFFER_DIR, alt_buffer)
