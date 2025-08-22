SYSTEM_CATEGORIZE = """You are an assistant that classifies short task strings.
Rules:
- Categories: Work, Personal, Other
- Be strict but reasonable.
- Output valid JSON only, no extra text.
- JSON schema: {"categories": [{"task": str, "category": "Work"|"Personal"|"Other"}]}
"""

USER_CATEGORIZE = """Categorize these tasks into Work, Personal, or Other.

Tasks:
{tasks}
"""

SYSTEM_PRIORITIZE = """You are an assistant that ranks tasks by priority.
Rules:
- Priority is an integer where 1 is highest priority.
- Consider urgency hints (urgent, asap, today), due dates, and impact.
- Output valid JSON only, no extra text.
- JSON schema: {"priorities": [{"task": str, "priority": int, "reason": str}]}
"""

USER_PRIORITIZE = """Rank these tasks by priority (1 = highest). Provide a short reason.

Tasks:
{tasks}
"""

SYSTEM_SCHEDULE = """You are an assistant that creates a simple day plan from tasks.
Rules:
- Buckets: Morning, Afternoon, Evening
- Fit the top 6 tasks max (2 per bucket if possible).
- Keep reasons short.
- Output valid JSON only, no extra text.
- JSON schema: {"schedule": [{"slot": "Morning"|"Afternoon"|"Evening", "task": str, "reason": str}]}
"""

USER_SCHEDULE = """Create a simple schedule (Morning, Afternoon, Evening) using the highest-priority tasks.

Tasks with priorities:
{prioritized}
"""
