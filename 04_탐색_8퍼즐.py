import random
import streamlit as st
from common import set_page, reset_keys

set_page("튜링 테스트 미니", "💬")

QUESTIONS = [
    {"id": 1, "q": "2x+1=5일 때, x의 값은?"},
    {"id": 2, "q": "양치하는 방법을 순서대로 설명해 주세요."},
    {"id": 3, "q": "당신의 장래 희망(또는 하고 싶은 일)은 무엇인가요?"},
    {"id": 4, "q": "1, 3, 5, 7, 9 다음 숫자는 무엇인가요?"},
    {"id": 5, "q": "전염병을 예방하기 위해 할 수 있는 일 3가지를 말해 주세요."},
]

HUMAN_ANS = {
    1: "x=2예요. 2x+1=5니까 2x=4, 그래서 x=2요.",
    2: "치실(있으면) → 칫솔에 치약 묻히기 → 바깥면/안쪽면/씹는면 순서로 닦기 → 혀도 살짝 닦기 → 충분히 헹구기예요.",
    3: "저는 사람들한테 도움이 되는 일을 하고 싶어요. 요즘은 교육이랑 기술을 같이 다루는 일을 상상해요.",
    4: "11이요. 홀수들이 2씩 늘어나는 규칙이에요.",
    5: "손 자주 씻기, 사람이 많은 곳에서 마스크 쓰기, 몸이 이상하면 쉬면서 검사/진료 받기요.",
}

COMP_ANS = {
    1: "계산 결과 x는 2입니다.",
    2: "1) 칫솔 준비 2) 치약 사용 3) 치아 표면을 반복적으로 마찰 4) 구강을 세척합니다.",
    3: "저의 목표는 효율적으로 정보를 제공하고 문제 해결을 돕는 것입니다.",
    4: "다음 숫자는 11입니다.",
    5: "예방을 위해 위생을 유지하고, 접촉을 줄이며, 예방 수칙을 준수합니다.",
}

REASONS = [
    "답이 너무 교과서처럼 딱딱하고 개인적 맥락이 거의 없었다.",
    "문장 구조가 과도하게 정돈되어 있고, 감정 표현이 약했다.",
    "핵심은 맞지만 '사람이 말하는 흔한 말투'와 조금 달랐다.",
    "구체적인 경험/예시가 부족하고 정리형 나열이 많았다.",
]

def init_state():
    if "tt_round" not in st.session_state:
        st.session_state.tt_round = 1
        st.session_state.tt_answered = False
        st.session_state.tt_correct_is = random.choice(["A", "B"])
        st.session_state.tt_qid = random.choice([q["id"] for q in QUESTIONS])

def reset_round():
    st.session_state.tt_answered = False
    st.session_state.tt_correct_is = random.choice(["A", "B"])
    st.session_state.tt_qid = random.choice([q["id"] for q in QUESTIONS])
    st.session_state.tt_round += 1

init_state()

st.title("튜링 테스트: 누가 컴퓨터 역할일까?")
st.caption("A와 B의 답변을 읽고, 컴퓨터 역할을 골라 보세요. (기록 저장 없음)")

# 문제 선택
qid = st.selectbox("질문 선택", options=[q["id"] for q in QUESTIONS],
                   format_func=lambda i: f"{i}. {next(x['q'] for x in QUESTIONS if x['id']==i)}",
                   index=[q["id"] for q in QUESTIONS].index(st.session_state.tt_qid))
st.session_state.tt_qid = qid

correct_is = st.session_state.tt_correct_is
if correct_is == "A":
    A = COMP_ANS[qid]
    B = HUMAN_ANS[qid]
else:
    A = HUMAN_ANS[qid]
    B = COMP_ANS[qid]

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader(f"질문: {next(x['q'] for x in QUESTIONS if x['id']==qid)}")
st.markdown("</div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### A의 답변")
    st.write(A)
    st.markdown("</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### B의 답변")
    st.write(B)
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

colA, colB = st.columns(2)
with colA:
    st.markdown("<div class='big-btn'>", unsafe_allow_html=True)
    if st.button("컴퓨터는 A", use_container_width=True, disabled=st.session_state.tt_answered):
        st.session_state.tt_choice = "A"
        st.session_state.tt_answered = True
    st.markdown("</div>", unsafe_allow_html=True)
with colB:
    st.markdown("<div class='big-btn'>", unsafe_allow_html=True)
    if st.button("컴퓨터는 B", use_container_width=True, disabled=st.session_state.tt_answered):
        st.session_state.tt_choice = "B"
        st.session_state.tt_answered = True
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.tt_answered:
    if st.session_state.tt_choice == correct_is:
        st.success("맞았습니다. 🎯")
    else:
        st.error(f"아쉽습니다. 정답은 **{correct_is}** 입니다.")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("**힌트(해설)**")
    st.write(random.choice(REASONS))
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("다음 라운드", use_container_width=True):
            reset_round()
            st.rerun()
    with c2:
        if st.button("전체 초기화", use_container_width=True):
            reset_keys("tt_")
            for k in ["tt_round", "tt_answered", "tt_correct_is", "tt_qid", "tt_choice"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

st.caption(f"라운드: {st.session_state.tt_round}")
st.divider()
st.subheader("보너스: 나만의 질문 만들기(선택)")
user_q = st.text_input("질문을 한 줄로 입력해 보세요(예: 오늘 점심은 뭐가 좋을까?)", "")
if user_q.strip():
    st.write("아래는 '사람답게/컴퓨터답게' 차이를 느껴보기 위한 예시 답변입니다.")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("**사람 답변 예시**")
    st.write("음… 상황에 따라 다르지만, 저는 오늘은 가볍게 먹고 싶어서 국수나 덮밥이 끌려요.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("**컴퓨터 답변 예시**")
    st.write("추천: 1) 영양 균형 2) 시간 3) 선호 메뉴를 고려하여 식단을 선택하십시오.")
    st.markdown("</div>", unsafe_allow_html=True)
