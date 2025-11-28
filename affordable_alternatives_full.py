# affordable_alternatives_full.py
import streamlit as st
import pandas as pd
import datetime
import difflib
from io import StringIO

st.set_page_config(page_title="Affordable Alternatives Full", layout="wide", page_icon="🍎")
st.title("Affordable Nutrition Alternatives — Fruits, Vegetables & Junk Foods")

st.markdown("""
Type an expensive food (or pick from dropdown) → see why it's expensive → 3–5 cheaper alternatives → nutrition comparison.  
Typing supports fuzzy matching.
""")

# ---------------------------
# Expanded ALTERNATIVES_DB
# Fruits, Vegetables, Junk/Fast Foods
# ---------------------------
ALTERNATIVES_DB = {
    # Fruits
    "banana": {"why":["rich in potassium","energy"], "alts":["apple","papaya","guava"]},
    "apple": {"why":["fiber","vitamin C"], "alts":["pear","banana","guava"]},
    "papaya": {"why":["vitamin C","fiber"], "alts":["banana","orange","mango"]},
    "mango": {"why":["vitamin A","fiber"], "alts":["papaya","banana","local mango"]},
    "guava": {"why":["vitamin C","fiber"], "alts":["amla","papaya","apple"]},
    "orange": {"why":["vitamin C"], "alts":["lemon","papaya","banana"]},
    "pineapple": {"why":["vitamin C","enzyme bromelain"], "alts":["papaya","apple","banana"]},
    "pomegranate": {"why":["antioxidants","vitamin C"], "alts":["jamun","black grapes","apple"]},
    "watermelon": {"why":["hydration","vitamin C"], "alts":["muskmelon","papaya","apple"]},
    "muskmelon": {"why":["vitamin A","hydration"], "alts":["watermelon","papaya","banana"]},
    "kiwi": {"why":["vitamin C","fiber"], "alts":["amla","guava","orange"]},
    "dragon_fruit": {"why":["fiber","vitamin C"], "alts":["papaya","watermelon","apple"]},
    "lychee": {"why":["vitamin C","antioxidants"], "alts":["guava","mango","banana"]},
    "cherries": {"why":["antioxidants","vitamin C"], "alts":["pomegranate","grapes","apple"]},
    "blueberries": {"why":["antioxidants","fiber"], "alts":["jamun","black grapes","pomegranate"]},
    "strawberries": {"why":["vitamin C","antioxidants"], "alts":["papaya","watermelon","banana"]},
    "jamun": {"why":["fiber","vitamins"], "alts":["black grapes","pomegranate","apple"]},
    "amla": {"why":["vitamin C","antioxidants"], "alts":["guava","orange","papaya"]},
    "pear": {"why":["fiber","vitamin C"], "alts":["apple","banana","guava"]},
    "plum": {"why":["fiber","vitamin C"], "alts":["apple","guava","banana"]},
    "peach": {"why":["vitamin A","fiber"], "alts":["papaya","apple","banana"]},
    "apricot": {"why":["vitamin A","fiber"], "alts":["papaya","apple","banana"]},
    "dates": {"why":["energy","fiber"], "alts":["raisins","banana","figs"]},
    "fig": {"why":["fiber","minerals"], "alts":["dates","banana","papaya"]},
    "coconut": {"why":["healthy fats","fiber"], "alts":["groundnut","sesame seeds","banana"]},
    # Vegetables
    "spinach": {"why":["iron","vitamin A"], "alts":["methi","cabbage","kale"]},
    "methi": {"why":["iron","fiber"], "alts":["spinach","drumstick leaves","cabbage"]},
    "coriander": {"why":["vitamin C","antioxidants"], "alts":["mint","spinach","cabbage"]},
    "cabbage": {"why":["fiber","vitamin C"], "alts":["cauliflower","broccoli","spinach"]},
    "cauliflower": {"why":["fiber","vitamin C"], "alts":["cabbage","broccoli","spinach"]},
    "broccoli": {"why":["vitamin C","vitamin K"], "alts":["cauliflower","cabbage","spinach"]},
    "kale": {"why":["vitamin K","vitamin C"], "alts":["spinach","methi","cabbage"]},
    "carrot": {"why":["vitamin A"], "alts":["pumpkin","tomato","capsicum"]},
    "beetroot": {"why":["fiber","iron"], "alts":["carrot","pumpkin","radish"]},
    "capsicum_green": {"why":["vitamin C"], "alts":["carrot","tomato","bell pepper red"]},
    "capsicum_red": {"why":["vitamin C"], "alts":["carrot","tomato","capsicum green"]},
    "zucchini": {"why":["fiber","vitamin A"], "alts":["bottle gourd","ridge gourd","cucumber"]},
    "bottle_gourd": {"why":["fiber","hydration"], "alts":["ridge gourd","pumpkin","cucumber"]},
    "ridge_gourd": {"why":["fiber","hydration"], "alts":["bottle gourd","pumpkin","cucumber"]},
    "pumpkin": {"why":["vitamin A","fiber"], "alts":["carrot","sweet potato","zucchini"]},
    "tomato": {"why":["vitamin C","lycopene"], "alts":["carrot","capsicum","pumpkin"]},
    "brinjal": {"why":["fiber","antioxidants"], "alts":["pumpkin","zucchini","capsicum"]},
    "cucumber": {"why":["hydration","fiber"], "alts":["bottle gourd","zucchini","lettuce"]},
    "drumstick": {"why":["vitamin C","calcium"], "alts":["spinach","methi","beans"]},
    "beans": {"why":["protein","fiber"], "alts":["peas","drumstick","spinach"]},
    "peas": {"why":["protein","fiber"], "alts":["beans","spinach","methi"]},
    "corn": {"why":["carbs","fiber"], "alts":["peas","sweet potato","millets"]},
    "onion": {"why":["fiber","antioxidants"], "alts":["leek","garlic","shallot"]},
    "garlic": {"why":["antioxidants"], "alts":["onion","leek","shallot"]},
    "ginger": {"why":["antioxidants"], "alts":["garlic","turmeric","onion"]},
    "mushroom_button": {"why":["protein","fiber"], "alts":["tofu","paneer","soy chunks"]},
    "mushroom_portobello": {"why":["umami","B-vitamins"], "alts":["button mushroom","paneer","tofu"]},
    "sweet_potato": {"why":["fiber","vitamin A"], "alts":["pumpkin","carrot","zucchini"]},
    "radish": {"why":["fiber","vitamin C"], "alts":["turnip","beetroot","cabbage"]},
    "turnip": {"why":["fiber","vitamin C"], "alts":["radish","beetroot","cabbage"]},
    "lettuce": {"why":["hydration","fiber"], "alts":["cucumber","spinach","capsicum green"]},
    "brussels_sprouts": {"why":["fiber","vitamin C"], "alts":["cabbage","broccoli","kale"]},
    "celery": {"why":["fiber","hydration"], "alts":["cucumber","lettuce","spinach"]},
    # Junk/Fast Foods (as before)
    "burger": {"why":["processed meat","cheese","fast food"], "alts":["grilled sandwich","paneer burger","veg cutlet sandwich"]},
    "pizza": {"why":["cheese","processed dough","high calorie"], "alts":["homemade veg pizza","whole wheat flatbread with veggies","paneer wrap"]},
    "cake": {"why":["sugar","butter","baking ingredients"], "alts":["banana bread","date cake","suji cake"]},
    "pastry": {"why":["butter","sugar"], "alts":["homemade puff with veg","fruit tart"]},
    "ice_cream": {"why":["sugar","cream"], "alts":["frozen yogurt","banana ice cream","mango sorbet"]},
    "chocolate_shake": {"why":["sugar","milk","chocolate syrup"], "alts":["banana milkshake","malted milk","buttermilk smoothie"]},
    "noodles": {"why":["processed noodles","MSG","oil"], "alts":["vegetable upma","poha","whole wheat pasta"]},
    "manchurian": {"why":["fried vegetables","sauce"], "alts":["steamed veg balls","soya chunks curry","paneer tikka"]},
    "chinese_bhel": {"why":["fried noodles","sauces","MSG"], "alts":["bhel puri","corn chaat","mixed sprouts salad"]},
    "fries": {"why":["fried potatoes","oil"], "alts":["baked potato wedges","roasted sweet potato","air-fried fries"]},
    "garlic_bread": {"why":["butter","bread"], "alts":["roasted garlic chapati","veg sandwich","grilled bread with olive oil"]},
    "donuts": {"why":["sugar","oil","flour"], "alts":["banana muffins","baked donuts","poha ladoo"]},
    "soft_drinks": {"why":["sugar","carbonation"], "alts":["buttermilk","lime water","coconut water"]},
    "energy_drinks": {"why":["caffeine","sugar"], "alts":["coconut water with salt","herbal tea","fruit juice"]},
    "milkshakes": {"why":["sugar","cream"], "alts":["banana shake","mango lassi","soy milkshake"]}
}

# ---------------------------
# Nutrition Reference (per serving)
# ---------------------------
NUTRITION_REF = {
    "banana":{"cal":105,"protein":1.3,"carbs":27,"fat":0.4,"fiber":3.1},
    "apple":{"cal":95,"protein":0.5,"carbs":25,"fat":0.3,"fiber":4.4},
    "papaya":{"cal":59,"protein":0.9,"carbs":15,"fat":0.4,"fiber":2.5},
    "mango":{"cal":99,"protein":0.8,"carbs":25,"fat":0.6,"fiber":2.6},
    "guava":{"cal":68,"protein":2.6,"carbs":14,"fat":1,"fiber":5.4},
    "orange":{"cal":62,"protein":1.2,"carbs":15,"fat":0.2,"fiber":3.1},
    "spinach":{"cal":23,"protein":2.9,"carbs":3.6,"fat":0.4,"fiber":2.2},
    "methi":{"cal":49,"protein":4,"carbs":7,"fat":0.5,"fiber":1.6},
    "cabbage":{"cal":22,"protein":1,"carbs":5,"fat":0.1,"fiber":2},
    "broccoli":{"cal":25,"protein":2,"carbs":5,"fat":0.3,"fiber":2},
    "carrot":{"cal":41,"protein":0.9,"carbs":10,"fat":0.2,"fiber":2.8},
    "burger":{"cal":295,"protein":13,"carbs":33,"fat":12,"fiber":2},
    "pizza":{"cal":285,"protein":12,"carbs":36,"fat":10,"fiber":2},
    "cake":{"cal":240,"protein":3,"carbs":35,"fat":10,"fiber":1},
    "ice_cream":{"cal":207,"protein":4,"carbs":24,"fat":11,"fiber":0},
    "noodles":{"cal":220,"protein":6,"carbs":35,"fat":7,"fiber":2},
    "DEFAULT":{"cal":100,"protein":2,"carbs":20,"fat":5,"fiber":1}
}

# PRETTY names
PRETTY = {k:k.replace("_"," ").title() for k in ALTERNATIVES_DB}
def pretty(k): return PRETTY.get(k, k.replace("_"," ").title())

# ---------------------------
# Categories
# ---------------------------
CATEGORIES = {
    "Fruits & Berries":[k for k in ALTERNATIVES_DB if k in ["banana","apple","papaya","mango","guava","orange","pineapple","pomegranate","watermelon","muskmelon","kiwi","dragon_fruit","lychee","cherries","blueberries","strawberries","jamun","amla","pear","plum","peach","apricot","dates","fig","coconut"]],
    "Vegetables & Greens":[k for k in ALTERNATIVES_DB if k in ["spinach","methi","coriander","cabbage","cauliflower","broccoli","kale","carrot","beetroot","capsicum_green","capsicum_red","zucchini","bottle_gourd","ridge_gourd","pumpkin","tomato","brinjal","cucumber","drumstick","beans","peas","corn","onion","garlic","ginger","mushroom_button","mushroom_portobello","sweet_potato","radish","turnip","lettuce","brussels_sprouts","celery"]],
    "Junk Foods / Fast Foods":[k for k in ALTERNATIVES_DB if k in ["burger","pizza","cake","pastry","ice_cream","chocolate_shake","noodles","manchurian","chinese_bhel","fries","garlic_bread","donuts","soft_drinks","energy_drinks","milkshakes"]]
}

EXPENSIVE_KEYS = sorted(ALTERNATIVES_DB.keys())

# Build dropdown
dropdown_options=[]
for cat, keys in CATEGORIES.items():
    if keys:
        dropdown_options.append(f"--- {cat} ---")
        dropdown_options += [pretty(k) for k in keys]

# UI controls
col1,col2=st.columns([3,1])
with col1:
    q=st.text_input("Type expensive food (fuzzy search OK)")
with col2:
    sel=st.selectbox("Or choose from categories", options=[""]+dropdown_options)

# Resolve selection
selected_key=None
if sel:
    pretty_to_key={pretty(k):k for k in EXPENSIVE_KEYS}
    selected_key=pretty_to_key.get(sel)

if not selected_key and q:
    q_norm=q.strip().lower().replace(" ","_")
    if q_norm in ALTERNATIVES_DB:
        selected_key=q_norm
    else:
        matches=difflib.get_close_matches(q.strip().lower(), EXPENSIVE_KEYS, n=3, cutoff=0.6)
        if matches:
            selected_key=matches[0]

if not selected_key and q:
    close=difflib.get_close_matches(q.strip().lower(), EXPENSIVE_KEYS, n=5, cutoff=0.5)
    if close:
        st.info("Did you mean: "+", ".join(pretty(c) for c in close)+"?")

# Show result
if selected_key:
    data=ALTERNATIVES_DB[selected_key]
    st.subheader(f"Expensive food: {pretty(selected_key)}")
    st.markdown("**Why it's expensive / key nutrients:**")
    st.write(", ".join(data["why"]))
    alt_keys=data["alts"][:5]
    st.markdown("**Affordable alternatives (3–5):**")
    st.write(", ".join(pretty(a) for a in alt_keys))

    # Comparison table
    rows=[]
    exp_nut=NUTRITION_REF.get(selected_key,NUTRITION_REF.get("DEFAULT"))
    rows.append({"Food":pretty(selected_key)+" (expensive)","Calories":exp_nut["cal"],"Protein (g)":exp_nut["protein"],"Carbs (g)":exp_nut["carbs"],"Fat (g)":exp_nut["fat"],"Fiber (g)":exp_nut["fiber"]})
    for a in alt_keys:
        nut=NUTRITION_REF.get(a,NUTRITION_REF.get("DEFAULT"))
        rows.append({"Food":pretty(a),"Calories":nut["cal"],"Protein (g)":nut["protein"],"Carbs (g)":nut["carbs"],"Fat (g)":nut["fat"],"Fiber (g)":nut["fiber"]})
    df_comp=pd.DataFrame(rows)
    st.subheader("Nutrition comparison (per serving, approx.)")
    st.table(df_comp.set_index("Food"))

    csv_buf=StringIO()
    df_comp.to_csv(csv_buf,index=False)
    st.download_button("Download this comparison as CSV",csv_buf.getvalue().encode(),file_name=f"{selected_key}_alternatives_{datetime.date.today()}.csv")

st.markdown("---")
st.subheader("Full alternatives database (preview)")
rows=[]
for k,v in ALTERNATIVES_DB.items():
    rows.append({"Expensive Food":pretty(k),"Why":"; ".join(v["why"]),"Alternatives":"; ".join(pretty(a) for a in v["alts"])})
df_full=pd.DataFrame(rows)
st.dataframe(df_full,height=300)
csv_buf_full=StringIO()
df_full.to_csv(csv_buf_full,index=False)
st.download_button("Download full DB (CSV)",csv_buf_full.getvalue().encode(),file_name=f"alternatives_full_{datetime.date.today()}.csv")
