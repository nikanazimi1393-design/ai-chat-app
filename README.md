# AI Chat App

A simple, self-hosted AI chatbot web app built with Python (Flask), connected to [OpenRouter](https://openrouter.ai) for AI responses. Built and run entirely from **Termux** on Android, with an optional live deployment to **Render**.

یک اپلیکیشن وب چت با هوش مصنوعی، ساده و خودمیزبان (self-hosted)، ساخته‌شده با پایتون (Flask) و متصل به [OpenRouter](https://openrouter.ai) برای دریافت پاسخ‌های هوش مصنوعی. کاملاً از داخل **ترموکس** روی اندروید ساخته و اجرا شده، با قابلیت دیپلوی روی **Render** برای داشتن یک آدرس (URL) دائمی و آنلاین.

---

## ✨ Features / ویژگی‌ها

- Real-time streaming responses (like ChatGPT) / پاسخ‌های استریم و لحظه‌ای (مثل ChatGPT)
- Clean, mobile-friendly chat UI / رابط کاربری تمیز و مناسب موبایل
- Fully configurable model & API key via environment variables / قابل تنظیم کامل با متغیرهای محیطی
- Runs locally in Termux or deployed online (Render) / قابل اجرا هم به‌صورت محلی در ترموکس و هم آنلاین روی Render

---

## 🧰 Requirements / پیش‌نیازها

- [Termux](https://f-droid.org/packages/com.termux/) installed on Android
- An [OpenRouter](https://openrouter.ai) account and API key
- (Optional) A [GitHub](https://github.com) account and [Render](https://render.com) account for online hosting

---

## 🚀 Setup in Termux / راه‌اندازی در ترموکس

### 1. Install dependencies / نصب پیش‌نیازها

\`\`\`bash
pkg update && pkg upgrade
pkg install python git -y
\`\`\`

### 2. Clone this project / کلون کردن پروژه

\`\`\`bash
git clone https://github.com/YOUR_USERNAME/ai-chat-app.git
cd ai-chat-app
\`\`\`

### 3. Install Python packages / نصب پکیج‌های پایتون

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Set your API key / تنظیم کلید API

\`\`\`bash
export OPENROUTER_API_KEY="sk-or-your-key-here"
export OPENROUTER_MODEL="openai/gpt-4o-mini"
\`\`\`

To make these permanent (so you don't need to set them every time you open Termux), add them to \`~/.bashrc\`:
برای اینکه همیشگی بشن (و لازم نباشه هر بار ترموکس رو باز میکنی دوباره ست‌شون کنی)، به فایل \`~/.bashrc\` اضافه‌شون کن:

\`\`\`bash
echo 'export OPENROUTER_API_KEY="sk-or-your-key-here"' >> ~/.bashrc
echo 'export OPENROUTER_MODEL="openai/gpt-4o-mini"' >> ~/.bashrc
source ~/.bashrc
\`\`\`

### 5. Run the app / اجرای اپ

\`\`\`bash
python app.py
\`\`\`

### 6. Open it in your browser / باز کردن در مرورگر

Go to / برو به:
\`\`\`
http://127.0.0.1:5000
\`\`\`

---

## ☁️ Deploying online with Render / دیپلوی آنلاین با Render

To get a permanent public URL that works even when your phone is off:
برای داشتن یک URL دائمی که حتی وقتی گوشیت خاموشه هم کار میکنه:

1. Push this project to a GitHub repository (see commands below).
2. Go to [render.com](https://render.com) and sign in with GitHub.
3. Click **New +** → **Web Service** and connect this repository.
4. Set:
   - **Build Command**: \`pip install -r requirements.txt\`
   - **Start Command**: \`gunicorn app:app --workers 1 --threads 8 --timeout 120\`
5. Under **Environment Variables**, add:
   - \`OPENROUTER_API_KEY\` = your OpenRouter key
   - \`OPENROUTER_MODEL\` = \`openai/gpt-4o-mini\`
6. Click **Create Web Service** and wait for deployment to finish.

---

## 📤 Pushing updates to GitHub / آپلود تغییرات جدید به گیت‌هاب

Whenever you change a file and want to update GitHub (and trigger a new deploy on Render):
هر وقت فایلی رو عوض کردی و خواستی گیت‌هاب رو آپدیت کنی (و یک دیپلوی جدید روی Render فعال بشه):

\`\`\`bash
cd ~/ai-chat-app
git add .
git commit -m "Describe your change here"
git push
\`\`\`

If this is your **first time** setting up git on this device / اگه اولین باره که گیت رو رو این دستگاه تنظیم میکنی:

\`\`\`bash
git config --global user.email "your-email@example.com"
git config --global user.name "your-github-username"
\`\`\`

When \`git push\` asks for a username and password:
وقتی \`git push\` یوزرنیم و پسورد خواست:
- **Username**: your GitHub username
- **Password**: a GitHub [Personal Access Token](https://github.com/settings/tokens) (not your account password)

---

## 📁 Project structure / ساختار پروژه

\`\`\`
ai-chat-app/
├── app.py              # Flask backend, connects to OpenRouter
├── requirements.txt    # Python dependencies
├── Procfile             # Start command for Render
├── templates/
│   └── index.html      # Chat page
└── static/
    └── style.css        # Chat page styling
\`\`\`

---

## ⚙️ Environment variables / متغیرهای محیطی

| Variable | Description (EN) | توضیح (فا) | Default |
|---|---|---|---|
| \`OPENROUTER_API_KEY\` | Your OpenRouter API key (required) | کلید API از OpenRouter (اجباری) | — |
| \`OPENROUTER_MODEL\` | Which AI model to use | مدل هوش مصنوعی مورد استفاده | \`openai/gpt-4o-mini\` |
| \`OPENROUTER_BASE_URL\` | API endpoint (change only if using a custom wrapper) | آدرس اپی (فقط در صورت استفاده از یک رپر اختصاصی تغییرش بده) | \`https://openrouter.ai/api/v1/chat/completions\` |

---

## 📝 License / لایسنس

Free to use and modify for personal projects.
برای استفاده و ویرایش در پروژه‌های شخصی آزاد است.
