import streamlit as st
from common import set_page, reset_keys

set_page("탐색 체험: 틱택토", "❎")

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
    # 1) 이길 수 있으면 이기기
    for i in available(board):
        tmp = board[:]
        tmp[i] = ai
        if winner(tmp) == ai:
            return i, "바로 이길 수 있는 수라서 선택했습니다."
    # 2) 상대가 이기려면 막기
    for i in available(board):
        tmp = board[:]
        tmp[i] = human
        if winner(tmp) == human:
            return i, "상대가 다음 수에 이길 수 있어 막았습니다."
    # 3) 중앙
    if board[4] == "":
        return 4, "중앙은 여러 줄(가로/세로/대각선)에 동시에 영향을 줍니다."
    # 4) 코너
    corners = [0,2,6,8]
    for i in corners:
        if board[i] == "":
            return i, "코너는 두 방향으로 이길 기회를 만들기 좋습니다."
    # 5) 나머지
    i = available(board)[0]
    return i, "남은 칸 중 하나를 선택했습니다."

def init():
    if "ttt_board" not in st.session_state:
        st.session_state.ttt_board = [""]*9
        st.session_state.ttt_turn = "X"  # 학생 X, 컴퓨터 O
        st.session_state.ttt_msg = "학생(X)부터 시작합니다."
        st.session_state.ttt_over = False
        st.session_state.ttt_ai_reason = ""

def reset():
    reset_keys("ttt_")
    for k in ["ttt_board","ttt_turn","ttt_msg","ttt_over","ttt_ai_reason"]:
        if k in st.session_state:
            del st.session_state[k]

init()

st.title("틱택토(탐색 느낌 체험)")
st.caption("학생이 두면 컴퓨터가 한 수 둡니다. 컴퓨터는 '이기기/막기/중앙/코너' 규칙으로 선택합니다.")

st.markdown(f"<div class='card'><b>상태</b>: {st.session_state.ttt_msg}<br/><span class='muted'>{st.session_state.ttt_ai_reason}</span></div>", unsafe_allow_html=True)

# 그리드
cols = st.columns(3)
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        i = r*3 + c
        label = st.session_state.ttt_board[i] if st.session_state.ttt_board[i] else " "
        disabled = st.session_state.ttt_over or st.session_state.ttt_board[i] != "" or st.session_state.ttt_turn != "X"
        if cols[c].button(label, key=f"cell_{i}", use_container_width=True, disabled=disabled):
            st.session_state.ttt_board[i] = "X"
            w = winner(st.session_state.ttt_board)
            if w:
                st.session_state.ttt_over = True
                st.session_state.ttt_msg = "무승부입니다." if w=="무승부" else f"{w} 승리!"
            else:
                # 컴퓨터 차례
                move, reason = best_move(st.session_state.ttt_board, ai="O", human="X")
                st.session_state.ttt_board[move] = "O"
                st.session_state.ttt_ai_reason = f"컴퓨터(O): {reason}"
                w2 = winner(st.session_state.ttt_board)
                if w2:
                    st.session_state.ttt_over = True
                    st.session_state.ttt_msg = "무승부입니다." if w2=="무승부" else f"{w2} 승리!"
                else:
                    st.session_state.ttt_msg = "다음은 학생(X) 차례입니다."
            st.rerun()

st.divider()
c1, c2 = st.columns(2)
with c1:
    if st.button("다시 시작", use_container_width=True):
        reset()
        st.rerun()
with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("**생각해 보기**")
    st.write("컴퓨터는 모든 경우를 다 보지 않아도(전수조사 없이) 간단한 규칙으로 꽤 그럴듯한 선택을 할 수 있습니다.")
    st.markdown("</div>", unsafe_allow_html=True)
