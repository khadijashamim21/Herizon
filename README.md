# 🌸 Herizon — Empowering Women Through Opportunities

*Herizon* is a women-only job hunting and support platform designed to connect women with *jobs, internships, freelancing, and learning materials* — all in one safe and empowering space.  
Built with ❤️ during a hackathon, the project focuses on women’s career growth and community engagement.

---

## ✨ Features

- 👩‍💼 *Women-only platform* with secure signup/login system  
- 📰 *Social Feed* — share posts, job updates, and study materials  
- 💬 *Comments & Likes* (basic interaction features)  
- 📤 *Material and Job Uploads*  
- 🛡️ *Admin Moderation* for safe content and verified profiles  
- 🎯 *Personalized feed* and trending posts  
- 🏅 *Badges and Verified Profiles*  
- 💾 *Save / Bookmark* jobs and materials  
- 🔍 *Filter & Search* by tags, job type, and topics  
- 👤 *Profile Pages* showing user’s posts, achievements, and badges  

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Django (Python) |
| Database | SQLite (default Django DB) |
| Styling | Custom CSS with Poppins font |
| Authentication | Django Auth System |

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

```bash
# Clone the repository
git clone https://github.com/khadijashamim21/herizon.git
cd herizon

# Create virtual environment
python -m venv env
env\Scripts\activate     # for Windows
# or
source env/bin/activate  # for Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
