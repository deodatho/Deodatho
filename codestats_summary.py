import requests
from datetime import datetime

USERNAME = "Deodatho"

def fetch_codestats_data(username):
    url = f"https://codestats.net/api/users/{username}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro: {response.status_code}")
        return None
    return response.json()

def generate_summary(data):
    today = datetime.now().strftime("%Y-%m-%d")
    total_xp = 0
    summary_lines = [f"## 📊 Code::Stats Summary ({today})\n"]

    for lang, details in sorted(data["languages"].items(), key=lambda x: x[1]['xps'], reverse=True)[:10]:
        xp = details["xps"]
        total_xp += xp
        summary_lines.append(f"- **{lang}**: {xp:,} XP")

    summary_lines.append(f"\n**Total XP:** {total_xp:,} XP")
    return "\n".join(summary_lines)

if __name__ == "__main__":
    data = fetch_codestats_data(USERNAME)
    if data:
        summary = generate_summary(data)
        with open("codestats.md", "w", encoding="utf-8") as f:
            f.write(summary)
