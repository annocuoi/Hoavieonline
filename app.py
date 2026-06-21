import json
import base64
import requests
import streamlit as st # type: ignore
import streamlit.components.v1 as components
import time
from PIL import Image
import io

# Cấu hình giao diện ứng dụng (phải nằm trước mọi lệnh st.)
st.set_page_config(
    page_title="Quản Lý Hoa - Tên Hội",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None
    }
)

st.markdown(
    """
    <style>
    /* Ẩn thanh toolbar Streamlit trên cùng */
    [data-testid="stToolbar"] {
        display: none;
    }
    
    /* Ẩn header */
    [data-testid="stHeader"] {
        display: none;
    }
    
    /* Ẩn menu */
    #MainMenu {
        visibility: hidden;
    }
    
    /* Ẩn footer */
    footer {
        visibility: hidden;
    }
    /* làm trong suốt ô selectbox */
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.35) !important;
        border-radius:12px !important;
    }

    /* bỏ nền xám bên trong */
    div[data-baseweb="select"] input {
        background: transparent !important;
    }

    /* vùng chứa chữ */
    div[data-baseweb="select"] span {
        background: transparent !important;
    }
    /* ẩn gạch nhập trong selectbox */
    div[data-baseweb="select"] input {
        caret-color: transparent !important;
    }
    /* tiêu đề tự co mọi màn hình */
    .title-hoi {
        display:flex;
        justify-content:center;
        align-items:center;
        gap:10px;

        font-size:clamp(22px, 6vw, 38px);

        font-weight:900;
        color:#000000;
        white-space:nowrap;
    }


    /* icon hoa tự co */
    .title-hoi span {
        white-space:nowrap;
    }
    /* chữ trong danh sách xổ xuống selectbox */
    div[role="option"],
    div[role="option"] *,
    ul[role="listbox"] *,
    [data-baseweb="popover"] * {
        color:#000000 !important;
        font-weight:700 !important;
    }


    /* nền dòng option */
    div[role="option"] {
        background:white !important;
    }
    /* chữ trong selectbox */
    div[data-baseweb="select"] * {
        color:#000000 !important;
    }

    /* chữ option đang chọn */
    div[data-baseweb="select"] span {
        color:#000000 !important;
        font-weight:700 !important;
    }


    /* chữ trong ô nhập */
    input {
        color:#000000 !important;
        font-weight:700 !important;
    }

    /* placeholder */
    input::placeholder {
        color:#555555 !important;
    }


    /* text area nếu có */
    textarea {
        color:#000000 !important;
    }
    /* ép toàn bộ chữ Streamlit */
    .stApp * {
        color:#111111 !important;
    }


    /* tiêu đề markdown HTML */
    
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] *,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span {
        color:#000000 !important;
        font-weight:700 !important;
    }


    /* chữ trong container */
    .element-container,
    .element-container * {
        color:#000000 !important;
    }


    /* chữ tab */
    button[data-baseweb="tab"] *,
    button[data-baseweb="tab"] p {
        color:#111111 !important;
    }


    /* radio lọc cấp */
    [data-testid="stRadio"] * {
        color:#111111 !important;
    }


    /* metric */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color:#000 !important;
    }

    html, body, .stApp {
        color:#111827 !important;
    }

    /* chữ thường */
    p, span, label, div {
        color:#111827 !important;
        font-weight:600;
    }

    /* tiêu đề */
    h1, h2, h3, h4 {
        color:#1e293b !important;
        font-weight:900 !important;
        text-shadow: 1px 1px 3px white;
    }

    /* tab */
    button[data-baseweb="tab"] p {
        color:#111827 !important;
        font-weight:800;
    }


    /* số thống kê 22 - 5 */
    [data-testid="stMetricValue"] {
        color:#000000 !important;
        font-weight:900;
    }


    /* tên hoa */
    .flower-name {
        color:#000 !important;
        font-weight:900;
        text-shadow:1px 1px 2px white;
    }


    /* chữ trong nút */
    button {
        color:#111827 !important;
        font-weight:700 !important;
    }


    /* select + nhập liệu */
    input, textarea {
        color:black !important;
        font-weight:700;
    }

    div[data-baseweb="select"] * {
        color:black !important;
    }

    /* toàn bộ nền */
    .stApp {
        background: linear-gradient(
            135deg,
            #1e1b4b,
            #581c87,
            #831843
        );
    }


    /* bỏ nền trắng chính giữa */
    .block-container {
        background: transparent !important;
    }


    /* các khung trắng */
    div[data-testid="stVerticalBlock"] {
        background: transparent !important;
    }


    /* tab */
    button[data-baseweb="tab"] {
        background: rgba(255,255,255,0.15);
        border-radius: 15px;
        color: white;
    }


    /* chữ toàn app */
    h1,h2,h3,p,span,label,div {
        color: white !important;
    }


    /* ô nhập */
    input {
        background: rgba(255,255,255,0.9)!important;
        color:black!important;
        border-radius:12px!important;
    }


    /* selectbox */
    div[data-baseweb="select"] {
        background:white;
        border-radius:12px;
    }


    </style>
    """,
    unsafe_allow_html=True
)

GRID_STYLE = """
<style>
html, body{
    overflow-x:hidden;
    max-width:100%;
}

.flower-grid{
    display:grid;
    grid-template-columns:repeat(auto-fit, minmax(80px, 1fr));
    gap:18px;

    width:100%;
    max-width:100%;
    overflow-x:hidden;

    padding-right:15px;
    box-sizing:border-box;
}

.flower-box{
    text-align:center;
}

.flower-box img{
    width:75px;
    height:75px;
    object-fit:cover;

    border-radius:10px;
    padding:3px;
    box-shadow:0 3px 8px rgba(0,0,0,.3);
}
.hoa-img{
    width:75px;
    height:75px;
    object-fit:cover;

    border:5px solid;
    border-radius:10px;
    padding:3px;

    box-shadow:0 3px 8px rgba(0,0,0,.3);
}

.flower-box img.cap-do{
    border:5px solid #ef4444;
}

.flower-box img.cap-tim{
    border:5px solid #c084fc;
}

.flower-box img.cap-xanh-la{
    border:5px solid #22c55e;
}

.flower-box img.cap-xanh-duong{
    border:5px solid #38bdf8;
}

.flower-box img.cap-cam{
    border:5px solid #f59e0b;
}

.flower-name{
    font-size:13px;
    font-weight:bold;
    margin-top:5px;
}


.member-grid{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:8px;
}


.member-box{
    text-align:center;
    border:1px solid #ddd;
    border-radius:10px;
    padding:6px;
}


.avatar{
    width:45px;
    height:45px;
    border-radius:50%;
    background:#8b5cf6;
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    margin:auto;
    font-size:20px;
    font-weight:bold;
}


.member-name{
    font-size:11px;
    font-weight:bold;
}


.member-count{
    font-size:10px;
}


</style>
"""
def anh_html(data):
    if not data:
        return ""

    if isinstance(data, bytes):
        img64 = base64.b64encode(data).decode()
    else:
        img64 = data

    return f"data:image/jpeg;base64,{img64}"
def background_image(file):
    with open(file, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image: url("data:image/png;base64,{data}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .block-container {{
            background: rgba(255,255,255,0.75);
            border-radius:20px;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )
background_image("nen.jpg")
def sap_xep_hoa(ds_hoa):

    thu_tu_cap = {
        "Đỏ": 1,
        "Cam": 2,
        "Tím": 3,
        "Xanh dương": 4,
        "Xanh lá": 5
    }

    return sorted(
        ds_hoa,
        key=lambda ten: thu_tu_cap.get(
            st.session_state.kho_hoa_tong.get(
                ten,
                {}
            ).get(
                "cap",
                ""
            ),
            99
        )
    )

# ====================================================
# ⚙️ CẤU HÌNH HỆ THỐNG (ĐỌC TOKEN TỪ SECRETS AN TOÀN)
# ====================================================
MAT_KHAU_HE_THONG = "111111"
TAI_KHOAN = {
    "admin": {
        "pass": "111111",
        "quyen": "admin"
    },

    "khach": {
        "pass": "123456",
        "quyen": "user"
    }
}


if "quyen" not in st.session_state:
    st.session_state.quyen = None

if "user_hien_tai" not in st.session_state:
    st.session_state.user_hien_tai = None

if "GITHUB_TOKEN" in st.secrets:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
else:
    GITHUB_TOKEN = ""

REPO_NAME = "annocuoi/quan-ly-hoa-vien"
FILE_PATH = "du_lieu_hoi_do_kiep.json"
BRANCH = "main"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
API_URL = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"

# ====================================================
# 🔒 KHU VỰC ĐĂNG NHẬP BẢO MẬT
# ====================================================
if "da_dang_nhap" not in st.session_state:
    st.session_state.da_dang_nhap = False

if not st.session_state.da_dang_nhap:
    st.markdown("<h2 style='text-align: center; color: #60A5FA; font-size: 24px;'>🔒 HỆ THỐNG BẢO MẬT</h2>", unsafe_allow_html=True)
    _, col_center, _ = st.columns([1, 1.5, 1])
    with col_center:
        with st.container(border=True):
            st.markdown("<p style='font-size: 14px;'>Vui lòng nhập mật khẩu chính xác để truy cập.</p>", unsafe_allow_html=True)
            ten_dang_nhap = st.text_input(
                "Tài khoản",
                placeholder="Nhập tài khoản...",
                label_visibility="collapsed"
            )
            mat_khau_nhap = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu...", label_visibility="collapsed")
            
            if st.button("🔓 Đăng Nhập", use_container_width=True):
                if ten_dang_nhap in TAI_KHOAN and mat_khau_nhap == TAI_KHOAN[ten_dang_nhap]["pass"]:

                    st.session_state.da_dang_nhap = True

                    st.session_state.quyen = TAI_KHOAN[ten_dang_nhap]["quyen"]

                    st.session_state.user_hien_tai = ten_dang_nhap

                    st.rerun()

                else:

                    st.error("Sai tài khoản hoặc mật khẩu")

    st.stop()

col_title, col_logout = st.columns([8, 2])
with col_logout:
    if st.button("🚪 Đăng xuất", type="secondary", use_container_width=True):
        st.session_state.da_dang_nhap = False
        st.rerun()

# ----------------------------------------------------
# 📂 HÀM ĐỌC DỮ LIỆU TỪ GITHUB
# ----------------------------------------------------
def tai_du_lieu_tu_github():
    mac_dinh = {"kho_hoa_tong": {}, "du_lieu_thanh_vien": {}}
    try:
        url_doc = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}&t={time.time()}"
        headers_doc = {"Accept": "application/vnd.github.v3.raw"}
        if GITHUB_TOKEN:
            headers_doc["Authorization"] = f"token {GITHUB_TOKEN}"
            
        response = requests.get(url_doc, headers=headers_doc, timeout=10)
        if response.status_code == 200:
            chuoi_thong_tin = response.text.strip()
            if not chuoi_thong_tin or chuoi_thong_tin == '""' or chuoi_thong_tin == '{}':
                return mac_dinh
                
            data = json.loads(chuoi_thong_tin)
            
            kho_tong = data.get("kho_hoa_tong", {})
            for ten_hoa in kho_tong:
                if kho_tong[ten_hoa].get("anh"):
                    try:
                        kho_tong[ten_hoa]["anh"] = base64.b64decode(kho_tong[ten_hoa]["anh"].encode("utf-8"))
                    except Exception:
                        kho_tong[ten_hoa]["anh"] = None
            return data
    except Exception as e:
        st.sidebar.warning(f"Đang kết nối đám mây... ({str(e)})")
    return mac_dinh

# ----------------------------------------------------
# 💾 HÀM GHI DỮ LIỆU LÊN GITHUB
# ----------------------------------------------------
def luu_du_lieu_len_github():
    if not GITHUB_TOKEN:
        st.error("Chưa cấu hình GITHUB_TOKEN!")
        return False

    try:
        kho_tong_copy = {}
        for ten_hoa, info in st.session_state.kho_hoa_tong.items():
            if info.get("anh") and isinstance(info["anh"], bytes):
                anh_str = base64.b64encode(info["anh"]).decode("utf-8")
            else:
                anh_str = info.get("anh") if isinstance(info.get("anh"), str) else None
                
            kho_tong_copy[ten_hoa] = {
                "cap": info["cap"],
                "anh": anh_str
            }
            
        data_to_save = {
            "kho_hoa_tong": kho_tong_copy,
            "du_lieu_thanh_vien": st.session_state.du_lieu_thanh_vien
        }
        
        json_str = json.dumps(data_to_save, ensure_ascii=False, indent=4)
        content_b64 = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
        
        payload = {
            "message": "Cập nhật dữ liệu từ ứng dụng Quản Lý Hoa",
            "content": content_b64,
            "branch": BRANCH
        }
        
        get_sha_res = requests.get(API_URL, headers=HEADERS, timeout=5)
        if get_sha_res.status_code == 200:
            payload["sha"] = get_sha_res.json()["sha"]
            
        response = requests.put(API_URL, headers=HEADERS, json=payload, timeout=10)
        if response.status_code in [200, 201]:
            return True
        else:
            st.error(f"Lỗi lưu file: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Lỗi mạng: {str(e)}")
        return False

# Khởi tạo nạp dữ liệu
if "kho_hoa_tong" not in st.session_state or "du_lieu_thanh_vien" not in st.session_state:
    du_lieu_goc = tai_du_lieu_tu_github()
    st.session_state.kho_hoa_tong = du_lieu_goc.get("kho_hoa_tong", {})
    st.session_state.du_lieu_thanh_vien = du_lieu_goc.get("du_lieu_thanh_vien", {})

st.markdown(
"""
<div class="title-hoi">
    <span>🌸</span>
    <span>TÊN HỘI</span>
    <span>🌸</span>
</div>
""",
unsafe_allow_html=True
)


tong_hoa_hoi_vien = sum(
    len(hoa)
    for hoa in st.session_state.du_lieu_thanh_vien.values()
)

tong_hoi_vien = len(
    st.session_state.du_lieu_thanh_vien
)


components.html(
f"""
<div style="
display:flex;
justify-content:center;
align-items:center;
gap:80px;
margin-top:10px;
margin-bottom:0px;
">

    <div style="text-align:center;">
        <div style="font-size:15px;">🌸 Tổng Hoa Hội Viên</div>
        <div style="font-size:28px;font-weight:bold;">
            {tong_hoa_hoi_vien}
        </div>
    </div>

    <div style="text-align:center;">
        <div style="font-size:15px;">👥 Hội viên</div>
        <div style="font-size:28px;font-weight:bold;">
            {tong_hoi_vien}
        </div>
    </div>

</div>
""",
height=75
)

st.write("---")
danh_sach_tv = list(st.session_state.du_lieu_thanh_vien.keys())

if st.session_state.quyen == "admin":

    tab_suu_tap, tab_hoi_vien, tab_xep_hang, tab_kho, tab_thong_tin = st.tabs(
        [
            "🌺 Bộ sưu tập",
            "👥 Hội viên",
            "🏆 Xếp hạng",
            "📦 Kho",
            "ℹ️ Thông tin"
        ]
    )

else:

    tab_suu_tap, tab_xep_hang, tab_thong_tin = st.tabs(
        [
            "🌺 Bộ sưu tập",
            "🏆 Xếp hạng",
            "ℹ️ Thông tin"
        ]
    )
# ====================================================
# KHU VỰC 1: QUẢN LÝ KHO HOA TỔNG
# ====================================================
if st.session_state.quyen == "admin":    
    with tab_kho:
        st.markdown("<h3 style='font-size: 18px;'>📦 1. Kho Hoa Tổng</h3>", unsafe_allow_html=True)
        col_kho1 = st.container()
        col_kho2 = st.container()
        
        with col_kho1:

            with st.expander(
                "➕ Thêm hoa mới",
                expanded=False
            ):
                if "key_them_hoa" not in st.session_state:
                    st.session_state.key_them_hoa = 0
                ten_hoa_moi = st.text_input(
                    "Tên hoa",
                    placeholder="Nhập tên hoa...",
                    key=f"txt_ten_hoa_moi_{st.session_state.key_them_hoa}"
                )
        
        
                cap_bac_moi = st.selectbox(
                    "Cấp bậc",
                    options=[
                        "Xanh lá",
                        "Xanh dương",
                        "Tím",
                        "Cam",
                        "Đỏ"
                    ],
                    key="sl_cap_bac_moi"
                )
        
        
                file_anh = st.file_uploader(
                    "Tải ảnh",
                    type=[
                        "png",
                        "jpg",
                        "jpeg"
                    ],
                    key=f"f_file_anh_{st.session_state.key_them_hoa}"
                )
        
        
                if st.button(
                    "📥 Thêm vào Kho",
                    use_container_width=True
                ):
        
                    ten_hoa_clean = ten_hoa_moi.strip()
        
        
                    if not ten_hoa_clean:
        
                        st.error(
                            "Vui lòng nhập tên!"
                        )
        
        
                    elif ten_hoa_clean in st.session_state.kho_hoa_tong:
        
        
                        st.warning(
                            "Đã tồn tại!"
                        )
        
        
                    else:
        
        
                        du_lieu_anh = None
        
        
                        if file_anh is not None:
        
                            try:
        
                                img = Image.open(file_anh)
        
        
                                if img.mode != "RGB":
        
                                    img = img.convert("RGB")
        
        
                                img.thumbnail(
                                    (300,300)
                                )
        
        
                                buffer = io.BytesIO()
        
        
                                img.save(
                                    buffer,
                                    format="JPEG",
                                    quality=70
                                )
        
        
                                du_lieu_anh = buffer.getvalue()
        
        
                            except Exception:
        
        
                                du_lieu_anh = file_anh.read()
        
        
                        st.session_state.kho_hoa_tong[
                            ten_hoa_clean
                        ] = {
        
                            "cap":cap_bac_moi,
        
                            "anh":du_lieu_anh
        
                        }
        
        
                        if luu_du_lieu_len_github():
                            st.session_state.key_them_hoa += 1
                            st.rerun()
        
        with col_kho2:
        
            st.markdown(
                "<p style='font-size:14px;font-weight:bold;'>📋 Danh sách hoa</p>",
                unsafe_allow_html=True
            )
        
            if not st.session_state.kho_hoa_tong:
        
                st.markdown(
                    "<p style='font-size:12px;color:gray;'>Kho đang trống.</p>",
                    unsafe_allow_html=True
                )
        
            else:

        # =============================
        # TÌM KIẾM + LỌC HOA
        # =============================

                tim_hoa = st.text_input(
                    "🔍 Tìm hoa",
                    placeholder="Nhập tên hoa...",
                    key="tim_hoa_kho"
                )
            
            
                dem_cap = {
                    "Đỏ": 0,
                    "Cam": 0,
                    "Tím": 0,
                    "Xanh dương": 0,
                    "Xanh lá": 0
                }

                for ten_hoa, info in st.session_state.kho_hoa_tong.items():
                    cap = info.get("cap", "")
                    if cap in dem_cap:
                        dem_cap[cap] += 1


                tong_hoa = sum(dem_cap.values())


                loc_cap = st.radio(
                    "Lọc cấp",
                    [
                        f"🌈 Tất cả: {tong_hoa}",
                        f"🔴 Đỏ: {dem_cap['Đỏ']}",
                        f"🟠 Cam: {dem_cap['Cam']}",
                        f"🟣 Tím: {dem_cap['Tím']}",
                        f"🔵 Xanh dương: {dem_cap['Xanh dương']}",
                        f"🟢 Xanh lá: {dem_cap['Xanh lá']}",
                    ],
                    horizontal=True,
                    key="loc_cap_kho"
                )

                loc_cap = (
                    loc_cap.split(":")[0]
                    .replace("🌈 ", "")
                    .replace("🔴 ", "")
                    .replace("🟠 ", "")
                    .replace("🟣 ", "")
                    .replace("🔵 ", "")
                    .replace("🟢 ", "")
                )
            
            
                danh_sach_loc = {}
            
            
                for ten_hoa, info in st.session_state.kho_hoa_tong.items():
            
            
                    if tim_hoa.lower() not in ten_hoa.lower():
            
                        continue
            
            
                    if loc_cap != "Tất cả":
            
                        if info["cap"] != loc_cap:
            
                            continue
            
            
                    danh_sach_loc[ten_hoa] = info
            
            
            
                if not danh_sach_loc:
            
                    st.info(
                        "Không tìm thấy hoa."
                    )
            
            
                else:
            
            
                    html = '<div class="flower-grid">'
            
            
                    for ten_hoa in sap_xep_hoa(danh_sach_loc.keys()):

                        info = danh_sach_loc[ten_hoa]

                        mau_cap = {
                            "Xanh lá": "cap-xanh-la",
                            "Xanh dương": "cap-xanh-duong",
                            "Tím": "cap-tim",
                            "Cam": "cap-cam",
                            "Đỏ": "cap-do"
                        }.get(info["cap"], "cap-do")


                        link_anh = anh_html(
                            info["anh"]
                        )
            
            
                        html += f"""
                        <div class="flower-box">

                            <img class="{mau_cap}"
                                src="{link_anh}">

                            <div class="flower-name">
                                {ten_hoa}
                            </div>

                        </div>
                        """
            
            
                    html += "</div>"
            
            
                    components.html(
                        GRID_STYLE + html,
                        height=450,
                        scrolling=True
                    )
        
        
                # =============================
                # XÓA HOA RIÊNG
                # =============================
        
                st.write("")
        
                hoa_xoa = st.selectbox(
                    "🗑️ Chọn hoa cần xóa",
                    ["-- Chọn hoa --"] + list(st.session_state.kho_hoa_tong.keys()),
                    key="chon_xoa_kho"
                )
        
        
                if st.button(
                    "🗑️ Xóa hoa khỏi kho",
                    use_container_width=True
                ):
        
                    if hoa_xoa != "-- Chọn hoa --":
        
                        del st.session_state.kho_hoa_tong[hoa_xoa]
        
        
                        for tv in st.session_state.du_lieu_thanh_vien:
        
                            st.session_state.du_lieu_thanh_vien[tv] = [
        
                                h for h in st.session_state.du_lieu_thanh_vien[tv]
        
                                if h != hoa_xoa
        
                            ]
        
        
                        if luu_du_lieu_len_github():
        
                            st.rerun()
        
        st.write("---")

# ====================================================
# KHU VỰC 2: CẤU HÌNH THÀNH VIÊN VÀ CẤP PHÁT
# ====================================================
if st.session_state.quyen == "admin":    
    with tab_hoi_vien:

        st.markdown(
            "<h3>👥 2. Hội Viên & Cấp Phát</h3>",
            unsafe_allow_html=True
        )

        col_tv1, col_tv2 = st.columns(2)


        # =====================
        # BÊN TRÁI: HỘI VIÊN
        # =====================
        with col_tv1:

            with st.expander(
                "➕ Quản lý hội viên",
                expanded=False
            ):
                if "key_them_tv" not in st.session_state:
                    st.session_state.key_them_tv = 0
                ten_tv_moi = st.text_input(
                    "➕ Nhập hội viên mới",
                    placeholder="Nhập tên...",
                    key=f"them_thanh_vien_{st.session_state.key_them_tv}"
                )
                if st.session_state.quyen == "admin":
                    if st.button(
                        "➕ Thêm hội viên",
                        use_container_width=True
                    ):
                        ten_tv_clean = ten_tv_moi.strip()

                        if ten_tv_clean:
                            st.session_state.du_lieu_thanh_vien[ten_tv_clean] = []

                            if luu_du_lieu_len_github():
                                st.session_state.key_them_tv += 1
                                st.rerun()

                tv_xoa = st.selectbox(
                    "🗑 Xóa hội viên",
                    ["-- Chọn --"] + list(st.session_state.du_lieu_thanh_vien.keys()),
                    key="xoa_tv"
                )

                if st.button(
                    "❌ Xóa",
                    use_container_width=True
                ):
                    if tv_xoa != "-- Chọn --":
                        del st.session_state.du_lieu_thanh_vien[tv_xoa]

                        if luu_du_lieu_len_github():
                            st.rerun()


        # =====================
        # BÊN PHẢI: CẤP HOA
        # =====================
        with col_tv2:

            st.markdown("## 🪷 Thêm Hoa Cho Hội Viên")

            danh_sach_tv = list(
                st.session_state.du_lieu_thanh_vien.keys()
            )

            tv_chon = st.selectbox(
                "👤 Chọn hội viên",
                danh_sach_tv,
                key="cap_tv"
            )

            # lấy hoa hội viên đang có
            hoa_da_co = st.session_state.du_lieu_thanh_vien.get(
                tv_chon,
                []
            )

            # lọc hoa chưa có
            hoa_chua_co = [
                hoa
                for hoa in st.session_state.kho_hoa_tong.keys()
                if hoa not in hoa_da_co
            ]


            if len(hoa_chua_co) > 0:

                hoa_chon = st.selectbox(
                    "🌸 Chọn hoa",
                    hoa_chua_co,
                    key="cap_hoa"
                )

                if st.button(
                    "🪷 Thêm Hoa",
                    use_container_width=True
                ):

                    st.session_state.du_lieu_thanh_vien[tv_chon].append(
                        hoa_chon
                    )

                    if luu_du_lieu_len_github():
                        st.rerun()

            else:

                st.info("✅ Hội viên đã có tất cả hoa")
with tab_xep_hang:

    st.markdown(
        """
    <div style="text-align:center;white-space:nowrap;margin-bottom:15px;">
    <div style="font-size:40px;line-height:1;">🏆</div>
    <div style="font-size:22px;font-weight:700;">Bảng Xếp Hạng Hội Viên</div>
    </div>
        """,
        unsafe_allow_html=True
    )

    bang_xep_hang = []

    for ten_tv, ds_hoa in st.session_state.du_lieu_thanh_vien.items():

        dem = {
            "Đỏ":0,
            "Cam":0,
            "Tím":0,
            "Xanh dương":0,
            "Xanh lá":0
        }

        for hoa in ds_hoa:
            info = st.session_state.kho_hoa_tong.get(hoa,{})
            cap = info.get("cap","")

            if cap in dem:
                dem[cap] += 1


        bang_xep_hang.append({
            "ten": ten_tv,
            "tong": len(ds_hoa),
            "cap": dem
        })


    bang_xep_hang = sorted(
        bang_xep_hang,
        key=lambda x:x["tong"],
        reverse=True
    )


    hang_xep = [
        bang_xep_hang[:1]   # top 1
    ]

    for i in range(1, len(bang_xep_hang), 2):
        hang_xep.append(
            bang_xep_hang[i:i+2]
        )


    html = ""
    so_top = 1


    for hang in hang_xep:

        cot = len(hang)

        html += f"""<div style="
display:grid;
grid-template-columns:repeat({cot},150px);
justify-content:center;
gap:12px;
margin-bottom:6px;
">"""


        for tv in hang:

            if so_top == 1:
                cup = "🥇"
                vien = "#ffd700"
                do_day_vien = "5px"
            elif so_top == 2:
                cup = "🥈"
                vien = "#c0c0c0"
                do_day_vien = "4px"
            elif so_top == 3:
                cup = "🥉"
                vien = "#cd7f32"
                do_day_vien = "4px"
            else:
                cup = f"#{so_top}"
                vien = "white"
                do_day_vien = "2px"


            html += f"""<div style="
border:{do_day_vien} solid {vien};
border-radius:8px;
width:140px;
height:140px;
background:rgba(255,255,255,0.85);
text-align:center;
font-size:14px;
line-height:1.15;
padding:3px;
overflow:hidden;
">

<div style="font-size:12px">{cup}</div>

<b>{tv['ten']}</b><br>

🌺 {tv['tong']}<br>

🔴{tv['cap']['Đỏ']}
🟠{tv['cap']['Cam']}<br>

🟣{tv['cap']['Tím']}
🔵{tv['cap']['Xanh dương']}<br>

🟢{tv['cap']['Xanh lá']}

</div>"""

            so_top += 1


        html += "</div>"


    st.markdown(
        html,
        unsafe_allow_html=True
    )
# ====================================================
# KHU VỰC 3: BỘ SƯU TẬP
# ====================================================
with tab_suu_tap:
    st.markdown("<h3 style='font-size: 18px;'>🔍 3. Bộ Sưu Tập</h3>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(
        [
            "👤 Cá Nhân",
            "👥 Toàn Hội",
            "🔎 Tra cứu"
        ]
    )
    
    with tab1:
    
        tv_xem = st.selectbox(
            "Xem kho của:",
            options=["-- Chọn --"] + danh_sach_tv,
            key="selectTV"
        )
    
    
        if tv_xem != "-- Chọn --" and tv_xem in st.session_state.du_lieu_thanh_vien:
    
    
            kho_hoa_tv = st.session_state.du_lieu_thanh_vien[tv_xem]
    
    
            if not kho_hoa_tv:
    
                st.markdown(
                    "<p style='font-size:13px;'>Trống.</p>",
                    unsafe_allow_html=True
                )
    
    
            else:
                dem_cap = {
                    "Đỏ": 0,
                    "Cam": 0,
                    "Tím": 0,
                    "Xanh dương": 0,
                    "Xanh lá": 0
                }

                for ten in kho_hoa_tv:
                    info = st.session_state.kho_hoa_tong.get(ten, {})
                    cap = info.get("cap", "")

                    if cap in dem_cap:
                        dem_cap[cap] += 1

                tong_hoa = sum(dem_cap.values())
                chon_cap = st.radio(
                    "Lọc cấp:",
                    [
                        f"🌈 Tất cả: {tong_hoa}",
                        f"🔴 Đỏ: {dem_cap['Đỏ']}",
                        f"🟠 Cam: {dem_cap['Cam']}",
                        f"🟣 Tím: {dem_cap['Tím']}",
                        f"🔵 Xanh dương: {dem_cap['Xanh dương']}",
                        f"🟢 Xanh lá: {dem_cap['Xanh lá']}"
                    ],
                    horizontal=True
                )

                if "Đỏ" in chon_cap:
                    loc_cap = "Đỏ"
                elif "Cam" in chon_cap:
                    loc_cap = "Cam"
                elif "Tím" in chon_cap:
                    loc_cap = "Tím"
                elif "Xanh dương" in chon_cap:
                    loc_cap = "Xanh dương"
                elif "Xanh lá" in chon_cap:
                    loc_cap = "Xanh lá"
                else:
                    loc_cap = "Tất cả"
    
    
                html = '<div class="flower-grid">'
    
    
                for ten_hoa in sap_xep_hoa(kho_hoa_tv):
                    info = st.session_state.kho_hoa_tong.get(
                        ten_hoa,
                        {"anh": None}
                    )

                    if "Đỏ" in chon_cap and info.get("cap") != "Đỏ":
                        continue

                    if "Cam" in chon_cap and info.get("cap") != "Cam":
                        continue

                    if "Tím" in chon_cap and info.get("cap") != "Tím":
                        continue

                    if "Xanh dương" in chon_cap and info.get("cap") != "Xanh dương":
                        continue

                    if "Xanh lá" in chon_cap and info.get("cap") != "Xanh lá":
                        continue
    
    
                    info = st.session_state.kho_hoa_tong.get(
                        ten_hoa,
                        {"anh": None}
                    )
    
    
                    link_anh = anh_html(info["anh"])
                    cap = info.get("cap", "")

                    if cap == "Đỏ":
                        mau = "#ef4444"

                    elif cap == "Tím":
                        mau = "#c084fc"

                    elif cap == "Xanh lá":
                        mau = "#22c55e"

                    elif cap == "Xanh dương":
                        mau = "#38bdf8"

                    elif cap == "Cam":
                        mau = "#f59e0b"

                    else:
                        mau = "#d6a83d"
                        
    
                    html += f"""
                    <div class="flower-box">
                        <img src="{link_anh}" style="border:5px solid {mau};">
                        <div class="flower-name">
                            {ten_hoa}
                        </div>
                    </div>
                    """
    
    
                html += "</div>"
    
    
                components.html(
        GRID_STYLE + html,
        height=450,
        scrolling=True
    )
    
    
                st.write("")
    
                if st.session_state.quyen == "admin":
                    hoa_thu_hoi = st.selectbox(
                        "↩️ Chọn hoa cần thu hồi",
                        ["-- Chọn hoa --"] + kho_hoa_tv,
                        key="chon_thu_hoi"
                    )
    
                if st.session_state.quyen == "admin":
                    if st.button(
                        "↩️ Thu hồi hoa",
                        use_container_width=True
                    ):
        
        
                        if hoa_thu_hoi != "-- Chọn hoa --":
        
        
                            st.session_state.du_lieu_thanh_vien[tv_xem].remove(
                                hoa_thu_hoi
                            )
        
        
                            if luu_du_lieu_len_github():
        
        
                                st.rerun()
    
    with tab2:

        # ==============================
        # ĐẾM CẤP HOA
        # ==============================
        dem_cap = {
            "Đỏ": 0,
            "Cam": 0,
            "Tím": 0,
            "Xanh dương": 0,
            "Xanh lá": 0
        }


        for ten_hoa, info in st.session_state.kho_hoa_tong.items():

            owners = [
                tv
                for tv, hoa_list
                in st.session_state.du_lieu_thanh_vien.items()
                if ten_hoa in hoa_list
            ]

            if owners:
                cap = info.get("cap", "")

                if cap in dem_cap:
                    dem_cap[cap] += 1


        tong_hoa = sum(dem_cap.values())


        chon_cap = st.radio(
            "Lọc cấp:",
            [
                f"🌈 Tất cả: {tong_hoa}",
                f"🔴 Đỏ: {dem_cap['Đỏ']}",
                f"🟠 Cam: {dem_cap['Cam']}",
                f"🟣 Tím: {dem_cap['Tím']}",
                f"🔵 Xanh dương: {dem_cap['Xanh dương']}",
                f"🟢 Xanh lá: {dem_cap['Xanh lá']}"
            ],
            horizontal=True,
            key="loc_cap_toan_hoi"
        )


        if not st.session_state.kho_hoa_tong:

            st.markdown(
                "<p style='font-size:13px;'>Chưa có hoa nào.</p>",
                unsafe_allow_html=True
            )


        else:

            html = '<div class="flower-grid">'


            for ten_hoa in sap_xep_hoa(st.session_state.kho_hoa_tong.keys()):

                info = st.session_state.kho_hoa_tong[ten_hoa]

                cap = info.get("cap", "")


                loc = chon_cap.split(":")[0]

                loc = (
                    loc.replace("🌈 ", "")
                    .replace("🔴 ", "")
                    .replace("🟠 ", "")
                    .replace("🟣 ", "")
                    .replace("🔵 ", "")
                    .replace("🟢 ", "")
                )


                if loc != "Tất cả" and cap != loc:
                    continue


                owners = [
                    tv
                    for tv, hoa_list
                    in st.session_state.du_lieu_thanh_vien.items()
                    if ten_hoa in hoa_list
                ]


                if owners:


                    link_anh = anh_html(info["anh"])


                    if cap == "Đỏ":
                        mau = "#ef4444"

                    elif cap == "Tím":
                        mau = "#c084fc"

                    elif cap == "Xanh lá":
                        mau = "#22c55e"

                    elif cap == "Xanh dương":
                        mau = "#38bdf8"

                    elif cap == "Cam":
                        mau = "#f59e0b"

                    else:
                        mau = "#d6a83d"


                    html += f"""
                    <div class="flower-box">
                        <img src="{link_anh}" 
                        style="border:5px solid {mau};">

                        <div class="flower-name">
                            {ten_hoa}
                        </div>
                    </div>
                    """


            html += "</div>"


            components.html(
                GRID_STYLE + html,
                height=450,
                scrolling=True
            )

    with tab3:

        st.markdown("## 🔍 Tra cứu hoa")

        tim_so_huu = st.text_input(
            "Nhập tên hoa",
            key="tim_so_huu_tra_cuu"
        )

        if tim_so_huu:

            ds_tim = []

            for ten_hoa in st.session_state.kho_hoa_tong.keys():

                if tim_so_huu.lower() in ten_hoa.lower():
                    ds_tim.append(ten_hoa)


            if ds_tim:

                hoa_chon = st.selectbox(
                    f"🌺 Tìm thấy {len(ds_tim)} hoa",
                    ds_tim,
                    key="chon_hoa_tra_cuu"
                )

                ds_co = []

                for tv, hoa_list in st.session_state.du_lieu_thanh_vien.items():

                    if hoa_chon in hoa_list:
                        ds_co.append(tv)


                st.success(
                    f"🌺 {hoa_chon} - Có {len(ds_co)} thành viên sở hữu"
                )

                for tv in ds_co:
                    st.markdown(
                        f"""
                        <p style="
                            color:#000000 !important;
                            font-weight:800 !important;
                            font-size:16px !important;
                            margin:6px 0;
                        ">
                        👤 {tv}
                        </p>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.warning("❌ Không tìm thấy hoa")
with tab_thong_tin:

    if st.session_state.quyen != "admin":
        du_lieu_tai_ve = {
            "tai_khoan": st.session_state.user_hien_tai,
            "du_lieu_hoi": st.session_state.du_lieu_thanh_vien
        }
        st.download_button(
            "💾 Tải dữ liệu hội về máy",
            data=json.dumps(du_lieu_tai_ve, ensure_ascii=False, indent=4),
            file_name="du_lieu_hoi_cua_toi.json",
            mime="application/json",
            use_container_width=True
        )

    st.markdown(
        """
        <div style="
        text-align:center;
        padding:20px;
        font-size:16px;
        ">


        <p>
        👑 Sáng tạo bởi: <b>Đức Tài</b><br><br>

        📱 Điện thoại: <b>0373.30.30.55</b><br><br>

        🌺 Phiên bản: <b>1.0</b><br>

        💻 Ứng dụng quản lý hoa hội
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )
