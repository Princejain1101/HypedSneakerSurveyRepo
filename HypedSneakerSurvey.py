import streamlit as st
from math import floor, ceil
def calc_new_price(low_value, high_value):
    tenthousands_low = floor(low_value / 10000) * 10000
    tenthousands_high = floor(high_value / 10000) * 10000

    if tenthousands_high != tenthousands_low:
        tenthousands_high_ceil = ceil(high_value / 10000) * 10000
        if tenthousands_high_ceil - 10000 <= tenthousands_low:
            return tenthousands_high_ceil - 1000
        else:
            return tenthousands_high_ceil - 10000

    # else fallback to 1000s
    thousands_low = floor(low_value / 1000) * 1000
    thousands_high = floor(high_value / 1000) * 1000

    if thousands_low != thousands_high:
        thousands_high_ceil = ceil(high_value / 1000) * 1000
        if thousands_high_ceil - 1000 <= thousands_low:
            return thousands_high_ceil - 100
        else:
            return thousands_high_ceil - 1000

    # else fallback to 100s
    hundreds_low = floor(low_value / 100) * 100
    hundreds_high = floor(high_value / 100) * 100

    # within 100s range
    if hundreds_low != hundreds_high:
        # within 100s range
        hundreds_high_ceil = ceil(high_value / 100) * 100
        # st.write("hundred high ceil = ", hundreds_high_ceil)
        if hundreds_high_ceil - 100 <= hundreds_low:
            return hundreds_high_ceil - 10
        else:
            return hundreds_high_ceil - 100

    # else fallback to 10s
    # else:
    # within 10s range
    tens_high_ceil = ceil(high_value / 10) * 10
    return tens_high_ceil - 10

def set_new_price(check_price_answer2):
    st.session_state.check_price_answer = check_price_answer2
    # st.write("1. check price answer = " + str(check_price_answer2))
    if st.session_state.check_price_answer is None:
        st.session_state.check_price = calc_new_price(st.session_state.buy_value, st.session_state.not_buy_value)
        # st.session_state.check_price = st.session_state.not_buy_value - 10
        return
    # st.write("2. check price answer = " + str(check_price_answer2))
    # st.session_state.check_price = st.session_state.not_buy_value - 10
    st.session_state.check_price = calc_new_price(st.session_state.buy_value, st.session_state.not_buy_value)

def update_buy_not_buy_price():
    if st.session_state.check_price_answer == "Yes":
        # assign price to low
        st.session_state["buy_value"] = st.session_state.check_price
        # st.write("setting buy value = " + str(st.session_state.check_price))
    elif st.session_state.check_price_answer == "No":
        # assign price to high
        st.session_state["not_buy_value"] = st.session_state.check_price
        # st.write("setting not buy value = " + str(st.session_state.check_price))
    else:
        return
    # st.write("buy_value = ", st.session_state.buy_value)
    # st.write("not_buy_value = ", st.session_state.not_buy_value)

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
if "check_price" not in st.session_state:
    st.session_state["check_price"] = None
if "check_price_answer" not in st.session_state:
    st.session_state["check_price_answer"] = None

with st.form("Get Buy Value"):
    buy_value = st.number_input("At what price you will definitely buy these sneakers?*", min_value=0, max_value=100000, step=1)
    buy_value_submitted = st.form_submit_button("Submit Buy Value")
    if buy_value_submitted:
        st.session_state["buy_value"] = buy_value
if st.session_state["buy_value"] is not None:
    with st.form("Get Not Buy Value"):
        not_buy_value = st.number_input("At what price you will definitely NOT buy these sneakers?*", min_value=0, max_value=100000,step=1)
        not_buy_value_submitted = st.form_submit_button("Submit Not Buy Value")
    if not_buy_value_submitted:
        st.session_state["not_buy_value"] = not_buy_value
if st.session_state["not_buy_value"] is not None and st.session_state["buy_value"] is not None:
    # st.write("A")
    if st.session_state["not_buy_value"] <= st.session_state["buy_value"] and st.session_state["check_price"] is None:
        # st.write("B")
        st.warning("NOT buy value must be greater than buy value")
        if st.button("Reset the survey"):
            # st.write("C")
            st.session_state["buy_value"] = None
            st.session_state["not_buy_value"] = None
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
                st.write("Thank you for taking the survey")






