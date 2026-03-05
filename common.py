from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

import streamlit as st

from reporting import build_report_pdf


ASSETS_DIR = Path(__file__).parent / "assets"


def set_page(title: str, icon: str = "🤖"):
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")
    _inject_css()


def _inject_css():
    st.markdown(
        """
        <style>
          /* 전체 배경 느낌 */
          [data-testid="stAppViewContainer"]{
            background: radial-gradient(1200px 600px at 15% 10%, rgba(124,58,237,0.10), transparent 60%),
                        radial-gradient(900px 500px at 80% 15%, rgba(16,185,129,0.10), transparent 55%),
                        linear-gradient(180deg, #F7F7FF 0%, #FFFFFF 60%);
          }
          .hero {
            border-radius: 22px;
            padding: 22px 22px 16px 22px;
            border: 1px solid rgba(17,24,39,0.10);
            background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(16,185,129,0.10));
            box-shadow: 0 10px 30px rgba(17,24,39,0.06);
            margin-bottom: 14px;
          }
          .hero h1 { margin: 0; font-size: 2.0rem; }
          .hero p { margin: 6px 0 0 0; color: rgba(17,24,39,0.7); font-size: 1.02rem; }

          .card {
            border-radius: 18px;
            padding: 16px 16px 14px 16px;
            border: 1px solid rgba(17,24,39,0.10);
            background: rgba(255,255,255,0.78);
            box-shadow: 0 10px 28px rgba(17,24,39,0.05);
          }
          .card .muted { color: rgba(17,24,39,0.65); }
          .section-title{
            font-weight: 800;
            font-size: 1.25rem;
            margin: 0.2rem 0 0.6rem 0;
          }
          .big-btn button { width: 100%; height: 3.1rem; font-size: 1.15rem; border-radius: 14px; }
          .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
          .tag {
            display:inline-block; padding: 3px 10px; border-radius: 999px;
            border: 1px solid rgba(17,24,39,0.15); background: rgba(255,255,255,0.65);
            font-size: 0.88rem; color: rgba(17,24,39,0.75);
            margin-right: 6px;
          }
          .divider-soft { border-top: 1px solid rgba(17,24,39,0.10); margin: 18px 0; }
        </style>
        """,
        unsafe_allow_html=True
    )


def hero(title: str, subtitle: str, tags: Optional[List[str]] = None):
    tags_html = ""
    if tags:
        tags_html = "".join([f"<span class='tag'>{t}</span>" for t in tags])
    st.markdown(
        f"""
        <div class="hero">
          <div>{tags_html}</div>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def card_start():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

def card_end():
    st.markdown("</div>", unsafe_allow_html=True)

def soft_divider():
    st.markdown("<div class='divider-soft'></div>", unsafe_allow_html=True)


def load_ox(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ox_quiz(
    *,
    key_prefix: str,
    questions: List[Dict[str, Any]],
    title: str = "✅ 개념 확인(○,×)",
) -> Dict[str, Any]:
    """Render OX quiz and return result dict (also stored in session_state)."""
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.caption("문항을 모두 선택한 뒤, 아래의 ‘채점하기’를 누르면 정답과 해설이 펼쳐집니다.")

    # render questions
    for i, q in enumerate(questions, start=1):
        st.markdown(f"**Q{i}.** {q['q']}")
        st.radio(
            label=f"선택(Q{i})",
            options=["○", "×"],
            horizontal=True,
            key=f"{key_prefix}_q{i}",
            label_visibility="collapsed",
        )

    col1, col2 = st.columns([1, 1])
    with col1:
        grade = st.button("채점하기", use_container_width=True, key=f"{key_prefix}_grade")
    with col2:
        reset = st.button("선택 초기화", use_container_width=True, key=f"{key_prefix}_reset")

    if reset:
        for i in range(1, len(questions)+1):
            k = f"{key_prefix}_q{i}"
            if k in st.session_state:
                del st.session_state[k]
        if f"{key_prefix}_result" in st.session_state:
            del st.session_state[f"{key_prefix}_result"]
        st.rerun()

    if grade:
        items = []
        score = 0
        for i, q in enumerate(questions, start=1):
            choice = st.session_state.get(f"{key_prefix}_q{i}")
            ans = "○" if q["a"] == "O" else "×"
            is_correct = (choice == ans)
            if is_correct:
                score += 1
            items.append({
                "q": q["q"],
                "choice": choice if choice else "-",
                "answer": ans,
                "is_correct": is_correct,
                "exp": q.get("exp", "")
            })
        res = {"score": score, "total": len(questions), "items": items}
        st.session_state[f"{key_prefix}_result"] = res

    res = st.session_state.get(f"{key_prefix}_result")
    if res:
        if res["score"] == res["total"]:
            st.success(f"만점입니다! ({res['score']}/{res['total']})")
        else:
            st.info(f"점수: {res['score']}/{res['total']}")

        with st.expander("정답/해설 보기", expanded=True):
            for i, it in enumerate(res["items"], start=1):
                icon = "✅" if it["is_correct"] else "❌"
                st.markdown(f"**{icon} Q{i}**  선택: {it['choice']} · 정답: {it['answer']}")
                if it.get("exp"):
                    st.caption(it["exp"])

    return res or {}


def report_section(
    *,
    unit_key: str,
    unit_title: str,
    build_results_fn,
):
    """Render report download section at bottom."""
    soft_divider()
    st.markdown("<div class='section-title'>🧾 PDF 결과 보고서</div>", unsafe_allow_html=True)
    st.caption("학번/이름을 입력하면, 현재 페이지에서 수행한 결과를 PDF로 내려받을 수 있습니다. (서버 저장 없음)")

    c1, c2 = st.columns(2)
    with c1:
        sid = st.text_input("학번", key=f"{unit_key}_sid", placeholder="예: 20517")
    with c2:
        name = st.text_input("이름", key=f"{unit_key}_name", placeholder="예: 홍길동")

    results = build_results_fn() or {}

    # 간단 요약 표시
    ox = results.get("ox")
    if ox:
        st.write(f"✅ 개념 확인 점수: **{ox.get('score',0)} / {ox.get('total',0)}**")
    acts = results.get("activities") or []
    if acts:
        st.write(f"🧪 활동/실습 기록: **{len(acts)}개**")

    can_make = bool(sid.strip()) and bool(name.strip())
    if not can_make:
        st.warning("학번과 이름을 입력하면 다운로드 버튼이 활성화됩니다.")
        return

    # font path
    font_path = str(ASSETS_DIR / "NanumGothic.ttf")
    if not Path(font_path).exists():
        # fallback (if Nanum absent)
        font_path = str(next(iter(ASSETS_DIR.glob("*.*")), ""))

    try:
        pdf_bytes = build_report_pdf(
            font_path=font_path,
            student_id=sid.strip(),
            student_name=name.strip(),
            unit_title=unit_title,
            results=results,
        )
    except Exception as e:
        st.error("PDF 생성 중 오류가 발생했습니다. (폰트/환경 문제일 수 있습니다.)")
        st.exception(e)
        return

    safe_title = re_sub(r"[^0-9A-Za-z가-힣_\-]+", "_", unit_title)[:40]
    safe_sid = re_sub(r"[^0-9A-Za-z]+", "", sid.strip())[:20]
    safe_name = re_sub(r"[^0-9A-Za-z가-힣]+", "", name.strip())[:20]
    filename = f"{safe_sid}_{safe_name}_{safe_title}.pdf"

    st.download_button(
        label="📥 PDF 다운로드",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
        use_container_width=True,
    )


def re_sub(pattern: str, repl: str, text: str) -> str:
    import re
    return re.sub(pattern, repl, text)
