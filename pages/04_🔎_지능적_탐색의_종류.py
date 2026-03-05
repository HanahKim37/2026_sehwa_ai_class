import streamlit as st
    from common import set_page, hero, card_start, card_end, ox_quiz, report_section, load_ox

    set_page("지능적 탐색의 종류", "🔎")

    hero(
        "🔎 지능적 탐색의 종류",
        "맹목적 탐색(깊이/너비)과 정보 이용 탐색(최상 우선/A*)을 비교하고, 탐색 순서를 직접 맞혀 봅니다.",
        tags=["맹목적", "정보 이용", "○×", "미니 시뮬"]
    )

    card_start()
    st.markdown("## 📘 교과서 핵심 개념")
    st.write("**맹목적 탐색**: 탐색에 대한 정보나 관련 경험을 활용하지 않고, 규칙에 따라 목표 상태를 찾을 때까지 다음 상태를 탐색합니다.")
    st.write("→ 예: **깊이 우선 탐색**, **너비 우선 탐색**")
    st.write("**정보 이용 탐색**: 관련 경험이나 지식을 활용해 효율성을 고려하며 탐색합니다.")
    st.write("→ 예: **최상 우선 탐색**, **A***")
    card_end()

    st.divider()

    qs = load_ox("data/ox_unit4.json")
    ox_res = ox_quiz(key_prefix="u4ox", questions=qs)

    st.divider()

    st.markdown("<div class='section-title'>🧩 미니 시뮬: 다음에 방문할 노드는?</div>", unsafe_allow_html=True)
    st.caption("아래 작은 트리를 보고, 탐색 규칙에 따라 ‘다음 방문 노드’를 골라 보세요.")

    st.markdown("**트리(왼쪽부터 방문한다고 가정)**")
    st.code("""A
├─ B
│  ├─ D
│  └─ E
└─ C
   ├─ F
   └─ G""", language="text")

    st.write("현재까지 방문: **A → B** (B에서 다음으로 진행)")
    dfs_next = "D"
    bfs_next = "C"

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🕳️ 깊이 우선(DFS)")
        pick1 = st.radio("다음 노드", options=["C", "D", "E"], horizontal=True, key="u4_dfs")
        if st.button("DFS 정답 확인", use_container_width=True):
            if pick1 == dfs_next:
                st.success("정답입니다. (가능한 한 ‘깊게’)")
            else:
                st.error(f"정답은 **{dfs_next}** 입니다.")
            st.info("깊이 우선 탐색은 한 갈래를 가능한 깊게 진행하다가 막히면 되돌아갑니다.")
    with col2:
        st.markdown("### 🌊 너비 우선(BFS)")
        pick2 = st.radio("다음 노드", options=["C", "D", "E"], horizontal=True, key="u4_bfs")
        if st.button("BFS 정답 확인", use_container_width=True):
            if pick2 == bfs_next:
                st.success("정답입니다. (같은 깊이를 먼저)")
            else:
                st.error(f"정답은 **{bfs_next}** 입니다.")
            st.info("너비 우선 탐색은 같은 깊이에 있는 노드를 먼저 모두 방문한 뒤 다음 깊이로 진행합니다.")

    def build_results():
        acts = [{"name": "탐색 순서 미니 시뮬", "desc": "DFS/BFS에서 다음 노드를 예측"}]
        return {"ox": ox_res, "activities": acts}

    report_section(unit_key="u4", unit_title="지능적 탐색의 종류", build_results_fn=build_results)
