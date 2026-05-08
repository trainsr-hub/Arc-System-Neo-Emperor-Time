def parse_units(units_text):
    """Chuyển đổi text định nghĩa đơn vị thành dict."""
    units_map = {}
    lines = units_text.strip().split('\n')
    for line in lines:
        if ':' in line:
            parts = line.split(':')
            name = parts[0].strip()
            try:
                multiplier = int(parts[1].strip())
                units_map[name] = multiplier
            except ValueError:
                continue
    return units_map

def calculate_tier(current_value, base_milestone):
    """Tính toán Tier từ 0-5 dựa trên Base Milestone."""
    if current_value >= base_milestone * 16: return 5
    if current_value >= base_milestone * 8: return 4
    if current_value >= base_milestone * 4: return 3
    if current_value >= base_milestone * 2: return 2
    if current_value >= base_milestone: return 1
    return 0

TIER_CONFIG = {
    5: {"label": "Tier V", "color": "#e0aaff"},
    4: {"label": "Tier IV", "color": "#28a745"},
    3: {"label": "Tier III", "color": "#6f42c1"},
    2: {"label": "Tier II", "color": "#007bff"},
    1: {"label": "Tier I", "color": "#ffc107"},
    0: {"label": "No Tier", "color": "#303030"},
}