import streamlit as st
import pandas as pd
import numpy as np
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt

# -----------------------------
# 숫자를 한국식 단위(만, 억)로 변환
# -----------------------------
def korean_number(num):
    if num >= 100000000:
        return f"{num // 100000000}억"
    elif num >= 10000:
        return f"{num // 10000}만"
    else:
        return str(num)

# -----------------------------
# 페이지 상태 초기화
# -----------------------------
if 'page' not in st.session_state:
    st.session_state.page = "main"

# -----------------------------
# 1. 메인 메뉴 페이지
# -----------------------------
def main_menu():
    st.set_page_config(page_title="해양 환경 대시보드", layout="wide")
    st.title("🌊 해양 환경 대시보드")
    st.markdown("최근 지구 온난화로 해수면과 해수온이 빠르게 상승하며, 산호 백화, 어류 분포 변화, 해양 산성화 등 해양 생태계에 심각한 영향을 끼치고 있다. 우리는 이 정보를 통해 기후 변화의 심각성을 인식하고, 청소년과 어른 모두 환경 보호 행동에 참여해야 한다." \
    "  한번 무슨 일이 일어나고 있는지 알아가보자!")

    col1, col2 = st.columns([1,3])

    with col1:
        st.subheader("📌 메뉴")
        if st.button("산호 백화현상"):
            st.session_state.page = "bleach"
            st.experimental_rerun()
        if st.button("기후 변화 문제"):
            st.session_state.page = "climate"
            st.experimental_rerun()
        if st.button("환경 실천 방법"):
            st.session_state.page = "actions"
            st.experimental_rerun()

    with col2:
        st.subheader("🌊 해수면 & 해수온 상승")
        years = np.arange(1980,2025)
        sea_level = np.linspace(0,13.6,len(years))
        sea_temp = np.linspace(0,0.78,len(years))
        fig, ax1 = plt.subplots(figsize=(8,4))
        ax1.plot(years, sea_level, color="#1f77b4", label="해수면 상승(mm)")
        ax2 = ax1.twinx()
        ax2.plot(years, sea_temp, color="#ff7f0e", linestyle="--", label="해수온 상승(°C)")
        ax1.set_xlabel("연도")
        ax1.set_ylabel("해수면 상승 (mm)", color="#1f77b4")
        ax2.set_ylabel("해수온 상승 (°C)", color="#ff7f0e")
        ax1.grid(alpha=0.3)
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        st.pyplot(fig)

# -----------------------------
# 2. 산호 백화현상 페이지
# -----------------------------
def bleach_page():
    st.title("📌 1980~2024년 산호 백화현상")
    if st.button("⬅️ 메인 메뉴로 돌아가기"):
        st.session_state.page = "main"
        st.experimental_rerun()

    years_known = np.array([1980, 1998, 2010, 2015, 2024])
    bleach_known = np.array([5,21,37,68,84])
    years_all = np.arange(1980,2025)
    interp = PchipInterpolator(years_known, bleach_known)
    bleach = np.clip(interp(years_all),0,100)
    remain = 100 - bleach

    df = pd.DataFrame({
        "연도": years_all,
        "백화화된 산호(%)": np.round(bleach,2),
        "남은 산호(%)": np.round(remain,2)
    })

    selected_year = st.select_slider("연도를 선택하세요:", options=years_all, value=2000)
    row = df[df["연도"]==selected_year].iloc[0]

    st.markdown(f"<h2 style='color:red'>{selected_year}년 백화화된 산호: {row['백화화된 산호(%)']}%</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:blue'>{selected_year}년 남은 산호: {row['남은 산호(%)']}%</h2>", unsafe_allow_html=True)

    # 그래프
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(years_all, bleach, color="red", linewidth=1.5, alpha=0.5, label="백화화된 산호")
    ax.plot(years_all, remain, color="blue", linewidth=1.5, alpha=0.5, label="남은 산호")
    
    # 선택한 점 표시 및 값 표시
    ax.scatter(selected_year, row["백화화된 산호(%)"], color="red", s=60)
    ax.text(selected_year, row["백화화된 산호(%)"]+2,
            f"{selected_year} {row['백화화된 산호(%)']}%", ha='center', fontsize=10, color="red")
    
    ax.scatter(selected_year, row["남은 산호(%)"], color="blue", s=60)
    ax.text(selected_year, row["남은 산호(%)"]+2,
            f"{selected_year} {row['남은 산호(%)']}%", ha='center', fontsize=10, color="blue")
    
    ax.set_xlabel("연도")
    ax.set_ylabel("비율(%)")
    ax.set_ylim(0,105)
    ax.set_xlim(1979,2025)
    ax.grid(alpha=0.3)
    ax.legend()
    st.pyplot(fig)

    st.markdown(
        """
        **설명:**  
        산호초 백화현상은 해수 온도가 상승하거나 해양 환경이 급격히 변할 때 산호가 공생조류를 잃고 하얗게 변하는 현상으로, 생존 위협의 심각한 신호입니다. 최근 2년간 전 세계 산호초의 약 80% 이상에서 백화 현상이 심화되었으며, 주요 산호 종은 멸종 위기에 처해 있습니다. 산호초는 해양 생물 서식지이자 어업 자원의 기반이므로 붕괴는 해양 생태계 균형을 무너뜨립니다.
        """
    )

# -----------------------------
# 3. 기후 변화 페이지
# -----------------------------
def climate_issue_page():
    st.title("🌊 기후 변화가 주는 문제")
    if st.button("⬅️ 메인 메뉴로 돌아가기"):
        st.session_state.page = "main"
        st.experimental_rerun()

    # 설명 요약
    st.markdown(
        """
        <h3>설명:</h3>
        해수 온도 상승과 해양 산성화는 산호초와 다양한 해양 생물에게 피해를 주고, 어류 폐사와 서식지 파괴를 촉진하며 해양 생물 다양성을 감소시킨다. 장기적인 해양 열파는 생태계 붕괴를 악화시키며, 이를 막기 위해 탄소 배출 저감, 해양 보호구역 확대, 산호 복원 등의 대응이 시급하다.
        """,
        unsafe_allow_html=True
    )

    years = np.arange(1980,2025)
    ph_drop = np.linspace(8.2, 8.0, len(years))
    temp_rise = np.linspace(0,0.78,len(years))
    habitat_loss = np.linspace(0,30,len(years))

    selected_year = st.select_slider("연도를 선택하세요:", options=years, value=2000)
    idx = selected_year - 1980

    st.markdown(f"<h2 style='color:red'>{selected_year}년 pH 감소: {ph_drop[idx]:.2f}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:orange'>{selected_year}년 해수 온도 상승: {temp_rise[idx]:.2f}°C</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:blue'>{selected_year}년 서식지 감소: {habitat_loss[idx]:.1f}%</h2>", unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(years, ph_drop, color="red", label="pH 감소")
    ax.plot(years, temp_rise, color="orange", label="해수 온도 상승")
    ax.plot(years, habitat_loss, color="blue", label="서식지 감소")
    
    # 선택한 점 표시 및 값 표시
    ax.scatter(selected_year, ph_drop[idx], color="red", s=60)
    ax.text(selected_year, ph_drop[idx]+0.01, f"{selected_year} {ph_drop[idx]:.2f}", ha='center', fontsize=10, color="red")
    
    ax.scatter(selected_year, temp_rise[idx], color="orange", s=60)
    ax.text(selected_year, temp_rise[idx]+0.01, f"{selected_year} {temp_rise[idx]:.2f}", ha='center', fontsize=10, color="orange")
    
    ax.scatter(selected_year, habitat_loss[idx], color="blue", s=60)
    ax.text(selected_year, habitat_loss[idx]+0.5, f"{selected_year} {habitat_loss[idx]:.1f}", ha='center', fontsize=10, color="blue")
    
    ax.set_xlabel("연도")
    ax.set_ylabel("값")
    ax.grid(alpha=0.3)
    ax.legend()
    st.pyplot(fig)

# -----------------------------
# 4. 환경 실천 페이지
# -----------------------------
def actions_page():
    st.title("🌱 환경 실천 효과")
    if st.button("⬅️ 메인 메뉴로 돌아가기"):
        st.session_state.page = "main"
        st.experimental_rerun()

    # 설명 요약
    st.markdown(
        """
        <h3>설명:</h3>
        기후 변화로 인한 해양 생태계 위기를 막기 위해 청소년과 어른 모두가 환경 보호 행동에 참여해야 한다. 대중교통 이용, 노플라스틱 캠페인, 탄소포인트제 등 작은 실천이 모이면 많은 탄소를 감축하고 해양 생태계를 보호할 수 있다.
        """,
        unsafe_allow_html=True
    )

    actions = {
        "자전거 30분": {"CO2":0.3,"빙하":0.07,"해수면":0.0002,"자동차":2,"나무":1},
        "대중교통 1회": {"CO2":0.5,"빙하":0.1,"해수면":0.0003,"자동차":5,"나무":2},
        "채식 1끼": {"CO2":1.0,"빙하":0.2,"해수면":0.0005,"자동차":10,"나무":5},
        "재활용": {"CO2":0.2,"빙하":0.03,"해수면":0.0001,"자동차":1,"나무":0.5},
        "전기 절약": {"CO2":0.4,"빙하":0.05,"해수면":0.00015,"자동차":1.5,"나무":0.7},
        "물 절약": {"CO2":0.1,"빙하":0.02,"해수면":0.00005,"자동차":0.5,"나무":0.2},
        "플라스틱 줄이기": {"CO2":0.15,"빙하":0.03,"해수면":0.00008,"자동차":0.7,"나무":0.3},
        "해안 정화 활동": {"CO2":0.25,"빙하":0.04,"해수면":0.00012,"자동차":1.2,"나무":0.5},
    }

    activities = st.multiselect("실천 활동 선택", options=list(actions.keys()))
    populations = [1,100,10000,1000000,100000000]
    population = st.selectbox("인원 수 선택", populations, format_func=korean_number)

    if activities:
        total = {"CO2":0,"빙하":0,"해수면":0,"자동차":0,"나무":0}
        for act in activities:
            for k in total:
                total[k] += actions[act][k]*population

        df_total = pd.DataFrame({
            "항목":["아낀 CO2","빙하 보존","해수면 상승 억제","자동차 운행 감소","나무 심기 효과"],
            "효과":[
                f"{total['CO2']:.2f} kg",
                f"{total['빙하']:.2f} L",
                f"{total['해수면']:.6f} mm",
                f"{korean_number(int(total['자동차']))} km",
                f"{korean_number(int(total['나무']))} 그루"
            ]
        })
        st.table(df_total)

# -----------------------------
# 페이지 상태 표시
# -----------------------------
if st.session_state.page=="main":
    main_menu()
elif st.session_state.page=="bleach":
    bleach_page()
elif st.session_state.page=="climate":
    climate_issue_page()
elif st.session_state.page=="actions":
    actions_page()
    