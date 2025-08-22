import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from gemini_agent import TaskAgentGemini, GeminiConfig

# from agent import TaskAgent, LLMConfig
from prompts import (
    SYSTEM_CATEGORIZE, USER_CATEGORIZE,
    SYSTEM_PRIORITIZE, USER_PRIORITIZE,
    SYSTEM_SCHEDULE, USER_SCHEDULE,
)

# --- Setup ---
load_dotenv()
st.set_page_config(page_title="Personal Task Agent", layout="wide")

st.title("🧠 Personal Task Agent")
st.caption("Paste tasks, then let AI categorize, prioritize, and draft a simple day plan.")

with st.expander("➕ Tips / Format", expanded=False):
    st.markdown(
        "- Enter one task per line (e.g., `Submit Q3 report by Friday`, `Book dentist`, `Fix login bug (urgent)`).\n"
        "- The agent will infer categories (Work/Personal/Other) and urgency.\n"
        "- Use the **Daily Schedule** button to get a Morning/Afternoon/Evening plan."
    )

# --- Input area ---
tasks_text = st.text_area("Tasks (one per line)", height=200, placeholder="Write report by Friday\nFix login bug (urgent)\nBook dentist\nGroceries\nPrepare team presentation")

left, right = st.columns([1, 1], gap="large")

# Instantiate agent lazily to allow UI to render without key
def get_agent():
    # cfg = LLMConfig()
    return TaskAgentGemini(GeminiConfig())

# Session state for results
if "categories" not in st.session_state:
    st.session_state["categories"] = None
if "priorities" not in st.session_state:
    st.session_state["priorities"] = None
if "schedule" not in st.session_state:
    st.session_state["schedule"] = None

def parse_tasks(text: str):
    tasks = [t.strip() for t in text.splitlines() if t.strip()]
    uniq = []
    seen = set()
    for t in tasks:
        if t not in seen:
            uniq.append(t)
            seen.add(t)
    return uniq

with left:
    if st.button("📂 Categorize"):
        if not tasks_text.strip():
            st.warning("Please enter some tasks first.")
        else:
            tasks = parse_tasks(tasks_text)
            try:
                agent = get_agent()
                from prompts import USER_CATEGORIZE as U
                cats = agent.categorize(
                    tasks,
                    system_prompt=SYSTEM_CATEGORIZE,
                    user_prompt=U.format(tasks="\n".join(f"- {t}" for t in tasks)),
                )
                st.session_state.categories = cats
                st.success("Categorized ✅")
            except Exception as e:
                st.error(f"Categorization failed: {e}")

    if st.button("🔥 Prioritize"):
        if not tasks_text.strip():
            st.warning("Please enter some tasks first.")
        else:
            tasks = parse_tasks(tasks_text)
            try:
                agent = get_agent()
                pr = agent.prioritize(
                    tasks,
                    system_prompt=SYSTEM_PRIORITIZE,
                    user_prompt=USER_PRIORITIZE.format(tasks="\n".join(f"- {t}" for t in tasks)),
                )
                st.session_state.priorities = pr
                st.success("Prioritized ✅")
            except Exception as e:
                st.error(f"Prioritization failed: {e}")

with right:
    if st.button("🗓️ Daily Schedule"):
        if not st.session_state.get("priorities"):
            # if no priorities yet, compute them first
            if not tasks_text.strip():
                st.warning("Please enter some tasks first.")
            else:
                tasks = parse_tasks(tasks_text)
                try:
                    agent = get_agent()
                    pr = agent.prioritize(
                        tasks,
                        system_prompt=SYSTEM_PRIORITIZE,
                        user_prompt=USER_PRIORITIZE.format(tasks="\n".join(f"- {t}" for t in tasks)),
                    )
                    st.session_state.priorities = pr
                except Exception as e:
                    st.error(f"Prioritization failed: {e}")
        if st.session_state.get("priorities"):
            try:
                agent = get_agent()
                pr = st.session_state.priorities
                pr_str = "\n".join(f"{i+1}. {p.task} (p={p.priority})" for i, p in enumerate(pr.priorities))
                sched = agent.schedule(
                    pr,
                    system_prompt=SYSTEM_SCHEDULE,
                    user_prompt=USER_SCHEDULE.format(prioritized=pr_str),
                )
                st.session_state.schedule = sched
                st.success("Schedule ready ✅")
            except Exception as e:
                st.error(f"Schedule failed: {e}")

# --- Output sections ---
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📂 Categories")
    cats = st.session_state.get("categories")
    if cats:
        df = pd.DataFrame([{"Task": c.task, "Category": c.category} for c in cats.categories])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.caption("Run **Categorize** to see categories.")

with col2:
    st.subheader("🔥 Priorities")
    pr = st.session_state.get("priorities")
    if pr:
        df = pd.DataFrame([{"Task": p.task, "Priority": p.priority, "Reason": p.reason} for p in pr.priorities])
        df = df.sort_values("Priority")
        st.dataframe(df, use_container_width=True, hide_index=True)
        if len(df):
            top = df.sort_values("Priority").iloc[0]["Task"]
            st.success(f"Suggested next task: **{top}**")
    else:
        st.caption("Run **Prioritize** to see ranking.")

with col3:
    st.subheader("🗓️ Day Plan")
    sch = st.session_state.get("schedule")
    if sch:
        df = pd.DataFrame([{"Slot": s.slot, "Task": s.task, "Reason": s.reason} for s in sch.schedule])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.caption("Click **Daily Schedule** to draft a plan.")

st.divider()
st.caption("Pro tip: add hints like “urgent”, “today”, or due dates to help the agent prioritize better.")
