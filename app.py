import streamlit as st
from PIL import Image
import io

# --- 設定網頁標題與排版 ---
st.set_page_config(page_title="圖片正方形產生器", page_icon="🖼️")
st.title("🖼️ 簡單圖片整圖工具")
st.markdown("""
此工具會將圖片調整為 **正方形**，並自動補上白邊 (20px)，
若超過 1000px 則自動縮小，完全不會裁切到原圖。
""")

# --- 核心處理函式 ---
def process_image(image, padding=20, max_size=1000):
    # 1. 取得原圖尺寸
    original_w, original_h = image.size
    
    # 2. 計算新畫布尺寸：長邊 + 雙倍 padding (上下或左右各20)
    new_side = max(original_w, original_h) + (padding * 2)
    
    # 3. 建立白色畫布
    canvas = Image.new("RGB", (new_side, new_side), (255, 255, 255))
    
    # 4. 計算置中位置
    x_offset = (new_side - original_w) // 2
    y_offset = (new_side - original_h) // 2
    
    # 5. 貼上圖片 (處理透明度)
    if image.mode in ('RGBA', 'LA'):
        canvas.paste(image, (x_offset, y_offset), image)
    else:
        canvas.paste(image, (x_offset, y_offset))
        
    # 6. 檢查是否需要縮小
    if new_side > max_size:
        canvas = canvas.resize((max_size, max_size), Image.Resampling.LANCZOS)
        
    return canvas

# --- 側邊欄或主要區塊 ---
uploaded_file = st.file_uploader("請上傳圖片 (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # 開啟上傳的圖片
        image = Image.open(uploaded_file)
        
        # 進行處理
        result_image = process_image(image)
        
        # --- 顯示結果 (使用兩欄排版) ---
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("原始圖片")
            st.image(image, use_container_width=True)
            st.caption(f"尺寸: {image.size[0]} x {image.size[1]}")

        with col2:
            st.subheader("處理結果")
            st.image(result_image, use_container_width=True)
            st.caption(f"尺寸: {result_image.size[0]} x {result_image.size[1]}")

        # --- 下載按鈕 ---
        # 將圖片轉為 Byte 串流以便下載
        buf = io.BytesIO()
        result_image.save(buf, format="JPEG", quality=95)
        byte_im = buf.getvalue()

        st.download_button(
            label="⬇️ 下載處理好的圖片",
            data=byte_im,
            file_name="square_fixed.jpg",
            mime="image/jpeg",
            use_container_width=True
        )

    except Exception as e:
        st.error(f"發生錯誤: {e}")