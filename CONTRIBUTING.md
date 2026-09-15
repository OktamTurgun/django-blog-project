# Loyihaga Hissa Qo'shish (Contributing Guide)

`django-blog-project` loyihasiga qiziqish bildirganingiz uchun tashakkur! Loyihani rivojlantirish bo'yicha taklif va hissalaringiz mamnuniyat bilan qabul qilinadi.

---

## 🚀 Qanday hissa qo'shish mumkin?

1. **Xatolar haqida xabar berish (Issues):**
   - Agar biror xatolik topsangiz, iltimos GitHub Issues bo'limida yangi issue oching va xatolikni qayta hosil qilish bosqichlarini tasvirlab bering.

2. **Yangi imkoniyatlar taklif qilish:**
   - Yangi g'oya yoki taklifingiz bo'lsa, avval uni muhokama qilish uchun issue ochishni tavsiya qilamiz.

3. **Kod orqali hissa qo'shish (Pull Requests):**
   - Repozitoriyani `Fork` qiling.
   - Yangi funksionallik uchun alohida tarmoq yarating (`git checkout -b feature/yangi-funksiya`).
   - O'zgarishlarni kiriting va testlar yozing.
   - Barcha mavjud va yangi testlar o'tishiga ishonch hosil qiling (`python manage.py test`).
   - Tarmoqni o'z forkingizga push qiling va `Pull Request` oching.

---

## 🧪 Testlar

Har qanday o'zgarishdan so'ng barcha testlarni tekshirish majburiydir:

```powershell
python manage.py test
```

Tizim sozlamalarini tekshirish:

```powershell
python manage.py check
```

---

## 📜 Kodlash Standartlari
- PEP 8 qoidalariga rioya qiling.
- Shablonlar Bootstrap 5 va responsive dizayn qoidalariga mos bo'lishi kerak.
- Commit xabarlarini tushunarli va mazmunli qilib yozing (masalan: `feat: ...`, `fix: ...`, `docs: ...`).
