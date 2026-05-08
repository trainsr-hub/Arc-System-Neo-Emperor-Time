def get_formatted_value(value, units_map, style="Max"):
    """Xử lý hiển thị theo phong cách Max (Resistor) hoặc Full (Decomposition)."""
    if value == 0:
        base_unit = sorted(units_map.items(), key=lambda x: x[1])[0][0]
        return f"0{base_unit}"

    sorted_units = sorted(units_map.items(), key=lambda x: x[1], reverse=True)

    if style == "Full":
        parts = []
        remaining = value
        for name, multiplier in sorted_units:
            if remaining >= multiplier:
                amt = remaining // multiplier
                remaining %= multiplier
                parts.append(f"{amt}{name}")
        return " ".join(parts) if parts else f"0{sorted_units[-1][0]}"

    else:
        for name, multiplier in sorted_units:
            if value >= multiplier:
                float_val = round(value / multiplier, 2)
                str_val = f"{float_val:g}"
                if "." not in str_val:
                    return f"{str_val}{name}"
                parts = str_val.split(".")
                return f"{parts[0]}{name}{parts[1]}"
        return str(value)