import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(page_title="VibeVault", page_icon="🎬", layout="wide")

# --- Session State ---
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "badge" not in st.session_state:
    st.session_state.badge = None

def headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def api_get(path, params=None):
    try:
        r = requests.get(f"{API}{path}", headers=headers(), params=params)
        return r.json() if r.ok else None
    except:
        return None

def api_post(path, data):
    try:
        r = requests.post(f"{API}{path}", headers=headers(), json=data)
        return r.json() if r.ok else None
    except:
        return None

# --- Auth Pages ---
def page_login():
    st.title("🎬 VibeVault")
    st.subheader("Platform Eksplorasi & Koleksi Entertainment Pribadi")
    st.divider()
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            if submitted:
                r = requests.post(f"{API}/auth/login", json={"username": username, "password": password})
                if r.ok:
                    data = r.json()
                    st.session_state.token = data["token"]
                    st.session_state.username = data["username"]
                    st.session_state.badge = data["badge"]
                    st.success("Login berhasil!")
                    st.rerun()
                else:
                    st.error("Username atau password salah!")

    with tab2:
        with st.form("register_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            bio = st.text_input("Bio singkat (opsional)")
            st.markdown("**Kuis Selera** — Pilih preferensimu:")
            fav_type = st.selectbox("Kamu lebih suka?", ["film", "musik"])
            fav_mood = st.selectbox("Mood favoritmu?", ["Epic", "Dark", "Dreamy", "Chill", "Energetic", "Melancholic"])
            submitted = st.form_submit_button("Register", use_container_width=True)
            if submitted:
                r = requests.post(f"{API}/auth/register", json={
                    "username": username, "password": password,
                    "bio": bio, "fav_type": fav_type, "fav_mood": fav_mood
                })
                if r.ok:
                    badge = r.json().get("badge")
                    st.success(f"Registrasi berhasil! Badge kamu: 🏅 {badge}")
                else:
                    st.error("Username sudah dipakai!")

# --- Main App ---
def page_discovery():
    st.header("🔍 Discovery")
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_type = st.selectbox("Tipe", ["Semua", "film", "musik"])
    with col2:
        filter_mood = st.selectbox("Mood", ["Semua", "Epic", "Dark", "Dreamy", "Chill", "Energetic", "Melancholic"])
    with col3:
        st.write("")
        st.write("")
        if st.button("🎲 Surprise Me!", use_container_width=True):
            t = None if filter_type == "Semua" else filter_type
            item = api_get("/items/surprise", {"type": t} if t else None)
            if item:
                st.info(f"**{item['title']}** ({item['type'].upper()}) — {item['mood']} | {item['genre']}\n\n{item['description']}")

    params = {}
    if filter_type != "Semua": params["type"] = filter_type
    if filter_mood != "Semua": params["mood"] = filter_mood
    items = api_get("/items", params) or []

    if not items:
        st.warning("Tidak ada item ditemukan.")
        return

    cols = st.columns(2)
    for i, item in enumerate(items):
        with cols[i % 2]:
            with st.container(border=True):
                emoji = "🎬" if item["type"] == "film" else "🎵"
                st.markdown(f"### {emoji} {item['title']}")
                st.caption(f"{item['genre']} • {item['mood']}")
                st.write(item["description"])
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("💾 Simpan", key=f"save_{item['id']}"):
                        api_post("/collection/", {"item_id": item["id"], "status": "saved"})
                        st.success("Disimpan!")
                with col_b:
                    if st.button("📌 Pin", key=f"pin_{item['id']}"):
                        api_post("/collection/", {"item_id": item["id"], "status": "pinned"})
                        st.success("Di-pin ke Moodboard!")

def page_collection():
    st.header("📚 Koleksi Saya")
    items = api_get("/collection/") or []
    if not items:
        st.info("Koleksi kamu masih kosong. Tambahkan dari Discovery!")
        return
    for item in items:
        with st.container(border=True):
            emoji = "🎬" if item["type"] == "film" else "🎵"
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{emoji} {item['title']}** — {item['genre']} • {item['mood']}")
                st.caption(f"Status: {'📌 Pinned' if item['status'] == 'pinned' else '💾 Saved'}")
            with col2:
                if st.button("🗑️ Hapus", key=f"del_{item['id']}"):
                    requests.delete(f"{API}/collection/{item['id']}", headers=headers())
                    st.rerun()

def page_moodboard():
    st.header("🎨 Personal Moodboard")
    mb = api_get("/moodboard/") or {}

    with st.form("moodboard_form"):
        theme_color = st.color_picker("Tema Warna", mb.get("theme_color", "#6C63FF"))
        quote = st.text_area("Quote / Caption", mb.get("quote", ""), placeholder="Tulis quote favoritmu...")
        is_public = st.toggle("Publik", mb.get("is_public", False))
        if st.form_submit_button("💾 Simpan Moodboard", use_container_width=True):
            api_post("/moodboard/", {"theme_color": theme_color, "quote": quote, "is_public": is_public})
            st.success("Moodboard disimpan!")
            st.rerun()

    st.divider()
    st.markdown("### Preview Moodboard")
    pinned = mb.get("pinned_items", [])
    color = mb.get("theme_color", "#6C63FF")
    quote_text = mb.get("quote", "")

    st.markdown(f"""
    <div style='background:{color}22; border-left: 5px solid {color};
                padding: 20px; border-radius: 12px; margin-bottom: 16px;'>
        <h3 style='color:{color}; margin:0'>🎨 {st.session_state.username}'s VibeVault</h3>
        <p style='font-style:italic; color:#555; margin-top:8px'>"{quote_text}"</p>
    </div>
    """, unsafe_allow_html=True)

    if pinned:
        st.markdown("**📌 Pinned Items:**")
        cols = st.columns(min(len(pinned), 3))
        for i, item in enumerate(pinned):
            with cols[i % 3]:
                emoji = "🎬" if item["type"] == "film" else "🎵"
                st.markdown(f"""
                <div style='background:{color}33; padding:12px; border-radius:8px; text-align:center'>
                    <b>{emoji} {item['title']}</b><br>
                    <small>{item['mood']}</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.caption("Belum ada item yang di-pin. Pin item dari Discovery!")

def page_profile():
    st.header("👤 Profil")
    with st.container(border=True):
        st.markdown(f"### 👋 {st.session_state.username}")
        st.markdown(f"🏅 **Badge:** {st.session_state.badge}")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.token = None
        st.session_state.username = None
        st.session_state.badge = None
        st.rerun()

# --- Router ---
if not st.session_state.token:
    page_login()
else:
    with st.sidebar:
        st.markdown(f"### 🎬 VibeVault")
        st.caption(f"👋 {st.session_state.username} • 🏅 {st.session_state.badge}")
        st.divider()
        page = st.radio("Navigasi", ["🔍 Discovery", "📚 Koleksi", "🎨 Moodboard", "👤 Profil"])

    if page == "🔍 Discovery":
        page_discovery()
    elif page == "📚 Koleksi":
        page_collection()
    elif page == "🎨 Moodboard":
        page_moodboard()
    elif page == "👤 Profil":
        page_profile()
