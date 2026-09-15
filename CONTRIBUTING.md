# Loyihaga Hissa Qo'shish Qo'llanmasi

Loyiha ochiq manbali bo'lib, uning rivojiga hissa qo'shish istagidagi har bir dasturchining taklif va o'zgarishlari mamnuniyat bilan qabul qilinadi.

---

## Hissa qo'shish bosqichlari

### 1. Xatoliklar va kamchiliklar haqida xabar berish (Issues)
- Kodda yoki interfeysda xatolik aniqlanganda GitHub Issues bo'limida yangi mavzu oching.
- Muammoni tavsiflashda xatolik yuzaga kelgan shart-sharoit, kutilgan natija va amaldagi natijani aniq ko'rsatib bering.

### 2. Yangi imkoniyatlar taklif qilish
- Loyihaga yangi modul yoki o'zgarish kiritishdan oldin uni muhokama qilish uchun Issue ochish tavsiya etiladi.

### 3. Kod orqali o'zgarish kiritish (Pull Requests)
1. Repozitoriyani shaxsiy profilingizga `Fork` qiling.
2. Yangi tarmoq (branch) yarating:
   ```bash
   git checkout -b feature/yangi-funksiya
   ```
3. O'zgarishlarni kiriting va zarur hollarda tegishli testlarni yozing.
4. Barcha mavjud va yangi testlar to'liq o'tishini tekshiring:
   ```bash
   python manage.py test
   ```
5. O'zgarishlarni commit qiling:
   ```bash
   git commit -m "feat: yangi funksionallik qo'shildi"
   ```
6. O'z forkingizga push qiling va asosiy repozitoriyaga `Pull Request` yuboring.

---

## Kodlash va uslub qoidalari

- Python kodi uchun PEP 8 standartlariga qat'iy rioya qiling.
- Shablonlar Bootstrap 5 va moslashuvchan dizayn qoidalariga muvofiq bo'lishi lozim.
- Commit xabarlari Conventional Commits formatida (masalan: `feat: ...`, `fix: ...`, `docs: ...`, `test: ...`) yozilishi tavsiya etiladi.
- Har qanday yangi funksiya yoki xatolik tuzatmasi tegishli testlar bilan ta'minlanishi shart.
