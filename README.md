# คนแบกโคม

นิทานสองนาทีแบบ interactive — 7 ทางแยก แล้วสรุปออกมาเป็น "นิทาน" หนึ่งเรื่องตามทางที่เลือกจริง
สร้างด้วย Claude Design canvas (`.dc.html` + dc-runtime)

## รันในเครื่อง

```bash
python3 -m http.server 8777
```

แล้วเปิด <http://localhost:8777/คนแบกโคม.dc.html>

ต้องเสิร์ฟผ่าน http เท่านั้น — เปิดไฟล์ตรงๆ ด้วย `file://` ไม่ได้ เพราะ dc-runtime
โหลด React/Babel และอ่าน template ผ่าน fetch

## โครงไฟล์

| ไฟล์ | คืออะไร |
|---|---|
| `คนแบกโคม.dc.html` | ทั้งงานอยู่ในไฟล์นี้ — template (`<x-dc>`) + logic (`DCLogic`) |
| `support.js` | dc-runtime (generated) โหลด React 18 + Babel จาก unpkg เอง |
| `image-slot.js` | คอมโพเนนต์ `<image-slot>` จาก starter (generated) |
| `art/` | ภาพประกอบ 7 ฉาก + พื้นหลังกลางคืน + โลโก้ mindfull |
| `tools/set-gate-key.py` | เปลี่ยนรหัสหน้า lock |

`support.js` กับ `image-slot.js` เป็นไฟล์ generated — อย่าแก้มือ

## โครงสร้างเนื้อเรื่อง

- `SCENES` — 7 ฉาก แต่ละฉากมี 4 ตัวเลือก แต่ละตัวเลือกถ่วงน้ำหนัก 5 แกน:
  `self` / `other` / `give` / `endure` / `change`
- `TALES` — นิทาน 7 แบบ แต่ละแบบมีเวกเตอร์ประจำตัว จับคู่ด้วย cosine similarity
  ถ้าคะแนนเบาเกินไปหรือสองอันดับแรกใกล้กันมาก จะตกไปที่ "นิทานที่ยังเล่าไม่จบ"
- `pattern()` — อ่านพฤติกรรมจริงจากลำดับที่เลือก (เลือกเพื่อตัวเองกี่ครั้ง, เดินคนเดียวกี่ครั้ง,
  เลือกไม่มองกี่ครั้ง) แยกจากผลนิทาน

## ถ้าจะ deploy

host ไฟล์ static ทั่วไป (Cloudflare Pages / Netlify) เสิร์ฟ **ทุกไฟล์ใน repo** ต่อให้ repo เป็น private
แปลว่า `README.md` กับ `tools/` จะเปิดดูได้จากอินเทอร์เน็ตถ้าไม่กัน ในรีโปมี `_redirects` กันไว้ให้แล้ว
(ใช้ได้ทั้ง Cloudflare Pages และ Netlify)

ถ้าย้าย host เจ้าอื่นที่ไม่รู้จัก `_redirects` ให้ย้ายไฟล์ที่จะเสิร์ฟจริงไปไว้ใน subdirectory
แล้วตั้งอันนั้นเป็น publish directory แทน — กันได้แน่นอนกว่า

ต้องเป็น `https://` ด้วย ไม่งั้นหน้า lock ใช้ไม่ได้ (`crypto.subtle` ต้องการ secure context)

## ที่ยังค้าง

- กด Enter ในช่องรหัสไม่ submit ต้องคลิกปุ่ม "ปลดล็อก" (`onSubmit` ไม่ยิงใน dc-runtime)
- console ขึ้น `ERR_INVALID_URL` — มาจาก `image-slot.js` หา sidecar ที่ไม่มีนอก omelette runtime ไม่กระทบการใช้งาน
