import folium
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium

from kerala_data import df

# Configure the Streamlit page before rendering any UI components.
st.set_page_config(
    page_title="Kerala Smart District Dashboard",
    page_icon="🌴",
    layout="wide",
)

# Global CSS is the easiest way to align Streamlit widgets with a custom dashboard look.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(19, 78, 74, 0.12), transparent 26%),
            radial-gradient(circle at top right, rgba(14, 116, 144, 0.08), transparent 20%),
            linear-gradient(180deg, #f7fbfa 0%, #eff6f4 100%);
        color: #163536;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero-card {
        background: linear-gradient(135deg, #0f3d3e 0%, #14532d 48%, #0f766e 100%);
        padding: 2rem 2.2rem;
        border-radius: 24px;
        color: #ffffff;
        box-shadow: 0 24px 60px rgba(15, 61, 62, 0.22);
        margin-bottom: 1.4rem;
    }

    .hero-kicker {
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-size: 0.76rem;
        opacity: 0.8;
        margin-bottom: 0.6rem;
    }

    .hero-title {
        font-size: 2.35rem;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 0.7rem;
    }

    .hero-text {
        font-size: 1rem;
        max-width: 780px;
        color: rgba(255, 255, 255, 0.88);
        margin-bottom: 0;
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #123c3d;
        margin: 0.25rem 0 0.9rem 0;
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.98);
        border: 1px solid rgba(15, 61, 62, 0.1);
        padding: 1rem;
        border-radius: 18px;
        box-shadow: 0 12px 30px rgba(17, 24, 39, 0.07);
    }

    .insight-card {
        background: rgba(255, 255, 255, 0.98);
        border: 1px solid rgba(15, 61, 62, 0.1);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        box-shadow: 0 12px 30px rgba(17, 24, 39, 0.07);
        min-height: 132px;
    }

    .insight-label {
        color: #4b5563;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }

    .insight-value {
        color: #0f3d3e;
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }

    .insight-copy {
        color: #475569;
        font-size: 0.95rem;
        margin: 0;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fffd 0%, #eef7f3 100%);
    }

    [data-testid="stSidebar"] * {
        color: #143536 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"],
    [data-testid="stSidebar"] [data-baseweb="popover"] {
        color: #143536 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.98) !important;
        border: 1px solid rgba(15, 118, 110, 0.28) !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 24px rgba(15, 61, 62, 0.08) !important;
        min-height: 52px !important;
    }

    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background: #dff4ea !important;
        border-radius: 999px !important;
        border: 1px solid rgba(15, 118, 110, 0.18) !important;
    }

    [data-testid="stSidebar"] [data-baseweb="tag"] span,
    [data-testid="stSidebar"] [data-baseweb="tag"] svg {
        color: #0f5d57 !important;
        fill: #0f5d57 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] button {
        color: #0f5d57 !important;
        background: #e6f6ef !important;
        border: 1px solid rgba(15, 93, 87, 0.22) !important;
        opacity: 1 !important;
        border-radius: 999px !important;
        width: 28px !important;
        height: 28px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] button:hover,
    [data-testid="stSidebar"] [data-baseweb="select"] button:focus,
    [data-testid="stSidebar"] [data-baseweb="select"] button:focus-visible {
        color: #ffffff !important;
        background: #0f766e !important;
        border-color: #0f766e !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.16) !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] button:hover *,
    [data-testid="stSidebar"] [data-baseweb="select"] button:focus *,
    [data-testid="stSidebar"] [data-baseweb="select"] button:focus-visible * {
        color: #ffffff !important;
        fill: #ffffff !important;
        stroke: #ffffff !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] button svg,
    [data-testid="stSidebar"] [data-baseweb="select"] [role="button"] svg {
        color: #0f5d57 !important;
        fill: #0f5d57 !important;
        stroke: #0f5d57 !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] [role="button"] {
        color: #0f5d57 !important;
        background: #e6f6ef !important;
        border-radius: 999px !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] [role="button"]:hover,
    [data-testid="stSidebar"] [data-baseweb="select"] [role="button"]:focus,
    [data-testid="stSidebar"] [data-baseweb="select"] [role="button"]:focus-visible {
        color: #ffffff !important;
        background: #0f766e !important;
        outline: none !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] [role="button"]:hover *,
    [data-testid="stSidebar"] [data-baseweb="select"] [role="button"]:focus *,
    [data-testid="stSidebar"] [data-baseweb="select"] [role="button"]:focus-visible * {
        color: #ffffff !important;
        fill: #ffffff !important;
        stroke: #ffffff !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] button:hover svg,
    [data-testid="stSidebar"] [data-baseweb="select"] button:focus svg,
    [data-testid="stSidebar"] [data-baseweb="select"] button:focus-visible svg {
        color: #ffffff !important;
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }

    [data-testid="stSidebar"] button[kind="secondary"] {
        border-radius: 14px !important;
        border: 1px solid rgba(15, 118, 110, 0.18) !important;
        background: #ffffff !important;
        color: #0f5d57 !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] button[kind="secondary"]:hover {
        background: #dff4ea !important;
        border-color: rgba(15, 118, 110, 0.28) !important;
        color: #0f5d57 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] button[title="Clear all"],
    [data-testid="stSidebar"] [data-baseweb="select"] button[aria-label="Clear all"],
    [data-testid="stSidebar"] [data-baseweb="select"] [role="button"][title="Clear all"],
    [data-testid="stSidebar"] [data-baseweb="select"] [role="button"][aria-label="Clear all"] {
        display: none !important;
    }

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] .st-b8,
    [data-testid="stSidebar"] .st-b9 {
        color: #143536 !important;
        caret-color: #0f766e !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] input {
        caret-color: transparent !important;
        cursor: pointer !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] div {
        cursor: pointer !important;
    }

    [data-testid="stSidebar"] [role="listbox"],
    [data-testid="stSidebar"] ul {
        background: rgba(255, 255, 255, 0.99) !important;
        border-radius: 14px !important;
    }

    [data-testid="stSidebar"] [data-baseweb="checkbox"] > div {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 8px !important;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: #123c3d !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.75rem;
    }

    .stTabs [data-baseweb="tab"] {
        color: #4b5563;
        font-weight: 700;
        padding: 0.35rem 0.1rem 0.65rem 0.1rem;
    }

    .stTabs [aria-selected="true"] {
        color: #0f766e !important;
    }

    .stCheckbox label,
    .stSelectbox label,
    .stMultiSelect label {
        color: #123c3d !important;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Keep a working copy so filters/sorts do not mutate the imported source dataframe.
base_df = df.copy()

# These mappings let the UI show readable names while the charts still use dataframe column keys.
metric_labels = {
    "Livability_Score": "Livability Score",
    "Literacy_Rate": "Literacy Rate",
    "Tourists_Lakhs": "Tourists (Lakhs)",
    "IT_Companies": "IT Companies",
    "MSME_Count": "MSME Count",
}
metric_suffix = {
    "Livability_Score": "",
    "Literacy_Rate": "%",
    "Tourists_Lakhs": " lakhs",
    "IT_Companies": "",
    "MSME_Count": "",
}

# Sidebar controls drive the filtered dashboard state for every downstream chart and summary.
st.sidebar.header("Dashboard Controls")
all_districts = sorted(base_df["District"].tolist())

if "district_filter" not in st.session_state:
    st.session_state["district_filter"] = all_districts

sidebar_action_cols = st.sidebar.columns(2)
if sidebar_action_cols[0].button("Select all", use_container_width=True):
    st.session_state["district_filter"] = all_districts
if sidebar_action_cols[1].button("Clear all", use_container_width=True):
    st.session_state["district_filter"] = []

selected_districts = st.sidebar.multiselect(
    "Districts",
    options=all_districts,
    key="district_filter",
)
sort_metric = st.sidebar.selectbox(
    "Focus metric",
    list(metric_labels.keys()),
    format_func=lambda value: metric_labels[value],
)
show_raw_data = st.sidebar.checkbox("Show data table", value=False)

# Apply the sidebar filters first so all metrics, cards, and charts stay in sync.
selected_districts = selected_districts or []
if not selected_districts:
    st.warning("Select at least one district from the sidebar to render the dashboard.")
    st.stop()

filtered_df = base_df[base_df["District"].isin(selected_districts)].copy()
if filtered_df.empty:
    st.warning("Select at least one district from the sidebar to render the dashboard.")
    st.stop()

# The selected focus metric decides the ranking logic used by summaries and the focus chart.
filtered_df = filtered_df.sort_values(sort_metric, ascending=False)

top_district = filtered_df.iloc[0]
avg_literacy = filtered_df["Literacy_Rate"].mean()
total_it = int(filtered_df["IT_Companies"].sum())
total_tourists = filtered_df["Tourists_Lakhs"].sum()
total_msmes = int(filtered_df["MSME_Count"].sum())

st.markdown(
    f"""
    <div class="hero-card">
        <div class="hero-kicker">Kerala Development Intelligence</div>
        <div class="hero-title">Kerala Smart District Dashboard</div>
        <p class="hero-text">
            A more polished view of literacy, tourism, enterprise growth, and livability trends across
            {len(filtered_df)} selected districts. The dashboard is currently focused on
            <b>{metric_labels[sort_metric]}</b>, so rankings and the lead district summary respond to that choice.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# The top-level metric row gives a fast dashboard summary before the detailed visual sections.
metric_cols = st.columns(4)
metric_cols[0].metric("Districts in View", len(filtered_df))
metric_cols[1].metric("Avg Literacy Rate", f"{avg_literacy:.1f}%")
metric_cols[2].metric("Total IT Companies", f"{total_it}")
metric_cols[3].metric("Tourists (Lakhs)", f"{total_tourists:.1f}")

insight_cols = st.columns(3)
insight_cols[0].markdown(
    f"""
    <div class="insight-card">
        <div class="insight-label">Top Performer</div>
        <div class="insight-value">{top_district["District"]}</div>
        <p class="insight-copy">
            Leads the current view in {metric_labels[sort_metric].lower()} with a value of {top_district[sort_metric]}{metric_suffix[sort_metric]}.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
insight_cols[1].markdown(
    f"""
    <div class="insight-card">
        <div class="insight-label">Enterprise Footprint</div>
        <div class="insight-value">{total_msmes:,} MSMEs</div>
        <p class="insight-copy">
            Small and medium enterprises add useful context beside tourism and technology concentration.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
insight_cols[2].markdown(
    f"""
    <div class="insight-card">
        <div class="insight-label">Coverage</div>
        <div class="insight-value">{filtered_df["District"].nunique()} districts</div>
        <p class="insight-copy">
            Filter the dashboard to compare a few districts or keep the full-state view for broader patterns.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

color_scale = ["#d1fae5", "#86efac", "#34d399", "#0f766e", "#134e4a"]
plot_bg = "rgba(255,255,255,0.98)"


def style_figure(fig):
    # Centralize Plotly styling so every chart shares the same spacing, fonts, and contrast.
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=plot_bg,
        margin=dict(l=24, r=24, t=64, b=32),
        font=dict(family="Manrope, sans-serif", color="#163536"),
        title_font=dict(size=20, color="#123c3d"),
        title_x=0,
        coloraxis_colorbar=dict(
            tickfont=dict(color="#163536"),
            title_font=dict(color="#163536"),
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        tickfont=dict(size=12, color="#163536"),
        title_font=dict(size=13, color="#365156"),
    )
    fig.update_yaxes(
        gridcolor="rgba(15, 61, 62, 0.1)",
        tickfont=dict(size=12, color="#163536"),
        title_font=dict(size=13, color="#365156"),
    )
    return fig


def format_top_bottom(dataframe, column, decimals=1, suffix=""):
    # Reuse the same summary sentence pattern below charts for easier maintenance.
    sorted_df = dataframe.sort_values(column, ascending=False)
    top_row = sorted_df.iloc[0]
    bottom_row = sorted_df.iloc[-1]
    top_value = f"{top_row[column]:,.{decimals}f}{suffix}"
    bottom_value = f"{bottom_row[column]:,.{decimals}f}{suffix}"
    return (
        f"{top_row['District']} leads at {top_value}, while "
        f"{bottom_row['District']} is lowest at {bottom_value}."
    )


def format_integer_top_bottom(dataframe, column):
    # Variant for count-like metrics where decimal formatting would look awkward.
    sorted_df = dataframe.sort_values(column, ascending=False)
    top_row = sorted_df.iloc[0]
    bottom_row = sorted_df.iloc[-1]
    return (
        f"{top_row['District']} has the highest {column.replace('_', ' ').lower()} at "
        f"{int(top_row[column]):,}, while {bottom_row['District']} has the lowest at "
        f"{int(bottom_row[column]):,}."
    )


# Tabs separate overview, comparison, and map views without making the page feel too long.
overview_tab, comparison_tab, map_tab = st.tabs(["Overview", "Comparison", "Map"])

with overview_tab:
    st.markdown('<div class="section-title">Livability Snapshot</div>', unsafe_allow_html=True)
    overview_col1, overview_col2 = st.columns([1.15, 1])

    with overview_col1:
        literacy_fig = px.bar(
            filtered_df.sort_values("Literacy_Rate", ascending=True),
            x="Literacy_Rate",
            y="District",
            orientation="h",
            color="Literacy_Rate",
            color_continuous_scale=color_scale,
            title="Literacy Rate by District",
            text="Literacy_Rate",
        )
        literacy_fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        style_figure(literacy_fig)
        st.plotly_chart(literacy_fig, width="stretch")
        st.caption(
            "This chart compares literacy across the selected districts. "
            + format_top_bottom(filtered_df, "Literacy_Rate", decimals=1, suffix="%")
            + f" The selected-district average is {filtered_df['Literacy_Rate'].mean():.1f}%."
        )

    with overview_col2:
        # Bubble size adds MSME scale without needing a separate chart.
        score_fig = px.scatter(
            filtered_df,
            x="Tourists_Lakhs",
            y="IT_Companies",
            size="MSME_Count",
            color="Livability_Score",
            hover_name="District",
            color_continuous_scale=color_scale,
            title="Tourism, IT, and MSME Ecosystem",
            size_max=38,
        )
        style_figure(score_fig)
        score_fig.update_yaxes(showgrid=True)
        score_fig.update_xaxes(showgrid=True, gridcolor="rgba(15, 61, 62, 0.08)")
        st.plotly_chart(score_fig, width="stretch")
        top_score = filtered_df.sort_values("Livability_Score", ascending=False).iloc[0]
        st.caption(
            "This bubble chart combines tourism, IT companies, MSME size, and livability in one view. "
            f"{top_score['District']} stands out with a livability score of {top_score['Livability_Score']}, "
            f"{top_score['Tourists_Lakhs']} lakhs of tourists, and {int(top_score['IT_Companies'])} IT companies. "
            "Districts farther to the right attract more tourists, higher points show stronger IT presence, "
            "and larger bubbles represent more MSMEs."
        )

    # This chart is the clearest visible response to the selected focus metric in the sidebar.
    focus_fig = px.bar(
        filtered_df.sort_values(sort_metric, ascending=False),
        x="District",
        y=sort_metric,
        color=sort_metric,
        color_continuous_scale=color_scale,
        title=f"Focus Metric: {metric_labels[sort_metric]}",
        text=sort_metric,
    )
    if sort_metric in ["Literacy_Rate", "Tourists_Lakhs", "Livability_Score"]:
        focus_fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    else:
        focus_fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    style_figure(focus_fig)
    focus_fig.update_layout(margin=dict(l=24, r=24, t=64, b=130))
    focus_fig.update_xaxes(tickangle=45, automargin=True)
    st.plotly_chart(focus_fig, width="stretch")
    st.caption(
        f"This chart directly responds to the selected focus metric. It ranks districts by {metric_labels[sort_metric].lower()}, "
        f"with {top_district['District']} currently leading at {top_district[sort_metric]}{metric_suffix[sort_metric]}."
    )

with comparison_tab:
    st.markdown('<div class="section-title">District Comparison</div>', unsafe_allow_html=True)
    comp_col1, comp_col2 = st.columns(2)

    with comp_col1:
        tourism_fig = px.bar(
            filtered_df.sort_values("Tourists_Lakhs", ascending=False),
            x="District",
            y="Tourists_Lakhs",
            color="Tourists_Lakhs",
            color_continuous_scale=color_scale,
            title="Tourist Arrivals",
            text="Tourists_Lakhs",
        )
        tourism_fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        style_figure(tourism_fig)
        tourism_fig.update_layout(margin=dict(l=24, r=24, t=64, b=150))
        tourism_fig.update_xaxes(tickangle=90, automargin=True)
        st.plotly_chart(tourism_fig, width="stretch")
        st.caption(
            "This graph shows tourist arrivals in lakhs for each selected district. "
            + format_top_bottom(filtered_df, "Tourists_Lakhs", decimals=1, suffix=" lakhs")
            + " Higher bars indicate districts with stronger tourism pull."
        )

    with comp_col2:
        it_fig = px.bar(
            filtered_df.sort_values("IT_Companies", ascending=False),
            x="District",
            y="IT_Companies",
            color="IT_Companies",
            color_continuous_scale=color_scale,
            title="IT Companies",
            text="IT_Companies",
        )
        it_fig.update_traces(textposition="outside")
        style_figure(it_fig)
        it_fig.update_layout(margin=dict(l=24, r=24, t=64, b=150))
        it_fig.update_xaxes(tickangle=90, automargin=True)
        st.plotly_chart(it_fig, width="stretch")
        st.caption(
            "This graph compares the number of IT companies by district. "
            + format_integer_top_bottom(filtered_df, "IT_Companies")
            + " Taller bars suggest stronger technology and business concentration."
        )

    rank_fig = px.bar(
        filtered_df.sort_values("Livability_Score", ascending=False),
        x="District",
        y="Livability_Score",
        color="Livability_Score",
        color_continuous_scale=color_scale,
        title="Livability Score Ranking",
        text="Livability_Score",
    )
    rank_fig.update_traces(textposition="outside")
    style_figure(rank_fig)
    rank_fig.update_layout(margin=dict(l=24, r=24, t=64, b=135))
    rank_fig.update_xaxes(tickangle=45, automargin=True)
    st.plotly_chart(rank_fig, width="stretch")
    st.caption(
        "This ranking combines literacy, tourism, and IT presence into one livability score. "
        + format_top_bottom(filtered_df, "Livability_Score", decimals=1)
        + " Districts with higher scores perform better overall across the dashboard indicators."
    )

with map_tab:
    st.markdown('<div class="section-title">Interactive District Map</div>', unsafe_allow_html=True)

    # Folium gives us a lightweight geographic view while Streamlit handles the surrounding layout.
    kerala_map = folium.Map(
        location=[10.5, 76.3],
        zoom_start=7,
        tiles="CartoDB positron",
    )

    for _, row in filtered_df.iterrows():
        # Marker color turns the livability score into a quick qualitative signal.
        if row["Livability_Score"] >= 60:
            color = "#15803d"
        elif row["Livability_Score"] >= 45:
            color = "#f59e0b"
        else:
            color = "#dc2626"

        popup = f"""
        <div style="font-family: Manrope, sans-serif; min-width: 190px;">
            <div style="font-size: 16px; font-weight: 800; color: #123c3d; margin-bottom: 6px;">{row['District']}</div>
            <div>Literacy: <b>{row['Literacy_Rate']}%</b></div>
            <div>Tourists: <b>{row['Tourists_Lakhs']} lakhs</b></div>
            <div>IT Companies: <b>{row['IT_Companies']}</b></div>
            <div>MSMEs: <b>{row['MSME_Count']:,}</b></div>
            <div>Livability: <b>{row['Livability_Score']}</b></div>
        </div>
        """

        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=row["IT_Companies"] / 18 + 5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.82,
            weight=2,
            popup=folium.Popup(popup, max_width=260),
            tooltip=row["District"],
        ).add_to(kerala_map)

    st_folium(kerala_map, width=None, height=560)
    st.caption(
        "This map places each district geographically. Circle size reflects IT company count, "
        "and marker color reflects livability level: green for stronger performance, orange for mid-range, "
        "and red for lower scores among the selected districts."
    )

if show_raw_data:
    # Keep the raw table optional so advanced users can inspect data without crowding the default view.
    st.markdown('<div class="section-title">District Dataset</div>', unsafe_allow_html=True)
    display_df = filtered_df.rename(
        columns={
            "Literacy_Rate": "Literacy Rate (%)",
            "Tourists_Lakhs": "Tourists (Lakhs)",
            "IT_Companies": "IT Companies",
            "MSME_Count": "MSME Count",
            "Livability_Score": "Livability Score",
        }
    )
    st.dataframe(display_df, width="stretch", hide_index=True)
