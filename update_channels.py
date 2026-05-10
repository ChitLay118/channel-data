import json
import requests

def fetch_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def auto_merge_json_workflow():
    urls = {
        "channels": "https://raw.githubusercontent.com/globetvapp/globetv.app/refs/heads/main/channels.json",
        "streams": "https://raw.githubusercontent.com/globetvapp/globetv.app/refs/heads/main/streams.json",
        "countries": "https://raw.githubusercontent.com/globetvapp/globetv.app/refs/heads/main/countries.json",
        "logos": "https://raw.githubusercontent.com/globetvapp/globetv.app/refs/heads/main/logos.json"
    }

    print("Fetching data from source URLs...")
    channels_data = fetch_json_from_url(urls["channels"])
    streams_data = fetch_json_from_url(urls["streams"])
    countries_list = fetch_json_from_url(urls["countries"])
    logos_list = fetch_json_from_url(urls["logos"])

    if not all([channels_data, streams_data, countries_list, logos_list]):
        print("Failed to fetch all necessary JSON data. Exiting.")
        return

    print("Processing and merging data...")
    country_map = {c["code"]: c["name"] for c in countries_list}
    channel_info_map = {c["id"]: {"title": c["name"], "country_code": c["country"]} for c in channels_data}
    
    logo_map = {}
    for l in logos_list:
        if l["channel"] not in logo_map:
            logo_map[l["channel"]] = l["url"]

    merged_data = []
    for s in streams_data:
        channel_id = s["channel"]
        info = channel_info_map.get(channel_id)
        
        if info:
            title = info["title"]
            country_code = info["country_code"]
            country_name = country_map.get(country_code, country_code)
            src = s["url"]
            thumb = logo_map.get(channel_id, "")
            
            merged_data.append({
                "title": title,
                "countries": country_name,
                "src": src,
                "thumb": thumb
            })

    output_filename = "channel.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)

    print(f"Successfully merged {len(merged_data)} items into {output_filename}")

if __name__ == "__main__":
    auto_merge_json_workflow()
