import psycopg2
from psycopg2.extras import RealDictCursor
from config.db_config import DB_CONFIG

def save_recipe(title, ingredients, recipe):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO recipes (title, ingredients, recipe) VALUES (%s, %s, %s)",
            (title, ingredients, recipe)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving recipe: {e}")

def fetch_recipes():
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipes")
        recipes = cursor.fetchall()
        conn.close()
        return recipes
    except Exception as e:
        print(f"Error fetching recipes: {e}")
        return []
