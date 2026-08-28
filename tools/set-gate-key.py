#!/usr/bin/env python3
"""
Set the lock-screen passphrase for คนแบกโคม.dc.html.

The passphrase is never written to disk, never printed, and never leaves this
machine. Only a fresh random salt and the PBKDF2-SHA256 digest are written into
the GATE block of the page.

    python3 tools/set-gate-key.py

Run it again any time to rotate the passphrase.
"""

import getpass
import hashlib
import os
import re
import secrets
import sys

ITER = 250_000
PAGE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "คนแบกโคม.dc.html")

BLOCK = re.compile(
    r'(const GATE = \{\s*\n)'
    r'\s*salt: "[0-9a-f]*",\s*\n'
    r'\s*hash: "[0-9a-f]*",\s*\n'
    r'\s*iter: \d+\s*\n'
    r'(\};)'
)


def main():
    if not os.path.exists(PAGE):
        sys.exit(f"cannot find {PAGE}")

    src = open(PAGE, encoding="utf-8").read()
    if not BLOCK.search(src):
        sys.exit("could not find the GATE block in the page — was it edited by hand?")

    first = getpass.getpass("รหัสใหม่ (ไม่แสดงบนจอ): ")
    if len(first.strip()) < 12:
        sys.exit("สั้นเกินไป — ขอ 12 ตัวขึ้นไป (ยาวสำคัญกว่าอักขระพิเศษ)")
    if first.strip().lower() != first.strip():
        print("หมายเหตุ: หน้า lock เทียบแบบ lowercase — ตัวพิมพ์ใหญ่จะไม่ถูกนับ")
    if getpass.getpass("พิมพ์ซ้ำอีกครั้ง: ") != first:
        sys.exit("ไม่ตรงกัน ยกเลิก")

    key = first.strip().lower().encode("utf-8")
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", key, salt, ITER, dklen=32)

    new = (
        r'\1'
        f'  salt: "{salt.hex()}",\n'
        f'  hash: "{digest.hex()}",\n'
        f'  iter: {ITER}\n'
        r'\2'
    )
    open(PAGE, "w", encoding="utf-8").write(BLOCK.sub(new, src, count=1))

    print("\nเรียบร้อย — เขียน salt + digest ใหม่ลง คนแบกโคม.dc.html แล้ว")
    print("ตัวรหัสไม่ได้ถูกบันทึกไว้ที่ไหนทั้งสิ้น จำเองหรือเก็บใน password manager")
    print("\nอย่าลืม:  git add -A && git commit -m 'Rotate gate passphrase'")


if __name__ == "__main__":
    main()
