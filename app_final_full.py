# app_final_full.py
import streamlit as st
import pandas as pd
import os, io, datetime
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Nutrition Hub", layout="wide", page_icon="🍎")
st.title("Student Nutrition Hub — Search • Log • Track • BMI")

# -------------------------
# Persistent log CSV file
# -------------------------
LOG_CSV = "intake_log.csv"

def ensure_log():
    if not os.path.exists(LOG_CSV):
        df = pd.DataFrame(columns=["timestamp","date","food_key","food_display","serving_qty","calories"])
        df.to_csv(LOG_CSV, index=False)
ensure_log()

# -------------------------
# Food database (expandable)
# -------------------------
# Key fields: key, display, serving, calories, protein, carbs, fat, fiber, sugar, image
FOODS = [
    # ---------------------------
    # FRUITS
    # ---------------------------
    {"key":"apple","display":"Apple","serving":"1 medium (182 g)","calories":95,"protein":0.5,"carbs":25,"fat":0.3,"fiber":4.4,"sugar":19,"image":""},
    {"key":"banana","display":"Banana","serving":"1 medium","calories":105,"protein":1.3,"carbs":27,"fat":0.4,"fiber":3,"sugar":14,"image":""},
    {"key":"mango","display":"Mango","serving":"1 cup","calories":99,"protein":0.8,"carbs":25,"fat":0.6,"fiber":3,"sugar":23,"image":""},
    {"key":"orange","display":"Orange","serving":"1 medium","calories":62,"protein":1.2,"carbs":15,"fat":0.2,"fiber":3,"sugar":12,"image":""},
    {"key":"watermelon","display":"Watermelon","serving":"1 cup","calories":46,"protein":0.9,"carbs":12,"fat":0.2,"fiber":0.6,"sugar":9,"image":""},
    {"key":"muskmelon","display":"Muskmelon","serving":"1 cup","calories":60,"protein":1.5,"carbs":14,"fat":0.3,"fiber":1.6,"sugar":13,"image":""},
    {"key":"pineapple","display":"Pineapple","serving":"1 cup","calories":82,"protein":1,"carbs":22,"fat":0.2,"fiber":2,"sugar":16,"image":""},
    {"key":"grapes","display":"Grapes","serving":"1 cup","calories":104,"protein":1,"carbs":27,"fat":0.2,"fiber":1.4,"sugar":23,"image":""},
    {"key":"pomegranate","display":"Pomegranate","serving":"1 cup seeds","calories":144,"protein":3,"carbs":32,"fat":2,"fiber":7,"sugar":23,"image":""},
    {"key":"guava","display":"Guava","serving":"1 medium","calories":37,"protein":1,"carbs":8,"fat":0.5,"fiber":3,"sugar":5,"image":""},
    {"key":"papaya","display":"Papaya","serving":"1 cup","calories":55,"protein":0.9,"carbs":14,"fat":0.2,"fiber":2.5,"sugar":8,"image":""},
    {"key":"kiwi","display":"Kiwi","serving":"1 medium","calories":42,"protein":0.8,"carbs":10,"fat":0.4,"fiber":2.1,"sugar":6,"image":""},
    {"key":"pear","display":"Pear","serving":"1 medium","calories":101,"protein":1,"carbs":27,"fat":0.2,"fiber":5.5,"sugar":17,"image":""},
    {"key":"strawberry","display":"Strawberry","serving":"1 cup","calories":49,"protein":1,"carbs":12,"fat":0.5,"fiber":3,"sugar":7,"image":""},
    {"key":"blueberry","display":"Blueberries","serving":"1 cup","calories":84,"protein":1,"carbs":21,"fat":0.5,"fiber":3.6,"sugar":15,"image":""},
    {"key":"dragonfruit","display":"Dragon Fruit","serving":"1 cup","calories":60,"protein":1.2,"carbs":13,"fat":0,"fiber":3,"sugar":8,"image":""},
    {"key":"chikoo","display":"Chikoo","serving":"1 medium","calories":83,"protein":0.4,"carbs":20,"fat":1,"fiber":5,"sugar":12,"image":""},
    {"key":"custardapple","display":"Custard Apple","serving":"1 fruit","calories":94,"protein":2,"carbs":23,"fat":0.3,"fiber":4.4,"sugar":19,"image":""},

    # ---------------------------
    # VEGETABLES
    # ---------------------------
    {"key":"carrot","display":"Carrot","serving":"1 medium","calories":25,"protein":0.6,"carbs":6,"fat":0.1,"fiber":1.7,"sugar":3,"image":""},
    {"key":"cabbage","display":"Cabbage","serving":"1 cup","calories":22,"protein":1,"carbs":5,"fat":0.1,"fiber":2,"sugar":2,"image":""},
    {"key":"spinach","display":"Spinach","serving":"1 cup cooked","calories":41,"protein":5,"carbs":7,"fat":0.5,"fiber":4,"sugar":0.4,"image":""},
    {"key":"corn","display":"Sweet Corn","serving":"1 cup","calories":132,"protein":5,"carbs":29,"fat":2,"fiber":4,"sugar":6,"image":""},
    {"key":"potato","display":"Potato","serving":"1 medium","calories":161,"protein":4,"carbs":37,"fat":0.2,"fiber":4,"sugar":2,"image":""},
    {"key":"tomato","display":"Tomato","serving":"1 medium","calories":22,"protein":1,"carbs":5,"fat":0.2,"fiber":1.5,"sugar":3,"image":""},
    {"key":"onion","display":"Onion","serving":"1 medium","calories":44,"protein":1.2,"carbs":10,"fat":0.1,"fiber":1.9,"sugar":5,"image":""},
    {"key":"beetroot","display":"Beetroot","serving":"1 cup","calories":59,"protein":2,"carbs":13,"fat":0.2,"fiber":3.8,"sugar":9,"image":""},
    {"key":"beans","display":"Green Beans","serving":"1 cup","calories":31,"protein":2,"carbs":7,"fat":0.2,"fiber":3,"sugar":3,"image":""},
    {"key":"peas","display":"Green Peas","serving":"1 cup","calories":134,"protein":8.5,"carbs":25,"fat":0.5,"fiber":8.8,"sugar":9,"image":""},
    {"key":"broccoli","display":"Broccoli","serving":"1 cup","calories":31,"protein":2.5,"carbs":6,"fat":0.3,"fiber":2.4,"sugar":1.5,"image":""},
    {"key":"cauliflower","display":"Cauliflower","serving":"1 cup","calories":25,"protein":2,"carbs":5,"fat":0.3,"fiber":2,"sugar":2,"image":""},
    {"key":"ladyfinger","display":"Ladyfinger (Bhindi)","serving":"1 cup","calories":33,"protein":2,"carbs":7,"fat":0.2,"fiber":3,"sugar":1,"image":""},
    {"key":"brinjal","display":"Brinjal (Eggplant)","serving":"1 cup","calories":35,"protein":0.8,"carbs":8,"fat":0.2,"fiber":3,"sugar":3,"image":""},
    {"key":"karela","display":"Bitter Gourd","serving":"1 cup","calories":24,"protein":1,"carbs":5,"fat":0.2,"fiber":2,"sugar":2,"image":""},
    {"key":"pumpkin","display":"Pumpkin","serving":"1 cup","calories":49,"protein":2,"carbs":12,"fat":0.2,"fiber":2.7,"sugar":6,"image":""},

    # ---------------------------
    # INDIAN STAPLES
    # ---------------------------
    {"key":"roti","display":"Roti","serving":"1 roti","calories":120,"protein":3,"carbs":18,"fat":3.5,"fiber":2,"sugar":0,"image":""},
    {"key":"rice","display":"Cooked Rice","serving":"1 cup","calories":206,"protein":4,"carbs":45,"fat":0.4,"fiber":0.6,"sugar":0,"image":""},
    {"key":"brown_rice","display":"Brown Rice","serving":"1 cup","calories":216,"protein":5,"carbs":45,"fat":1.8,"fiber":3.5,"sugar":1,"image":""},
    {"key":"dal","display":"Dal","serving":"1 cup","calories":198,"protein":9,"carbs":29,"fat":3,"fiber":15,"sugar":2,"image":""},
    {"key":"idli","display":"Idli","serving":"1 idli","calories":58,"protein":2,"carbs":12,"fat":0.4,"fiber":1,"sugar":0,"image":""},
    {"key":"dosa","display":"Dosa","serving":"1 dosa","calories":133,"protein":3,"carbs":17,"fat":5,"fiber":1,"sugar":1,"image":""},
    {"key":"poha","display":"Poha","serving":"1 plate","calories":250,"protein":5,"carbs":45,"fat":8,"fiber":2,"sugar":3,"image":""},
    {"key":"upma","display":"Upma","serving":"1 cup","calories":250,"protein":6,"carbs":44,"fat":8,"fiber":3,"sugar":3,"image":""},
    {"key":"paratha","display":"Paratha","serving":"1 paratha","calories":260,"protein":4,"carbs":38,"fat":10,"fiber":3,"sugar":1,"image":""},

    # ---------------------------
    # PROTEIN / DAIRY
    # ---------------------------
    {"key":"egg","display":"Boiled Egg","serving":"1 egg","calories":78,"protein":6,"carbs":0.6,"fat":5,"fiber":0,"sugar":0.6,"image":""},
    {"key":"paneer","display":"Paneer","serving":"100 g","calories":265,"protein":18,"carbs":2,"fat":21,"fiber":0,"sugar":1,"image":""},
    {"key":"milk","display":"Milk","serving":"1 cup","calories":149,"protein":8,"carbs":12,"fat":8,"fiber":0,"sugar":12,"image":""},
    {"key":"curd","display":"Curd","serving":"1 cup","calories":98,"protein":11,"carbs":3.4,"fat":4.3,"fiber":0,"sugar":3,"image":""},

    # ---------------------------
    # NUTS / SEEDS
    # ---------------------------
    {"key":"groundnut","display":"Groundnuts","serving":"30 g","calories":166,"protein":7,"carbs":6,"fat":14,"fiber":2,"sugar":1,"image":""},
    {"key":"cashew","display":"Cashews","serving":"30 g","calories":155,"protein":5,"carbs":9,"fat":12,"fiber":1,"sugar":2,"image":""},
    {"key":"almonds","display":"Almonds","serving":"10 nuts","calories":82,"protein":3,"carbs":3,"fat":7,"fiber":1.5,"sugar":1,"image":""},
    {"key":"walnuts","display":"Walnuts","serving":"30 g","calories":200,"protein":4,"carbs":4,"fat":20,"fiber":2,"sugar":1,"image":""},
    {"key":"chia","display":"Chia Seeds","serving":"1 tbsp","calories":58,"protein":2,"carbs":5,"fat":4,"fiber":5,"sugar":0,"image":""},

    # ---------------------------
    # JUNK / STREET FOOD
    # ---------------------------
    {"key":"pizza","display":"Pizza Slice","serving":"1 slice","calories":285,"protein":12,"carbs":33,"fat":12,"fiber":2,"sugar":3,"image":""},
    {"key":"burger","display":"Veg Burger","serving":"1 burger","calories":320,"protein":10,"carbs":35,"fat":14,"fiber":3,"sugar":6,"image":""},
    {"key":"french_fries","display":"French Fries","serving":"1 medium","calories":365,"protein":4,"carbs":48,"fat":17,"fiber":4,"sugar":0.3,"image":""},
    {"key":"maggi","display":"Maggi (1 pack)","serving":"1 pack","calories":350,"protein":7,"carbs":52,"fat":12,"fiber":2,"sugar":3,"image":""},
    {"key":"fried_rice","display":"Veg Fried Rice","serving":"1 plate","calories":420,"protein":8,"carbs":60,"fat":14,"fiber":3,"sugar":4,"image":""},
    {"key":"hakka_noodles","display":"Hakka Noodles","serving":"1 plate","calories":430,"protein":9,"carbs":64,"fat":14,"fiber":3,"sugar":6,"image":""},
    {"key":"manchurian","display":"Veg Manchurian","serving":"6 pcs","calories":280,"protein":6,"carbs":22,"fat":16,"fiber":2,"sugar":4,"image":""},
    {"key":"chinese_bhel","display":"Chinese Bhel","serving":"1 plate","calories":450,"protein":8,"carbs":55,"fat":20,"fiber":4,"sugar":6,"image":""},
    {"key":"vada_pav","display":"Vada Pav","serving":"1 pc","calories":300,"protein":5,"carbs":40,"fat":12,"fiber":2,"sugar":3,"image":""},
    {"key":"samosa","display":"Samosa","serving":"1 pc","calories":285,"protein":4,"carbs":32,"fat":15,"fiber":3,"sugar":2,"image":""},
    {"key":"pani_puri","display":"Pani Puri","serving":"6 pcs","calories":120,"protein":2,"carbs":18,"fat":4,"fiber":2,"sugar":5,"image":""},

    # ---------------------------
    # BEVERAGES
    # ---------------------------
    {"key":"tea","display":"Tea with milk","serving":"1 cup","calories":30,"protein":1,"carbs":5,"fat":0.5,"fiber":0,"sugar":5,"image":""},
    {"key":"coffee","display":"Coffee with milk","serving":"1 cup","calories":45,"protein":1.5,"carbs":7,"fat":1,"fiber":0,"sugar":6,"image":""},
    {"key":"juice","display":"Fruit Juice (packed)","serving":"1 glass","calories":110,"protein":0,"carbs":26,"fat":0,"fiber":0,"sugar":24,"image":""},
]

# Build lookup maps
FOOD_MAP = {f["key"]: f for f in FOODS}
DISPLAY_LIST = [f"{f['display']} — {f['serving']}" for f in FOODS]
KEY_BY_DISPLAY = {DISPLAY_LIST[i]: FOODS[i]["key"] for i in range(len(FOODS))}

# -------------------------
# Sidebar: BMI check & tracker controls
# -------------------------
st.sidebar.header("Student Tools")

st.sidebar.subheader("BMI Check (quick)")
age = st.sidebar.number_input("Age (years)", min_value=3, max_value=120, value=12)
height_cm = st.sidebar.number_input("Height (cm)", min_value=50, max_value=250, value=140)
weight_kg = st.sidebar.number_input("Weight (kg)", min_value=10.0, max_value=200.0, value=35.0, step=0.5)

if st.sidebar.button("Check BMI"):
    bmi = weight_kg / ((height_cm/100)**2)
    st.sidebar.write(f"Your BMI: {bmi:.1f}")
    if age < 18:
        st.sidebar.info("For children/adolescents BMI-for-age charts are recommended. This is an approximate adult-style BMI indicator.")
    if bmi < 18.5:
        st.sidebar.warning("Approximate classification: Underweight")
    elif bmi < 25:
        st.sidebar.success("Approximate classification: Normal weight")
    elif bmi < 30:
        st.sidebar.warning("Approximate classification: Overweight")
    else:
        st.sidebar.error("Approximate classification: Obese")

st.sidebar.markdown("---")
if st.sidebar.button("Show today's intake summary"):
    df = pd.read_csv(LOG_CSV) if os.path.exists(LOG_CSV) else pd.DataFrame()
    today = datetime.date.today().isoformat()
    df_today = df[df["date"] == today]
    if df_today.empty:
        st.sidebar.info("No intake logged today.")
    else:
        total = int(df_today["calories"].sum())
        st.sidebar.write(f"Total calories today: {total} kcal")
        st.sidebar.table(df_today[["timestamp","food_display","serving_qty","calories"]].tail(10))

# -------------------------
# Main area: Search / select / add
# -------------------------
st.header("Search food (type or choose)")

col1, col2 = st.columns([3,1])
with col1:
    q = st.text_input("Type a food name (e.g., banana, roti, maggi, pizza)")
with col2:
    sel = st.selectbox("Or choose", options=[""] + DISPLAY_LIST)

selected_key = None
if sel:
    selected_key = KEY_BY_DISPLAY.get(sel)
if q and not selected_key:
    ql = q.strip().lower()
    # find exact or substring
    found = None
    for k, f in FOOD_MAP.items():
        if ql == k or ql in k or ql in f["display"].lower():
            found = k
            break
    if found:
        selected_key = found

# Display selection
if selected_key:
    food = FOOD_MAP[selected_key]
    st.subheader(f"{food['display']}  —  {food['serving']}")
    c1, c2 = st.columns([1,2])
    with c1:
        img_path = food.get("image","")
        if img_path and os.path.exists(img_path):
            st.image(img_path, width=220)
        else:
            # placeholder image
            placeholder = Image.new('RGB', (320,200), color=(240,240,240))
            d = ImageDraw.Draw(placeholder)
            d.text((12,12), food["display"], fill=(10,10,10))
            buf = io.BytesIO()
            placeholder.save(buf, format="PNG")
            buf.seek(0)
            st.image(buf, width=220)
    with c2:
        nut = {
            "Calories (kcal)": food.get("calories"),
            "Protein (g)": food.get("protein"),
            "Carbs (g)": food.get("carbs"),
            "Fat (g)": food.get("fat"),
            "Fiber (g)": food.get("fiber"),
            "Sugar (g)": food.get("sugar"),
        }
        st.table(pd.DataFrame.from_dict(nut, orient='index', columns=["Value"]))

    servings = st.number_input("Servings to add", min_value=0.25, max_value=10.0, step=0.25, value=1.0)
    if st.button("Add to my intake"):
        ts = datetime.datetime.now().isoformat(timespec='seconds')
        date = datetime.date.today().isoformat()
        cal = food.get("calories",0) * servings
        new_row = {"timestamp":ts,"date":date,"food_key":selected_key,"food_display":food["display"],"serving_qty":servings,"calories":cal}
        pd.DataFrame([new_row]).to_csv(LOG_CSV, mode='a', header=False, index=False)
        st.success(f"Added {servings} serving(s) of {food['display']} — {int(cal)} kcal")

else:
    st.info("No food selected. Type a name or choose from the dropdown.")

# -------------------------
# Intake log & graphs
# -------------------------
st.markdown("---")
st.header("My Intake & Progress")

def load_log():
    if os.path.exists(LOG_CSV):
        df = pd.read_csv(LOG_CSV, parse_dates=["timestamp"])
        return df
    return pd.DataFrame(columns=["timestamp","date","food_key","food_display","serving_qty","calories"])

df_log = load_log()

# Show table and download
st.subheader("Saved intake log")
if df_log.empty:
    st.info("No intake saved yet.")
else:
    st.dataframe(df_log.sort_values("timestamp", ascending=False).reset_index(drop=True), height=300)
    csv = df_log.to_csv(index=False).encode()
    st.download_button("Download my intake CSV", csv, file_name="intake_log.csv")

# Graph: calories per day (last 14 days)
if not df_log.empty:
    df_log["date"] = pd.to_datetime(df_log["date"]).dt.date
    last_dates = sorted(df_log["date"].unique())[-14:]
    agg = df_log[df_log["date"].isin(last_dates)].groupby("date")["calories"].sum().reindex(pd.to_datetime(last_dates).date, fill_value=0).reset_index()
    fig, ax = plt.subplots(figsize=(8,3))
    ax.bar(agg["date"].astype(str), agg["calories"])
    ax.set_title("Calories per day (last up to 14 days)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Calories (kcal)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Show today's breakdown
    today = datetime.date.today()
    df_today = df_log[df_log["date"] == today]
    if not df_today.empty:
        st.subheader("Today's items")
        st.table(df_today[["timestamp","food_display","serving_qty","calories"]].reset_index(drop=True))

st.markdown("---")
st.subheader("Admin / How to extend the database")

st.markdown("""
**Add new food items:**  
1. Edit the `FOODS` list at the top of this file. Add a dict with keys:
   `key`,`display`,`serving`,`calories`,`protein`,`carbs`,`fat`,`fiber`,`sugar`,`image`  
2. Save the file and restart the app.

**Add images:**  
- Create an `images/` folder inside the app directory.  
- Name the image file with the food `key` (e.g., `banana.jpg`) or put any filename and set the `"image":"images/banana.jpg"` in the FOODS list.  
- The app first looks for `image` path and shows it if found.

**Notes:**  
- This app saves intake permanently to `intake_log.csv` (app folder).  
- For multi-user or cloud deployments, replace CSV storage with a database or per-user storage.
""")

st.caption("Values are approximate and for education. For medical advice consult a professional.")
