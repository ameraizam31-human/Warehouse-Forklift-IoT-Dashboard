import streamlit as st
import pandas as pd
import random
from datetime import date, timedelta

# --- CONFIGURATION & PAGE SETUP ---
st.set_page_config(page_title="Forklift Operations Dashboard", layout="wide", page_icon="🏭")

# --- INJECT CUSTOM CSS ---
def inject_custom_css():
    st.markdown("""
    <style>
    /* Dark Theme Optimization */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Live Pulsing Dot */
    .live-indicator {
        display: flex;
        align-items: center;
        font-weight: 600;
        color: #10b981;
        margin-bottom: 20px;
        font-family: 'Inter', sans-serif;
        background: rgba(16, 185, 129, 0.1);
        padding: 8px 16px;
        border-radius: 20px;
        width: fit-content;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .pulse-dot {
        height: 10px;
        width: 10px;
        background-color: #10b981;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1.1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Custom KPI Cards */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 30px;
        flex-wrap: wrap;
    }
    .kpi-card {
        background-color: #1E293B;
        border-top: 4px solid #3b82f6; 
        border-radius: 8px;
        padding: 15px 20px;
        flex: 1;
        min-width: 140px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
    }
    .kpi-title {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-bottom: 5px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #f8fafc;
    }
    
    /* Efficiency Score Card */
    .score-card {
        background: linear-gradient(135deg, #06b6d4, #3b82f6);
        border-radius: 8px;
        padding: 20px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 15px -3px rgba(6, 182, 212, 0.3);
    }
    .score-value {
        font-size: 3rem;
        font-weight: 900;
    }
    
    .score-card-lazy {
        background: linear-gradient(135deg, #ef4444, #f97316);
        border-radius: 8px;
        padding: 20px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 15px -3px rgba(239, 68, 68, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# --- LIVE FEED INDICATOR ---
st.markdown("""
<div class="live-indicator">
    <div class="pulse-dot"></div>
    DEMO MODE - SIMULATED DATA
</div>
""", unsafe_allow_html=True)

st.title("Warehouse Forklift Operations Dashboard")
st.markdown("Monitor real-time forklift productivity, shift performance, and manage staff rosters.")

# --- DATA GENERATION (CACHED) ---
@st.cache_data
def load_advanced_data():
    """Generates 4-month data with behavioral logic, shifts, and team rotations."""
    random.seed(42)  # deterministic demo data: same numbers on every restart
    workers_full = ["Ahmad", "Chong", "Hafiz", "Muthu", "Raju", "Siti", "Amin", 
                    "Devi", "Kamal", "Wei Ting", "Faizal", "Sarah", "Kumar", "Zaki"]
    
    team_a = workers_full[:7]
    team_b = workers_full[7:]
    
    lazy_workers = ["Kamal", "Faizal", "Zaki"]
    departments = ["Warehouse", "Logistics", "Operations"]
    
    dept_map = {w: random.choice(departments) for w in workers_full}
    dept_map["Ahmad"] = "Warehouse"
    
    ahmad_april_targets = {
        "Unloaded IBC": 101,
        "Loaded IBC": 305,
        "Loading Pallet": 50,
        "Unloading Pallet": 15,
        "Standby IBC": 600
    }
    
    data = []
    
    for m in range(1, 5):
        m_start = date(2026, m, 1)
        if m in [1, 3]: m_end = date(2026, m, 31)
        elif m == 2: m_end = date(2026, m, 28)
        else: m_end = date(2026, m, 30)
            
        m_days = (m_end - m_start).days + 1
        m_dates = [m_start + timedelta(days=i) for i in range(m_days)]
        
        top_worker = ["Raju", "Siti", "Chong", "Ahmad"][m-1]
        w_data_all = {}
        
        # Calculate targets and distribute for the month
        for w in workers_full:
            if m == 4 and w == "Ahmad":
                targets = ahmad_april_targets
            else:
                if w in lazy_workers:
                    multiplier = random.uniform(0.10, 0.25)
                else:
                    multiplier = random.uniform(1.1, 1.3) if w == top_worker else random.uniform(0.7, 1.0)
                
                targets = {
                    "Unloaded IBC": int(101 * multiplier),
                    "Loaded IBC": int(305 * multiplier),
                    "Loading Pallet": int(50 * multiplier),
                    "Unloading Pallet": max(0, int(15 * multiplier)),
                    "Standby IBC": int(600 * multiplier)
                }
                
            w_data = {metric: [0]*m_days for metric in targets}
            for metric, total in targets.items():
                vals = [0] * m_days
                for _ in range(total):
                    vals[random.randint(0, m_days - 1)] += 1
                w_data[metric] = vals
            w_data_all[w] = w_data
                
        # Assign Daily Rows based on Shift Logic
        for i, day_date in enumerate(m_dates):
            iso_week = day_date.isocalendar()[1]
            is_even_week = (iso_week % 2 == 0)
            
            for w in workers_full:
                # Shift Rotation Logic
                if w in team_a:
                    shift = "Morning Shift" if is_even_week else "Night Shift"
                else:
                    shift = "Night Shift" if is_even_week else "Morning Shift"
                
                # Behavioral Time Tracking
                if w in lazy_workers:
                    time_on = round(random.uniform(1.0, 3.5), 1) 
                else:
                    time_on = round(random.uniform(6.0, 8.5), 1)
                
                time_off = round(9.5 - time_on, 1)
                
                data.append({
                    "Date": day_date,
                    "Worker": w,
                    "Department": dept_map[w],
                    "Team": "Team A" if w in team_a else "Team B",
                    "Shift": shift,
                    "Time On Forklift (hrs)": time_on,
                    "Time Off Forklift (hrs)": time_off,
                    "Unloaded IBC": w_data_all[w]["Unloaded IBC"][i],
                    "Loaded IBC": w_data_all[w]["Loaded IBC"][i],
                    "Loading Pallet": w_data_all[w]["Loading Pallet"][i],
                    "Unloading Pallet": w_data_all[w]["Unloading Pallet"][i],
                    "Standby IBC": w_data_all[w]["Standby IBC"][i]
                })
                
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df['Total Moved'] = df['Unloaded IBC'] + df['Loaded IBC'] + df['Loading Pallet'] + df['Unloading Pallet']
    return df, team_a, team_b

df, team_a_list, team_b_list = load_advanced_data()

# --- SIDEBAR CONTROLS ---
st.sidebar.markdown("### ⚙️ Dashboard Controls")

min_date = date(2026, 1, 1)
max_date = date(2026, 4, 30)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) or isinstance(date_range, list):
    if len(date_range) == 2:
        start_filter, end_filter = date_range
    elif len(date_range) == 1:
        start_filter, end_filter = date_range[0], date_range[0]
    else:
        start_filter, end_filter = min_date, max_date
else:
    start_filter, end_filter = date_range, date_range

workers_list = ["All Workers"] + sorted(df['Worker'].unique().tolist())
selected_worker = st.sidebar.selectbox("Worker Selection", workers_list)

departments_list = ["All Departments"] + sorted(df['Department'].unique().tolist())
selected_dept = st.sidebar.selectbox("Department Filter", departments_list)

shifts_list = ["All Shifts", "Morning Shift", "Night Shift"]
selected_shift = st.sidebar.selectbox("Shift Filter", shifts_list)

# Register New Staff Form
st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 Register New Staff")
with st.sidebar.form("new_staff_form", clear_on_submit=True):
    new_name = st.text_input("Staff Name")
    new_dept = st.selectbox("Assign Department", ["Warehouse", "Logistics", "Operations"])
    submitted = st.form_submit_button("Register Staff")
    
    if submitted:
        if new_name.strip():
            st.sidebar.info(f"Demo only: {new_name} ({new_dept}) is not saved. Connect a database to persist staff.")
        else:
            st.sidebar.error("Please enter a valid name.")

# --- APPLY FILTERS ---
filtered_df = df[(df['Date'] >= start_filter) & (df['Date'] <= end_filter)]

if selected_worker != "All Workers":
    filtered_df = filtered_df[filtered_df['Worker'] == selected_worker]

if selected_dept != "All Departments":
    filtered_df = filtered_df[filtered_df['Department'] == selected_dept]

if selected_shift != "All Shifts":
    filtered_df = filtered_df[filtered_df['Shift'] == selected_shift]

# --- TABS LAYOUT ---
tab1, tab2 = st.tabs(["📊 Productivity Analytics", "📅 Shift Roster Planning"])

with tab1:
    st.markdown("### 📊 Overall Productivity Overview")

    if not filtered_df.empty:
        avg_time_on = filtered_df['Time On Forklift (hrs)'].mean()
        avg_time_off = filtered_df['Time Off Forklift (hrs)'].mean()
        kpi_unloaded = filtered_df['Unloaded IBC'].sum()
        kpi_loaded = filtered_df['Loaded IBC'].sum()
        kpi_loading_p = filtered_df['Loading Pallet'].sum()
        kpi_unloading_p = filtered_df['Unloading Pallet'].sum()
        kpi_standby = filtered_df['Standby IBC'].sum()

        kpis_html = f"""
        <div class="kpi-container">
            <div class="kpi-card" style="border-top-color: #10b981;">
                <div class="kpi-title">⏱️ Avg Time On</div>
                <div class="kpi-value">{avg_time_on:.1f} hrs</div>
            </div>
            <div class="kpi-card" style="border-top-color: #ef4444;">
                <div class="kpi-title">☕ Avg Time Off</div>
                <div class="kpi-value">{avg_time_off:.1f} hrs</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">📥 Unloaded IBC</div>
                <div class="kpi-value">{kpi_unloaded:,}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">📤 Loaded IBC</div>
                <div class="kpi-value">{kpi_loaded:,}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">🔲 Loading Pallet</div>
                <div class="kpi-value">{kpi_loading_p:,}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">🔳 Unloading Pallet</div>
                <div class="kpi-value">{kpi_unloading_p:,}</div>
            </div>
            <div class="kpi-card" style="border-top-color: #f59e0b;">
                <div class="kpi-title">⏳ Standby IBC</div>
                <div class="kpi-value">{kpi_standby:,}</div>
            </div>
        </div>
        """
        st.markdown(kpis_html, unsafe_allow_html=True)

        col_main1, col_main2 = st.columns([2, 1])

        with col_main1:
            st.markdown("### 📈 Task Volume & Shift Trend")
            trend_data = filtered_df.groupby(['Date', 'Shift'])['Total Moved'].sum().unstack().fillna(0)
            st.line_chart(trend_data)

        with col_main2:
            if selected_worker == "All Workers":
                st.markdown("### 🎯 Behavioral Efficiency")
                time_dist = pd.DataFrame({
                    "Metric": ["Time On Forklift", "Time Off Forklift"],
                    "Average Hours": [avg_time_on, avg_time_off]
                }).set_index("Metric")
                st.bar_chart(time_dist, color="#3b82f6")
            else:
                st.markdown(f"### 🎯 {selected_worker}'s Assessment")
                avg_w_time_on = filtered_df['Time On Forklift (hrs)'].mean()
                total_tasks = filtered_df['Total Moved'].sum()
                days_count = filtered_df['Date'].nunique()
                avg_daily_tasks = total_tasks / (days_count if days_count > 0 else 1)
                
                score = min(100, int(((avg_daily_tasks / 12.0) * 0.6 + (avg_w_time_on / 7.5) * 0.4) * 100))
                card_class = "score-card" if score > 40 else "score-card-lazy"
                status_text = "Good Standing" if score > 40 else "Requires Managerial Review"
                
                st.markdown(f"""
                <div class="{card_class}">
                    <div>Efficiency Score</div>
                    <div class="score-value">{score}%</div>
                    <div style="font-size: 0.9rem; margin-top: 10px; opacity: 0.9;">
                        Status: {status_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🏆 Worker Leaderboard & Behavioral Audit")

        leaderboard = filtered_df.groupby('Worker').agg({
            'Total Moved': 'sum',
            'Standby IBC': 'sum',
            'Time On Forklift (hrs)': 'mean',
            'Time Off Forklift (hrs)': 'mean'
        }).reset_index()
        
        leaderboard = leaderboard.sort_values(by='Total Moved', ascending=False)
        leaderboard.rename(columns={
            'Total Moved': 'Total Tasks Completed',
            'Time On Forklift (hrs)': 'Avg Time On (hrs)',
            'Time Off Forklift (hrs)': 'Avg Time Off (hrs)'
        }, inplace=True)
        
        # Advanced matplotlib background gradient
        styled_leaderboard = leaderboard.style.background_gradient(
            subset=['Total Tasks Completed'], cmap='ocean'
        ).background_gradient(
            subset=['Avg Time On (hrs)'], cmap='Blues'
        ).background_gradient(
            subset=['Avg Time Off (hrs)'], cmap='Reds'
        ).format({
            'Avg Time On (hrs)': "{:.1f}",
            'Avg Time Off (hrs)': "{:.1f}"
        })
        
        st.dataframe(styled_leaderboard, hide_index=True)

    else:
        st.warning("No data found for the selected filters.")

with tab2:
    st.markdown("### 📅 Shift Roster Planning")
    st.markdown("Management of weekly shift rotations (Team A and Team B).")
    
    # Calculate the ISO week from the selected start filter
    iso_year, current_week, iso_day = start_filter.isocalendar()
    
    def get_shift_teams_for_roster(week_num):
        # Base query from master df, bypassing the global date filter
        mask = df['Date'].apply(lambda x: x.isocalendar()[1]) == week_num
        
        # Apply the other filters dynamically
        if selected_worker != "All Workers":
            mask = mask & (df['Worker'] == selected_worker)
        if selected_dept != "All Departments":
            mask = mask & (df['Department'] == selected_dept)
        if selected_shift != "All Shifts":
            mask = mask & (df['Shift'] == selected_shift)
            
        week_df = df[mask]
        
        # Extract unique workers
        morning_team = sorted(week_df[week_df['Shift'] == 'Morning Shift']['Worker'].unique().tolist())
        night_team = sorted(week_df[week_df['Shift'] == 'Night Shift']['Worker'].unique().tolist())
        
        return morning_team, night_team
        
    last_week = current_week - 1
    next_week = current_week + 1
    
    st.info(f"**Reference Filter Date:** {start_filter.strftime('%B %d, %Y')} (ISO Week {current_week})")
    
    col_w1, col_w2, col_w3 = st.columns(3)
    
    with col_w1:
        st.markdown(f"#### ⏪ Last Week (Week {last_week})")
        morning_team, night_team = get_shift_teams_for_roster(last_week)
        
        st.markdown("☀️ **Morning Shift:**")
        st.markdown("\n".join([f"- {w}" for w in morning_team]) if morning_team else "- *No staff in filter*")
            
        st.markdown("🌙 **Night Shift:**")
        st.markdown("\n".join([f"- {w}" for w in night_team]) if night_team else "- *No staff in filter*")
            
    with col_w2:
        st.markdown(f"#### 🔽 Current Week (Week {current_week})")
        morning_team, night_team = get_shift_teams_for_roster(current_week)
        
        st.markdown("☀️ **Morning Shift:**")
        st.markdown("\n".join([f"- {w}" for w in morning_team]) if morning_team else "- *No staff in filter*")
            
        st.markdown("🌙 **Night Shift:**")
        st.markdown("\n".join([f"- {w}" for w in night_team]) if night_team else "- *No staff in filter*")
        
    with col_w3:
        st.markdown(f"#### ⏩ Next Week (Week {next_week})")
        morning_team, night_team = get_shift_teams_for_roster(next_week)
        
        st.markdown("☀️ **Morning Shift:**")
        st.markdown("\n".join([f"- {w}" for w in morning_team]) if morning_team else "- *No staff in filter*")
            
        st.markdown("🌙 **Night Shift:**")
        st.markdown("\n".join([f"- {w}" for w in night_team]) if night_team else "- *No staff in filter*")

st.markdown("---")
st.markdown("### 📋 Database Export")
col_exp1, col_exp2 = st.columns(2)
with col_exp1:
    st.download_button(
        label=f"⬇️ Download Filtered View ({len(filtered_df):,} rows)",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='filtered_operations_report.csv',
        mime='text/csv'
    )
with col_exp2:
    st.download_button(
        label="⬇️ Download Full Master Dataset (CSV)",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='master_roster_operations_report.csv',
        mime='text/csv'
    )
