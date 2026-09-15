# 🚀 Django Blog Loyihasi (Modern Magazine & Community Blog)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0%2B-092E20.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3.svg?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Tests](https://img.shields.io/badge/Tests-27%20Passed-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Zamonaviy dizayn, foydalanuvchi profillari, moderatsiya tartibi va o'quvchilar tavsiyalari asosida ishlovchi professional darajadagi blog platformasi.

---

## ✨ Asosiy Imkoniyatlar (Features)

### 👤 1. Foydalanuvchi va Profil Tizimi (`accounts`)
- **Ro'yxatdan o'tish va Kirish**: Email majburiy bo'lgan xavfsiz avtorizatsiya va darhol tizimga kirish (`auto-login`).
- **Ommaviy Profil Sahifasi (`/accounts/profile/<username>/`)**:
  - Shaxsiy avatar, bio, veb-sayt havolasi.
  - Muallifning jami ko'rishlari va yig'gan tavsiyalari statistikasi.
  - Foydalanuvchi chop etgan barcha tasdiqlangan maqolalari ro'yxati.
- **Profil Sozlamalari (`/accounts/profile/edit/`)**: Avatar rasmini yuklash, ism, familiya, bio va boshqa ma'lumotlarni tahrirlash.
- **Parolni Xavfsiz O'zgartirish**: Django'ning standart `PasswordChangeView` orqali yangilash.

### 📝 2. Maqolalar Boshqaruvi (`blog`)
- **Post Yaratish**: Kategoriya, rasm, matn va teglarni tanlash imkoniyati.
- **Unikal Slug**: Bir xil sarlavhali postlar bo'lsa ham unikal URL generatsiya qilish (`-1`, `-2`).
- **Post Tahrirlash va O'chirish**:
  - Faqat muallif o'z postini tahrirlashi mumkin. Tahrirlangan post xavfsizlik va sifat nazorati uchun avtomatik `pending` (moderatsiya) holatiga qaytadi.
  - Postni o'chirish maxsus tasdiqlash oynasi (`post_confirm_delete.html`) orqali bajariladi.
- **Mening Postlarim (`/posts/my-posts/`)**: Muallif barcha yozgan postlari holati (`pending`, `approved`, `rejected`), ko'rishlar soni va admin tavsiyasi nishonini ko'rib turadi.

### 🛡️ 3. Moderatsiya Tizimi
- Har bir yangi post administrator tomonidan tekshirilmaguncha umumiy ro'yxatda va bosh sahifada ko'rinmaydi.
- Admin panel orqali postlarni bir tugma bilan ommaviy tasdiqlash (`Approve`) yoki rad etish (`Reject`).

### ⭐ 4. Foydalanuvchilar Tavsiyasi Tizimi (Recommendation / Like)
- Har bir o'quvchi ma'qul kelgan postga "Tavsiya qilish" tugmasini bosa oladi.
- Bir foydalanuvchi bitta postga bir marta ovoz beradi (ikkinchi marta bosganda bekor qilinadi).
- Muallif o'z postiga tavsiya bera olmaydi.
- Eng ko'p tavsiya to'plagan maqolalar bosh sahifada eng yuqori o'rinlarga chiqadi.

### 📰 5. Bosh Sahifa: Zamonaviy "Magazine Layout"
- Oddiy kartochkalar o'rniga zamonaviy onlayn nashrlar va jurnallar uslubidagi asimmetrik tartib:
  - **Asosiy Hero Post**: Chapda to'liq balandlikdagi katta rasm, dark overlay, muallif avatari, tavsiyalar soni va hover zoom effekti.
  - **Yon Postlar**: O'ngda ixcham gorizontal kartochkalar.
- Qo'shimcha bloklar:
  - Eng yangi postlar
  - Eng ko'p ko'rilgan postlar
  - Haftaning ommabop postlari (oxirgi 7 kun)
  - Oyning ommabop postlari (oxirgi 30 kun)

### 💬 6. Izohlar Tizimi
- Har bir maqolaga fikr qoldirish (faqat ro'yxatdan o'tganlar uchun).
- Izoh muallifining avatari va profiliga to'g'ridan-to'g'ri o'tish havolasi.
- Izoh yozganda yoki sahifa qayta yangilanganda ko'rishlar soni asossiz oshib ketishidan himoyalangan.

### 🔍 7. Qidiruv, Filtrlash va Sahifalash
- Kategoriyalar va teglar bo'yicha saralash.
- Sarlavha va maqola matni bo'yicha global qidiruv.
- Har bir sahifada 6 tadan postlarni chiroyli ko'rsatuvchi sahifalash (Pagination).

### 🚫 8. Maxsus Xato Sahifalari
- Brendlangan `404 — Sahifa topilmadi` va `500 — Server xatosi` sahifalari.

---

## 🛠️ Texnologiyalar Steki

| Qatlam | Texnologiya |
|---|---|
| **Backend** | Python 3.10+, Django 5.x / 6.x |
| **Baza** | SQLite (standart), PostgreSQL ga oson ulanadi |
| **Media/Rasmlar** | Pillow |
| **Frontend** | HTML5, Bootstrap 5.3.3, Bootstrap Icons |
| **Dizayn uslubi** | Custom Vanilla CSS (Plus Jakarta Sans, Dark Navbar, Glassmorphism, Micro-animations) |

---

## 📁 Loyiha Tuzilishi

```text
django-blog-project/
├── accounts/                   # Foydalanuvchilar ilovasi
│   ├── models.py               # UserProfile modeli va signallar
│   ├── views.py                # Profil, profil tahrirlash, ro'yxatdan o'tish
│   ├── forms.py                # RegisterForm, ProfileEditForm
│   ├── urls.py                 # Hisoblar marshrutlari
│   └── tests.py                # accounts bo'yicha testlar
├── blog/                       # Asosiy blog ilovasi
│   ├── models.py               # Post, Category, Tag, Comment
│   ├── views.py                # home, post_list, post_detail, create/edit/delete
│   ├── forms.py                # PostForm, CommentForm
│   ├── admin.py                # Moderatsiya va qidiruv filtrlari
│   ├── urls.py                 # Postlar marshrutlari
│   └── tests.py                # blog bo'yicha to'liq testlar
├── config/                     # Loyiha konfiguratsiyasi
│   ├── settings.py             # Sozlamalar (apps, media, static, templates)
│   └── urls.py                 # Asosiy marshrutlar
├── templates/                  # HTML shablonlar
│   ├── base.html               # Asosiy shablon (navbar, meta, footer)
│   ├── 404.html                # 404 xato sahifasi
│   ├── 500.html                # 500 xato sahifasi
│   ├── accounts/               # Profil va autentifikatsiya shablonlari
│   └── blog/                   # Postlar, magazine layout, sharhlar
├── static/                     # Statik fayllar (CSS, JS)
│   └── css/style.css           # Maxsus dizayn stillari
├── .env.example                # Muhit o'zgaruvchilari shabloni
├── .gitignore                  # Git e'tiborsiz qoldiradigan fayllar
├── requirements.txt            # Kerakli Python kutubxonalari
├── manage.py
├── LICENSE                     # MIT litsenziyasi
└── README.md
```

---

## ⚙️ O'rnatish va Ishga Tushirish

Loyihani mahalliy kompyuteringizda ishga tushirish uchun quyidagi bosqichlarni bajaring:

### 1. Repozitoriyani klonlash
```bash
git clone https://github.com/OktamTurgun/django-blog-project.git
cd django-blog-project
```

### 2. Virtual muhit yaratish va faollashtirish
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Bog'liqliklarni (requirements) o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Ma'lumotlar bazasini tayyorlash (Migrations)
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Administrator (Superuser) yaratish
Postlarni tasdiqlash va boshqarish uchun admin hisobini oching:
```bash
python manage.py createsuperuser
```

### 6. Serverni ishga tushirish
```bash
python manage.py runserver
```

Brauzerda quyidagi manzillarni oching:
- **Asosiy blog sahifasi:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Avtomatlashtirilgan Testlar

Loyiha sifatini va har bir funksiyaning ishonchliligini ta'minlash uchun 27 ta keng qamrovli avtotest yozilgan:

```bash
python manage.py test
```

Tizim sozlamalari yaxlitligini tekshirish:
```bash
python manage.py check
```

---

## 👨‍💻 Muallif

- **O'ktam Turg'unov** — [GitHub Profili](https://github.com/OktamTurgun)

## 📄 Litsenziya

Ushbu loyiha [MIT Litsenziyasi](LICENSE) asosida ochiq manbali hisoblanadi.