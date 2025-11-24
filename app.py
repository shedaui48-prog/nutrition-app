# app.py
import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw
import io, base64

st.set_page_config(page_title="Student Nutrition App (Per Serving)", page_icon="🍔", layout="centered")
st.title("🍽️ Student Nutrition — Per Serving (School-friendly)")

# --------------------------
# Food database (per serving)
# --------------------------
FOODS = [
    {"name":"apple","display":"Apple","serving":"1 medium (182 g)","calories":95,"protein":0.5,"carbs":25,"fat":0.3,"fiber":4.4,"sugar":19,"iron":0.1,"calcium":11,"vitA":98,"vitC":8.4,"image":""},
    {"name":"banana","display":"Banana","serving":"1 medium (118 g)","calories":105,"protein":1.3,"carbs":27,"fat":0.4,"fiber":3.1,"sugar":14,"iron":0.3,"calcium":6,"vitA":76,"vitC":10.3,"image":""},
    {"name":"roti","display":"Roti / Chapati","serving":"1 medium (40 g)","calories":120,"protein":3.0,"carbs":18,"fat":3.5,"fiber":2.0,"sugar":0,"iron":0.7,"calcium":20,"vitA":0,"vitC":0,"image":""},
    {"name":"rice_cup","display":"Cooked White Rice","serving":"1 cup (158 g)","calories":206,"protein":4.3,"carbs":45,"fat":0.4,"fiber":0.6,"sugar":0,"iron":0.2,"calcium":16,"vitA":0,"vitC":0,"image":""},
    {"name":"dal_cup","display":"Cooked Dal","serving":"1 cup (198 g)","calories":198,"protein":9,"carbs":29,"fat":3,"fiber":15,"sugar":2,"iron":3.3,"calcium":40,"vitA":30,"vitC":3,"image":""},

    {"name":"idli","display":"Idli","serving":"1 medium idli","calories":58,"protein":2,"carbs":12,"fat":0.4,"fiber":0.8,"sugar":0.5,"iron":0.4,"calcium":10,"vitA":0,"vitC":0,"image":""},
    {"name":"dosa","display":"Dosa","serving":"1 medium dosa","calories":168,"protein":3.9,"carbs":25,"fat":4,"fiber":1.5,"sugar":1,"iron":1.2,"calcium":20,"vitA":50,"vitC":0,"image":""},
    {"name":"paratha","display":"Paratha","serving":"1 medium paratha","calories":260,"protein":5,"carbs":38,"fat":10,"fiber":2.5,"sugar":1,"iron":1.5,"calcium":40,"vitA":0,"vitC":0,"image":""},
    {"name":"poha","display":"Poha","serving":"1 plate (150 g)","calories":180,"protein":3,"carbs":28,"fat":5,"fiber":2,"sugar":2,"iron":1,"calcium":20,"vitA":0,"vitC":2,"image":""},
    {"name":"upma","display":"Upma","serving":"1 plate (150 g)","calories":200,"protein":5,"carbs":30,"fat":7,"fiber":2,"sugar":1,"iron":0.8,"calcium":25,"vitA":0,"vitC":1,"image":""},

    {"name":"maggi","display":"Maggi (1 prepared pack)","serving":"1 pack prepared (~120 g)","calories":350,"protein":7,"carbs":52,"fat":12,"fiber":2,"sugar":3,"iron":1,"calcium":20,"vitA":0,"vitC":0,"image":""},
    {"name":"noodles_hakka","display":"Hakka Noodles (veg)","serving":"1 plate (~300 g)","calories":430,"protein":9,"carbs":64,"fat":14,"fiber":3,"sugar":6,"iron":1.6,"calcium":40,"vitA":0,"vitC":6,"image":""},
    {"name":"schezwan_noodles","display":"Schezwan Noodles","serving":"1 plate (~300 g)","calories":480,"protein":10,"carbs":66,"fat":18,"fiber":3,"sugar":8,"iron":1.8,"calcium":40,"vitA":0,"vitC":6,"image":""},
    {"name":"fried_rice","display":"Veg Fried Rice","serving":"1 plate (~300 g)","calories":420,"protein":8,"carbs":60,"fat":14,"fiber":3,"sugar":4,"iron":1.5,"calcium":30,"vitA":0,"vitC":6,"image":""},
    {"name":"schezwan_fried_rice","display":"Schezwan Fried Rice","serving":"1 plate (~300 g)","calories":500,"protein":9,"carbs":64,"fat":20,"fiber":3,"sugar":6,"iron":1.7,"calcium":35,"vitA":0,"vitC":6,"image":""},
    {"name":"veg_manchurian_gravy","display":"Veg Manchurian (gravy)","serving":"1 bowl (~200 g)","calories":340,"protein":6,"carbs":28,"fat":20,"fiber":3,"sugar":6,"iron":1.2,"calcium":30,"vitA":0,"vitC":2,"image":""},
    {"name":"veg_manchurian_dry","display":"Veg Manchurian (dry)","serving":"1 plate (~200 g)","calories":280,"protein":5,"carbs":24,"fat":16,"fiber":2,"sugar":4,"iron":1.0,"calcium":25,"vitA":0,"vitC":2,"image":""},
    {"name":"chinese_bhel","display":"Chinese Bhel","serving":"1 plate (~200 g)","calories":310,"protein":6,"carbs":38,"fat":12,"fiber":2,"sugar":8,"iron":1.1,"calcium":20,"vitA":0,"vitC":4,"image":""},
    {"name":"spring_roll","display":"Spring Roll (1)","serving":"1 piece (~60 g)","calories":150,"protein":3,"carbs":18,"fat":7,"fiber":1.5,"sugar":2,"iron":0.6,"calcium":10,"vitA":0,"vitC":0,"image":""},
    {"name":"momos_veg","display":"Veg Momos (6 pcs)","serving":"6 pieces","calories":220,"protein":6,"carbs":30,"fat":6,"fiber":2,"sugar":3,"iron":0.9,"calcium":20,"vitA":0,"vitC":0,"image":""},
    {"name":"chilli_paneer","display":"Chilli Paneer","serving":"1 plate (~200 g)","calories":360,"protein":12,"carbs":20,"fat":22,"fiber":2,"sugar":8,"iron":1.5,"calcium":120,"vitA":0,"vitC":4,"image":""},
    {"name":"chilli_gobi","display":"Chilli Gobi","serving":"1 plate (~180 g)","calories":260,"protein":4,"carbs":28,"fat":12,"fiber":3,"sugar":6,"iron":1.0,"calcium":20,"vitA":0,"vitC":6,"image":""},

    {"name":"veg_burger","display":"Veg Burger","serving":"1 burger","calories":320,"protein":10,"carbs":35,"fat":14,"fiber":3,"sugar":6,"iron":2.1,"calcium":120,"vitA":80,"vitC":2,"image":""},
    {"name":"cheese_burger","display":"Cheese Burger","serving":"1 burger","calories":450,"protein":20,"carbs":40,"fat":22,"fiber":2,"sugar":6,"iron":2.5,"calcium":200,"vitA":100,"vitC":2,"image":""},
    {"name":"pizza_slice","display":"Pizza (1 slice, veg)","serving":"1 slice (~100 g)","calories":285,"protein":12,"carbs":33,"fat":12,"fiber":2,"sugar":3,"iron":2,"calcium":200,"vitA":120,"vitC":2,"image":""},
    {"name":"french_fries_small","display":"French Fries (small)","serving":"1 small (~80 g)","calories":230,"protein":3,"carbs":28,"fat":11,"fiber":3,"sugar":0.2,"iron":0.6,"calcium":10,"vitA":2,"vitC":10,"image":""},
    {"name":"sandwich_veg","display":"Veg Sandwich (2 slices)","serving":"1 sandwich","calories":250,"protein":8,"carbs":30,"fat":8,"fiber":4,"sugar":5,"iron":1.2,"calcium":80,"vitA":20,"vitC":2,"image":""},

    {"name":"pav_bhaji","display":"Pav Bhaji (1 plate)","serving":"1 plate (~300 g)","calories":350,"protein":7,"carbs":50,"fat":12,"fiber":6,"sugar":8,"iron":2,"calcium":50,"vitA":100,"vitC":20,"image":""},
    {"name":"vada_pav","display":"Vada Pav","serving":"1 piece","calories":300,"protein":5,"carbs":40,"fat":12,"fiber":2,"sugar":3,"iron":1,"calcium":20,"vitA":0,"vitC":0,"image":""},
    {"name":"samosa","display":"Samosa","serving":"1 medium (80 g)","calories":285,"protein":4,"carbs":32,"fat":15,"fiber":3,"sugar":2,"iron":1,"calcium":20,"vitA":0,"vitC":0,"image":""},
    {"name":"kachori","display":"Kachori","serving":"1 piece","calories":230,"protein":4,"carbs":28,"fat":10,"fiber":2,"sugar":2,"iron":0.9,"calcium":15,"vitA":0,"vitC":0,"image":""},
    {"name":"pani_puri","display":"Pani Puri (6)","serving":"6 pieces","calories":120,"protein":2,"carbs":18,"fat":4,"fiber":2,"sugar":5,"iron":0.7,"calcium":10,"vitA":0,"vitC":2,"image":""},
    {"name":"sevpuri","display":"Sev Puri (1 plate)","serving":"1 plate (~150 g)","calories":210,"protein":3,"carbs":30,"fat":7,"fiber":3,"sugar":6,"iron":1.0,"calcium":30,"vitA":0,"vitC":2,"image":""},
    {"name":"bhel_puri","display":"Bhel Puri (1 plate)","serving":"1 plate (~150 g)","calories":220,"protein":4,"carbs":32,"fat":6,"fiber":4,"sugar":8,"iron":1.0,"calcium":20,"vitA":0,"vitC":2,"image":""},

    {"name":"chips_small","display":"Pack of Chips (small)","serving":"1 small pack (~30 g)","calories":160,"protein":2,"carbs":15,"fat":10,"fiber":1,"sugar":0.5,"iron":0.4,"calcium":10,"vitA":0,"vitC":0,"image":""},
    {"name":"chocolate_bar","display":"Chocolate Bar (40 g)","serving":"1 bar","calories":220,"protein":2.5,"carbs":25,"fat":12,"fiber":1,"sugar":22,"iron":1.4,"calcium":40,"vitA":0,"vitC":0,"image":""},
    {"name":"biscuit_snack","display":"Biscuits (3 pcs)","serving":"3 biscuits (~30 g)","calories":150,"protein":2,"carbs":20,"fat":6,"fiber":0.5,"sugar":8,"iron":0.7,"calcium":30,"vitA":0,"vitC":0,"image":""},

    {"name":"milk_cup","display":"Whole Milk","serving":"1 cup (244 g)","calories":149,"protein":7.9,"carbs":12,"fat":8,"fiber":0,"sugar":12,"iron":0,"calcium":276,"vitA":112,"vitC":0,"image":""},
    {"name":"egg_boiled","display":"Boiled Egg","serving":"1 large","calories":78,"protein":6.3,"carbs":0.6,"fat":5.3,"fiber":0,"sugar":0.6,"iron":0.8,"calcium":25,"vitA":160,"vitC":0,"image":""},
    {"name":"paneer_100g","display":"Paneer (100 g)","serving":"100 g","calories":265,"protein":18,"carbs":1.2,"fat":20.8,"fiber":0,"sugar":1,"iron":0.5,"calcium":208,"vitA":30,"vitC":0,"image":""},
    {"name":"chicken_curry","display":"Chicken Curry (1 cup)","serving":"1 cup (~200 g)","calories":240,"protein":20,"carbs":6,"fat":14,"fiber":0,"sugar":2,"iron":1.5,"calcium":20,"vitA":0,"vitC":0,"image":""},
]

# Build lookups
FOOD_BY_NAME = {item['name']: item for item in FOODS}
FOOD_DISPLAY = {item['name']: f"{item['display']} — {item['serving']}" for item in FOODS}
all_food_names = [item['name'] for item in FOODS]
all_display = [FOOD_DISPLAY[item['name']] for item in FOODS]

# --------------------------
# Sidebar: calorie calculator & underweight suggestions
# --------------------------
st.sidebar.header("Tools")
st.sidebar.subheader("Calorie Estimator")
age = st.sidebar.number_input("Age (years)", min_value=3, max_value=120, value=12)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
height_cm = st.sidebar.number_input("Height (cm)", min_value=50, max_value=250, value=140)
weight_kg = st.sidebar.number_input("Weight (kg)", min_value=10.0, max_value=200.0, value=35.0, step=0.5)
activity = st.sidebar.selectbox("Activity level", ["Low (sedentary)", "Moderate (school + play)", "High (sports daily)"])

def estimate_calorie(age, gender, weight, height, activity_level):
    if gender == "Male":
        bmr = 10*weight + 6.25*height - 5*age + 5
    elif gender == "Female":
        bmr = 10*weight + 6.25*height - 5*age - 161
    else:
        bmr = 10*weight + 6.25*height - 5*age - 78
    multiplier = 1.2
    if activity_level.startswith("Moderate"):
        multiplier = 1.55
    elif activity_level.startswith("High"):
        multiplier = 1.75
    return int(bmr * multiplier)

estimated_cal = estimate_calorie(age, gender, weight_kg, height_cm, activity)
st.sidebar.markdown(f"**Estimated daily calories:** {estimated_cal} kcal (approx.)")

st.sidebar.subheader("Underweight Check (BMI)")
if st.sidebar.button("Check BMI / Suggestions"):
    bmi = weight_kg / ((height_cm/100)**2)
    st.sidebar.write(f"Your BMI: {bmi:.1f}")
    if bmi < 18.5:
        st.sidebar.warning("BMI suggests underweight (approx). Consider calorie-dense healthy foods and consult a doctor/nutritionist.")
    else:
        st.sidebar.success("BMI not in underweight range (approx).")
    st.sidebar.markdown("**If underweight — suggested foods/snacks:**")
    st.sidebar.write("- Milk, paneer, yogurt, banana with peanut butter\n- Nuts (almonds, peanuts) as snacks\n- Chapati with ghee + dal\n- Eggs / paneer / chicken for protein\n- Frequent small meals and healthy snacks")

# --------------------------
# Main UI: search and display
# --------------------------
st.header("Search food (type OR choose)")

col1, col2 = st.columns([3,2])
with col1:
    q = st.text_input("Type a food (e.g. roti, idli, maggi, pizza, burger)", value="")
with col2:
    sel = st.selectbox("Or choose from list", options=[""] + all_display)

selected_food_key = None
if sel:
    for k, v in FOOD_DISPLAY.items():
        if v == sel:
            selected_food_key = k
            break

if q:
    q_lower = q.strip().lower()
    if q_lower in FOOD_BY_NAME:
        selected_food_key = q_lower
    else:
        matches = [name for name in all_food_names if q_lower in name or q_lower in FOOD_DISPLAY[name].lower()]
        if len(matches) == 1:
            selected_food_key = matches[0]
        elif len(matches) > 1:
            st.info(f"Multiple matches: {', '.join([FOOD_DISPLAY[m] for m in matches[:8]])}. Please refine or choose from dropdown.")
            selected_food_key = None
        else:
            st.warning("No match found. Try different spelling or choose from dropdown.")

# Display selected food
if selected_food_key:
    food = FOOD_BY_NAME[selected_food_key]
    st.subheader(food['display'])
    st.write(f"**Serving:** {food.get('serving','-')}")
    nut = {
        "Calories (kcal)": food['calories'],
        "Protein (g)": food['protein'],
        "Carbs (g)": food['carbs'],
        "Fat (g)": food['fat'],
        "Fiber (g)": food.get('fiber','-'),
        "Sugar (g)": food.get('sugar','-'),
        "Iron (mg)": food.get('iron','-'),
        "Calcium (mg)": food.get('calcium','-'),
        "Vitamin A (µg)": food.get('vitA','-'),
        "Vitamin C (mg)": food.get('vitC','-'),
    }
    df = pd.DataFrame.from_dict(nut, orient='index', columns=["Value"])
    st.table(df)

    img_url = food.get('image','')
    if img_url:
        st.image(img_url, caption=food['display'])
    else:
        placeholder = Image.new('RGB', (360,200), color=(245,245,245))
        d = ImageDraw.Draw(placeholder)
        d.text((12,12), food['display'], fill=(20,20,20))
        st.image(placeholder)

    label = "Healthy choice" if food['calories'] <= 250 and food['fat'] <= 10 else "Moderate / Treat"
    st.info(f"Quick note: {label}")

    if food['calories'] > 400:
        st.warning("High calorie item — treat it occasionally.")
    elif food['calories'] <= 150:
        st.success("Light snack / healthy option.")
else:
    st.write("No food selected yet. Type or choose a food to see its nutrition per serving.")

st.write("---")
st.caption("Values are approximate per serving and intended for education. For medical/dietary advice consult a professional.")

# --------------------------
# Download DB as CSV
# --------------------------
if st.button("Download foods as CSV"):
    df_all = pd.DataFrame(FOODS)
    csv = df_all.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="foods_per_serving.csv">Download foods_per_serving.csv</a>'
    st.markdown(href, unsafe_allow_html=True)
