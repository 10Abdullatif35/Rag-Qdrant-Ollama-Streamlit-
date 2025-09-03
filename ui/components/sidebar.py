import streamlit as st

def sidebar(category_options: list[str]) -> tuple[str | None, int]:
    """Sol kenar çubuğunu çizer ve seçilen değerleri döndürür."""
    with st.sidebar:
        st.title("⚙️ Filtreler")

        category = st.selectbox(
            "Kategori",
            category_options,
            index=0,  # “Tümü” öntanımlı
        )

        top_k = st.slider(
            "Kaç bağlam getirilsin? (top_k)",
            min_value=1,
            max_value=10,
            value=5,
            step=1,
        )

    # “Tümü” seçildiyse None olarak dön
    return (None if category == "Tümü" else category), top_k
