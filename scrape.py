import requests
import json
import statistics

with open("config.json") as config_file:
    config = json.load(config_file)
    API_KEY = config["SERPAPI_KEY"]

def get_google_shopping_prices(product_name, country="fr"):
    params = {
       'api_key': API_KEY,
        'q': product_name,
        'location': '98146, Washington, United States',
        'gl': country,
        'hl': 'en',
        'google_domain': 'google.com',
        'include_ai_overview': 'true',
        'num': 100
    }

    api_result = requests.get('https://api.scaleserp.com/search', params)

    results = api_result.json()
    
    prices = []

    for result in results.get("organic_results", []):
        if "rich_snippet" in result and "top" in result["rich_snippet"]:
            detected_extensions = result["rich_snippet"]["top"].get("detected_extensions", {})
            if "price" in detected_extensions:
                prices.append(float(detected_extensions["price"]))

    if prices:
        print(f"No of products searched {len(prices)}")
        return min(prices), max(prices), statistics.mean(prices)
    return None, None, None


product = "L'Oréal Paris Revitalift"
min_price, max_price, mean_price = get_google_shopping_prices(product)
print(f"Min Price: €{min_price}, Max Price: €{max_price}, Mean Price: €{mean_price}")