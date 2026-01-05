"""Streamlit dashboard for Rural Connectivity Mapper 2026.

This module provides an interactive web dashboard for visualizing and analyzing
connectivity data from ANATEL, IBGE, and Starlink.
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.data_utils import load_data, save_data
from src.utils.anatel_utils import (
    fetch_anatel_broadband_data,
    fetch_anatel_mobile_data,
    get_anatel_provider_stats,
    convert_anatel_to_connectivity_points
)
from src.utils.ibge_utils import (
    fetch_ibge_municipalities,
    get_rural_areas_needing_connectivity,
    get_ibge_statistics_summary
)
from src.utils.starlink_utils import (
    check_starlink_availability,
    get_starlink_service_plans,
    get_starlink_coverage_map,
    get_starlink_vs_competitors
)
from src.utils.country_config import (
    get_supported_countries,
    get_country_config,
    get_latam_summary
)

# Page configuration
st.set_page_config(
    page_title="Rural Connectivity Mapper 2026",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2ca02c;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main dashboard application."""
    
    # Header
    st.markdown('<div class="main-header">🛰️ Rural Connectivity Mapper 2026</div>', 
                unsafe_allow_html=True)
    st.markdown("**Analyzing Starlink expansion and connectivity across Latin America**")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=Connectivity+Mapper", 
                 use_container_width=True)
        st.markdown("---")
        
        # Country selection
        st.subheader("🌍 Country Selection")
        countries = get_supported_countries()
        country_names = {code: get_country_config(code).name for code in countries}
        selected_country = st.selectbox(
            "Select Country",
            options=countries,
            format_func=lambda x: f"{country_names[x]} ({x})",
            index=0
        )
        
        country_config = get_country_config(selected_country)
        st.info(f"""
        **{country_config.name}**
        - 🏛️ Regulator: {country_config.telecom_regulator}
        - 📊 Stats Agency: {country_config.stats_agency}
        - 💱 Currency: {country_config.currency}
        - 🗣️ Language: {country_config.official_language}
        """)
        
        st.markdown("---")
        
        # View selection
        st.subheader("📊 Dashboard Views")
        view = st.radio(
            "Select View",
            ["Overview", "ANATEL Data", "IBGE Demographics", 
             "Starlink Availability", "LATAM Comparison", "Interactive Map"]
        )
        
        st.markdown("---")
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Main content based on selected view
    if view == "Overview":
        show_overview(selected_country)
    elif view == "ANATEL Data":
        show_anatel_data(selected_country)
    elif view == "IBGE Demographics":
        show_ibge_data(selected_country)
    elif view == "Starlink Availability":
        show_starlink_data(selected_country)
    elif view == "LATAM Comparison":
        show_latam_comparison()
    elif view == "Interactive Map":
        show_interactive_map(selected_country)


def show_overview(country_code: str):
    """Show overview dashboard."""
    st.markdown('<div class="sub-header">📈 Connectivity Overview</div>', 
                unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Providers", "12+", delta="3 new")
    with col2:
        st.metric("Avg Download Speed", "85.5 Mbps", delta="12.3 Mbps")
    with col3:
        st.metric("Coverage", "78.5%", delta="5.2%")
    with col4:
        st.metric("Starlink Users", "550K", delta="50K")
    
    st.markdown("---")
    
    # Two column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Provider Market Share")
        provider_stats = get_anatel_provider_stats()
        
        if country_code == 'BR' and provider_stats:
            df = pd.DataFrame([
                {'Provider': k, 'Market Share': v['market_share']} 
                for k, v in provider_stats.items()
            ])
            fig = px.pie(df, values='Market Share', names='Provider', 
                        title='Market Share by Provider')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🚀 Speed Distribution")
        speeds_data = {
            'Provider': ['Starlink', 'Claro', 'Vivo', 'TIM', 'Oi'],
            'Download (Mbps)': [150, 95, 90, 85, 60],
            'Upload (Mbps)': [15, 14, 13, 12, 8]
        }
        df_speeds = pd.DataFrame(speeds_data)
        fig = go.Figure(data=[
            go.Bar(name='Download', x=df_speeds['Provider'], y=df_speeds['Download (Mbps)']),
            go.Bar(name='Upload', x=df_speeds['Provider'], y=df_speeds['Upload (Mbps)'])
        ])
        fig.update_layout(barmode='group', title='Speed Comparison')
        st.plotly_chart(fig, use_container_width=True)
    
    # IBGE Summary for Brazil
    if country_code == 'BR':
        st.markdown("---")
        st.subheader("📊 IBGE Statistics Summary")
        ibge_summary = get_ibge_statistics_summary()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Municipalities", f"{ibge_summary['total_municipalities']:,}")
            st.metric("Rural Population", f"{ibge_summary['rural_population']:,}")
        with col2:
            st.metric("Rural Internet Access", f"{ibge_summary['rural_households_with_internet']}%")
            st.metric("Digital Divide", f"{ibge_summary['urban_rural_digital_divide_percentage']}%")
        with col3:
            st.metric("Low Coverage Areas", f"{ibge_summary['municipalities_with_low_coverage']:,}")
            st.metric("Priority States", len(ibge_summary['priority_states']))


def show_anatel_data(country_code: str):
    """Show ANATEL data view."""
    st.markdown('<div class="sub-header">📡 ANATEL Connectivity Data</div>', 
                unsafe_allow_html=True)
    
    if country_code != 'BR':
        st.warning(f"ANATEL data is only available for Brazil. Showing data for {country_code}'s telecom regulator would be displayed here.")
        return
    
    # State filter
    states = ['All', 'SP', 'RJ', 'MG', 'BA', 'CE', 'DF']
    selected_state = st.selectbox("Filter by State", states)
    state_filter = None if selected_state == 'All' else selected_state
    
    # Fetch data
    broadband_data = fetch_anatel_broadband_data(state=state_filter)
    mobile_data = fetch_anatel_mobile_data(state=state_filter)
    
    # Display broadband data
    st.subheader("📶 Broadband Fixed Internet")
    if broadband_data:
        df_broadband = pd.DataFrame(broadband_data)
        st.dataframe(df_broadband, use_container_width=True)
        
        # Visualization
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(df_broadband, x='municipality', y='subscribers', 
                        color='provider', title='Subscribers by Municipality')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.scatter(df_broadband, x='avg_speed_mbps', y='coverage_percentage',
                           size='subscribers', color='technology', 
                           hover_data=['municipality', 'provider'],
                           title='Speed vs Coverage')
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Display mobile data
    st.subheader("📱 Mobile Coverage")
    if mobile_data:
        df_mobile = pd.DataFrame(mobile_data)
        st.dataframe(df_mobile, use_container_width=True)


def show_ibge_data(country_code: str):
    """Show IBGE demographic data."""
    st.markdown('<div class="sub-header">👥 IBGE Demographic Data</div>', 
                unsafe_allow_html=True)
    
    if country_code != 'BR':
        st.warning(f"IBGE data is only available for Brazil. Data from {get_country_config(country_code).stats_agency} would be displayed here.")
        return
    
    # Rural areas needing connectivity
    st.subheader("🏘️ Priority Rural Areas")
    priority_areas = get_rural_areas_needing_connectivity()
    
    if priority_areas:
        df_priority = pd.DataFrame(priority_areas)
        st.dataframe(df_priority, use_container_width=True)
        
        # Visualization
        fig = px.scatter(df_priority, x='internet_coverage', y='priority_score',
                        size='rural_population', color='state',
                        hover_data=['municipality'],
                        title='Priority Areas: Coverage vs Priority Score',
                        labels={'internet_coverage': 'Internet Coverage (%)',
                               'priority_score': 'Priority Score'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Download option
        csv = df_priority.to_csv(index=False)
        st.download_button(
            label="📥 Download Priority Areas Data (CSV)",
            data=csv,
            file_name=f"priority_rural_areas_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )


def show_starlink_data(country_code: str):
    """Show Starlink availability data."""
    st.markdown('<div class="sub-header">🛰️ Starlink Availability</div>', 
                unsafe_allow_html=True)
    
    # Coverage map
    st.subheader("📡 Coverage Map")
    coverage = get_starlink_coverage_map(country_code)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Service Status", coverage.get('service_status', 'Unknown').title())
        st.metric("Coverage", f"{coverage.get('coverage_percentage', 0)}%")
    with col2:
        st.metric("Active Users", f"{coverage.get('active_users', 0):,}")
        st.metric("Ground Stations", coverage.get('ground_stations', 0))
    with col3:
        st.metric("Satellites Overhead", coverage.get('total_satellites_overhead', 0))
        if 'launch_date' in coverage:
            st.metric("Launch Date", coverage['launch_date'])
    
    # Service plans
    st.markdown("---")
    st.subheader("💰 Service Plans")
    plans = get_starlink_service_plans()
    
    if plans:
        df_plans = pd.DataFrame(plans)
        st.dataframe(df_plans[['name', 'price_brl_monthly', 'hardware_cost_brl', 
                                'download_speed', 'latency', 'suitable_for']], 
                    use_container_width=True)
    
    # Availability checker
    st.markdown("---")
    st.subheader("📍 Check Availability at Location")
    
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude", value=-15.7801, format="%.4f")
    with col2:
        lon = st.number_input("Longitude", value=-47.9292, format="%.4f")
    
    if st.button("Check Availability"):
        with st.spinner("Checking Starlink availability..."):
            availability = check_starlink_availability(lat, lon)
            
            if availability['service_available']:
                st.success(f"✅ Starlink is available at ({lat}, {lon})")
            else:
                st.warning(f"⏳ Starlink status: {availability['status']}")
            
            st.json(availability)


def show_latam_comparison():
    """Show LATAM countries comparison."""
    st.markdown('<div class="sub-header">🌎 LATAM Countries Comparison</div>', 
                unsafe_allow_html=True)
    
    # Get summary
    summary = get_latam_summary()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Countries", summary['total_countries'])
    with col2:
        st.metric("Unique Providers", summary['unique_providers_count'])
    with col3:
        st.metric("Languages", len(summary['languages']))
    with col4:
        st.metric("Currencies", len(summary['currencies']))
    
    # Country details
    st.subheader("📊 Country Details")
    countries_df = pd.DataFrame([
        {
            'Code': code,
            'Country': data['name'],
            'Language': data['language'],
            'Currency': data['currency'],
            'Providers': data['providers_count']
        }
        for code, data in summary['countries'].items()
    ])
    st.dataframe(countries_df, use_container_width=True)
    
    # Starlink coverage comparison
    st.subheader("🛰️ Starlink Coverage Across LATAM")
    
    coverage_data = []
    for country_code in get_supported_countries():
        coverage = get_starlink_coverage_map(country_code)
        if coverage.get('coverage_percentage'):
            coverage_data.append({
                'Country': coverage.get('country_name', country_code),
                'Coverage %': coverage.get('coverage_percentage', 0),
                'Active Users': coverage.get('active_users', 0),
                'Ground Stations': coverage.get('ground_stations', 0)
            })
    
    if coverage_data:
        df_coverage = pd.DataFrame(coverage_data)
        fig = px.bar(df_coverage, x='Country', y='Coverage %', 
                    title='Starlink Coverage by Country',
                    color='Coverage %', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)


def show_interactive_map(country_code: str):
    """Show interactive map."""
    st.markdown('<div class="sub-header">🗺️ Interactive Connectivity Map</div>', 
                unsafe_allow_html=True)
    
    # Get country center
    country_config = get_country_config(country_code)
    center_lat, center_lon = country_config.coordinates_center
    
    # Create map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5)
    
    # Add markers for sample data
    if country_code == 'BR':
        # Add ANATEL data points
        broadband_data = fetch_anatel_broadband_data()
        for record in broadband_data:
            # Get coordinates (simplified)
            coords_map = {
                'São Paulo': (-23.5505, -46.6333),
                'Rio de Janeiro': (-22.9068, -43.1729),
                'Belo Horizonte': (-19.9167, -43.9345),
                'Salvador': (-12.9714, -38.5014),
                'Fortaleza': (-3.7172, -38.5433)
            }
            coords = coords_map.get(record['municipality'])
            if coords:
                folium.Marker(
                    coords,
                    popup=f"<b>{record['municipality']}</b><br>"
                          f"Provider: {record['provider']}<br>"
                          f"Speed: {record['avg_speed_mbps']} Mbps<br>"
                          f"Coverage: {record['coverage_percentage']}%",
                    tooltip=record['municipality'],
                    icon=folium.Icon(color='blue', icon='info-sign')
                ).add_to(m)
    
    # Display map
    st_folium(m, width=1200, height=600)
    
    st.info("💡 Click on markers to see connectivity details for each location")


if __name__ == "__main__":
    main()
