import streamlit as st
from common import set_page, hero, card_start, card_end, ox_quiz, report_section, load_ox

set_page("인공지능과 탐색", "🧭")

hero(
    "🧭 인공지능과 탐색",
    "‘초기 상태 → 목표 상태’로 가는 길을 찾는 탐색의 기본 개념을 정리하고, 탐색이 필요한 문제의 특징을 이해합니다.",
    tags=["초기/목표", "○×", "탐색 준비"]
)

card_start()
st.markdown("## 📘 교과서 핵심 개념")
st.write("탐색은 **초기 상태에서 목표 상태를 찾아가는 과정**입니다.")
st.write("교과서에서는 지능적 탐색이 필요한 문제의 특징을 다음과 같이 설명합니다: 문제가 복잡하고, 해결 방법이 있으며, 가능한 해의 수가 많이 존재합니다.")
st.write("탐색이 필요한 대표 문제로 **경로 발견 문제(길 찾기·미로·8-퍼즐 등)**, **게임 문제(틱택토·바둑·체스 등)**가 소개됩니다.")
card_end()

st.divider()

qs = load_ox("data/ox_unit3.json")
ox_res = ox_quiz(key_prefix="u3ox", questions=qs)

st.divider()

st.markdown("<div class='section-title'>🧠 미니 체크: 이 문제는 어떤 유형일까?</div>", unsafe_allow_html=True)
st.caption("탐색 목적이 무엇인지에 따라 문제를 분류해 봅니다.")

problems = [
    ("스페인에서 오스트리아까지 가는 경로를 찾는다.", "경로 발견 문제", "목적지는 ‘최단 경로’(또는 효율적 경로)를 찾는 것입니다."),
    ("틱택토에서 상대를 이기기 위한 최선의 수를 고른다.", "게임 문제", "상대보다 먼저 이기는 것이 핵심 목적입니다."),
    ("8-퍼즐에서 목표 상태로 도달하는 이동 순서를 찾는다.", "경로 발견 문제", "목표 상태에 도달하는 경로(이동 순서)를 찾습니다."),
]

sel = st.selectbox("문제 선택", options=[p[0] for p in problems])
picked = next(p for p in problems if p[0] == sel)
guess = st.radio("분류", options=["경로 발견 문제", "게임 문제"], horizontal=True)

if st.button("정답 확인", use_container_width=True):
    if guess == picked[1]:
        st.success("정답입니다.")
    else:
        st.error(f"오답입니다. 정답은 **{picked[1]}** 입니다.")
    st.info(picked[2])

def build_results():
    acts = [{"name": "문제 유형 분류", "desc": "경로 발견/게임 문제를 분류해 봄"}]
    return {"ox": ox_res, "activities": acts}

report_section(unit_key="u3", unit_title="인공지능과 탐색", build_results_fn=build_results)
