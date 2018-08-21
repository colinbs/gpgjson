# GPG key to JSON

This script converts the outputs of the `gpg --list-keys` command to JSON and prints it to the console it into a file.

## Usage

If you want to convert all keys of the key-ring, run the script with `-a`

```bash
python gpgjson.py -a
```

If you want to only convert a single key, pass the whole fingerprint to the script
```bash
python gpgjson.py ABCDEF0123456789ABCDEF01234567890123456789
```

If the script is invoked with the `-o <outfile>` option, an output file with the JSON contents is created.

## Documentation

The code is documented with [Literate](https://github.com/zyedidia/Literate). To create a
HTML documentation simply install Literate, navigate into the lit/ directory and run
```bash
lit gpgjson.lit
```

Literate also generates the python script. It is identical to the script in the root
directory. So use this one in case you don't want to install Literate.

## Example

Example output of the script:

```json
[
    {
        "pub0": {
            "alg": "rsa4096",
            "cdate": "2016-12-24",
            "flags": "SC",
            "exdate": "2018-03-29",
            "uid0": {
                "trust": "expired",
                "name": "Alice",
                "email": "<alice@example.com>"
            }
        },
        "sub0": {},
        "fprint": "ABCDEF0123456789ABCDEF01234567890123456789"
    },
    {
        "pub1": {
            "alg": "rsa4096",
            "cdate": "2017-01-01",
            "flags": "SC",
            "exdate": "2018-01-01",
            "uid0": {
                "trust": "ultimate",
                "name": "Bob",
                "email": "<bob@example.com>"
            }
        },
        "sub1": {
            "alg": "rsa2048",
            "cdate": "2018-03-26",
            "flags": "E",
            "exdate": "2019-03-26"
        },
        "fprint": "01234567890123456789ABCDEFABCDEF012345CDEF"
    }
]
```
