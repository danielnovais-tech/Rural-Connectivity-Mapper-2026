#!/usr/bin/env python3
"""Streamlit Web Dashboard for Rural Connectivity Mapper 2026."""

import streamlit as st
import pandas as pd
import json
import csv
from datetime import datetime
from pathlib import Path
import io
import tempfile

from src.models import ConnectivityPoint, SpeedTest
from src.utils import (
    load_data, save_data, generate_report, simulate_router_impact,
    generate_map, analyze_temporal_evolution, measure_speed,
    validate_coordinates
)


# Configuration constants
DATA_PATH = 'src/data/pontos.json'
MAP_HEIGHT = 600  # Height in pixels for embedded maps


# Page configuration
st.set_page_config(
    page_title="Rural Connectivity Mapper 2026",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        padding-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stAlert {
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


def display_header():
    """Display dashboard header."""
    st.markdown('<div class="main-header">🌍 Rural Connectivity Mapper 2026</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Analyze and visualize rural internet connectivity across Brazil</div>', unsafe_allow_html=True)
    st.markdown("---")


def display_statistics(data):
    """Display key statistics from connectivity data."""
    if not data:
        st.warning("No data available to display statistics.")
        return
    
    # Calculate statistics
    total_points = len(data)
    avg_quality = sum(point['quality_score']['overall_score'] for point in data) / total_points
    avg_download = sum(point['speed_test']['download'] for point in data) / total_points
    avg_upload = sum(point['speed_test']['upload'] for point in data) / total_points
    avg_latency = sum(point['speed_test']['latency'] for point in data) / total_points
    
    # Count ratings
    ratings = [point['quality_score']['rating'] for point in data]
    excellent = ratings.count('Excellent')
    good = ratings.count('Good')
    fair = ratings.count('Fair')
    poor = ratings.count('Poor')
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Points", total_points)
        st.metric("Average Quality", f"{avg_quality:.1f}/100")
    
    with col2:
        st.metric("Avg Download", f"{avg_download:.1f} Mbps")
        st.metric("Avg Upload", f"{avg_upload:.1f} Mbps")
    
    with col3:
        st.metric("Avg Latency", f"{avg_latency:.1f} ms")
        st.metric("Excellent", excellent)
    
    with col4:
        st.metric("Good", good)
        st.metric("Fair/Poor", fair + poor)


def display_data_table(data):
    """Display connectivity data in a table."""
    if not data:
        st.warning("No data available to display.")
        return
    
    # Prepare data for display
    rows = []
    for point in data:
        row = {
            'Provider': point['provider'],
            'Latitude': point['latitude'],
            'Longitude': point['longitude'],
            'Download (Mbps)': round(point['speed_test']['download'], 2),
            'Upload (Mbps)': round(point['speed_test']['upload'], 2),
            'Latency (ms)': round(point['speed_test']['latency'], 2),
            'Quality Score': round(point['quality_score']['overall_score'], 2),
            'Rating': point['quality_score']['rating'],
            'Timestamp': point['timestamp']
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)


def upload_csv_data():
    """Handle CSV file upload and data import."""
    st.subheader("📤 Upload Connectivity Data")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload a CSV file with columns: latitude, longitude, provider, download, upload, latency, jitter, packet_loss"
    )
    
    if uploaded_file is not None:
        try:
            # Read CSV file
            content = uploaded_file.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(content))
            
            points = []
            for row in csv_reader:
                # Validate coordinates
                lat = float(row['latitude'])
                lon = float(row['longitude'])
                
                if not validate_coordinates(lat, lon):
                    st.warning(f"Skipping row with invalid coordinates: {row}")
                    continue
                
                # Create SpeedTest
                speed_test = SpeedTest(
                    download=float(row['download']),
                    upload=float(row['upload']),
                    latency=float(row['latency']),
                    jitter=float(row.get('jitter', 0)),
                    packet_loss=float(row.get('packet_loss', 0))
                )
                
                # Create ConnectivityPoint
                point = ConnectivityPoint(
                    latitude=lat,
                    longitude=lon,
                    provider=row['provider'],
                    speed_test=speed_test,
                    timestamp=row.get('timestamp', datetime.now().isoformat()),
                    point_id=row.get('id')
                )
                
                points.append(point.to_dict())
            
            if points:
                # Save to data file
                save_data(DATA_PATH, points)
                st.success(f"✅ Successfully imported {len(points)} connectivity points!")
                st.rerun()
            else:
                st.error("No valid data points found in the uploaded file.")
        
        except Exception as e:
            st.error(f"Error importing CSV: {e}")


def run_speed_test():
    """Run on-demand speed test."""
    st.subheader("🚀 On-Demand Speed Test")
    
    st.info("Click the button below to run a speed test on your current connection.")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("Run Speed Test", type="primary"):
            with st.spinner("Running speed test... This may take up to 60 seconds."):
                result = measure_speed()
                
                if result:
                    st.session_state['speed_test_result'] = result
                else:
                    st.error("Speed test failed. Please try again.")
    
    # Display results if available
    if 'speed_test_result' in st.session_state:
        result = st.session_state['speed_test_result']
        
        st.success("Speed test completed!")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Download", f"{result['download']:.2f} Mbps")
        with col2:
            st.metric("Upload", f"{result['upload']:.2f} Mbps")
        with col3:
            st.metric("Latency", f"{result['latency']:.2f} ms")
        with col4:
            st.metric("Stability", f"{result['stability']:.2f}%")


def visualize_map(data):
    """Display interactive map."""
    st.subheader("🗺️ Interactive Connectivity Map")
    
    if not data:
        st.warning("No data available for map visualization. Please upload data first.")
        return
    
    # Generate map
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as tmp:
            map_path = generate_map(data, tmp.name)
            
            # Read and display the HTML map
            with open(map_path, 'r', encoding='utf-8') as f:
                map_html = f.read()
            
            st.components.v1.html(map_html, height=MAP_HEIGHT, scrolling=True)
    
    except Exception as e:
        st.error(f"Error generating map: {e}")


def generate_reports(data):
    """Generate and download reports."""
    st.subheader("📊 Generate Reports")
    
    if not data:
        st.warning("No data available for report generation. Please upload data first.")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("JSON Report"):
            report_path = generate_report(data, 'json', 'dashboard_report.json')
            with open(report_path, 'r') as f:
                st.download_button(
                    "Download JSON",
                    f.read(),
                    file_name='connectivity_report.json',
                    mime='application/json'
                )
    
    with col2:
        if st.button("CSV Report"):
            report_path = generate_report(data, 'csv', 'dashboard_report.csv')
            with open(report_path, 'r') as f:
                st.download_button(
                    "Download CSV",
                    f.read(),
                    file_name='connectivity_report.csv',
                    mime='text/csv'
                )
    
    with col3:
        if st.button("TXT Report"):
            report_path = generate_report(data, 'txt', 'dashboard_report.txt')
            with open(report_path, 'r') as f:
                st.download_button(
                    "Download TXT",
                    f.read(),
                    file_name='connectivity_report.txt',
                    mime='text/plain'
                )
    
    with col4:
        if st.button("HTML Report"):
            report_path = generate_report(data, 'html', 'dashboard_report.html')
            with open(report_path, 'r') as f:
                st.download_button(
                    "Download HTML",
                    f.read(),
                    file_name='connectivity_report.html',
                    mime='text/html'
                )


def simulate_improvements(data):
    """Simulate router impact on connectivity."""
    st.subheader("🔧 Router Impact Simulation")
    
    if not data:
        st.warning("No data available for simulation. Please upload data first.")
        return
    
    st.info("Simulate 15-25% quality improvement from router upgrades")
    
    if st.button("Run Simulation", type="primary"):
        with st.spinner("Running simulation..."):
            improved_data = simulate_router_impact(data)
            
            # Save improved data
            save_data(DATA_PATH, improved_data)
            
            st.success("✅ Simulation completed and saved!")
            st.rerun()


def analyze_trends(data):
    """Display temporal evolution analysis."""
    st.subheader("📈 Temporal Analysis")
    
    if not data:
        st.warning("No data available for analysis. Please upload data first.")
        return
    
    analysis = analyze_temporal_evolution(data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Points Analyzed", analysis['total_points'])
        st.metric("Average Quality Score", f"{analysis['trends']['avg_quality_score']}/100")
        st.metric("Average Download Speed", f"{analysis['trends']['avg_download']} Mbps")
        st.metric("Average Latency", f"{analysis['trends']['avg_latency']} ms")
    
    with col2:
        st.write("**Key Insights:**")
        for insight in analysis['insights']:
            st.write(f"• {insight}")


def main():
    """Main dashboard application."""
    display_header()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page:",
        ["📊 Dashboard", "📤 Upload Data", "🚀 Speed Test", "🗺️ Map View", "📈 Analysis", "🔧 Simulation"]
    )
    
    # Load data
    data = load_data(DATA_PATH)
    
    # Display selected page
    if page == "📊 Dashboard":
        st.header("Dashboard Overview")
        display_statistics(data)
        st.markdown("---")
        st.subheader("Connectivity Data")
        display_data_table(data)
        st.markdown("---")
        generate_reports(data)
    
    elif page == "📤 Upload Data":
        upload_csv_data()
        if data:
            st.markdown("---")
            st.subheader("Current Data")
            display_data_table(data)
    
    elif page == "🚀 Speed Test":
        run_speed_test()
    
    elif page == "🗺️ Map View":
        visualize_map(data)
    
    elif page == "📈 Analysis":
        analyze_trends(data)
    
    elif page == "🔧 Simulation":
        simulate_improvements(data)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "**Rural Connectivity Mapper 2026**\n\n"
        "Analyze and visualize rural internet connectivity "
        "across Brazil, aligned with Starlink's 2026 expansion roadmap."
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("🇧🇷 Made with ❤️ for improving rural connectivity in Brazil")


if __name__ == '__main__':
    main()
