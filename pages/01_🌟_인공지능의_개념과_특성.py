import random
import streamlit as st
from common import set_page, hero, card_start, card_end, ox_quiz, report_section, load_ox

set_page("인공지능의 개념과 특성", "🌟")

hero(
    "🌟 인공지능의 개념과 특성",
    "‘인공지능’의 뜻과 활용 사례를 정리하고, 튜링 테스트를 통해 인공지능의 특성을 체감합니다.",
    tags=["교과서 핵심", "○×", "튜링 테스트"]
)

# 1) 교과서 핵심 개념
card_start()
st.markdown("## 📘 교과서 핵심 개념")
st.write("인공지능은 인간이 가진 지적 능력(인식·학습·추론·문제 해결 등)의 일부 또는 전체를 컴퓨팅 시스템으로 구현한 ‘인공적인 지능’입니다.")
st.write("교과서에서 ‘지능’은 새로운 대상이나 상황의 의미를 이해하고, 합리적으로 적응하는 방법을 알아내는 지적 활동 능력으로 설명합니다.")
st.write("인공지능은 챗봇, 자율 주행, 의료 진단 등 실생활과 다양한 연구 분야에서 활용됩니다.")
card_end()

st.divider()

# 2) OX
qs = load_ox("data/ox_unit1.json")
ox_res = ox_quiz(key_prefix="u1ox", questions=qs)

st.divider()

# 3) 튜링 테스트 미니
st.markdown("<div class='section-title'>💬 튜링 테스트 미니 체험</div>", unsafe_allow_html=True)
st.caption("A와 B의 답변 중 ‘컴퓨터 역할’을 골라 보세요. (정답/해설은 즉시 공개)")

QUESTIONS = [
    ("2x+1=5일 때, x의 값은?", "x=2예요. 2x+1=5니까 2x=4, 그래서 x=2요.", "계산 결과 x는 2입니다."),
    ("양치하는 방법을 순서대로 설명해 주세요.", "치실(있으면) → 칫솔에 치약 → 바깥/안쪽/씹는면 → 혀 → 헹굼이에요.", "1) 칫솔 준비 2) 치약 사용 3) 치아를 반복적으로 마찰 4) 구강 세척"),
    ("전염병을 예방하기 위해 할 수 있는 일 3가지는?", "손 씻기, 사람이 많은 곳에서 마스크, 몸이 이상하면 쉬고 진료받기요.", "위생 유지, 접촉 감소, 예방 수칙을 준수합니다."),
    ("사랑은 무엇이라고 생각하나요?", "사람마다 다른데… 저는 서로를 지켜주고 싶어지는 마음 같아요.", "사랑은 긍정적 감정 및 관계 유지를 의미합니다."),
]

if "u1_tt_log" not in st.session_state:
    st.session_state.u1_tt_log = []

q_text, human, comp = random.choice(QUESTIONS)
correct_is = random.choice(["A", "B"])
A = comp if correct_is == "A" else human
B = human if correct_is == "A" else comp

card_start()
st.markdown(f"### ❓ 질문: {q_text}")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**A의 답변**")
    st.write(A)
with col2:
    st.markdown("**B의 답변**")
    st.write(B)

c1, c2 = st.columns(2)
with c1:
    pickA = st.button("컴퓨터는 A", use_container_width=True)
with c2:
    pickB = st.button("컴퓨터는 B", use_container_width=True)
card_end()

def _record(choice: str):
    ok = (choice == correct_is)
    st.session_state.u1_tt_log.append({
        "q": q_text,
        "choice": choice,
        "answer": correct_is,
        "is_correct": ok
    })
    return ok

if pickA or pickB:
    choice = "A" if pickA else "B"
    ok = _record(choice)
    if ok:
        st.success("맞았습니다. 🎯")
    else:
        st.error(f"아쉽습니다. 정답은 **{correct_is}** 입니다.")
    st.info("힌트: 문장이 지나치게 정돈되어 있거나 개인적 맥락이 거의 없을 때, ‘컴퓨터답다’고 느끼는 경우가 많습니다.")

if st.session_state.u1_tt_log:
    with st.expander("내 기록 보기(이번 접속 동안만)", expanded=False):
        for i, it in enumerate(st.session_state.u1_tt_log, start=1):
            icon = "✅" if it["is_correct"] else "❌"
            st.write(f"{icon} {i}. 선택={it['choice']} / 정답={it['answer']} · 질문: {it['q']}")

# Report
def build_results():
    acts = []
    if st.session_state.get("u1_tt_log"):
        correct = sum(1 for x in st.session_state.u1_tt_log if x["is_correct"])
        acts.append({"name": "튜링 테스트", "desc": f"시도 {len(st.session_state.u1_tt_log)}회 · 정답 {correct}회"})
    return {"ox": ox_res, "activities": acts}

report_section(unit_key="u1", unit_title="인공지능의 개념과 특성", build_results_fn=build_results)
