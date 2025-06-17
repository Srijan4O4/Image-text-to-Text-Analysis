import streamlit as st
from analyze import analyze_product

st.title("Product Authenticity Checker")

# File + text inputs
uploaded = st.file_uploader("Upload product image", type=["png", "jpg", "jpeg"])
name     = st.text_input("Product name")
desc     = st.text_area("Description / Listing text")

# New: temperature slider
temperature = st.slider(
    "Model temperature (controls randomness)",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.05,
    help="Lower = more deterministic, Higher = more creative"
)

if st.button("Analyze"):
    if not uploaded or not name or not desc:
        st.warning("Please provide image, name, and description.")
    else:
        # save uploaded to disk
        temp_path = f"temp_{uploaded.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded.getvalue())

        try:
            # pass the temperature through to your API wrapper
            verdict = analyze_product(
                image_path=temp_path,
                product_name=name,
                description=desc
            )
            st.success(f"Result: **{verdict}** (temp={temperature})")
        except Exception as e:
            st.error(f"API error: {e}")
