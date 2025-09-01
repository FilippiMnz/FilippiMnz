import os
import requests
from datetime import datetime, timedelta

# --- Configurações ---
API_URL = "https://pwn.college/api/v1/users/133382/solves"
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def fetch_api_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados da API: {e}")
        return None

def process_data(api_data):
    if not api_data:
        return {}
    contributions = {}
    for item in api_data:
        if item.get('type') == 'correct':
            date_str = item.get('date')
            if date_str:
                activity_date = datetime.fromisoformat(date_str).date()
                contributions[activity_date] = contributions.get(activity_date, 0) + 1
    return contributions

def get_color(count):
    if count == 0: return COLORS[0]
    if 1 <= count <= 5: return COLORS[1]
    if 6 <= count <= 10: return COLORS[2]
    if 11 <= count <= 15: return COLORS[3]
    return COLORS[4]

def generate_svg(contributions):
    today = datetime.now().date()
    end_date = today
    start_date = end_date - timedelta(days=365)

    grid_start_date = start_date - timedelta(days=(start_date.weekday() + 1) % 7)

    SQUARE_SIZE = 10
    SQUARE_MARGIN = 2
    
    svg = f'<svg width="720" height="120" xmlns="http://www.w3.org/2000/svg" style="background-color:#0d1117;">'
    svg += '<style>.day-square:hover { stroke: #58a6ff; stroke-width: 1px; }</style>'
    svg += f'<text x="10" y="20" fill="#c9d1d9" font-family="monospace" font-size="14">Pwn.college Activity</text>'

    for day_offset in range(53 * 7):
        current_date = grid_start_date + timedelta(days=day_offset)

        if current_date < start_date or current_date > end_date:
            continue
        
        count = contributions.get(current_date, 0)
        color = get_color(count)
        
        week_index = day_offset // 7
        day_of_week_index = day_offset % 7
        
        x = week_index * (SQUARE_SIZE + SQUARE_MARGIN) + 10
        y = day_of_week_index * (SQUARE_SIZE + SQUARE_MARGIN) + 35
        
        svg += (f'<rect x="{x}" y="{y}" width="{SQUARE_SIZE}" height="{SQUARE_SIZE}" '
                f'fill="{color}" rx="2" ry="2" class="day-square">'
                f'<title>{current_date}: {count} solves</title></rect>')
    
    svg += '</svg>'
    return svg

if __name__ == "__main__":
    api_data = fetch_api_data()
    if api_data:
        processed_contributions = process_data(api_data)
        svg_content = generate_svg(processed_contributions)
        
        with open("hacking_activity.svg", "w") as f:
            f.write(svg_content)
        
        print("Gráfico 'hacking_activity.svg' gerado com sucesso! ✔️")
        print("Contribuições (apenas 'correct'):", processed_contributions)
    else:
        print("Falha ao buscar dados. O gráfico não foi atualizado.")
