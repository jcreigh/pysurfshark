# pysurfshark

A python interface to Surfshark's API

1) There aren't any checks
2) It's messy
4) I'm not even sure I can name the project pysurfshark, but here we are

Nothing is set in stone, don't rely on this, etc

## Wireguard

I mainly made this to generate Wireguard configs for Linux, since the official client doesn't support it

Just run `generate_wireguard_config.py`, follow the prompts, and then fill out the config the rest of the way

This script assumes a basic understanding of Wireguard. Review the following if you are unsure:
* [Wireguard quickstart](https://www.wireguard.com/quickstart/)
* [wg-quick(8) man page](https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8)
