import urllib.parse
import streamlit as st
from PIL import Image

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="متجر الأثاث والديكور",
    page_icon="🛋️",
    layout="centered"
)

# دعم الاتجاه من اليمين إلى اليسار للغة العربية وتنسيق البطاقات
st.markdown("""
<style>
    div[data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
    }
    .product-card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #e0e0e0;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .product-title {
        font-size: 20px;
        font-weight: bold;
        margin: 10px 0 5px 0;
        color: #333;
    }
    .product-price {
        font-size: 22px;
        color: #2e7d32;
        font-weight: bold;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# إدارة حالة المنتج المحدد
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

st.title("🛋️ متجر الأثاث المنزلي")
st.write("مرحباً بك! اختر المنتج الذي ترغب في شرائه لإتمام الطلب:")

# عرض المنتجات في عمودين
col1, col2 = st.columns(2)

# --- المنتج الأول: الأثاث (image_0.png) ---
with col1:
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    try:
        # تحميل وعرض صورة الأثاث
        img_furniture = Image.open("image_0.png")
        st.image(img_furniture, use_container_width=True)
    except FileNotFoundError:
        st.warning("⚠️ لم يتم العثور على صورة الأثاث (image_0.png)")
    
    st.markdown('<div class="product-title">طقم أثاث منزلي</div>', unsafe_allow_html=True)
    st.markdown('<div class="product-price">65,000 دج</div>', unsafe_allow_html=True)
    
    if st.button("طلب الأثاث 🛋️", use_container_width=True, key="btn_furniture"):
        st.session_state.selected_product = {"name": "طقم أثاث فاخر", "price": "65,000 دج"}
    st.markdown('</div>', unsafe_allow_html=True)

# --- المنتج الثاني: المرآة (image_1.png) ---
with col2:
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    try:
        # تحميل وعرض صورة المرآة
        img_mirror = Image.open("image_1.png")
        st.image(img_mirror, use_container_width=True)
    except FileNotFoundError:
        st.warning("⚠️ لم يتم العثور على صورة المرآة (image_1.png)")
        
    st.markdown('<div class="product-title">مرآة ديكور جدارية</div>', unsafe_allow_html=True)
    st.markdown('<div class="product-price">3,000 دج</div>', unsafe_allow_html=True)
    
    if st.button("طلب المرآة 🪞", use_container_width=True, key="btn_mirror"):
        st.session_state.selected_product = {"name": "مرآة ديكور عصرية", "price": "3,000 دج"}
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# نافذة نموذج الطلب عند اختيار منتج
if st.session_state.selected_product:
    prod = st.session_state.selected_product
    st.subheader(f"📝 استمارة الطلب: {prod['name']} ({prod['price']})")

    with st.form("order_form"):
        col_name, col_surname = st.columns(2)
        with col_name:
            first_name = st.text_input("الاسم *")
        with col_surname:
            last_name = st.text_input("اللقب *")

        phone = st.text_input("رقم الهاتف *")
        email = st.text_input("البريد الإلكتروني")
        address = st.text_area("مكان السكن / العنوان بالتفصيل *")

        submit_button = st.form_submit_button("إرسال الطلب عبر واتساب 📲", use_container_width=True)

    if submit_button:
        if not first_name or not last_name or not phone or not address:
            st.error("يرجى ملء جميع الحقول المطلوبة (الاسم، اللقب، الهاتف، ومكان السكن).")
        else:
            # تجهيز نص الرسالة للواتساب
            full_name = f"{first_name.strip()} {last_name.strip()}"
            message = (
                f"طلب جديد من الزبون: {full_name}\n"
                f"-----------------------------\n"
                f"📦 المنتج: {prod['name']}\n"
                f"💰 السعر: {prod['price']}\n"
                f"👤 الاسم واللقب: {full_name}\n"
                f"📞 رقم الهاتف: {phone}\n"
                f"📧 البريد الإلكتروني: {email if email else 'غير محدد'}\n"
                f"📍 مكان السكن: {address}\n"
            )

            # تحويل النص إلى ترميز مناسب لروابط الويب
            encoded_message = urllib.parse.quote(message)
            
            # رقم الواتساب بالصيغة الدولية الجزائرية (213)
            whatsapp_number = "213784803429"
            whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"

            st.success("تم تجهيز طلبك بنجاح! اضغط على الزر أدناه لإرساله مباشرة عبر واتساب:")
            st.markdown(
                f'<a href="{whatsapp_url}" target="_blank" style="'
                f'display: inline-block; padding: 12px 24px; background-color: #25D366; '
                f'color: white; text-align: center; text-decoration: none; font-size: 18px; '
                f'border-radius: 8px; font-weight: bold; width: 100%;">'
                f'فتح واتساب وإرسال الطلب 💬</a>',
                unsafe_allow_html=True
            )