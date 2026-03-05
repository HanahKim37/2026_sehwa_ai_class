import streamlit as st
from common import set_page

set_page("탐색 종류 정리", "📌")

st.title("탐색 종류 정리(한 장 요약)")
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("큰 분류")
st.write("- **맹목적 탐색**: 정보 없이 규칙에 따라 목표를 찾을 때까지 탐색(예: 깊이 우선, 너비 우선)")
st.write("- **정보 이용 탐색**: 경험/지식/평가함수 같은 정보를 활용해 불필요한 탐색을 줄임(예: 최상 우선, A*)")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("핵심 비교")
st.write("- **깊이 우선 탐색**: 한 갈래를 깊게 → 막히면 되돌아감(백트래킹)")
st.write("- **너비 우선 탐색**: 같은 깊이의 노드를 먼저 모두 탐색")
st.write("- **A***: f(n)=g(n)+h(n) (누적 거리 + 남은 거리 추정)")
st.markdown("</div>", unsafe_allow_html=True)

st.info("왼쪽 메뉴의 ○,× 문항으로 바로 확인해 볼 수 있습니다.")
