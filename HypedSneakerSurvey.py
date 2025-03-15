import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import re
from layout_utils import set_bg_hack_url, remove_top_white
from consent_form import consent_text, consent_header
from price_calculations import calc_new_price, set_new_price, update_buy_not_buy_price
from datetime import datetime
import streamlit.components.v1 as components
from indifferencesurvey import indifference_survey
from favorite_brand import favorite_brand_api
st.set_page_config(layout="wide")

sneaker1nolabel = "airforce1-nolabel.png"
sneaker2nolabel = "airforce1ambush-nolabel.png"
worksheet="SneakerPreferenceStudyResponseFinal"
set_bg_hack_url()
remove_top_white()
scroll_script = """
<script>
setTimeout(function() {
    window.scrollTo(0, document.body.scrollHeight);
}, 1000); // Delay of 100 milliseconds
</script>
"""
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def check_email(email):
    if email == "": return None
    return True if re.fullmatch(regex, email) else False

conn = st.connection("gsheets", type=GSheetsConnection)

def check_email_in_db(email):
    existing_data_email_df = conn.read(worksheet=worksheet, usecols=[1], ttl=5)
    previous_emails_list = existing_data_email_df.iloc[:, 0].tolist()
    if email in previous_emails_list:
        return True
    else:
        return False

def update_results_to_sheet():
    existing_data = conn.read(worksheet=worksheet, usecols=list(range(15)), ttl=5)
    now = datetime.now()
    date = now.date()
    time = now.time()
    empty = "NA"
    same_price_choice = None
    if "same_price_question" in st.session_state:
        if "Option 1" in st.session_state["same_price_question"]:
            same_price_choice = "Option 1"
        elif "Option 2" in st.session_state["same_price_question"]:
            same_price_choice = "Option 2"
        elif "indifferent" in st.session_state["same_price_question"]:
            same_price_choice = "Indifferent"
    result_data = pd.DataFrame([
        {
            "name": st.session_state["name"],
            "email": st.session_state["email"],
            "date": date,
            "time": time,
            "never buy AF1" : st.session_state["never_buy_choice_sneaker1"] if st.session_state["never_buy_choice_sneaker1"] else empty,
            "never buy AF1Ambush" : st.session_state["never_buy_choice_sneaker2"] if st.session_state["never_buy_choice_sneaker2"] else empty,
            "buy price": st.session_state.store_buy_value if st.session_state.store_buy_value else empty,
            "not buy price": st.session_state.store_not_buy_value if st.session_state.store_not_buy_value else empty,
            "maximum price": st.session_state["maximum_value"] if st.session_state["maximum_value"] else empty,
            "survey part1 done" : st.session_state["survey_part_one"] if st.session_state["survey_part_one"] else empty,
            "same price preference" : same_price_choice if same_price_choice else empty,
            "option 2 price" : st.session_state["not_buy_ambush_question"] if "not_buy_ambush_question" in st.session_state else empty,
            "indifference price" : st.session_state["indifference_question"] if "indifference_question" in st.session_state else empty,
            "indifference survey done" : st.session_state["run_indifference_survey"] if st.session_state["run_indifference_survey"] else empty,
            "brands" : st.session_state["get_brands"] if st.session_state["get_brands"] else empty,
        }
    ])
    updated_data = pd.concat([existing_data, result_data], ignore_index=True)
    conn.update(worksheet=worksheet, data=updated_data)

# st.dataframe(existing_data)

def check_exit():
    # st.write("not buy value = ", st.session_state.not_buy_value)
    # st.write("buy value = ", st.session_state.buy_value)
    if st.session_state["not_buy_value"] <= st.session_state["buy_value"] + 10:
        return True
    else:
        return False
if "consent_form" not in st.session_state:
    st.session_state["consent_form"] = None
if "name" not in st.session_state:
    st.session_state["name"] = None
if "email" not in st.session_state:
    st.session_state["email"] = None
if "sneaker_image" not in st.session_state:
    st.session_state["sneaker_image"] = None
if "never_buy_choice_sneaker1" not in st.session_state:
    st.session_state["never_buy_choice_sneaker1"] = None
if "never_buy_choice_sneaker2" not in st.session_state:
    st.session_state["never_buy_choice_sneaker2"] = None
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
if "exit_survey" not in st.session_state:
    st.session_state["exit_survey"] = None
if "scroll_to_bottom" not in st.session_state:
    st.session_state.scroll_to_bottom = True
if "maximum_value" not in st.session_state:
    st.session_state["maximum_value"] = None
if "survey_part_one" not in st.session_state:
    st.session_state["survey_part_one"] = None
if "run_indifference_survey" not in st.session_state:
    st.session_state["run_indifference_survey"] = None
if "get_brands" not in st.session_state:
    st.session_state["get_brands"] = None

st.markdown("<h1 style='text-align: center; color: black;'>Sneaker Preference Study</h1>", unsafe_allow_html=True)
# st.session_state["survey_part_one"] = True
# st.session_state["maximum_value"] = 40
if st.session_state["exit_survey"] is None:
    if st.session_state["survey_part_one"] is None:
        if st.session_state["consent_form"] is None:
            st.write(consent_header)
            with st.form("consent form"):
                name = st.text_input("Enter your name")
                email = st.text_input("Enter your email")
                if check_email(email) is False:
                    st.warning("Please enter a valid email")
                st.write(consent_text)
                consent_confirm = st.checkbox("I agree")
                submit = st.form_submit_button("Submit")
                if submit:
                    if consent_confirm is not True:
                        st.warning("Please agree to the consent form")
                    if name is "":
                        st.warning("Please enter a name")
                    if email is "":
                        st.warning("Please enter a email")
                    if email is not "":
                        if check_email(email) is False:
                            st.warning("Please enter a valid email")
                        elif check_email_in_db(email) is True:
                            st.warning("User already filled the survey")
                if consent_confirm is True and name is not None and email is not None and check_email(email) == True and check_email_in_db(email) is False and submit:
                    st.session_state["consent_form"] = True
                    st.session_state["name"] = name
                    st.session_state["email"] = email
                    st.rerun()
        if st.session_state["consent_form"] is not None:
            components.html(scroll_script, height=0)

            sneakerimage = sneaker1nolabel
            if st.session_state["never_buy_choice_sneaker1"] is not None:
                sneakerimage = sneaker2nolabel

            if st.session_state["sneaker_image"] is not None and st.session_state["survey_part_one"] is None:
                left_co, cent_co, right_co = st.columns([1,3,1])
                with cent_co:
                    st.image([img for img in [sneakerimage]], width=550)
            else:
                # with st.form("Sneaker image"):
                if sneakerimage is sneaker1nolabel:
                    st.markdown("<center><p>Please take a look at this Nike Air Force 1 sneakers below</p></center>", unsafe_allow_html=True)
                else:
                    st.markdown("<center><p>Please take a look at this Nike Air Force 1 Ambush sneakers below</p></center>", unsafe_allow_html=True)

                left_co, cent_co, right_co = st.columns([1,3,1])
                with cent_co:
                    st.image([img for img in [sneakerimage]], width=550)
                left_su, cent_su, right_su = st.columns([3,2,3])
                with cent_su:
                    submit = st.button("Confirm")
                if submit:
                    st.session_state["sneaker_image"] = True
                    st.rerun()

        if st.session_state["sneaker_image"] is not None and st.session_state["buy_value"] is None:
            components.html(scroll_script, height=0)

            with st.form("Get Buy Value"):
                buy_value = st.number_input("Q1. At what price (in USD) would you DEFINITELY BUY these sneakers?*", value=None, min_value=0, max_value=100000, step=1, placeholder=None)
                never_buy_choice = st.checkbox("Check this box If you would never buy these sneakers whatever its price may be.")
                buy_value_submitted = st.form_submit_button("please submit your choice")
                if buy_value_submitted and never_buy_choice is True :
                    if st.session_state["never_buy_choice_sneaker1"] is True: ## sneaker2 is also not buy
                        st.session_state["never_buy_choice_sneaker2"] = True
                        st.session_state["exit_survey"] = True
                        st.rerun()
                    else:
                        st.session_state["never_buy_choice_sneaker1"] = True
                        st.session_state["sneaker_image"] = None
                        st.rerun()
                if buy_value_submitted and st.session_state["never_buy_choice_sneaker1"] is not True:
                    st.session_state["buy_value"] = buy_value
                    st.session_state["store_buy_value"] = buy_value
                    st.rerun()
                if buy_value_submitted and st.session_state["never_buy_choice_sneaker2"] is not True:
                    st.session_state["buy_value"] = buy_value
                    st.session_state["store_buy_value"] = buy_value
                    st.rerun()
        if st.session_state["buy_value"] is not None and st.session_state["not_buy_value"] is None:
            components.html(scroll_script, height=0)

            with st.form("Get Not Buy Value"):
                not_buy_value = st.number_input("Q2. At what price (in USD) would you DEFINITELY NOT BUY these sneakers?*", value=None, min_value=0, max_value=100000,step=1)
                not_buy_value_submitted = st.form_submit_button("please submit your choice")
            if not_buy_value_submitted:
                st.session_state["not_buy_value"] = not_buy_value
                st.session_state["store_not_buy_value"] = not_buy_value
                st.rerun()
        if st.session_state["not_buy_value"] is not None and st.session_state["buy_value"] is not None and st.session_state["survey_part_one"] is None:
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
                # st.write("Your new Range is: " + str(st.session_state.buy_value) + " -> " + str(st.session_state.not_buy_value))
                # st.write("D")
                set_new_price(st.session_state.check_price_answer)
                if not check_exit():
                    with st.form("Check Next Possible Price"):
                        st.write(
                            f"You mentioned that you would DEFINITELY NOT buy these Air Force 1 sneakers at a price of \${st.session_state.not_buy_value}")

                        placeholder_for_radio = st.empty()
                        # st.write("A check price answer = " + str(st.session_state.check_price_answer))
                        left_col, center_col, right_col = st.columns((3,1,2))
                        with left_col:
                            change = st.form_submit_button("please submit your choice")#, on_click=set_new_price, args=[st.session_state.check_price_answer])
                            # form_submitted = st.form_submit_button("Submit Possible Price form")
                        with placeholder_for_radio:
                            check_price_answer = st.radio(f"Q3. Would you buy these sneakers at a price of **\${st.session_state["check_price"]}** ?", ["Yes", "No"])
                            # st.write("B check price answer = " + str(st.session_state.check_price_answer))
                        if change:
                            st.session_state.check_price_answer = check_price_answer
                            update_buy_not_buy_price()
                            st.rerun()
                        with right_col:
                            if st.form_submit_button("Start from Q1?"):
                                st.session_state["buy_value"] = None
                                st.session_state["not_buy_value"] = None
                                st.session_state["maximum_value"] = None
                                st.rerun()

                else:
                    with st.form("Get final maximum price"):
                        st.write(
                            f"You mentioned that you would not buy these Air Force 1 sneakers at a price of \${st.session_state.not_buy_value} but that you would buy them at a price of \${st.session_state.buy_value}")
                        maximum_price = st.slider("Q4. What is the maximum price at which you would buy these sneakers?", value = None, min_value = st.session_state["buy_value"], max_value = st.session_state["not_buy_value"], step=1)
                        submit = st.form_submit_button(f"Submit your maximum price")
                        if submit:
                            st.session_state["maximum_value"] = maximum_price
                            # with st.spinner():
                            #     update_results_to_sheet()
        if st.session_state["maximum_value"] is not None and st.session_state["survey_part_one"] is None:
            with st.form("Exit survey"):
                st.write(f"Maximum price was \${st.session_state.maximum_value}")
                left_col, center_col, right_col = st.columns((3,1,2))
                with left_col:
                    name = st.session_state["name"]
                    email = st.session_state["email"]
                    maximum_value = st.session_state["maximum_value"]
                    if st.form_submit_button("Continue to part 2 of the survey"):
                        st.session_state["survey_part_one"] = True
                        st.rerun()
                    # st.link_button("Continue to part 2 of the survey", f"https://indifferencesurvey.streamlit.app/?name={name}&email={email}&maximum_value={maximum_value}")
                with right_col:
                    submit = st.form_submit_button("Retake this survey")
                    if submit:
                        st.session_state["buy_value"] = None
                        st.session_state["not_buy_value"] = None
                        st.session_state["maximum_value"] = None
                        st.rerun()
    if st.session_state["survey_part_one"] is not None and st.session_state["run_indifference_survey"] is None:
        if indifference_survey(st.session_state["maximum_value"]):
            st.session_state["run_indifference_survey"] = True
            st.rerun()
            #     st.write(f"Maximum price was \${st.session_state.maximum_value}")
            #     left_col, cent_col, right_col = st.columns(3)
            #     with left_col:
            #         if st.form_submit_button("Exit survey"):
            #             st.session_state["exit_survey"] = True
            #             st.rerun()
            #     with cent_col:
            #     with right_col:
            #         if st.form_submit_button("Retake survey"):
            #             st.session_state["buy_value"] = None
            #             st.session_state["not_buy_value"] = None
            #             st.session_state["maximum_value"] = None
            #             st.rerun()
    if st.session_state["run_indifference_survey"] is not None and st.session_state["get_brands"] is None:
        brands = favorite_brand_api()
        st.session_state["get_brands"] = brands
    if st.session_state["get_brands"] is not None:
        st.session_state["exit_survey"] = True
        st.rerun()
else:
    with st.spinner():
        update_results_to_sheet()
    left_co, cent_co, last_co = st.columns([1,3,1])
    with cent_co:
        st.image([img for img in ["thankyousurvey3.png"]], width=550)

# Inject the JavaScript at the end of the app

st.divider()




