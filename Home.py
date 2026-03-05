import streamlit as st
from common import set_page, hero, card_start, card_end

set_page("AI 기초 연습(고2)", "✨")

hero(
    "✨ 인공지능 기초 연습 사이트",
    "고2 ‘인공지능 기초’ 수업용 연습 페이지입니다. 각 단원은 왼쪽 메뉴에서 선택하세요.",
    tags=["기록 없음", "노트북 최적화", "개념+실습 순서"]
)

col1, col2, col3 = st.columns(3)
with col1:
    card_start()
    st.markdown("### 🌟 인공지능의 개념과 특성")
    st.write("교과서 핵심 개념 → ○× 개념 확인 → 튜링 테스트 미니 체험")
    card_end()
with col2:
    card_start()
    st.markdown("### 🧠 인공지능과 문제 해결")
    st.write("생활 속 문제를 ‘인공지능 관점’으로 바꾸어 보고, 해결 방안을 작성해 봅니다.")
    card_end()
with col3:
    card_start()
    st.markdown("### 🧭~🗺️ 탐색 단원")
    st.write("탐색 개념 → 탐색 종류 → 실제 실습(틱택토/8-퍼즐/길찾기 A*)")
    card_end()

st.divider()
st.info("각 단원 페이지 하단에는 ‘PDF 결과 보고서’가 있습니다. 학번/이름을 입력하면 현재 결과를 내려받을 수 있습니다.")
