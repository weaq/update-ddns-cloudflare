# update-ddns-cloudflare
update your public IP to cloudflare.com


# 🧠 สรุปสั้น ๆ

* ใช้ **API Token ** ❌ ไม่ใช้ Global API Key
* Template: **Edit zone DNS**
* Scope: `weaq.cc` เฉพาะ Domain เท่านั้น

---

# 🔐 วิธีสร้าง API Token (อัปเดต DNS ได้)

## 🧭 เข้าเมนู

👉 [https://dash.cloudflare.com/profile/api-tokens](https://dash.cloudflare.com/profile/api-tokens)

หรือกดตามนี้:

* มุมขวาบน → คลิกโปรไฟล์
* ไปที่ **My Profile**
* แท็บ **API Tokens**

---

# 🚀 ขั้นตอนสร้าง

## 1. กดปุ่ม

👉 **Create Token**

---

## 2. เลือก Template (ง่ายสุด)

จะมีหลายแบบ ให้เลือก:

👉 **Edit zone DNS** ✅ (แนะนำ)

กด **Use template**

---

## 3. ตั้งค่า Scope (จุดที่คนพลาดบ่อย)

ในหน้า config:

### 🔹 Permissions

ให้เป็นแบบนี้:

```
Zone → DNS → Edit
```

---

### 🔹 Zone Resources

เลือก:

```
Include → Specific zone → weaq.cc
```

** อย่าเลือก “All zones” ถ้าไม่จำเป็น **

---

## 4. กดต่อ

* Continue to summary
* Create Token

---

## 5. ⚠️ Copy Token ทันที

จะได้ string ประมาณนี้:

```bash id="cgb4ny"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

👉 **จะโชว์ครั้งเดียว ถ้าหายต้องสร้างใหม่**

---

# ✅ เอาไปใช้ใน script

แทนที่:

```python id="u7n2lq"
CF_API_TOKEN = "YOUR_API_TOKEN"
```

---

# 🔥 ทดสอบว่าใช้ได้ไหม

รัน:

```
python3 ddns.py
```

ถ้าได้แบบนี้คือผ่าน:

```
✅ Updated weaq.cc -> x.x.x.x
หรือ
✅ IP unchanged. Skip update.
```

---

# ตั้ง auto run

## ใช้ PM2:

pm2 start ddns.py --name ddns --interpreter python3 --cron "*/5 * * * *"

# หรือ cron ปกติ

crontab -e

*/5 * * * * python3 /path/ddns.py >> /var/log/ddns.log 2>&1