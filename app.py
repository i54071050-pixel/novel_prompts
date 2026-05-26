import streamlit as st

st.set_page_config(page_title="小說設定 Prompt 產生器", page_icon="✍️", layout="centered")
st.title("✍️ 小說設定 Prompt 產生器")
st.write("填寫以下設定，快速生成小說提示詞！")
st.divider()

# --- 第一部分：世界觀設定 ---
st.header("🌍 世界觀設定")
col1, col2 = st.columns(2)
with col1:
    background = st.selectbox("故事背景", ["現代都市", "古代仙俠", "科幻未來", "賽博朋克", "末日廢土", "其他（自訂）"])
    # ✨ 新增：選「其他」才顯示輸入框
    if background == "其他（自訂）":
        background = st.text_input("請輸入自訂背景", placeholder="例如：蒸汽龐克維多利亞時代", key="bg_custom")

with col2:
    category = st.selectbox("故事類別", ["戀愛言情", "熱血冒險", "奇幻魔法", "懸疑推理", "古代宮廷", "其他（自訂）"])
    # ✨ 新增：選「其他」才顯示輸入框
    if category == "其他（自訂）":
        category = st.text_input("請輸入自訂類別", placeholder="例如：克蘇魯恐怖", key="cat_custom")

st.divider()

# --- 第二部分：角色設定 ---
st.header("👥 角色設定")

PERSONALITY_OPTIONS = ["傲嬌", "腹黑", "溫柔高冷", "毒舌", "病嬌", "陽光健氣", "天然呆", "深沉內斂", "智商在線"]

# ✨ 新增：用 session_state 儲存角色清單
if "characters" not in st.session_state:
    st.session_state.characters = [
        {"name": "主角1", "appearance": "", "tags": [], "custom": ""},
        {"name": "主角2", "appearance": "", "tags": [], "custom": ""},
    ]

# 新增 / 移除角色按鈕
col_add, col_del = st.columns([1, 1])
with col_add:
    if st.button("➕ 新增角色"):
        n = len(st.session_state.characters) + 1
        st.session_state.characters.append(
            {"name": f"角色 {n}", "appearance": "", "tags": [], "custom": ""}
        )
with col_del:
    if st.button("➖ 移除最後一位") and len(st.session_state.characters) > 1:
        st.session_state.characters.pop()

# ✨ 動態產生 tabs
tab_labels = [
    f"{char['name'] if char['name'] else f'角色 {i+1}'}"
    for i, char in enumerate(st.session_state.characters)
]
tabs = st.tabs(tab_labels)

for i, (tab, char) in enumerate(zip(tabs, st.session_state.characters)):
    with tab:
        st.session_state.characters[i]["name"] = st.text_input(
            "名字或稱呼", value=char["name"], key=f"c{i}_name"
        )
        st.session_state.characters[i]["appearance"] = st.text_input(
            "外貌描述", value=char["appearance"],
            placeholder="例如：白髮、藍眼、黑色風衣", key=f"c{i}_app"
        )
        st.session_state.characters[i]["tags"] = st.multiselect(
            "性格標籤", PERSONALITY_OPTIONS,
            default=char["tags"], key=f"c{i}_tags"
        )
        st.session_state.characters[i]["custom"] = st.text_input(
            "自訂性格補充", value=char["custom"],
            placeholder="例如：外冷內熱", key=f"c{i}_cust"
        )

st.divider()

# --- 第三部分：互動與補充 ---
st.header("互動與其他")
interaction = st.text_input("主角間的互動模式", placeholder="例如：歡喜冤家、相愛相殺、單戀")
other_setting = st.text_area("其他補充設定", placeholder="例如：金手指系統、前世記憶、特殊世界觀")
st.divider()

# --- 第四部分：自動組裝 Prompt ---
# 組裝每位角色的文字
characters_text = ""
for i, char in enumerate(st.session_state.characters):
    personality_list = list(char["tags"])
    if char["custom"]:
        personality_list.append(char["custom"])
    personality_str = "、".join(personality_list) if personality_list else "未設定"

    characters_text += (
        f"{i+1}. {char['name'] if char['name'] else f'角色{i+1}'}：\n"
        f"   - 外貌：{char['appearance'] if char['appearance'] else '未設定'}\n"
        f"   - 性格：{personality_str}\n"
    )

prompt_template = (
    f"請幫我逐章節撰寫小說。設定如下：\n"
    f"【世界觀】\n"
    f"- 故事背景：{background if background else '未設定'}\n"
    f"- 故事類別：{category if category else '未設定'}\n\n"
    f"【角色設定】\n"
    f"{characters_text}\n"
    f"【關係與其他】\n"
    f"- 互動模式：{interaction if interaction else '未設定'}\n"
    f"- 其他設定：{other_setting if other_setting else '無'}\n\n"
    f"請根據以上設定，提供引人入勝的故事開頭與主要角色關係發展建議。逐章節撰寫內容，在每一章節最後詢問使用者是否有需要修正的語句和情節，並提供兩個可能的發展建議提供使用者選擇。\n\n"
    f"【寫作要求】\n"
    f"1. 請用生動的動作與對話展現出角色的專屬性格，不要流於平鋪直敘。\n"
    f"2. 開頭要帶有懸念，迅速抓住讀者的注意力。"
)

st.subheader("📋 將 Prompt 直接複製到 AI 吧")
st.code(prompt_template, language="text")
