import sqlite3

DB_NAME = "brand_profiles.db"


def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS brand_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_name TEXT NOT NULL UNIQUE,
            official_website TEXT NOT NULL,
            keywords TEXT
        )
    """)

    connection.commit()
    connection.close()
    print("Database and table created successfully!")


def add_brand(brand_name, official_website, keywords):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO brand_profiles
            (brand_name, official_website, keywords)
            VALUES (?, ?, ?)
        """, (brand_name, official_website, keywords))

        connection.commit()
        print(brand_name, "added successfully!")

    except sqlite3.IntegrityError:
        print(brand_name, "already exists in the database.")

    finally:
        connection.close()


def get_all_brands():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM brand_profiles")
    brands = cursor.fetchall()

    connection.close()
    return brands


if __name__ == "__main__":
    create_database()

    add_brand(
        "Nike",
        "https://www.nike.com",
        "Nike, Nike shoes, Nike sportswear"
    )

    add_brand(
        "Adidas",
        "https://www.adidas.com",
        "Adidas, Adidas shoes, Adidas sportswear"
    )

    print("\nSaved Brand Profiles:")

    for brand in get_all_brands():
        print(brand)