import random
import streamlit as st
from common import set_page, reset_keys

set_page("탐색 체험: 8-퍼즐", "🧩")

GOAL = (1,2,3,4,5,6,7,8,0)  # 0 = 빈칸

def pretty(state):
    # 3x3 문자열
    rows = []
    for r in range(3):
        row = []
        for c in range(3):
            v = state[r*3+c]
            row.append("□" if v==0 else str(v))
        rows.append("  ".join(row))
    return "\n".join(rows)

def moves(state):
    z = state.index(0)
    r, c = divmod(z, 3)
    cand = []
    def swap(i,j):
        s = list(state)
        s[i], s[j] = s[j], s[i]
        return tuple(s)
    if r>0: cand.append(swap(z, z-3))
    if r<2: cand.append(swap(z, z+3))
    if c>0: cand.append(swap(z, z-1))
    if c<2: cand.append(swap(z, z+1))
    return cand

def match_count(state):
    # 목표 상태와 일치하는 칸 수(빈칸 제외)
    cnt = 0
    for i,v in enumerate(state):
        if v!=0 and v==GOAL[i]:
            cnt += 1
    return cnt

def scramble(steps=12):
    s = GOAL
    for _ in range(steps):
        s = random.choice(moves(s))
    return s

def init():
    if "puz_state" not in st.session_state:
        st.session_state.puz_state = scramble()
        st.session_state.puz_stage = 1
        st.session_state.puz_answered = False
        st.session_state.puz_choice = None
        st.session_state.puz_options = []

def new_round():
    opts = moves(st.session_state.puz_state)
    random.shuffle(opts)
    st.session_state.puz_options = opts[:3] if len(opts) >= 3 else opts
    st.session_state.puz_answered = False
    st.session_state.puz_choice = None

def reset():
    reset_keys("puz_")
    for k in ["puz_state","puz_stage","puz_answered","puz_choice","puz_options"]:
        if k in st.session_state:
            del st.session_state[k]

init()
if not st.session_state.puz_options:
    new_round()

st.title("8-퍼즐: '목표와 더 가까운 다음 상태' 고르기")
st.caption("평가 기준(간단 버전): **목표 상태와 일치하는 숫자 칸 수**가 더 많아지는 쪽이 '가까움'입니다.")

left, right = st.columns([1, 1.3])
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("현재 상태")
    st.code(pretty(st.session_state.puz_state), language="text")
    st.write(f"일치하는 칸 수: **{match_count(st.session_state.puz_state)}**")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.puz_state == GOAL:
        st.success("목표 상태에 도달했습니다! 🎉")
        if st.button("새 퍼즐", use_container_width=True):
            reset()
            st.rerun()
        st.stop()

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("다음 상태 후보(하나 선택)")
    opts = st.session_state.puz_options

    labels = []
    for i, s in enumerate(opts):
        labels.append(f"후보 {i+1} (일치 {match_count(s)}칸)")

    choice = st.radio("선택", options=list(range(len(opts))), format_func=lambda i: labels[i], index=0, disabled=st.session_state.puz_answered)
    st.session_state.puz_choice = choice

    c1, c2 = st.columns(2)
    with c1:
        if st.button("정답/해설 보기", use_container_width=True, disabled=st.session_state.puz_answered):
            st.session_state.puz_answered = True
    with c2:
        if st.button("후보 다시 뽑기", use_container_width=True, disabled=st.session_state.puz_answered):
            new_round()
            st.rerun()

    # 후보 보드 표시
    for i, s in enumerate(opts):
        st.markdown(f"**후보 {i+1}**")
        st.code(pretty(s), language="text")

    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.puz_answered:
    opts = st.session_state.puz_options
    scores = [match_count(s) for s in opts]
    best_i = max(range(len(opts)), key=lambda i: scores[i])
    if st.session_state.puz_choice == best_i:
        st.success("선택이 좋습니다. 목표 상태에 더 가까워집니다.")
    else:
        st.error(f"가장 가까운 후보는 **후보 {best_i+1}** 입니다.")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("**해설**: 이 페이지에서는 '목표와 일치하는 칸 수'로 가까움을 판단합니다. (정보를 이용한 탐색의 가장 단순한 감각 체험)")
    st.write("각 후보의 일치 칸 수:", ", ".join([f"후보{i+1}={scores[i]}칸" for i in range(len(opts))]))
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("내 선택대로 진행", use_container_width=True):
            st.session_state.puz_state = opts[st.session_state.puz_choice]
            new_round()
            st.rerun()
    with c2:
        if st.button("가장 좋은 후보로 진행", use_container_width=True):
            st.session_state.puz_state = opts[best_i]
            new_round()
            st.rerun()
    with c3:
        if st.button("처음부터(새 퍼즐)", use_container_width=True):
            reset()
            st.rerun()
