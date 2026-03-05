import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

def set_page(title: str, icon: str = "🤖"):
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")
    _inject_css()

def _inject_css():
    st.markdown(
        """
        <style>
          .big-btn button { width: 100%; height: 3.2rem; font-size: 1.2rem; }
          .center { text-align:center; }
          .muted { color: rgba(49,51,63,0.6); }
          .card { border: 1px solid rgba(49,51,63,0.15); border-radius: 16px; padding: 16px 18px; background: rgba(255,255,255,0.6); }
          .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
          .grid3 { display:grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        </style>
        """,
        unsafe_allow_html=True
    )

def pill(text: str):
    st.markdown(f"<span style='display:inline-block;padding:2px 10px;border-radius:999px;border:1px solid rgba(49,51,63,0.2);font-size:0.9rem;'>{text}</span>", unsafe_allow_html=True)

def reset_keys(prefix: str):
    # session_state에서 특정 접두사 키들을 제거
    for k in list(st.session_state.keys()):
        if k.startswith(prefix):
            del st.session_state[k]
