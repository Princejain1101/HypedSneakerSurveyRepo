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

def calc_new_price_up(low_value, high_value):
    # st.write("low value = ", low_value)
    # st.write("high value = ", high_value)
    tenthousands_low = floor(low_value / 10000) * 10000
    tenthousands_high = floor(high_value / 10000) * 10000


    if tenthousands_high != tenthousands_low:
        # st.write("tenthousands high = ", tenthousands_high)
        # st.write("tenthousands low = ", tenthousands_low)
        tenthousands_low_floor = floor(low_value / 10000) * 10000
        if tenthousands_low_floor + 10000 < tenthousands_high:
            return tenthousands_low_floor + 10000
        # else:
        #     return tenthousands_low_floor + 10000


    # else fallback to 1000s
    thousands_low = floor(low_value / 1000) * 1000
    thousands_high = floor(high_value / 1000) * 1000

    if thousands_low != thousands_high:
        # st.write("thousands high = ", thousands_high)
        # st.write("thousands low = ", thousands_low)
        thousands_low_floor = floor(low_value / 1000) * 1000
        if thousands_low_floor + 1000 < thousands_high:
            return thousands_low_floor + 1000
        # else:
        #     return thousands_low_floor + 1000

    # else fallback to 100s
    hundreds_low = floor(low_value / 100) * 100
    hundreds_high = floor(high_value / 100) * 100

    # within 100s range
    if hundreds_low != hundreds_high:
        # st.write("hundreds high = ", hundreds_high)
        # st.write("hundreds low = ", hundreds_low)
        # within 100s range
        hundreds_low_floor = floor(low_value / 100) * 100
        # st.write("hundred high ceil = ", hundreds_high_ceil)
        if hundreds_low_floor + 100 < hundreds_high:
            return hundreds_low_floor + 100
        # else:
        #     return hundreds_low_floor + 100

    # else fallback to 10s
    # else:
    # within 10s range
    tens_low_floor = floor(low_value / 10) * 10
    return tens_low_floor + 10


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

def set_new_price_up(check_price_answer2):
    st.session_state.check_price_answer = check_price_answer2
    # st.write("1. check price answer = " + str(check_price_answer2))
    if st.session_state.check_price_answer is None:
        st.session_state.check_price = calc_new_price_up(st.session_state.buy_value, st.session_state.not_buy_value)
        # st.session_state.check_price = st.session_state.not_buy_value - 10
        return
    # st.write("2. check price answer = " + str(check_price_answer2))
    # st.session_state.check_price = st.session_state.not_buy_value - 10
    st.session_state.check_price = calc_new_price_up(st.session_state.buy_value, st.session_state.not_buy_value)
    # st.write("new price = ", st.session_state.check_price)

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
