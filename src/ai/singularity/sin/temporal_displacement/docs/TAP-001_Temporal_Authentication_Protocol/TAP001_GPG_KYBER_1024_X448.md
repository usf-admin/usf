# GPG Kyber 1024 (X448)

## 1. Create Keys

```bash
gpg --full-generate-key

Choose: ECC and Kyber
Choose: Kyber 1024 (X448)
Choose: 0
Enter name
Enter email
Enter comment
Enter passphrase

gpg --list-keys
gpg --list-sigs
gpg --check-sigs
gpg --list-sigs --with-fingerprint
gpg --list-keys --fingerprint --fingerprint
gpg --list-keys --with-colons
gpg --armor --export | gpg --list-packets
gpg --armor --export ZEEEN@TAP001.HSIE_GPG_KYBER_1024_X448 > TAP001_HSIE_GPG_KYBER_1024_X448_PUB_ZEEEN.asc
gpg --armor --export-secret-keys ZEEEN@TAP001.HSIE_GPG_KYBER_1024_X448 > TAP001_HSIE_GPG_KYBER_1024_X448_SEC_ZEEEN.asc
gpg --list-packets TAP001_HSIE_GPG_KYBER_1024_X448_PUB_ZEEEN.asc
gpg --list-packets TAP001_HSIE_GPG_KYBER_1024_X448_SEC_ZEEEN.asc

# sign-verify-encrypt
gpg --clearsign TAP001.HSIE.associated_outgoing_message.message_content.zeeen
gpg --verify TAP001.HSIE.associated_outgoing_message.message_content.zeeen.asc
gpg --encrypt --recipient ZEEEN@TAP001.HSIE_GPG_KYBER_1024_X448 TAP001.HSIE.associated_outgoing_message.message_content.zeeen.asc

# sign-then-encrypt
gpg --encrypt --sign --recipient ZEEEN@TAP001.HSIE_GPG_KYBER_1024_X448 TAP001.HSIE.associated_outgoing_message.message_content.zeeen

# decrypt-then-verify
gpg --decrypt TAP001.HSIE.associated_outgoing_message.message_content.zeeen.gpg
```
---