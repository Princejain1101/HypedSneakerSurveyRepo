import streamlit as st
from math import floor, ceil
from streamlit_gsheets import GSheetsConnection
import pandas as pd


conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="ResponseTable", usecols=list(range(3)), ttl=5)

# st.dataframe(existing_data)


def check_exit():
    # st.write("not buy value = ", st.session_state.not_buy_value)
    # st.write("buy value = ", st.session_state.buy_value)
    if st.session_state["not_buy_value"] <= st.session_state["buy_value"] + 10:
        return True
    else:
        return False

if "buy_value" not in st.session_state:
    st.session_state["buy_value"] = None
if "not_buy_value" not in st.session_state:
    st.session_state["not_buy_value"] = None
if "store_buy_value" not in st.session_state:
    st.session_state["store_buy_value"] = None
if "store_not_buy_value" not in st.session_state:
    st.session_state["store_not_buy_value"] = None
if "check_price" not in st.session_state:
    st.session_state["check_price"] = None
if "check_price_answer" not in st.session_state:
    st.session_state["check_price_answer"] = None

buy_value_placeholder = st.empty()
if st.session_state.store_buy_value is None:
    with buy_value_placeholder.form("Get Buy Value"):
        buy_value = st.number_input("At what price you will definitely buy these sneakers?*", min_value=0, max_value=100000, step=1)
        buy_value_submitted = st.form_submit_button("Submit Buy Value")
        if buy_value_submitted:
            st.session_state["buy_value"] = buy_value
            st.session_state["store_buy_value"] = buy_value
            buy_value_placeholder.empty()
not_buy_value_placeholder = st.empty()
if st.session_state["buy_value"] is not None and st.session_state.store_not_buy_value is None:
    with not_buy_value_placeholder.form("Get Not Buy Value"):
        not_buy_value = st.number_input("At what price you will definitely NOT buy these sneakers?*", min_value=0, max_value=100000,step=1)
        not_buy_value_submitted = st.form_submit_button("Submit Not Buy Value")
    if not_buy_value_submitted:
        st.session_state["not_buy_value"] = not_buy_value
        st.session_state["store_not_buy_value"] = not_buy_value
        not_buy_value_placeholder.empty()
if st.session_state["not_buy_value"] is not None and st.session_state["buy_value"] is not None:
    # st.write("A")
    if st.session_state["not_buy_value"] <= st.session_state["buy_value"] and st.session_state["check_price"] is None:
        # st.write("B")
        st.warning("NOT buy value must be greater than buy value")
        if st.button("Reset the survey"):
            # st.write("C")
            st.session_state["buy_value"] = None
            st.session_state["not_buy_value"] = None
            st.session_state["store_buy_value"] = None
            st.session_state["store_not_buy_value"] = None
            st.rerun()
    else:
        st.write("Your new Range is: " + str(st.session_state.buy_value) + " -> " + str(st.session_state.not_buy_value))
        # st.write("D")
        set_new_price(st.session_state.check_price_answer)
        if not check_exit():
            with st.form("Check Next Possible Price"):
                placeholder_for_radio = st.empty()
                # st.write("A check price answer = " + str(st.session_state.check_price_answer))
                change = st.form_submit_button("Submit Possible Price")#, on_click=set_new_price, args=[st.session_state.check_price_answer])
                # form_submitted = st.form_submit_button("Submit Possible Price form")
            with placeholder_for_radio:
                check_price_answer = st.radio("Would you like to buy at " + str(st.session_state["check_price"])+ " ?", ["Yes", "No"])
                # st.write("B check price answer = " + str(st.session_state.check_price_answer))
            if change:
                st.session_state.check_price_answer = check_price_answer
                update_buy_not_buy_price()
                # st.write("AB check price answer = " + str(check_price_answer))
                st.rerun()
        else:
            # st.write("buy value = ", st.session_state["buy_value"])
            # st.write("not buy value = ", st.session_state["not_buy_value"])
            final_price = st.slider("Chose a value between range", min_value = st.session_state["buy_value"], max_value = st.session_state["not_buy_value"], step=1)
            st.write("final price = ", final_price)
            submit = st.button("Submit your results")
            if submit:
                result_data = pd.DataFrame([
                    {
                        "buy price": st.session_state.store_buy_value,
                        "not buy price": st.session_state.store_not_buy_value,
                        "final price": final_price,
                    }
                ])
                updated_data = pd.concat([existing_data, result_data], ignore_index=True)
                conn.update(worksheet="ResponseTable", data=updated_data)
                st.write("Thank you for taking the survey")






