import streamlit as st
from common import set_page, pill

set_page("인공지능 기초 연습(정적 기록 없음)", "🤖")

st.title("인공지능 기초 연습 사이트")
st.write("이 사이트는 **기록을 남기지 않는 연습용**입니다. 각 단원은 왼쪽 메뉴에서 선택할 수 있습니다.")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("1) 개념 확인(○,×)")
    st.write("핵심 개념을 짧게 확인하고, 선택 즉시 정답과 해설을 확인합니다.")
    pill("빠른 반복")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("2) 튜링 테스트")
    st.write("A와 B의 답변을 읽고, 누가 '컴퓨터 역할'인지 추리합니다.")
    pill("판단 근거 연습")
    st.markdown("</div>", unsafe_allow_html=True)

with c3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("3) 탐색 체험")
    st.write("틱택토, 8-퍼즐, 길찾기(A*)를 직접 해 보며 탐색을 체감합니다.")
    pill("직접 조작")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.info("왼쪽 메뉴에서 단원을 선택해 시작하세요. (노트북 화면 기준으로 제작)")
