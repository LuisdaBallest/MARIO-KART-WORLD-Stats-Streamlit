import pandas as pd
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Load data
characters = pd.read_csv('mario_kart_stats_chars.csv')
karts = pd.read_csv('mario_kart_vehicles.csv')
special_stats = pd.read_csv('vehicles_stats_special.csv')

# Load new substat data
character_substats = pd.read_csv('driver_speed_broken_down.csv')
vehicle_substats = pd.read_csv('vehicle_speed_broken_down.csv')

# Page configuration
st.set_page_config(
    page_title="MK World Stats", 
    page_icon="🌎",
    layout="wide"
)

# Apply custom styles for progress bars
st.markdown("""
    <style>
            
    /* Default progress bar color */
    .stProgress > div > div > div > div {
        background-color: #FF9800;
    }
    
    /* Individual colored bars */
    .asphalt-bar {
        background-color: #757575 !important;
    }
    
    .dirt-bar {
        background-color: #8D6E63 !important;
    }
    
    .water-bar {
        background-color: #2196F3 !important;
    }
    
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 0px;
        margin-bottom: 0px;
    }
    .positive-adjustment {
        color: #00C853;  /* Green color for positive adjustments */
        font-weight: bold;
    }
    .negative-adjustment {
        color: #E60012;  /* Red color for negative adjustments */
        font-weight: bold;
    }
    .substat-label {
        font-size: 0.9rem;
        margin-bottom: 0;
    }
    
    /* Custom progress bar containers */
    .custom-progress {
        height: 20px;
        background-color: #f0f0f0;
        border-radius: 5px;
        margin: 10px 0;
        overflow: hidden;
    }
    .custom-progress-bar {
        height: 100%;
        border-radius: 5px;
    }
            
        .attribution {
        position: relative;
        margin-top: 0px;
        padding: 0px 0px;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        font-size: 0.85rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        max-width: 100%;
        text-align: center;
    }

    .attribution a {
        color: #0066cc;
        text-decoration: none;
    }

    .attribution a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="attribution">
        <p style="margin-bottom: 8px;"><strong>Sources & Acknowledgements:</strong></p>
        <ul style="list-style-type: none; padding-left: 10px; margin: 0;">
            <li style="margin-bottom: 8px;">
                📖 Information, images and stats from the Super Mario Wiki<br>
                <a href="https://www.mariowiki.com/Mario_Kart_World" target="_blank">mariowiki.com/Mario_Kart_World</a>
            </li>
            <li style="margin-bottom: 8px;">
                👤 Thanks to u/Shokaah for the detailed Reddit post<br>
                <a href="https://www.reddit.com/r/mariokart/comments/1lnrtpx/mario_kart_world_stats_and_builder_updated_with/" target="_blank">Reddit: Mario Kart World Stats and Builder</a>
            </li>
            <li>
                ✖️ Credit to @CrypticJacknife for additional data<br>
                <a href="https://x.com/CrypticJacknife/status/1933004726809080286" target="_blank">X.com: Detailed Stats Breakdown</a>
            </li>
        </ul>
    </div>
""", unsafe_allow_html=True)
st.markdown("---")
st.title("Mario Kart World 🌎")
st.header("Character and Vehicle Stats")

# Function to display statistics with progress bar
def show_stat_with_bar(label, value, max_value=10, adjustment=0):
    # Ensure value is within range
    normalized_value = min(max(value, 0), max_value) / max_value
    
    # Display label, bar and numeric value
    if adjustment != 0:
        adjustment_class = "positive-adjustment" if adjustment > 0 else "negative-adjustment"
        st.write(f"**{label}** <span class='{adjustment_class}'>({'+' if adjustment > 0 else ''}{adjustment})</span>", unsafe_allow_html=True)
    else:
        st.write(f"**{label}**")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(normalized_value)
    with col2:
        st.write(f"{value}/{max_value}")

def show_speed_substats(substats_data, item_name, item_type="Driver"):
    if substats_data is not None:
        st.markdown("##### Speed Substats")
        
        # Asphalt - Gray
        st.markdown('<p class="substat-label">Asphalt</p>', unsafe_allow_html=True)
        asphalt_val = substats_data.get("Asphalt", 0)
        normalized_asphalt = min(max(asphalt_val, 0), 9) / 9 * 100  # Convert to percentage
        
        col1, col2 = st.columns([3, 1])
        with col1:
            # Custom HTML progress bar with gray color
            st.markdown(f"""
            <div class="custom-progress">
                <div class="custom-progress-bar asphalt-bar" style="width: {normalized_asphalt}%;"></div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.write(f"{asphalt_val}/10")
        
        # Dirt - Brown
        st.markdown('<p class="substat-label">Dirt</p>', unsafe_allow_html=True)
        dirt_val = substats_data.get("Dirt", 0)
        normalized_dirt = min(max(dirt_val, 0), 9) / 9 * 100  # Convert to percentage
        
        col1, col2 = st.columns([3, 1])
        with col1:
            # Custom HTML progress bar with brown color
            st.markdown(f"""
            <div class="custom-progress">
                <div class="custom-progress-bar dirt-bar" style="width: {normalized_dirt}%;"></div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.write(f"{dirt_val}/10")
        
        # Water - Blue
        st.markdown('<p class="substat-label">Water</p>', unsafe_allow_html=True)
        water_val = substats_data.get("Water", 0)
        normalized_water = min(max(water_val, 0), 9) / 9 * 100  # Convert to percentage
        
        col1, col2 = st.columns([3, 1])
        with col1:
            # Custom HTML progress bar with blue color
            st.markdown(f"""
            <div class="custom-progress">
                <div class="custom-progress-bar water-bar" style="width: {normalized_water}%;"></div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.write(f"{water_val}/10")

def show_stat_with_bar_total(label, value, max_value=20, adjustment=0):
    # Ensure value is within range
    normalized_value = min(max(value, 0), max_value) / max_value
    
    # Display label, bar and numeric value
    if adjustment != 0:
        adjustment_class = "positive-adjustment" if adjustment > 0 else "negative-adjustment"
        st.write(f"**{label}** <span class='{adjustment_class}'>({'+' if adjustment > 0 else ''}{adjustment})</span>", unsafe_allow_html=True)
    else:
        st.write(f"**{label}**")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(normalized_value)
    with col2:
        st.write(f"{value}/{max_value}")

# Simplified function to load image from direct URL
def load_image_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            return img
        else:
            st.warning(f"Could not load image (code {response.status_code})")
            return None
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

# Function to resize image to a fixed height while maintaining proportions
def resize_image_to_height(image, target_height=150):
    if image is None:
        return None
        
    # Calculate new width maintaining aspect ratio
    width, height = image.size
    new_width = int(width * (target_height / height))
    
    # Resize image
    resized_image = image.resize((new_width, target_height), Image.LANCZOS)
    return resized_image

# Function to determine if a character is in the light or heavy category
def is_special_character(character):
    # Check if character has an asterisk indicating it's special
    if character.endswith("*"):
        character_clean = character.replace("*", "").strip()
        
        if character_clean in ["Baby Peach", "Baby Daisy", "Para-Biddybud", "Swoop"]:
            return "light"
        elif character_clean == "Bowser":
            return "heavy"
    return None

# Function to check if special adjustments apply
def get_adjustments(character, vehicle):
    character_type = is_special_character(character)
    special_vehicles = special_stats["Vehicle"].tolist()
    
    adjustments = {"Speed": 0, "Acceleration": 0, "Weight": 0, "Handling": 0}
    
    if character_type and vehicle in special_vehicles:
        # Apply adjustments based on character type
        if character_type in ["light", "heavy"]:
            adjustments["Speed"] = -1
            adjustments["Handling"] = 1
    
    return adjustments

# Containers to organize the interface
col1, col2 = st.columns(2)

# Character selection
with col1:
    st.header("Select a Driver")
    selected_character = st.selectbox("Driver", characters["Driver"].tolist())
    
    # Display character image and stats
    if selected_character:
        character_data = characters[characters["Driver"] == selected_character].iloc[0]
        
        # Load image from direct URL
        if "Img" in character_data and pd.notna(character_data["Img"]):
            img_url = character_data["Img"]
            img = load_image_from_url(img_url)
            if img:
                # Resize to fixed height
                img_resized = resize_image_to_height(img)
                # Create container to center the image
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(img_resized)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Display character stats
        st.subheader("Character Stats")
        character_stats = {
            "Speed": character_data.get("Speed", 0),
            "Acceleration": character_data.get("Acceleration", 0),
            "Weight": character_data.get("Weight", 0),
            "Handling": character_data.get("Handling", 0)
        }
        
        for stat, value in character_stats.items():
            if pd.notna(value):
                show_stat_with_bar(stat, value)
        
        # Display speed substats if available
        if selected_character in character_substats["Driver"].values:
            substat_data = character_substats[character_substats["Driver"] == selected_character].iloc[0]
            substats = {
                "Avg": substat_data.get("Avg", 0),
                "Asphalt": substat_data.get("Asphalt", 0),
                "Dirt": substat_data.get("Dirt", 0),
                "Water": substat_data.get("Water", 0)
            }
            
            st.markdown("---")
            show_speed_substats(substats, selected_character, "Driver")

# Vehicle selection
with col2:
    st.header("Select a Vehicle")
    selected_vehicle = st.selectbox("Vehicle", karts["Vehicle"].tolist())
    
    # Display vehicle image and stats
    if selected_vehicle:
        vehicle_data = karts[karts["Vehicle"] == selected_vehicle].iloc[0]
        
        # Load image from direct URL
        if "Img" in vehicle_data and pd.notna(vehicle_data["Img"]):
            img_url = vehicle_data["Img"]
            img = load_image_from_url(img_url)
            if img:
                # Resize to fixed height
                img_resized = resize_image_to_height(img)
                # Create container to center the image
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(img_resized)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Display vehicle stats
        st.subheader("Vehicle Stats")
        vehicle_stats = {
            "Speed": vehicle_data.get("Speed", 0),
            "Acceleration": vehicle_data.get("Acceleration", 0),
            "Weight": vehicle_data.get("Weight", 0),
            "Handling": vehicle_data.get("Handling", 0)
        }
        
        for stat, value in vehicle_stats.items():
            if pd.notna(value):
                show_stat_with_bar(stat, value)
        
        # Display speed substats if available
        if selected_vehicle in vehicle_substats["Vehicle"].values:
            substat_data = vehicle_substats[vehicle_substats["Vehicle"] == selected_vehicle].iloc[0]
            substats = {
                "Avg": substat_data.get("Avg", 0),
                "Asphalt": substat_data.get("Asphalt", 0),
                "Dirt": substat_data.get("Dirt", 0),
                "Water": substat_data.get("Water", 0)
            }
            
            st.markdown("---")
            show_speed_substats(substats, selected_vehicle, "Vehicle")

# Display combined stats
if selected_character and selected_vehicle:
    st.markdown("---")

    character_data = characters[characters["Driver"] == selected_character].iloc[0]
    vehicle_data = karts[karts["Vehicle"] == selected_vehicle].iloc[0]
    
    # Get special adjustments based on character and vehicle
    adjustments = get_adjustments(selected_character, selected_vehicle)
    
    # Calculate combined stats with adjustments
    combined_stats = {}
    for stat in ["Speed", "Acceleration", "Weight", "Handling"]:
        if stat in character_data and stat in vehicle_data and pd.notna(character_data[stat]) and pd.notna(vehicle_data[stat]):
            # Sum base stats
            combined_stats[stat] = character_data[stat] + vehicle_data[stat]
            
            # Apply adjustments if applicable
            if stat in adjustments and adjustments[stat] != 0:
                combined_stats[stat] += adjustments[stat]
    
    # Warning message about special adjustments
    character_type = is_special_character(selected_character)
    
    # Check if character has an asterisk in its name
    has_asterisk = selected_character.endswith("*")
    
    # Display special adjustments message if applicable
    if character_type and selected_vehicle in special_stats["Vehicle"].tolist():
        st.info(f"""
        **Special combination!** 
        
        The character {selected_character} is in the {character_type} class and is using a special vehicle.
        
        The following adjustments apply:
        - Speed: -1 point
        - Handling: +1 point
        """)
    
    # Display special stats only if character has an asterisk, regardless of vehicle
    if has_asterisk:
        st.subheader("Special Stats applied to Vehicle")
        
        # If the vehicle is also in special_stats, show those stats
        if selected_vehicle in special_stats["Vehicle"].values:
            special_vehicle = special_stats[special_stats["Vehicle"] == selected_vehicle].iloc[0]
            for col in ["Speed", "Acceleration", "Weight", "Handling"]:
                if col in special_vehicle and pd.notna(special_vehicle[col]):
                    show_stat_with_bar(col, special_vehicle[col])
        # Otherwise show a message explaining the character's special properties
        else:
            st.write("""
            This character has special properties that affect certain vehicles.
            When paired with special vehicles (those marked with *), this character will receive:
            - Speed: -1 point
            - Handling: +1 point
            """)
    
    # Display combined stats 
    st.subheader("Total Combined Stats")
    
    # Create two columns to display progress bars
    left_col, right_col = st.columns(2)
    
    with left_col:
        show_stat_with_bar_total("Speed", combined_stats.get("Speed", 0), adjustment=adjustments.get("Speed", 0))
        show_stat_with_bar_total("Acceleration", combined_stats.get("Acceleration", 0), adjustment=adjustments.get("Acceleration", 0))

    with right_col:
        show_stat_with_bar_total("Weight", combined_stats.get("Weight", 0), adjustment=adjustments.get("Weight", 0))
        show_stat_with_bar_total("Handling", combined_stats.get("Handling", 0), adjustment=adjustments.get("Handling", 0))


# Add Mini-Turbo Duration section
st.markdown("---")
st.subheader("Pink Mini-Turbo Duration")
st.info("""
**Mini-Turbo has a 1 to 1 relation to acceleration**, meaning that the higher your acceleration stat, the longer your mini-turbo boost lasts.""")

# Calculate Mini-Turbo Duration: (Acceleration Stat + 59) / 24
acceleration = combined_stats.get("Acceleration", 0)
mini_turbo_duration = (acceleration + 59) / 24

# Display the formula and result
st.markdown(f"""
**Formula**: (Acceleration + 59) / 24

**Calculation**: ({acceleration} + 59) / 24
""")

# Create a visual representation with icon and large text
st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: center; margin: 20px 0;">
    <span style="font-size: 80px; margin-right: 15px;">⏱️</span>
    <span style="font-size: 80px; font-weight: bold; color: #9C27B0;">{mini_turbo_duration:.2f}</span>
    <span style="font-size: 24px; margin-left: 10px;">seconds</span>
</div>
""", unsafe_allow_html=True)

# Add explanation of Mini-Turbo Duration
st.info("""
**What is Pink Mini-Turbo Duration?**  
Mini-Turbo Duration determines how long your mini-turbo boost lasts when performing a drift. 
Higher values mean longer-lasting boosts, which can provide a significant advantage in races, 
especially on tracks with many turns.
""")
