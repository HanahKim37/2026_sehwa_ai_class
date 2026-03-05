import streamlit as st
from common import set_page, hero, card_start, card_end, ox_quiz, report_section, load_ox

set_page("인공지능과 문제 해결", "🧠")

hero(
    "🧠 인공지능과 문제 해결",
    "실생활의 불편을 ‘인공지능 관점’으로 다시 보고, 해결 방안을 스스로 설계해 봅니다.",
    tags=["교과서 사례", "○×", "문제→해결"]
)

# 1) 핵심 개념
card_start()
st.markdown("## 📘 교과서 핵심 개념")
st.write("챗봇 서비스는 사용자가 질문을 하면 인공지능이 답변하는 서비스입니다.")
st.write("교과서는 앞으로 인공지능이 일상적인 문제 해결뿐 아니라 더 많은 곳에서 활용될 것으로 예상한다고 설명합니다.")
st.write("인공지능은 긴 정보를 요약하거나, 다양한 데이터를 수집·분석해 예측과 대응을 돕는 방식으로 문제 해결에 활용될 수 있습니다.")
card_end()

st.divider()

# 2) OX
qs = load_ox("data/ox_unit2.json")
ox_res = ox_quiz(key_prefix="u2ox", questions=qs)

st.divider()

# 3) 실습: 문제 → 해결 방안 작성
st.markdown("<div class='section-title'>🛠️ 실습: ‘문제점 → 인공지능 해결 방안’ 작성</div>", unsafe_allow_html=True)
st.caption("아래 예시 중 하나를 고르거나, 직접 문제를 적어 보고 인공지능을 이용한 해결 방안을 작성해 보세요.")

examples = [
    {
        "title": "긴 영상 때문에 불필요한 내용까지 오래 시청해야 한다.",
        "sample": "인공지능 비디오 요약 서비스를 활용해 핵심(하이라이트)만 요약 영상으로 받아 본다(뉴스 요약, 강의 정리 등)."
    },
    {
        "title": "수질 오염 문제를 해결하는 데 어려움이 있다.",
        "sample": "공공데이터·기상 데이터 등을 수집해 수질 오염을 예측하고, 오염을 발견하면 주변 로봇에 신호를 보내 정화 작업을 진행한다."
    },
    {
        "title": "나의 생활 속 불편(직접 선택)",
        "sample": "예: 학교/교통/학습/건강 등에서 데이터를 모아 예측·추천·자동화로 해결할 수 있는지 생각해 본다."
    }
]

choice = st.selectbox("문제 선택", options=[e["title"] for e in examples])
picked = next(e for e in examples if e["title"] == choice)

st.markdown("**① 문제점(한 줄)**")
problem_text = st.text_area("문제점", value=choice if choice != "나의 생활 속 불편(직접 선택)" else "", height=80, key="u2_problem")

st.markdown("**② 인공지능을 이용한 해결 방안(2~5줄)**")
solution_text = st.text_area("해결 방안", height=120, key="u2_solution")

show = st.checkbox("교과서 예시 해설 보기", value=False)
if show:
    st.info(picked["sample"])

st.markdown("**③ 한 번 더 생각해 보기(선택)**")
data_text = st.text_input("이 해결 방안에 필요한 데이터는 무엇일까? (예: 이용 기록, 시간표, 센서 값…)", key="u2_data")

# store note for report
def build_results():
    acts = []
    note_lines = []
    if problem_text.strip() or solution_text.strip():
        acts.append({"name": "문제 해결 설계", "desc": "문제점과 해결 방안을 작성함"})
        note_lines.append(f"[문제점]\n{problem_text.strip()}")
        note_lines.append(f"\n[해결 방안]\n{solution_text.strip()}")
        if data_text.strip():
            note_lines.append(f"\n[필요 데이터(선택)]\n{data_text.strip()}")
        if show:
            note_lines.append(f"\n[교과서 예시(참고)]\n{picked['sample']}")
    note = "\n".join(note_lines) if note_lines else ""
    return {"ox": ox_res, "activities": acts, "note": note}

report_section(unit_key="u2", unit_title="인공지능과 문제 해결", build_results_fn=build_results)
