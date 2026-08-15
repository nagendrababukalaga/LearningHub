# 📋 LearningHub — Technical Project Overview & Hackathon Submission

## 🎯 Executive Summary

**Project Name**: LearningHub  
**Target Category**: AI / Vibe Coding Hackathon 2026  
**Primary Focus**: Personalized Python Learning Platform for Students  
**Core Innovation**: **Personal Learning Memory** (capturing individual student mental models, analogies, code snippets, doubts, and mistakes) + **Intelligent Rule-Based Revision Engine**.

---

## 🧩 Architectural Design & Data Flow

```
+-----------------------------------------------------------------------------------+
|                                STUDENT DASHBOARD                                  |
|  - "What should I do today?" Daily Planner                                       |
|  - Real-Time Learning Analytics (Streak, Overall %, Mastered Topics)              |
|  - Automated Revision Alert Cards                                                 |
+-----------------------------------------+-----------------------------------------+
                                          |
        +---------------------------------+---------------------------------+
        |                                                                   |
        v                                                                   v
+----------------------------------+               +----------------------------------+
|      7-LEVEL PYTHON PATH         |               |     PERSONAL LEARNING MEMORY     |
| - 35 Topics (Levels 1 to 7)      |               | - My Own Explanation             |
| - 70+ Curated Resources          | <-----------> | - Real-Life Analogy              |
| - 35 Practice Coding Challenges  |               | - What Confused Me / Pitfalls    |
| - 5 Understanding Levels         |               | - What Helped Me Click           |
+----------------------------------+               +----------------------------------+
        |                                                                   |
        v                                                                   v
+----------------------------------+               +----------------------------------+
|    DOUBTS & MISTAKES TRACKER     |               |   RULE-BASED REVISION ENGINE     |
| - Open / Resolved Doubts         | ------------> | - Need-Revision Weight (+50)     |
| - Error Types & Lessons Learned  |               | - Open Doubts Weight (+30)       |
| - Broken vs Fixed Code Snippets  |               | - Logged Mistakes Weight (+25)   |
+----------------------------------+               +----------------------------------+
        |                                                                   |
        +---------------------------------+---------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        CONTEXTUAL AI LEARNING ASSISTANT                           |
|  - Injects Student Memory, Analogies & Mistakes into Prompt Context               |
|  - Offline Resilient Fallback Engine (Simplify, Analogy, Practice, Debug, Plan)   |
|  - Optional OpenAI / External LLM API Compatibility                              |
+-----------------------------------------------------------------------------------+
```

---

## 📂 Modular Django Architecture

The backend is organized into 8 single-responsibility Django apps in `apps/`:

1. **`accounts`**: Custom `Profile` model with automatic signal creation, experience levels, career goals, study target minutes, and consecutive day streak tracking.
2. **`learning`**: Hierarchical data model (`LearningPath` $\rightarrow$ `Level` $\rightarrow$ `Topic` $\rightarrow$ `Resource`). Supports bookmarking and bi-directional topic traversal (`get_previous_topic()`, `get_next_topic()`).
3. **`memory`**: Engine for `PersonalLearningMemory`, `LearningDoubt` (with resolution notes), `LearningMistake` (with error categorization and lessons learned), and `TopicNote`.
4. **`progress`**: Manages `UserTopicProgress` (5 understanding levels: `not_started`, `learning`, `need_revision`, `comfortable`, `strong`), `PracticeProblem`, `UserPractice`, `DailyTask`, and contains the `RevisionRecommendationEngine` and `DailyPlanGenerator`.
5. **`bootcamp`**: 30-Day intensive Python curriculum with daily tasks, code starters, and completion logs.
6. **`guidance`**: Senior engineer career guidance, debugging strategies, interview preparation articles, and daily wisdom tips.
7. **`ai_assistant`**: Session-based AI Assistant workspace with dynamic memory context injection and offline educational generation.
8. **`core`**: Landing page, global multi-model search, error handlers (404/500), and `global_context` context processor for badges and profile state across all templates.

---

## 🎨 UI/UX Design Principles (Vanilla Web Standards)

- **Pure Vanilla CSS**: Zero external utility dependencies (no Tailwind, Bootstrap, or node_modules).
- **HSL Semantic Design Tokens**: Light and dark themes with smooth transitions, responsive typography (Inter, Plus Jakarta Sans, Fira Code), and high-contrast accessibility.
- **Micro-Interactions**: Hover lifts, badge pills, streak counters, code copy buttons, and AJAX auto-save feedback.

---

## 📊 Verification & Test Metrics

- **Unit Tests**: 11 automated test cases passing in `python manage.py test`.
- **E2E User Flow Tests**: 15 full end-to-end user flows verified via `python scripts/verify_all_flows.py`.
- **Seeded Content**: 7 levels, 35 topics, 71 resources, 35 practice problems, 30 bootcamp days, 6 mentor guides, 6 daily tips, and 4 student success stories.
