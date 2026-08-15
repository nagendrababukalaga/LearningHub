import os
import json
import requests
from django.conf import settings
from apps.memory.models import PersonalLearningMemory, LearningDoubt, LearningMistake
from apps.learning.models import Topic

class ContextualAIService:
    """
    Context-aware AI Learning Assistant service.
    Injects the student's personal learning memory, logged mistakes, and active doubts
    into the prompt context, and provides an intelligent offline fallback when no external API key is present.
    """

    @classmethod
    def generate_response(cls, user, prompt_text, topic_id=None, action_mode='general'):
        topic = None
        student_memory = None
        topic_doubts = []
        topic_mistakes = []

        if topic_id:
            try:
                topic = Topic.objects.get(id=topic_id)
                student_memory = PersonalLearningMemory.objects.filter(user=user, topic=topic).first()
                topic_doubts = list(LearningDoubt.objects.filter(user=user, topic=topic).values_list('doubt_text', flat=True))
                topic_mistakes = list(LearningMistake.objects.filter(user=user, topic=topic).values_list('mistake_description', flat=True))
            except Topic.DoesNotExist:
                pass

        # Build context metadata
        context_summary = []
        if topic:
            context_summary.append(f"Topic: {topic.title} (Level {topic.level.level_number})")
        if student_memory and student_memory.is_filled:
            if student_memory.real_life_analogy:
                context_summary.append(f"Student Analogy: '{student_memory.real_life_analogy}'")
            if student_memory.what_confused_me:
                context_summary.append(f"Past Confusion: '{student_memory.what_confused_me}'")
        if topic_mistakes:
            context_summary.append(f"Logged Mistakes: {len(topic_mistakes)} recorded")
        if topic_doubts:
            context_summary.append(f"Recorded Doubts: {len(topic_doubts)} active")

        # Try external API if configured
        api_key = getattr(settings, 'AI_API_KEY', '')
        if api_key:
            try:
                return cls._call_external_llm(api_key, prompt_text, topic, student_memory, topic_doubts, topic_mistakes, action_mode)
            except Exception as e:
                # Graceful fallback to offline engine
                pass

        # Use Intelligent Built-in Fallback Generator
        return cls._generate_intelligent_fallback(prompt_text, topic, student_memory, topic_doubts, topic_mistakes, action_mode)

    @classmethod
    def _generate_intelligent_fallback(cls, prompt_text, topic, student_memory, topic_doubts, topic_mistakes, action_mode):
        topic_name = topic.title if topic else "Python Programming"
        
        # 1. Simplify Mode
        if action_mode == 'simplify' or 'simplify' in prompt_text.lower() or 'eli5' in prompt_text.lower():
            analogy_cue = ""
            if student_memory and student_memory.real_life_analogy:
                analogy_cue = f"\n\n> **Connecting to your personal memory:** *\"{student_memory.real_life_analogy}\"*"

            return f"""### 💡 Simplified Breakdown: **{topic_name}**

Let's strip away the technical jargon and understand the core concept:

1. **The Big Idea**: In Python, `{topic_name}` solves the problem of organizing instructions and managing state cleanly without repeating yourself.
2. **Mental Model**: Think of it as a set of labeled containers that follow predictable rules every single time code executes.{analogy_cue}

```python
# Clean, readable idiomatic Python demonstration
def demonstrate_concept():
    # Focused example
    data = ["step_1", "step_2", "step_3"]
    for idx, item in enumerate(data, start=1):
        print(f"Executing {{idx}}: {{item}}")

demonstrate_concept()
```

**Golden Rule**: *Always write explicit code that your future self can understand in 10 seconds.*"""

        # 2. Analogy Mode
        if action_mode == 'analogy' or 'analogy' in prompt_text.lower() or 'metaphor' in prompt_text.lower():
            return f"""### 🌟 Real-World Analogies for **{topic_name}**

Here are two clear mental models to make this concept stick:

#### 1. The Kitchen Blueprint Analogy
- Think of `{topic_name}` like a **standardized recipe card** in a restaurant. 
- The recipe itself takes up almost no space on the counter, but whenever the chef calls the recipe, delicious meals are prepared consistently without re-inventing the steps.

#### 2. The Labeled Storage Locker
- When managing data in memory, `{topic_name}` acts like a **transparent, labeled locker**. 
- You can instantly check what is inside, replace items if mutable, or keep them securely locked if immutable.

> **Tip**: Write down your own version of these analogies in your **Personal Learning Memory** tab to reinforce your mental model!"""

        # 3. Practice Challenge Mode
        if action_mode == 'practice' or 'challenge' in prompt_text.lower() or 'exercise' in prompt_text.lower():
            return f"""### 🎯 Custom Coding Challenges for **{topic_name}**

Put your understanding to the test with these two challenges:

#### Challenge 1: The Warmup (Easy)
Write a Python function `solve_warmup(input_data)` that validates the input and returns a clean formatted string.
```python
def solve_warmup(items: list) -> str:
    # 1. Filter out empty items
    # 2. Join the remaining items with ' -> '
    # 3. Return the result in uppercase
    pass

# Test case:
# solve_warmup(["python", "", "django", "sqlite"]) -> "PYTHON -> DJANGO -> SQLITE"
```

#### Challenge 2: The Edge Case (Medium)
Handle boundary conditions, empty lists, or unexpected inputs gracefully with `try...except` and return a safe fallback.

> **Next Step**: Open the **Practice Tracker** in LearningHub to submit your solution and record your reflections!"""

        # 4. Debug / Mistake Analysis Mode
        if action_mode == 'debug' or 'mistake' in prompt_text.lower() or 'error' in prompt_text.lower():
            mistake_context = ""
            if topic_mistakes:
                mistake_context = f"\n\n> **Reviewing your logged mistake:** *\"{topic_mistakes[0]}\"*"

            return f"""### 🛠️ Common Pitfalls & Debugging Guide: **{topic_name}**{mistake_context}

Here are the top traps developers encounter when working with `{topic_name}`:

1. **Syntax & Variable Assignment Errors**:
   - Confusing `=` (assignment) with `==` (equality check).
   - Indentation inconsistency (mixing 4 spaces with tabs).

2. **Scope & Mutability Bugs**:
   - Accidentally modifying a shared mutable list or dictionary while iterating over it.
   - Forgetting that variables created inside a function are local unless returned or passed.

3. **How to Debug Systematically**:
   - Always inspect the bottom-most line of the traceback first.
   - Use `print(f"DEBUG: {{val=}} ({{type(val)=}})")` to verify actual data types before the failing line."""

        # 5. Quick Study Plan Mode
        if action_mode == 'study_plan' or 'plan' in prompt_text.lower():
            return f"""### ⏱️ 15-Minute Micro-Study Plan for **{topic_name}**

Here is your focused, zero-distraction routine:

- **Minute 0–5 (Concept Review)**: Read the topic overview and study the syntax snippet.
- **Minute 5–10 (Active Recall)**: Open the **Personal Learning Memory** section and write your own 2-sentence summary without looking.
- **Minute 10–14 (Practice)**: Solve the topic practice problem in your editor.
- **Minute 14–15 (Checkoff)**: Mark your understanding level (Comfortable or Strong) and log any remaining doubts.

*Ready to start? Open the topic and set your timer!*"""

        # General Query Response
        return f"""### 🐍 LearningHub AI Assistant — **{topic_name}**

I analyzed your learning context for **{topic_name}**.

Regarding: *"**{prompt_text}**"*

Here is a structured, practical answer:

1. **Key Principle**: In Python, `{topic_name}` is designed with PEP 20 philosophy: *Explicit is better than implicit, and readability counts.*
2. **Implementation Pattern**:
```python
# Idiomatic Python pattern
def process_learning_topic(topic_name: str, is_active: bool = True):
    \"\"\"Process topic with clean error handling and type annotations.\"\"\"
    if not is_active:
        return None
    return f"Mastering {topic_name.title()} with LearningHub!"

result = process_learning_topic("{topic_name.lower()}")
print(result)
```
3. **Actionable Next Step**: Check off your daily learning task on the **Dashboard** and try solving the associated practice challenge.

Feel free to ask me to **simplify this**, **give an analogy**, or **create practice challenges** anytime!"""

    @classmethod
    def _call_external_llm(cls, api_key, prompt_text, topic, student_memory, topic_doubts, topic_mistakes, action_mode):
        # Optional OpenAI / Compatible Endpoint Call
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        system_content = "You are the LearningHub AI Learning Assistant, a friendly, encouraging, expert Python mentor for college students."
        if topic:
            system_content += f"\nCurrent Topic: {topic.title} (Level {topic.level.level_number})."
        if student_memory and student_memory.is_filled:
            system_content += f"\nStudent's own mental model: {student_memory.what_i_understood}. Real life analogy: {student_memory.real_life_analogy}."
        if topic_mistakes:
            system_content += f"\nStudent's past mistakes on this topic: {', '.join(topic_mistakes[:3])}."

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt_text}
            ],
            "max_tokens": 600,
            "temperature": 0.7
        }

        res = requests.post(url, headers=headers, json=payload, timeout=10)
        res.raise_for_status()
        data = res.json()
        return data["choices"][0]["message"]["content"]
