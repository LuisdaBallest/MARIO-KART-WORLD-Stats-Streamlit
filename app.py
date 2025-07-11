import pandas as pd
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Load data
characters = pd.read_csv('mario_kart_stats_chars.csv')
karts = pd.read_csv('mario_kart_vehicles.csv')
special_stats = pd.read_csv('vehicles_stats_special.csv')

# Page configuration
st.set_page_config(
    page_title="MK World Stats", 
    page_icon="🌎",
    layout="wide"
)


# Apply custom styles for progress bars
st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-color: #FF9800;
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
    </style>
    <div class="attribution">
        The information, images and stats is from the Super Mario Wiki<br>
        Source: <a href="https://www.mariowiki.com/Mario_Kart_World" target="_blank">https://www.mariowiki.com/Mario_Kart_World</a>
    </div>
""", unsafe_allow_html=True)
st.markdown("---")
st.title("Mario Kart World 🌎")
st.header("Character and Vehicle Stats")

# Function to display statistics with progress bar
def show_stat_with_bar(label, value, max_value=9, adjustment=0):
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

def show_stat_with_bar_total(label, value, max_value=18, adjustment=0):
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