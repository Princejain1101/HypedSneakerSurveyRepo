import streamlit as st

def favorite_brand_api():
    if "favorite_brand" not in st.session_state:
        st.session_state["favorite_brand"] = None
    if "second_favorite_brand" not in st.session_state:
        st.session_state["second_favorite_brand"] = None
    if "final_favorite_brand_list" not in st.session_state:
        st.session_state["final_favorite_brand_list"] = None
    brand_list = ["Adidas", "Hoka", "Soloman", "New Balance", "On", "Converse", "Reebok", "Nike", "Yeezy", "Vans",
                  "Asics", "None of the above"]
    if st.session_state["favorite_brand"] is None:
        with st.form("favorite brand"):
            st.write(f"Please take a bit more time to answer questions about your preferences for sneakers")
            brand = st.radio("What is your favorite brand of sneakers?", brand_list)
            if "None of the above" in brand:
                user_brand = st.text_input("Please enter your favorite brand")
                submit = st.form_submit_button("Submit")
                if submit and user_brand:
                    st.session_state["favorite_brand"] = user_brand
                    st.rerun()
            else:
                submit = st.form_submit_button("Submit")
                if submit and brand:
                    st.session_state["favorite_brand"] = brand
                    st.rerun()
    if st.session_state["favorite_brand"] and st.session_state["second_favorite_brand"] is None:
        with st.form("Exclusive check"):
            exclusive = st.radio(f"Do you exclusively buy {st.session_state["favorite_brand"]} brand of sneakers?", ("Yes", "No"), index=None)
            submit = st.form_submit_button("Submit")
            if exclusive and submit:
                if "Yes" in exclusive:
                    st.write("favorite brand ", st.session_state["favorite_brand"])
                    return st.session_state["favorite_brand"]
                else:
                    st.session_state["second_favorite_brand"] = True
                    st.rerun()
    if st.session_state["second_favorite_brand"] is not None:
        if st.session_state["favorite_brand"] in brand_list:
            brand_list.remove(st.session_state["favorite_brand"])
        with st.form("second favorite_brand"):
            brands = st.multiselect("What are the various other brands that you would consider buying? Please check all the brands that you would consider buying?", brand_list)
            if "None of the above" in brands:
                user_brand = st.text_input("Please enter your favorite brand")
                submit = st.form_submit_button("Submit")
                if submit and user_brand:
                    st.session_state["final_favorite_brand_list"] = [st.session_state["favorite_brand"], user_brand]
                    str_brands = ','.join(st.session_state["final_favorite_brand_list"])
                    return str_brands
                    st.rerun()
            else:
                submit = st.form_submit_button("Submit")
                if submit:
                    st.session_state["final_favorite_brand_list"] = brands
                    str_brands =  ','.join([st.session_state["favorite_brand"]] + brands)
                    return str_brands
                    # st.write("brands: ", brands)
                    # st.rerun()

