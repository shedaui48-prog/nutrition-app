import streamlit as st

st.set_page_config(page_title="Affordable Food Alternatives", page_icon="🍌")

st.title("🍏 Affordable Alternatives to Expensive Foods")
st.write("Type an expensive food item to find 3–5 cheaper, healthy alternatives.")

# Database of expensive foods and their nutrient profile + alternatives
food_data = {
    "avocado": {
        "nutrients": ["healthy fats", "fiber", "vitamin E", "potassium"],
        "alternatives": ["banana", "groundnut", "coconut", "sesame seeds", "bottle gourd"]
    },
    "blueberries": {
        "nutrients": ["antioxidants", "vitamin C", "fiber"],
        "alternatives": ["jamun", "black grapes", "amla", "pomegranate"]
    },
    "strawberries": {
        "nutrients": ["vitamin C", "antioxidants"],
        "alternatives": ["amla", "orange", "guava", "pineapple"]
    },
    "kiwi": {
        "nutrients": ["vitamin C", "fiber", "antioxidants"],
        "alternatives": ["amla", "orange", "mosambi"]
    },
    "dragon fruit": {
        "nutrients": ["fiber", "vitamin C", "antioxidants"],
        "alternatives": ["papaya", "watermelon", "pomegranate"]
    },
    "broccoli": {
        "nutrients": ["fiber", "vitamin K", "vitamin C"],
        "alternatives": ["cauliflower", "cabbage", "spinach"]
    },
    "asparagus": {
        "nutrients": ["folate", "fiber", "vitamin K"],
        "alternatives": ["beans", "green peas", "spinach"]
    },
    "zucchini": {
        "nutrients": ["fiber", "vitamin A"],
        "alternatives": ["bottle gourd", "ridge gourd", "cucumber"]
    },
    "almonds": {
        "nutrients": ["healthy fats", "vitamin E", "protein"],
        "alternatives": ["groundnuts", "sesame seeds", "sunflower seeds"]
    },
    "walnuts": {
        "nutrients": ["omega-3", "healthy fats"],
        "alternatives": ["flax seeds", "groundnuts", "sesame seeds"]
    },
    "chia seeds": {
        "nutrients": ["omega-3", "fiber"],
        "alternatives": ["flax seeds", "basil seeds (sabja)", "sesame seeds"]
    },
    "salmon": {
        "nutrients": ["omega-3", "protein"],
        "alternatives": ["sardines", "mackerel (bangda)", "eggs", "tofu"]
    },
    "quinoa": {
        "nutrients": ["protein", "fiber", "magnesium"],
        "alternatives": ["millets", "brown rice", "oats"]
    },
    "olive oil": {
        "nutrients": ["healthy fats", "vitamin E"],
        "alternatives": ["mustard oil", "groundnut oil", "coconut oil"]
    }
}

# Input field
query = st.text_input("Enter an expensive food item (e.g., avocado, broccoli, almonds)")

if query:
    food = query.lower()

    if food in food_data:
        st.subheader(f"💰 Expensive Food: {food.capitalize()}")

        st.write("### Key Nutrients")
        st.write(", ".join(food_data[food]["nutrients"]))

        st.write("### 🟢 Affordable Alternatives (3–5 options)")
        for alt in food_data[food]["alternatives"]:
            st.write(f"- {alt.capitalize()}")

    else:
        st.error("Food not found in database. Try common expensive items like avocado, quinoa, broccoli, almonds, etc.")

