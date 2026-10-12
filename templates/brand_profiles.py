brand_profiles = [
    {
        "brand_name": "Nike",
        "official_website": "https://www.nike.com",
        "keywords": ["Nike", "Nike shoes", "Nike sportswear"]
    },
    {
        "brand_name": "Adidas",
        "official_website": "https://www.adidas.com",
        "keywords": ["Adidas", "Adidas shoes", "Adidas sportswear"]
    }
]


def get_all_brands():
    return brand_profiles


def get_brand_by_name(name):
    for brand in brand_profiles:
        if brand["brand_name"].lower() == name.lower():
            return brand
    return None


if __name__ == "__main__":
    for brand in get_all_brands():
        print(brand["brand_name"], "-", brand["official_website"])