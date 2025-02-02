import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px

# Function to convert local image file to base64




# Set page config with base64 image as page icon
st.set_page_config(
    page_title="🚌Transport Dashboard",
   
    layout="wide"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #203b56;
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextInput>div>div>input {
        background-color: #2c4a6e;
        color: white;
    }
    .stTable {
        background-color: #2c4a6e;
        color: white;
    }
    .stProgress>div>div>div {
        background-color: #4CAF50;
    }
    .css-1aumxhk {
        color: white;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #2c4a6e;
        padding: 10px 50px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .logo {
        display: flex;
        align-items: center;
    }
    .logo img {
        width: 40px;
        height: 40px;
        margin-right: 10px;
    }
    .logo span {
        color: #4CAF50;
        font-size: 1.8em;
        font-weight: bold;
    }
    .nav-links {
        display: flex;
        justify-content: space-evenly;
        width: 60%;
    }
    .nav-link {
        color: white;
        font-size: 1.1em;
        text-decoration: none;
        padding: 10px 20px;
        border-radius: 5px;
        background-color: #4CAF50;
        transition: background-color 0.3s;
        text-align: center;
    }
    .nav-link:hover {
        background-color: #45a049;
    }
    .chart-container {
        background-color: #2c4a6e;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .chart-container .plotly-graph-div {
        width: 100% !important;
    }
    .footer {
        text-align: center;
        padding: 20px;
        background-color: #2c4a6e;
        color: white;
        position: relative;
        width:100%;
        bottom: 0;
        margin-top:50px;
    }
    .footer a {
        color: #4CAF50;
        font-weight: bold;
        text-decoration: none;
    }
    .footer a:hover {
        color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "live_tracker"

# Live Tracker Page
def live_tracker():
    st.title("🚌 Track Your Ride In Real Time")
    
    # Create two columns, one for the map and one for the pie chart
    col1, col2 = st.columns([3, 2])  # Adjusted column width for larger pie chart
    
    with col1:
        # Create a map centered on India (New Delhi coordinates)
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)  # Centered on India
        
        # Define locations for markers (example data for India)
        locations = {
            "New Delhi - Bus 101": [28.6139, 77.2090],
            "Mumbai - Train A": [19.0760, 72.8777],
            "Bengaluru - Metro M1": [12.9716, 77.5946]
        }
        
        # Add markers with custom icons and popups
        for name, coords in locations.items():
            folium.Marker(
                location=coords,
                popup=f"<b>{name}</b>",  # Popup with location name
                icon=folium.Icon(color="blue" if "Bus" in name else "red" if "Train" in name else "green")
            ).add_to(m)
        
        # Draw lines between markers to simulate directions
        route_coords = [
            locations["New Delhi - Bus 101"],
            locations["Mumbai - Train A"],
            locations["Bengaluru - Metro M1"]
        ]
        folium.PolyLine(
            locations=route_coords,
            color="blue",
            weight=2.5,
            opacity=1,
            popup="Route Direction"
        ).add_to(m)
        
        # Display the map
        folium_static(m)

    with col2:
        # Crowd Insights Pie Chart
        st.markdown("### Crowd Levels by Transport Mode")
        crowd_data = {
            "Transport": ["Bus 101", "Train A", "Metro M1"],
            "Crowd Level": [60, 30, 10]  # Example percentages for High, Medium, Low
        }
        crowd_df = pd.DataFrame(crowd_data)

        # Create a pie chart with increased width and styling
        fig = px.pie(crowd_df, values="Crowd Level", names="Transport", title="Crowd Distribution",
                     color_discrete_sequence=px.colors.sequential.Plasma)
        
        # Increase the size of the pie chart and make it responsive
        fig.update_layout(
            width=600,  # Adjust width to make it wider
            height=400,  # Adjust height if needed
            title_font=dict(size=20),
            margin=dict(t=50, b=50, l=50, r=50)  # Add some padding around the chart
        )

        st.plotly_chart(fig, use_container_width=True)

# Route & Schedule Page
def route_schedule():
    st.title("🗺 Route & Schedule")
    
    # Input fields for "From" and "To"
    col1, col2 = st.columns(2)
    with col1:
        from_location = st.text_input("From", placeholder="Enter starting location")
    with col2:
        to_location = st.text_input("To", placeholder="Enter destination")
    
    # Example route data
    routes = [
        {"Transport": "Bus + Metro", "Time": "45 mins", "Cost": "₹50"},
        {"Transport": "Train + Walking", "Time": "35 mins", "Cost": "₹75"},
        {"Transport": "Bus Only", "Time": "55 mins", "Cost": "₹30"},
    ]
    
    # Display route options
    st.write("### Route Options")
    for route in routes:
        st.write(f"{route['Transport']}** - {route['Time']} - {route['Cost']}")

    # Example timetable
    st.write("### Timetable")
    timetable = pd.DataFrame({
        "Time": ["8:00 AM", "8:15 AM", "8:30 AM"],
        "Route": ["Bus 101", "Train A", "Metro M1"],
        "Status": ["On Time", "Delayed", "On Time"]
    })
    st.table(timetable)

# Crowd Insights Page with Bar Graph
def crowd_insights():
    st.title("👥 Crowd Insights")
    
    # Example crowd data
    crowd_data = {
        "Transport": ["Bus 101", "Train A", "Metro M1"],
        "Crowd Level": ["High", "Medium", "Low"],
        "Trend": ["Getting busier", "Stable", "Getting quieter"],
        "Crowd Percentage": [60, 30, 10]
    }
    
    # Display crowd levels
    st.write("### Crowd Levels")
    crowd_df = pd.DataFrame(crowd_data)
    st.table(crowd_df)
    
    # Add Bar Graph
    st.write("### Crowd Levels Bar Chart")
    bar_fig = px.bar(
        crowd_df, 
        x='Transport', 
        y='Crowd Percentage', 
        color='Crowd Level', 
        title="Crowd Percentage by Transport Mode",
        color_discrete_map={"High": "red", "Medium": "orange", "Low": "green"}
    )
    bar_fig.update_layout(
        width=600, 
        height=400,
        title_font=dict(size=20),
        margin=dict(t=50, b=50, l=50, r=50)
    )
    st.plotly_chart(bar_fig, use_container_width=True)
    
    # Tips section
    st.write("### Tips")
    st.write("Try the 8:15 AM train for a quieter ride.")

# Eco Impact Page
def eco_impact():
    st.title("🌍 Eco Impact")

    # Description of the feature
    st.write("### Why Eco Impact?")
    st.write("EcoImpact showcases the environmental benefits of using public transport over private vehicles. "
             "By choosing greener commuting options, you help reduce CO2 emissions, save fuel, and contribute to a healthier planet! "
             "Every small action counts toward a sustainable future. 🚆🌱")

    # Personal impact metrics
    st.write("### Personal Impact")
    st.write("CO2 Saved: 12 kg this week")
    st.write("Fuel Saved: 10 liters")
    st.write("Distance Traveled by Public Transport: 50 km")
    st.write("Equivalent Trees Planted: 1.2 trees 🌳")
    st.progress(0.8)  # Monthly eco goal progress

    # Community impact
    st.write("### Community Impact")
    st.write("Total CO2 saved by all users this month: 1,000 kg")
    st.write("Total Fuel Saved: 850 liters")
    st.write("Total Distance Covered by Public Transport: 42,000 km")
    st.write("Total Equivalent Trees Planted: 100 trees 🌲")

    # Leaderboard
    st.write("### Top Eco-Friendly Commuters")
    leaderboard = pd.DataFrame({
        "Rank": [1, 2, 3, 4, 5],
        "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "CO2 Saved (kg)": [50, 45, 40, 38, 35],
        "Fuel Saved (liters)": [40, 38, 35, 32, 30]
    })
    st.table(leaderboard)

    # Fun facts & tips
    st.write("### Fun Facts & Tips")
    st.write("🚌 Taking the bus reduces emissions by 45% compared to driving.")
    st.write("🚶 Walking or biking for short trips can cut emissions to zero!")
    st.write("🚆 Trains are one of the most energy-efficient modes of transport.")
    st.write("🌱 Switching to public transport for just 2 days a week can reduce your carbon footprint by 25%.")

    # Encouraging user engagement
    st.write("### Take Action!")
    st.write("Want to reduce your carbon footprint even more? Try carpooling, biking, or using electric public transport options. "
             "Challenge yourself to cut down your CO2 emissions by 10% next month! 🌍💚")

# Main App
def main():
    # Header with logo on the left
    st.markdown("""
    <div class="header">
        <div class="logo">
            <img src="data:image/png;base64,{}" width="100" height="100"/>
            <span>Transport Dashboard</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation using st.session_state
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Live Tracker"):
            st.session_state.page = "live_tracker"
    with col2:
        if st.button("Route & Schedule"):
            st.session_state.page = "route_schedule"
    with col3:
        if st.button("Crowd Insights"):
            st.session_state.page = "crowd_insights"
    with col4:
        if st.button("Eco Impact"):
            st.session_state.page = "eco_impact"

    # Page selection logic
    if st.session_state.page == "live_tracker":
        live_tracker()
    elif st.session_state.page == "route_schedule":
        route_schedule()
    elif st.session_state.page == "crowd_insights":
        crowd_insights()
    elif st.session_state.page == "eco_impact":
        eco_impact()

    # Footer with contact and additional links
    st.markdown("""
    <div class="footer">
        <p>Contact Us: <a href="mailto:contact@transportdashboard.com">contact@transportdashboard.com</a></p>
        <p><a href="https://www.transportdashboard.com/about" target="_blank">About Us</a> | 
           <a href="https://twitter.com/transportdashboard" target="_blank">Twitter</a> | 
           <a href="https://facebook.com/transportdashboard" target="_blank">Facebook</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
