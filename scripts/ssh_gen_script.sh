#!bin/bash
# Run with root privileges

echo | ssh-keygen -t ed25519 -C "$1" -P '' # -P for passphrase
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub