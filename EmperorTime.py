import streamlit as st
from utils.storage import load_data, save_data, clear_all_data
from utils.formatter import get_formatted_value
from utils.logic import parse_units, calculate_tier, TIER_CONFIG

# --- Khởi tạo ---
if 'vault' not in st.session_state:
    st.session_state.vault = load_data()

# --- Sidebar: Form tạo kho ---
with st.sidebar:
    st.header("🛠 Thiết lập Kho mới")
    with st.form("new_asset_form", clear_on_submit=True):
        new_name = st.text_input("Tên tài sản")
        new_units_raw = st.text_area("Đơn vị (Tên:Hệ số)", value="K:1\nM:1000")
        new_style = st.selectbox("Kiểu hiển thị", options=["Max", "Full"])
        new_base = st.number_input("Mốc Tier I (Base)", min_value=1, value=1000)
        new_step = st.number_input("Bước nhảy (Step)", min_value=1, value=1)
        new_note_template = st.text_area("Ghi chú", value="Tích lũy: {v}")
        
        if st.form_submit_button("Tạo kho lưu trữ"):
            u_map = parse_units(new_units_raw)
            if new_name and u_map:
                new_item = {
                    "id": len(st.session_state.vault) + 1,
                    "name": new_name, "value": 0, "units_map": u_map,
                    "display_style": new_style, "base_milestone": new_base, 
                    "step": new_step, "note_template": new_note_template
                }
                st.session_state.vault.append(new_item)
                save_data(st.session_state.vault)
                st.rerun()

# --- Giao diện chính ---
st.title("🏆 Progress Vault System")

if not st.session_state.vault:
    st.warning("Chưa có kho lưu trữ nào.")
else:
    for index, item in enumerate(st.session_state.vault):
        current_val, base, u_map = item['value'], item['base_milestone'], item['units_map']
        style = item.get('display_style', 'Max')
        tier_idx = calculate_tier(current_val, base)
        tier_info = TIER_CONFIG[tier_idx]
        formatted_val = get_formatted_value(current_val, u_map, style)
        
        with st.container():
            col1, col2, col3 = st.columns([2, 1.2, 0.8])
            with col1:
                st.markdown(f"""
                    <div style="padding: 15px; border-radius: 10px; border-left: 12px solid {tier_info['color']}; background-color: #f8f9fa;">
                        <h2 style="margin: 0; font-size: 18px; color: #555;">{item['name']} <small style="color:#aaa">[{style}]</small></h2>
                        <div style="display: flex; align-items: baseline; gap: 10px;">
                            <span style="font-size: 32px; font-weight: bold; color: {tier_info['color']};">{tier_info['label']}</span>
                            <span style="font-size: 22px; color: #333;">{formatted_val}</span>
                        </div>
                        <p style="margin: 5px 0 0 0; font-style: italic; color: #666; font-size: 13px;">{item['note_template'].format(v=formatted_val)}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                sc1, sc2 = st.columns(2)
                change = sc1.number_input(f"Lượng", value=10, step=item['step'], key=f"n_{index}")
                u_sel = sc2.selectbox(f"Đơn vị", options=list(u_map.keys()), key=f"u_{index}")
                actual_change = change * u_map[u_sel]
                
            with col3:
                st.write("Thao tác")
                b1, b2 = st.columns(2)
                if b1.button("➕", key=f"a_{index}"):
                    st.session_state.vault[index]['value'] += actual_change
                    save_data(st.session_state.vault)
                    st.rerun()
                if b2.button("➖", key=f"s_{index}"):
                    st.session_state.vault[index]['value'] = max(0, current_val - actual_change)
                    save_data(st.session_state.vault)
                    st.rerun()

        # Progress Bar
        if tier_idx < 5:
            floor = base * (2 ** (tier_idx - 1)) if tier_idx > 0 else 0
            ceil = base * (2 ** tier_idx)
            progress = min(max((current_val - floor) / (ceil - floor), 0.0), 1.0)
            fmt_ceil = get_formatted_value(ceil, u_map, style="Max")
            st.write("\n")
            st.progress(progress, text=f"Next: {formatted_val} / {fmt_ceil}")
            st.markdown(f"<p style='text-align: center; font-size: 14px; font-weight: bold; margin-top: -15px;'>{progress*100:.2f}%</p>", unsafe_allow_html=True)
        st.divider()

if st.sidebar.button("🗑 Xóa tất cả dữ liệu"):
    clear_all_data()
    st.session_state.vault = []
    st.rerun()