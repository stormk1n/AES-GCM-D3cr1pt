Copy the ./Sample\ JS\ Snippets/obfuscated.js code and crack it with [webcrack](https://webcrack.netlify.app/)

once cracked, notice the file is encrypted with AES, tried decoding it at runtime as the browser parsed it but no luck there, same with cyberchef.

Save the cracked code to a file, and spin up a virtual environment then install pycryptodome with;
```bash
python3 -m venv pycrypto && \
source pycrypto/bin/activate && \
pip install pycryptodome
```
Now, using the d3cr1pt.py script alongside the file, as
```bash
python3 d3cr1pt.py app.js | tee debuff.js
``` 

# Side project caused by a minor derail on [HTB - Cohort lab](https://www.hackthebox.com/machines/Cohort) 