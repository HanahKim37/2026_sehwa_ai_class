import heapq
import random
import streamlit as st
from common import set_page, hero, card_start, card_end, ox_quiz, report_section, load_ox

set_page("지능적 탐색 과정의 적용", "🗺️")

hero(
    "🗺️ 지능적 탐색 과정의 적용",
    "틱택토·8-퍼즐·길찾기를 직접 해 보며, ‘평가 함수’로 탐색 효율을 높이는 감각을 익힙니다.",
    tags=["틱택토", "8-퍼즐", "A*", "OPEN/CLOSED", "○×"]
)

# --- OX (A* 개념)
qs = load_ox("data/ox_unit5.json")
ox_res = ox_quiz(key_prefix="u5ox", questions=qs, title="✅ 개념 확인: 평가 함수와 A*")

st.divider()

# --- Tabs for activities
tabs = st.tabs(["❎ 틱택토", "🧩 8-퍼즐", "🗺️ 길찾기(A*)"])

# --- 1) TicTacToe
LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]
def winner(board):
    for a,b,c in LINES:
        if board[a] and board[a]==board[b]==board[c]:
            return board[a]
    if all(board):
        return "무승부"
    return None

def available(board):
    return [i for i,v in enumerate(board) if v==""]

def best_move(board, ai="O", human="X"):
    for i in available(board):
        tmp = board[:]
        tmp[i] = ai
        if winner(tmp) == ai:
            return i, "바로 이길 수 있는 수라서 선택했습니다."
    for i in available(board):
        tmp = board[:]
        tmp[i] = human
        if winner(tmp) == human:
            return i, "상대가 다음 수에 이길 수 있어 막았습니다."
    if board[4] == "":
        return 4, "중앙은 여러 줄에 동시에 영향을 줍니다."
    for i in [0,2,6,8]:
        if board[i] == "":
            return i, "코너는 두 방향으로 기회를 만들기 좋습니다."
    i = available(board)[0]
    return i, "남은 칸 중 하나를 선택했습니다."

def init_ttt():
    if "u5_ttt_board" not in st.session_state:
        st.session_state.u5_ttt_board = [""]*9
        st.session_state.u5_ttt_over = False
        st.session_state.u5_ttt_msg = "학생(X)부터 시작합니다."
        st.session_state.u5_ttt_reason = ""
        st.session_state.u5_ttt_last = ""

def reset_ttt():
    for k in list(st.session_state.keys()):
        if k.startswith("u5_ttt_") or k.startswith("u5_cell_"):
            del st.session_state[k]

with tabs[0]:
    init_ttt()
    card_start()
    st.markdown("### ❎ 틱택토: 한 수 두고, 컴퓨터의 선택 이유 확인하기")
    st.caption("컴퓨터는 ‘이기기→막기→중앙→코너’ 규칙으로 한 수를 선택합니다.")
    st.write(st.session_state.u5_ttt_msg)
    if st.session_state.u5_ttt_reason:
        st.info(f"컴퓨터(O): {st.session_state.u5_ttt_reason}")
    card_end()

    cols = st.columns(3)
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            i = r*3 + c
            label = st.session_state.u5_ttt_board[i] if st.session_state.u5_ttt_board[i] else " "
            disabled = st.session_state.u5_ttt_over or st.session_state.u5_ttt_board[i] != ""
            if cols[c].button(label, key=f"u5_cell_{i}", use_container_width=True, disabled=disabled):
                st.session_state.u5_ttt_board[i] = "X"
                w = winner(st.session_state.u5_ttt_board)
                if w:
                    st.session_state.u5_ttt_over = True
                    st.session_state.u5_ttt_last = w
                    st.session_state.u5_ttt_msg = "무승부입니다." if w=="무승부" else f"{w} 승리!"
                else:
                    move, reason = best_move(st.session_state.u5_ttt_board)
                    st.session_state.u5_ttt_board[move] = "O"
                    st.session_state.u5_ttt_reason = reason
                    w2 = winner(st.session_state.u5_ttt_board)
                    if w2:
                        st.session_state.u5_ttt_over = True
                        st.session_state.u5_ttt_last = w2
                        st.session_state.u5_ttt_msg = "무승부입니다." if w2=="무승부" else f"{w2} 승리!"
                    else:
                        st.session_state.u5_ttt_msg = "다음은 학생(X) 차례입니다."
                st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("다시 시작", use_container_width=True):
            reset_ttt()
            st.rerun()
    with c2:
        st.markdown("**생각해 보기**: 모든 경우를 완전 탐색하지 않아도, 규칙만으로 꽤 그럴듯한 판단이 가능합니다.")

# --- 2) 8 puzzle (choose best next state)
GOAL = (1,2,3,4,5,6,7,8,0)

def pretty(state):
    rows=[]
    for r in range(3):
        row=[]
        for c in range(3):
            v=state[r*3+c]
            row.append("□" if v==0 else str(v))
        rows.append("  ".join(row))
    return "\n".join(rows)

def moves(state):
    z = state.index(0)
    r,c = divmod(z,3)
    cand=[]
    def swap(i,j):
        s=list(state)
        s[i],s[j]=s[j],s[i]
        return tuple(s)
    if r>0: cand.append(swap(z,z-3))
    if r<2: cand.append(swap(z,z+3))
    if c>0: cand.append(swap(z,z-1))
    if c<2: cand.append(swap(z,z+1))
    return cand

def h_mismatch(state):
    # 앞으로 맞춰야 하는 퍼즐 수(빈칸 제외)
    mism=0
    for i,v in enumerate(state):
        if v!=0 and v!=GOAL[i]:
            mism+=1
    return mism

def scramble(steps=10):
    s=GOAL
    for _ in range(steps):
        s=random.choice(moves(s))
    return s

def init_puz():
    if "u5_puz_state" not in st.session_state:
        st.session_state.u5_puz_state = scramble()
        st.session_state.u5_puz_round = 0
        st.session_state.u5_puz_correct = 0
        st.session_state.u5_puz_opts = []

def new_puz_round():
    opts = moves(st.session_state.u5_puz_state)
    random.shuffle(opts)
    st.session_state.u5_puz_opts = opts[:3] if len(opts) >= 3 else opts
    st.session_state.u5_puz_round += 1

def reset_puz():
    for k in list(st.session_state.keys()):
        if k.startswith("u5_puz_"):
            del st.session_state[k]

with tabs[1]:
    init_puz()
    if not st.session_state.u5_puz_opts:
        new_puz_round()

    card_start()
    st.markdown("### 🧩 8-퍼즐: 평가 함수 감각 익히기")
    st.caption("여기서는 A*의 아이디어를 단순화해, ‘앞으로 맞춰야 하는 퍼즐 수(h)’가 줄어드는 쪽을 ‘더 좋은 선택’으로 봅니다.")
    st.write("현재 상태:")
    st.code(pretty(st.session_state.u5_puz_state), language="text")
    st.write(f"h(n) = 앞으로 맞춰야 하는 퍼즐 수: **{h_mismatch(st.session_state.u5_puz_state)}**")
    card_end()

    st.markdown("**다음 상태 후보 중 더 좋은 것을 고르세요.**")
    opts = st.session_state.u5_puz_opts
    labels = [f"후보 {i+1} (h={h_mismatch(s)})" for i,s in enumerate(opts)]
    choice = st.radio("선택", options=list(range(len(opts))), format_func=lambda i: labels[i], horizontal=True, key="u5_puz_choice")

    if st.button("정답 확인", use_container_width=True):
        hs = [h_mismatch(s) for s in opts]
        best = min(range(len(opts)), key=lambda i: hs[i])
        if choice == best:
            st.success("좋은 선택입니다. (h가 가장 작음)")
            st.session_state.u5_puz_correct += 1
        else:
            st.error(f"가장 좋은 후보는 **후보 {best+1}** 입니다.")
        st.info("A*에서는 f(n)=g(n)+h(n)로 ‘지금까지 비용 + 남은 비용 추정’을 함께 봅니다. 여기서는 h만 체감해 봅니다.")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("내 선택으로 진행", use_container_width=True):
                st.session_state.u5_puz_state = opts[choice]
                st.session_state.u5_puz_opts = []
                st.rerun()
        with c2:
            if st.button("가장 좋은 후보로 진행", use_container_width=True):
                st.session_state.u5_puz_state = opts[best]
                st.session_state.u5_puz_opts = []
                st.rerun()

    st.caption(f"라운드: {st.session_state.u5_puz_round} · 좋은 선택: {st.session_state.u5_puz_correct}")

    if st.button("새 퍼즐로 다시", use_container_width=True):
        reset_puz()
        st.rerun()

# --- 3) Pathfinding A*
NODES = ["스페인","포르투갈","프랑스","이탈리아","스위스","독일","체코","폴란드","오스트리아"]
H = {
    "스페인": 200, "포르투갈": 170, "프랑스": 150, "이탈리아": 110,
    "스위스": 120, "독일": 90, "체코": 40, "폴란드": 40, "오스트리아": 0,
}
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
START, GOALN = "스페인", "오스트리아"

def astar(start, goal):
    open_heap=[]
    heapq.heappush(open_heap, (H[start], 0, start))
    best_g={start:0}
    parent={start:None}
    open_set={start}
    closed=set()
    logs=[]

    while open_heap:
        f,g,node=heapq.heappop(open_heap)
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

        if node==goal:
            break

        for nxt,w in G[node].items():
            if nxt in closed:
                continue
            ng=g+w
            if ng < best_g.get(nxt, 10**9):
                best_g[nxt]=ng
                parent[nxt]=node
                heapq.heappush(open_heap, (ng+H[nxt], ng, nxt))
                open_set.add(nxt)

    if goal not in parent:
        return None, logs

    path=[]
    cur=goal
    while cur is not None:
        path.append(cur)
        cur=parent[cur]
    path.reverse()
    return path, logs

def path_cost(path):
    if not path or len(path)==1:
        return 0
    s=0
    for a,b in zip(path, path[1:]):
        s += G[a][b]
    return s

def init_pf():
    if "u5_pf_path" not in st.session_state:
        st.session_state.u5_pf_path = [START]
        st.session_state.u5_pf_cost = 0
        st.session_state.u5_pf_done = False

def reset_pf():
    for k in list(st.session_state.keys()):
        if k.startswith("u5_pf_"):
            del st.session_state[k]

with tabs[2]:
    init_pf()
    card_start()
    st.markdown("### 🗺️ 길찾기: 스페인 → 오스트리아")
    st.caption("직접 경로를 만들어 보고, A*가 선택하는 경로와 비교합니다. (f=g+h)")
    st.write("현재 경로:", " → ".join(st.session_state.u5_pf_path))
    st.write(f"누적 거리 g(n): **{st.session_state.u5_pf_cost}**")
    card_end()

    cur = st.session_state.u5_pf_path[-1]
    if cur != GOALN:
        nxt = st.selectbox("다음으로 이동", options=list(G[cur].keys()), key="u5_pf_next")
        if st.button("이동", use_container_width=True, key="u5_pf_go"):
            st.session_state.u5_pf_path.append(nxt)
            st.session_state.u5_pf_cost += G[cur][nxt]
            st.rerun()
    else:
        st.success("도착했습니다!")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("한 칸 되돌리기", use_container_width=True, disabled=len(st.session_state.u5_pf_path)<=1):
            if len(st.session_state.u5_pf_path) > 1:
                a = st.session_state.u5_pf_path[-2]
                b = st.session_state.u5_pf_path[-1]
                st.session_state.u5_pf_cost -= G[a][b]
                st.session_state.u5_pf_path = st.session_state.u5_pf_path[:-1]
            st.rerun()
    with c2:
        if st.button("처음부터", use_container_width=True):
            reset_pf()
            st.rerun()
    with c3:
        st.write("")

    st.markdown("**h(n): 목표(오스트리아)까지의 추정 거리(직선 거리)**")
    st.write(", ".join([f"{k}={v}" for k,v in H.items()]))

    st.divider()

    astar_path, logs = astar(START, GOALN)
    if astar_path:
        st.markdown("#### ⭐ A* 결과(참고)")
        st.write("A* 경로:", " → ".join(astar_path))
        st.write(f"A* 총 거리: **{path_cost(astar_path)}**")

    if st.checkbox("A* OPEN/CLOSED 단계 로그 보기"):
        for i, step in enumerate(logs, start=1):
            st.markdown(f"**과정 {i}** · 선택: **{step['선택']}** · f={step['f']}, g={step['g']}, h={step['h']}")
            open_str = ", ".join([f"{n}(f={f})" for n,f in step['OPEN']]) if step["OPEN"] else "-"
            st.write(f"OPEN: {open_str}")
            st.write(f"CLOSED: {', '.join(step['CLOSED'])}")
            st.write("---")

# Report
def build_results():
    acts = []
    # TicTacToe result
    last = st.session_state.get("u5_ttt_last")
    if last:
        acts.append({"name": "틱택토", "desc": f"결과: {last}"})
    # 8 puzzle progress
    if "u5_puz_round" in st.session_state:
        acts.append({"name": "8-퍼즐", "desc": f"라운드 {st.session_state.u5_puz_round} · 좋은 선택 {st.session_state.u5_puz_correct}"})
    # Pathfinding
    if "u5_pf_path" in st.session_state:
        acts.append({"name": "길찾기", "desc": f"내 경로 거리 {st.session_state.u5_pf_cost} · 경로: {' → '.join(st.session_state.u5_pf_path)}"})
    return {"ox": ox_res, "activities": acts}

report_section(unit_key="u5", unit_title="지능적 탐색 과정의 적용", build_results_fn=build_results)
