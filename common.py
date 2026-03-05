import heapq
import streamlit as st
from common import set_page, reset_keys

set_page("탐색 체험: 길찾기(A*)", "🗺️")

# 나라 그래프(교재 활동 흐름을 기준으로 단순화)
NODES = ["스페인","포르투갈","프랑스","이탈리아","스위스","독일","체코","폴란드","오스트리아"]

# 직선거리 h(n) (오스트리아까지)
H = {
    "스페인": 200,
    "포르투갈": 170,
    "프랑스": 150,
    "이탈리아": 110,
    "스위스": 120,
    "독일": 90,
    "체코": 40,
    "폴란드": 40,
    "오스트리아": 0,
}

# 연결(가중치: 두 나라 간 거리). 수치들은 활동 예시의 진행을 재현하기 위한 값(단순화).
G = {
    "스페인": {"포르투갈": 50, "프랑스": 60},
    "포르투갈": {"스페인": 50},
    "프랑스": {"스페인": 60, "독일": 100, "스위스": 80, "이탈리아": 100},
    "이탈리아": {"프랑스": 100, "스위스": 30},
    "스위스": {"프랑스": 80, "이탈리아": 30, "독일": 40, "오스트리아": 60},
    "독일": {"프랑스": 100, "스위스": 40, "체코": 10, "폴란드": 30},
    "체코": {"독일": 10, "오스트리아": 50},
    "폴란드": {"독일": 30, "오스트리아": 70},
    "오스트리아": {"체코": 50, "폴란드": 70, "스위스": 60},
}

START = "스페인"
GOAL = "오스트리아"

def astar(start, goal):
    # 반환: 경로, 단계 로그
    open_heap = []
    heapq.heappush(open_heap, (H[start], 0, start, None))  # f, g, node, parent
    best_g = {start: 0}
    parent = {start: None}
    logs = []

    open_set = {start}
    closed = set()

    while open_heap:
        f, g, node, _ = heapq.heappop(open_heap)
        if node not in open_set:
            continue
        open_set.remove(node)
        closed.add(node)

        logs.append({
            "선택": node,
            "g": g,
            "h": H[node],
            "f": f,
            "OPEN": sorted([(n, best_g.get(n, 10**9) + H[n]) for n in open_set], key=lambda x: x[1]),
            "CLOSED": list(closed),
        })

        if node == goal:
            break

        for nxt, w in G[node].items():
            if nxt in closed:
                continue
            ng = g + w
            if ng < best_g.get(nxt, 10**9):
                best_g[nxt] = ng
                parent[nxt] = node
                heapq.heappush(open_heap, (ng + H[nxt], ng, nxt, node))
                open_set.add(nxt)

    if goal not in parent:
        return None, logs

    # 경로 복원
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path, logs

def bfs_fewest_edges(start, goal):
    from collections import deque
    q = deque([start])
    parent = {start: None}
    while q:
        cur = q.popleft()
        if cur == goal:
            break
        for nxt in G[cur].keys():
            if nxt not in parent:
                parent[nxt] = cur
                q.append(nxt)
    if goal not in parent:
        return None
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return list(reversed(path))

def path_cost(path):
    if not path or len(path) == 1:
        return 0
    cost = 0
    for a,b in zip(path, path[1:]):
        cost += G[a][b]
    return cost

def init():
    if "pf_path" not in st.session_state:
        st.session_state.pf_path = [START]
        st.session_state.pf_cost = 0

def reset():
    reset_keys("pf_")
    for k in ["pf_path","pf_cost"]:
        if k in st.session_state:
            del st.session_state[k]

init()

st.title("길찾기: 스페인 → 오스트리아")
st.caption("학생이 직접 경로를 만들어 보고, 너비 우선 탐색(경유 국가 수 최소)과 A*(거리 고려)를 비교합니다.")

left, right = st.columns([1, 1.2])

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("직접 경로 만들기")
    cur = st.session_state.pf_path[-1]
    st.write(f"현재 위치: **{cur}**")
    st.write("현재 경로:", " → ".join(st.session_state.pf_path))
    st.write(f"누적 거리(간단 모델): **{st.session_state.pf_cost}**")

    if cur == GOAL:
        st.success("도착했습니다!")
    else:
        next_options = list(G[cur].keys())
        nxt = st.selectbox("다음으로 이동", options=next_options)
        if st.button("이동", use_container_width=True):
            st.session_state.pf_path.append(nxt)
            st.session_state.pf_cost += G[cur][nxt]
            st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("한 칸 되돌리기", use_container_width=True, disabled=len(st.session_state.pf_path)<=1):
            if len(st.session_state.pf_path) > 1:
                a = st.session_state.pf_path[-2]
                b = st.session_state.pf_path[-1]
                st.session_state.pf_cost -= G[a][b]
                st.session_state.pf_path = st.session_state.pf_path[:-1]
            st.rerun()
    with c2:
        if st.button("처음부터", use_container_width=True):
            reset()
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("h(n): 오스트리아까지의 추정 거리(직선 거리)")
    st.write(", ".join([f"{k}={v}" for k,v in H.items()]))
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("비교 결과")
    bfs_path = bfs_fewest_edges(START, GOAL)
    astar_path, logs = astar(START, GOAL)

    if bfs_path:
        st.write("**너비 우선 탐색(경유 국가 수 최소)**")
        st.write(" → ".join(bfs_path))
        st.write(f"경유 수(간선 수): {len(bfs_path)-1} · 거리(가중치 합): {path_cost(bfs_path)}")

    if astar_path:
        st.write("**A* (f(n)=g(n)+h(n))**")
        st.write(" → ".join(astar_path))
        st.write(f"경유 수(간선 수): {len(astar_path)-1} · 거리(가중치 합): {path_cost(astar_path)}")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("A* 진행(간단 로그)")
    if st.checkbox("단계별로 보기"):
        for i, step in enumerate(logs, start=1):
            st.markdown(f"**과정 {i}** · 선택 노드: **{step['선택']}** · f={step['f']}, g={step['g']}, h={step['h']}")
            open_str = ", ".join([f"{n}(f={f})" for n,f in step["OPEN"]]) if step["OPEN"] else "-"
            st.write(f"OPEN: {open_str}")
            st.write(f"CLOSED: {', '.join(step['CLOSED'])}")
            st.write("---")
    st.markdown("</div>", unsafe_allow_html=True)
