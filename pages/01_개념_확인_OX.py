import json
import random
import streamlit as st
from common import set_page, reset_keys

set_page("개념 확인(○,×)", "✅")

DATA_PATH = "data/ox_questions.json"

def load_questions():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def init_state():
    if "ox_order" not in st.session_state:
        qs = load_questions()
        order = list(range(len(qs)))
        random.shuffle(order)
        st.session_state.ox_order = order
        st.session_state.ox_idx = 0
        st.session_state.ox_answered = False
        st.session_state.ox_choice = None
        st.session_state.ox_correct = 0

def reset_all():
    reset_keys("ox_")
    for k in ["ox_order", "ox_idx", "ox_answered", "ox_choice", "ox_correct"]:
        if k in st.session_state:
            del st.session_state[k]

init_state()
qs = load_questions()
order = st.session_state.ox_order
idx = st.session_state.ox_idx

st.title("개념 확인: ○,×")
st.caption("선택 즉시 정답/해설이 아래에 표시됩니다. (기록 저장 없음)")

if idx >= len(order):
    st.success(f"끝! 정답 {st.session_state.ox_correct} / {len(order)}")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("처음부터 다시", use_container_width=True):
            reset_all()
            st.rerun()
    with c2:
        if st.button("문항 다시 섞기", use_container_width=True):
            reset_all()
            st.rerun()
    st.stop()

q = qs[order[idx]]
st.markdown(f"""<div class='card'>
<div class='muted'>단원: {q['unit']}</div>
<h3 style='margin-top:8px;'>Q{idx+1}. {q['q']}</h3>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='big-btn'>", unsafe_allow_html=True)
    if st.button("○", use_container_width=True, disabled=st.session_state.ox_answered):
        st.session_state.ox_choice = "O"
        st.session_state.ox_answered = True
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='big-btn'>", unsafe_allow_html=True)
    if st.button("×", use_container_width=True, disabled=st.session_state.ox_answered):
        st.session_state.ox_choice = "X"
        st.session_state.ox_answered = True
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.ox_answered:
    correct = (st.session_state.ox_choice == q["a"])
    if correct:
        st.success("정답입니다.")
        # 중복 가산 방지: 현재 문항에서 처음 맞힐 때만
        if "ox_scored_idx" not in st.session_state:
            st.session_state.ox_scored_idx = set()
        if idx not in st.session_state.ox_scored_idx:
            st.session_state.ox_correct += 1
            st.session_state.ox_scored_idx.add(idx)
    else:
        st.error(f"오답입니다. 정답은 **{ '○' if q['a']=='O' else '×' }** 입니다.")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"**해설**: {q['exp']}")
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("다음 문항", use_container_width=True):
            st.session_state.ox_idx += 1
            st.session_state.ox_answered = False
            st.session_state.ox_choice = None
            st.rerun()
    with c2:
        if st.button("이 문항 다시 보기", use_container_width=True):
            st.session_state.ox_answered = False
            st.session_state.ox_choice = None
            st.rerun()
    with c3:
        if st.button("전체 초기화", use_container_width=True):
            reset_all()
            st.rerun()

st.divider()
st.caption(f"진행: {idx+1}/{len(order)} · 현재 정답 수: {st.session_state.ox_correct}")
