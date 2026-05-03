import os
import pyzim

with pyzim.Zim.open("./gramwiki_2025-08-full.zim") as zim:
    print('=== CSS ===')
    for e in zim.iter_entries():
        if "only=styles" in e.url:
            print(e.url)