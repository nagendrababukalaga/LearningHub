# 🚀 LearningHub — Personalized Python Learning Platform

> *"Don't just give students resources. Give them a learning journey."*  
> *"LearningHub doesn't just track what you learned. It remembers how YOU learned."*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0%2B-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Hackathon](https://img.shields.io/badge/Hackathon-AI%20%26%20Vibe%20Coding%202026-orange.svg)]()

---

## 💡 The Problem We Solve

Students today have access to infinite free learning content across YouTube, documentation, blog posts, and coding platforms.

However, having too many resources creates **analysis paralysis**:
- *What should I learn first?*
- *How do I retain what I learned without forgetting syntax 3 days later?*
- *Why did I make this mistake, and how do I avoid repeating it in interviews?*
- *What should I work on today?*

**LearningHub solves this by transforming scattered content into a structured, personalized learning journey with Personal Learning Memory, systematic error tracking, and intelligent revision.**

---

## 🌟 Core Features

### 1. 🐍 Complete 7-Level Python Master Curriculum
- **Level 1**: Fundamentals & Core Syntax (6 Topics)
- **Level 2**: Control Flow & Logical Thinking (4 Topics)
- **Level 3**: Data Structures Mastery (5 Topics)
- **Level 4**: Functions & Modular Architecture (5 Topics)
- **Level 5**: Intermediate Python & Memory Management (5 Topics)
- **Level 6**: Object-Oriented Engineering (5 Topics)
- **Level 7**: Practical Applications & Interview Prep (5 Topics)
- **Total**: 35 Topics, 70+ curated external resources, 35 coding challenges with starter code and hints.

### 2. 🧠 Personal Learning Memory (Core Differentiator)
Normal platforms explain a concept once and forget it. LearningHub captures:
- **What I Understood** in the student's own words.
- **Real-Life Analogies & Metaphors** that made the concept click.
- **Custom Sandbox Code Snippets**.
- **What Confused Me** (common stumbling blocks).
- **What Helped Me Understand** (the "Aha!" moment).

### 3. 🎯 Daily Learning Planner ("What should I do today?")
Generates a structured, 5-phase daily routine (~45 mins total):
1. **Learn**: Read concept overview and study syntax.
2. **Understand**: Formulate your own analogy in Personal Learning Memory.
3. **Practice**: Solve a hands-on coding challenge in the Practice Tracker.
4. **Review**: 10-minute flash revision of high-priority concepts.
5. **Complete**: Mark your understanding level (Learning, Need Revision, Comfortable, Strong).

### 4. 🔄 Rule-Based Revision Recommendation Engine
An intelligent recommendation algorithm that scores topics needing review based on:
- `need_revision` status (+50 points)
- Open, unresolved doubts (+30 points)
- Logged coding mistakes (+25 points)
- In-progress `learning` status (+20 points)
- Staleness (>5 days since last activity)

### 5. ❓ Doubts & ⚠️ Mistakes Trackers
- **Doubts Tracker**: Log questions as you study, filter by open/resolved, and record solutions.
- **Mistakes Tracker**: Categorize errors (Syntax, Logic, Runtime, Type, Conceptual) and write down the exact fix and lesson learned.

### 6. 🚀 30-Day Intensive Python Bootcamp
- 30 daily progressive milestones from Hello World to REST APIs and capstones.
- Daily learning objectives, hands-on tasks, starter code, and reflection journals.

### 7. 🧭 Senior Engineer Mentor Guidance
- In-depth strategy guides for escaping tutorial hell, debugging like a senior dev, cracking technical interviews, and building portfolio-worthy software.
- Senior engineer daily wisdom tips.

### 8. ✨ Contextual AI Learning Assistant
- **Context Injection**: Injects the student's own stored Personal Learning Memory, doubts, and mistakes into prompts.
- **Offline Resilient**: Ships with an offline intelligent educational generator (Simplify, Analogy, Practice Challenges, Debugging Traps, 15-Min Study Plan) + optional OpenAI API key support.

---

## ⚡ Quickstart & Installation

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone & Enter Repository
```bash
git clone https://github.com/your-username/LearningHub.git
cd LearningHub
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Seed Database
```bash
python manage.py migrate
python manage.py seed_learninghub
```

### 5. Start Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to: **`http://127.0.0.1:8000/`**

---

## 🔑 Demo & Admin Credentials

The seeder automatically provisions the following accounts:

| Role | Username | Password | Notes |
|---|---|---|---|
| **Demo Student** | `demo_student` | `password123` | Pre-populated with learning memory, active doubts, logged mistakes, and study streak |
| **Superuser / Admin** | `admin` | `admin123` | Full access to Django Admin at `/admin/` |

---

## 🧪 Running Automated Tests

Run the full automated test suite (11 unit tests covering all 8 modules):
```bash
python manage.py test
```

Run the end-to-end user flow verification script:
```bash
python scripts/verify_all_flows.py
```

---

## 🏛️ Project Architecture

```
LearningHub/
├── manage.py
├── requirements.txt
├── README.md
├── PROJECT_OVERVIEW.md
├── .env.example
├── learninghub/               # Django Core Configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                      # 8 Modular Django Apps
│   ├── accounts/             # Student Profiles, Goals, Streaks
│   ├── learning/             # 7-Level Curriculum, Topics, Resources, Bookmarks
│   ├── memory/               # Personal Learning Memory, Doubts, Mistakes
│   ├── progress/             # Daily Plan, Practice Tracker, Revision Engine
│   ├── bootcamp/             # 30-Day Python Bootcamp Curriculum & Tracker
│   ├── guidance/             # Senior Mentor Guides & Daily Tips
│   ├── ai_assistant/         # AI Assistant with Memory Context & Fallback
│   └── core/                 # Landing Page, Global Search, Context Processors
├── static/
│   ├── css/                  # Vanilla CSS Design System (HSL tokens, Dark/Light)
│   │   ├── main.css
│   │   ├── components.css
│   │   ├── landing.css
│   │   ├── dashboard.css
│   │   └── topic.css
│   └── js/                   # Vanilla JavaScript Interactivity
│       ├── main.js
│       ├── topic_memory.js
│       └── ai_chat.js
├── templates/                 # Semantic HTML5 Templates
│   ├── base.html
│   ├── accounts/
│   ├── learning/
│   ├── memory/
│   ├── progress/
│   ├── bootcamp/
│   ├── guidance/
│   ├── ai_assistant/
│   └── core/
└── scripts/
    └── verify_all_flows.py   # E2E Test Suite
```

---

## 🚀 Business Model & Future Roadmap

- **Free Core Tier (100% Free Forever)**: Full 7-level curriculum, Personal Learning Memory, practice tracker, mistake logs, and rule-based revision.
- **Pro Mentorship (Future Concept)**: 1-on-1 GitHub pull request code reviews, live mock technical interviews, and resume project architecture reviews with senior engineers.
- **Future Learning Paths**: Java Master Path, Data Structures & Algorithms (DSA), Full-Stack Web Development, SQL & Database Engineering.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
