# Django Blog Loyihasi

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0%2B-092E20.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3.svg?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Tests](https://img.shields.io/badge/Tests-27%20Passed-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Zamonaviy veb-arxitektura tamoyillari asosida yaratilgan, foydalanuvchi profillari, ko'p bosqichli moderatsiya tartibi, tavsiyalar mexanizmi va asimmetrik jurnalistika (magazine) ko'rinishiga ega professional blog platformasi.

---

## Mundarija

- [Loyiha haqida](#loyiha-haqida)
- [Funksional imkoniyatlar](#funksional-imkoniyatlar)
- [Texnologiyalar steki](#texnologiyalar-steki)
- [Loyiha tuzilishi](#loyiha-tuzilishi)
- [O'rnatish va ishga tushirish](#ornatish-va-ishga-tushirish)
- [Avtomatlashtirilgan testlar](#avtomatlashtirilgan-testlar)
- [Konfiguratsiya](#konfiguratsiya)
- [Hissa qo'shish](#hissa-qoshish)
- [Litsenziya](#litsenziya)

---

## Loyiha haqida

Ushbu platforma mualliflar va o'quvchilar o'rtasida bilim almashish, fikr bildirish hamda sifatli maqolalarni saralash uchun qulay muhit yaratish maqsadida ishlab chiqilgan. Tizim xavfsizlik, modulli tuzilish va yuqori darajadagi foydalanuvchi tajribasini (UX) ta'minlaydi.

---

## Funksional imkoniyatlar

### 1. Foydalanuvchi va hisoblar boshqaruvi (accounts)
- **Xavfsiz autentifikatsiya:** Ro'yxatdan o'tishda majburiy email tasdig'i, avtomatik tizimga kiritish va xavfsiz chiqish.
- **Ommaviy profil sahifasi (`/accounts/profile/<username>/`):** Shaxsiy avatar, qisqacha ma'lumot (bio), veb-sayt havolasi, muallif maqolalari ro'yxati hamda umumiy ko'rishlar va tavsiyalar statistikasi.
- **Profil tahrirlash:** Avatar rasmini yuklash, ism, familiya, email va biografiyani yangilash.
- **Parol o'zgartirish:** Django standart PasswordChangeView orqali himoyalangan parolni yangilash mexanizmi.

### 2. Maqolalar boshqaruvi (blog)
- **Maqola yaratish:** Sarlavha, bo'lim (kategoriya), muqova rasmi, asosiy matn va teglarni biriktirish.
- **Unikal slug generatsiyasi:** Bir xil sarlavhali maqolalar uchun avtomatik unikal URL manzillari shakllantirish.
- **Tahrirlash va o'chirish:**
  - Faqat maqola muallifi o'z postini tahrirlashi mumkin.
  - Tahrirlangan post sifat nazorati uchun avtomatik `pending` holatiga qaytariladi.
  - O'chirish maxsus tasdiqlash oynasi orqali xavfsiz amalga oshiriladi.
- **Muallif paneli (`/posts/my-posts/`):** Shaxsiy maqolalar ro'yxati, ularning moderatsiya holati (`pending`, `approved`, `rejected`), ko'rishlar va tavsiyalar hisoblagichi.

### 3. Moderatsiya tizimi
- Yangi qo'shilgan va tahrirlangan postlar administrator tomonidan tasdiqlanmaguncha ommaviy ro'yxatda aks etmaydi.
- Django Admin panel orqali postlarni saralash, bittalab yoki guruhlab tasdiqlash va rad etish amallari mavjud.

### 4. O'zaro tavsiyalar tizimi (Recommendation Engine)
- Ro'yxatdan o'tgan foydalanuvchilar yoqqan maqolalarga tavsiya bera oladi.
- Bir foydalanuvchi bitta maqolaga faqat bitta ovoz bera oladi (ikkinchi marta bosilganda tavsiya bekor qilinadi).
- Muallif o'z maqolasiga tavsiya bera olmaydi.
- Eng ko'p tavsiya to'plagan maqolalar bosh sahifada ustuvor o'rinda namoyish etiladi.

### 5. Bosh sahifa va Magazine Layout
- Professional jurnallar uslubidagi asimmetrik bloklar:
  - **Asosiy maqola (Hero):** To'liq balandlikdagi muqova rasm, gradient qoplama, toifa va tavsiya nishonlari, sarlavha, muallif avatari va ko'rishlar ko'rsatkichi.
  - **Yon maqolalar:** O'ng ustunda joylashgan ixcham gorizontal kartochkalar.
- Tematik bo'limlar:
  - Eng yangi maqolalar
  - Eng ko'p ko'rilgan maqolalar
  - Haftaning ommabop maqolalari (oxirgi 7 kun)
  - Oyning ommabop maqolalari (oxirgi 30 kun)

### 6. Izohlar tizimi
- Maqolalar bo'yicha muhokama yuritish (faqat tizimga kirgan foydalanuvchilar uchun).
- Izoh muallifining avatari va profiliga to'g'ridan-to'g'ri o'tish imkoniyati.
- Izoh qoldirish yoki sahifani yangilash paytida post ko'rishlar soni asossiz oshib ketmasligi kafolatlangan.

### 7. Qidiruv, saralash va sahifalash
- Kategoriya va teglar bo'yicha filtrlash.
- Sarlavha va matn bo'yicha global qidiruv.
- Natijalarni sahifalarga taqsimlash (Pagination).

### 8. Maxsus xato sahifalari
- Brendlangan `404 — Sahifa topilmadi` va `500 — Server xatosi` shablonlari.

---

## Texnologiyalar steki

| Yo'nalish | Texnologiya | Tavsif |
|---|---|---|
| Backend | Python 3.10+, Django 5.x / 6.x | Asosiy web-freymvork va biznes mantiq |
| Ma'lumotlar bazasi | SQLite / PostgreSQL | Relyatsion ma'lumotlar bazasi |
| Media boshqaruvi | Pillow | Rasmlarni qayta ishlash va yuklash |
| Frontend | HTML5, Bootstrap 5.3, Bootstrap Icons | Foydalanuvchi interfeysi va moslashuvchanlik |
| Uslublar | Maxsus Vanilla CSS | Dizayn tizimi, tipografiya, animatsiyalar |

---

## Loyiha tuzilishi

```text
django-blog-project/
├── accounts/                   # Foydalanuvchilar va profillar ilovasi
│   ├── models.py               # UserProfile modeli va signallar
│   ├── views.py                # Profil, profil tahrirlash, ro'yxatdan o'tish
│   ├── forms.py                # RegisterForm, ProfileEditForm
│   ├── urls.py                 # Hisoblar marshrutlari
│   └── tests.py                # accounts ilovasi testlari
├── blog/                       # Asosiy blog ilovasi
│   ├── models.py               # Post, Category, Tag, Comment modellari
│   ├── views.py                # Asosiy sahifa, ro'yxat, detail, CRUD
│   ├── forms.py                # PostForm, CommentForm
│   ├── admin.py                # Admin panel sozlamalari va moderatsiya
│   ├── urls.py                 # Maqolalar marshrutlari
│   └── tests.py                # blog ilovasi testlari
├── config/                     # Loyiha asosiy konfiguratsiyasi
│   ├── settings.py             # Sozlamalar (apps, media, static, templates)
│   └── urls.py                 # Global marshrutlar
├── templates/                  # HTML shablonlar
│   ├── base.html               # Asosiy shablon (header, navbar, footer)
│   ├── 404.html                # 404 xato sahifasi
│   ├── 500.html                # 500 xato sahifasi
│   ├── accounts/               # Profil va autentifikatsiya sahifalari
│   └── blog/                   # Blog, magazine layout, sharhlar sahifalari
├── static/                     # Statik resurslar
│   └── css/style.css           # Maxsus CSS stillari
├── .env.example                # Muhit o'zgaruvchilari namunasi
├── .gitignore                  # Versiya nazoratidan chiqarilgan fayllar
├── requirements.txt            # Python paketlari ro'yxati
├── manage.py                   # Django boshqaruv skripti
├── CONTRIBUTING.md             # Loyihaga hissa qo'shish qoidalari
├── LICENSE                     # MIT litsenziyasi matni
└── README.md                   # Loyiha hujjati
```

---

## O'rnatish va ishga tushirish

Loyihani mahalliy muhitda ishga tushirish uchun quyidagi ketma-ketlikni bajaring:

### 1. Repozitoriyani yuklab olish
```bash
git clone https://github.com/OktamTurgun/django-blog-project.git
cd django-blog-project
```

### 2. Virtual muhitni yaratish va faollashtirish

Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Bog'liqliklarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Ma'lumotlar bazasi migratsiyasini bajarish
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Administrator hisobini yaratish
```bash
python manage.py createsuperuser
```

### 6. Loyihani ishga tushirish
```bash
python manage.py runserver
```

Brauzer orqali kirish:
- Asosiy sahifa: `http://127.0.0.1:8000/`
- Administrator paneli: `http://127.0.0.1:8000/admin/`

---

## Avtomatlashtirilgan testlar

Loyiha barqarorligini ta'minlash uchun 27 ta test senariysi ishlab chiqilgan:

```bash
python manage.py test
```

Tizim sozlamalari yaxlitligini tekshirish:
```bash
python manage.py check
```

---

## Konfiguratsiya

Ishlab chiqarish (production) muhitida ishlatish uchun `.env.example` faylidan namuna sifatida foydalanib `.env` faylini shakllantiring:

```text
SECRET_KEY=maxfiy-kalitni-kiriting
DEBUG=False
ALLOWED_HOSTS=sizning-domeningiz.uz,127.0.0.1
```

---

## Hissa qo'shish

Loyiha rivojiga hissa qo'shish, xatoliklar haqida xabar berish yoki yangi takliflar kiritish tartibi bilan [CONTRIBUTING.md](CONTRIBUTING.md) faylida tanishishingiz mumkin.

---

## Litsenziya

Ushbu loyiha [MIT Litsenziyasi](LICENSE) shartlari asosida tarqatiladi.