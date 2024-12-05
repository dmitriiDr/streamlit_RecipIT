import streamlit as st
import requests
import psycopg2
from psycopg2.extras import RealDictCursor


QWEN_API_URL = "http://qwen_api_server:11434/api/generate"


DB_CONFIG = {
    "dbname": "cookbook_db",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": 5432
}


def generate_recipe(ingredients):
    payload = {
        "model": "qwen",
        "prompt": f"Create a recipe using these ingredients: {ingredients}",
        "max_tokens": 50,
        "stream": False
    }
    try:
        response = requests.post(QWEN_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("text", "No recipe generated.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with Qwen API: {e}")
        return None

# save recipe to PostgreSQL
def save_recipe_to_db(title, ingredients, recipe):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO recipes (title, ingredients, recipe) VALUES (%s, %s, %s)",
            (title, ingredients, recipe)
        )
        conn.commit()
        conn.close()
        st.success("Recipe saved successfully!")
    except Exception as e:
        st.error(f"Failed to save recipe: {e}")


def fetch_recipes():
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipes")
        recipes = cursor.fetchall()
        conn.close()
        return recipes
    except Exception as e:
        st.error(f"Failed to fetch recipes: {e}")
        return []

# Streamlit
st.title("RecipIT (AI Recipe Generator)")
st.sidebar.title("Options")
option = st.sidebar.selectbox("Select an option", ["Generate Recipe", "View Cookbook"])

if option == "Generate Recipe":
    st.header("Generate a Recipe")
    ingredients = st.text_area("Enter ingredients (comma-separated):")
    if st.button("Generate Recipe"):
        if ingredients:
            recipe = generate_recipe(ingredients)
            if recipe:
                st.subheader("Generated Recipe")
                st.write(recipe)
                title = st.text_input("Give your recipe a title:")
                if st.button("Save Recipe"):
                    if title:
                        save_recipe_to_db(title, ingredients, recipe)
                    else:
                        st.error("Please provide a title for your recipe.")
        else:
            st.error("Please enter ingredients.")

elif option == "View Cookbook":
    st.header("Your Cookbook")
    recipes = fetch_recipes()
    if recipes:
        for recipe in recipes:
            st.subheader(recipe["title"])
            st.write("**Ingredients:**", recipe["ingredients"])
            st.write("**Recipe:**", recipe["recipe"])
    else:
        st.write("No recipes found. Generate one to get started!")
