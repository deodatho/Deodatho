import requests
from datetime import datetime, timedelta
import json
from pathlib import Path

USERNAME = "Deodatho"
CACHE_FILE = f"codestats_{USERNAME}.json"
CACHE_EXPIRY = timedelta(hours=6)

class CodeStatsAPI:
    BASE_URL = "https://codestats.net/api/users/"
    
    def __init__(self, username):
        self.username = username
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "CodeStats-Reporter/1.0"})
    
    def get_user_data(self, use_cache=True):
        if use_cache and self._is_cache_valid():
            return self._load_cache()
        
        try:
            response = self.session.get(
                f"{self.BASE_URL}{self.username}",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            self._save_cache(data)
            return data
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None
    
    def _is_cache_valid(self):
        if not Path(CACHE_FILE).exists():
            return False
        mod_time = datetime.fromtimestamp(Path(CACHE_FILE).stat().st_mtime)
        return (datetime.now() - mod_time) < CACHE_EXPIRY
    
    def _load_cache(self):
        with open(CACHE_FILE) as f:
            return json.load(f)
    
    def _save_cache(self, data):
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f, indent=2)

def generate_report(data, filename="codestats.md"):
    if not data:
        return False
    
    report = [
        f"# Code::Stats Report for {USERNAME}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"## 📊 Overview",
        f"- **Total XP**: {data.get('total_xp', 0):,}",
        f"- **Languages Used**: {len(data.get('languages', {}))}\n",
        "## 🏆 Top Languages"
    ]
    
    languages = sorted(
        data["languages"].items(),
        key=lambda x: x[1]["xps"],
        reverse=True
    )[:10]
    
    for lang, details in languages:
        report.append(f"- {lang}: {details['xps']:,} XP")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    
    return True

if __name__ == "__main__":
    api = CodeStatsAPI(USERNAME)
    data = api.get_user_data()
    if generate_report(data):
        print("Report generated successfully!")
    else:
        print("Failed to generate report")
