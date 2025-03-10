import streamlit as st
def indifference_survey(maximum_value):
    # left_col, right_col = st.columns(2)
    # with left_col:
    #     st.image([img for img in ["airforce1.png"]], width=350)
    # with right_col:
    #     st.image([img for img in ["airforce1ambush.png"]], width=350)
    price = maximum_value
    if "both_sneakers_image" not in st.session_state:
        st.session_state["both_sneakers_image"] = None
    if "same_price_question" not in st.session_state:
        st.session_state["same_price_question"] = None
    if "not_buy_ambush_question" not in st.session_state:
        st.session_state["not_buy_ambush_question"] = None
    if "verify_not_buy_ambush_question" not in st.session_state:
        st.session_state["verify_not_buy_ambush_question"] = None
    if "indifference_question" not in st.session_state:
        st.session_state["indifference_question"] = None
    if "verify_indifference_question" not in st.session_state:
        st.session_state["verify_indifference_question"] = None
    if "verify_indifference_question_partA" not in st.session_state:
        st.session_state["verify_indifference_question_partA"] = None
    if "verify_indifference_question_partB" not in st.session_state:
        st.session_state["verify_indifference_question_partB"] = None


    if st.session_state["both_sneakers_image"] is not None:
        left_co, cent_co, right_co = st.columns([50, 1, 50])
        with left_co:
            st.image([img for img in ["airforce1.png"]], width=350)
        with right_co:
            st.image([img for img in ["airforce1ambush.png"]], width=350)
    else:
        # with st.form("Sneaker image"):
        st.markdown("<center><p>Please take a look at these Nike Air Force 1 and Air Force 1 Ambush sneakers below</p></center>",
                    unsafe_allow_html=True)
        left_co, cent_co, right_co = st.columns([50, 1, 50])
        with left_co:
            st.image([img for img in ["airforce1.png"]], width=550)
        with right_co:
            st.image([img for img in ["airforce1ambush.png"]], width=550)
        left_su, cent_su, right_su = st.columns([3, 2, 3])
        with cent_su:
            submit = st.button("Confirm")
        if submit:
            st.session_state["both_sneakers_image"] = True
            st.rerun()
    if st.session_state["both_sneakers_image"] is not None and st.session_state["same_price_question"] is None:
        with st.form(key='buy ambush form at same price'):
            st.write(f"**Now please compare the following two options**: \n\nBoth the Air Force 1 and the Air Force 1 Ambush are priced at **\${price}**")
            same_price = st.radio("Q1. Which option do you prefer?", (f"Option 1: Air Force 1 at a price of \${price}", f"Option 2: Air Force 1 Ambush at a price of \${price}", "I am indifferent between Option 1 and Option 2"))
            if st.form_submit_button("please confirm your choice"):
                # if "Option 1 " in same_price:
                #     st.write("Option1 AirForce1 is chosen, so you are likely not a right candidate. Please exit the survey.")
                #     if st.form_submit_button("Exit the survey"):
                #         st.stop()
                if "indifferent" in same_price:
                    return True
                else:
                # if "Option 1" in same_price or "Option 2" in same_price and "indifferent" not in same_price:
                    st.session_state["same_price_question"] = same_price
                    st.rerun()
                # else:
                #     st.write("That was your final question! Thank you for taking the survey!")
                #     return True
                    # if st.form_submit_button("Exit the survey"):
                    #     st.stop()
    if st.session_state["same_price_question"] is not None and st.session_state["not_buy_ambush_question"] is None:
        if "Option 1" in st.session_state["same_price_question"]:
            with st.form(" Not Buy AirForce1 Price"):
                not_buy_ambush_price = st.number_input(
                    f"**At equal prices (\${price}), you prefer the Option 1 Air Force 1**.\n\nNow, please fill out a price for the **Option 2 Air Force 1 Ambush** at which you would DEFINITELY choose **Option 2 Air Force 2 Ambush**",
                    value=None, min_value=0, max_value=price, step=1)
                if st.form_submit_button("please confirm your choice"):
                    st.session_state["not_buy_ambush_question"] = not_buy_ambush_price
                    st.rerun()
        else:
            with st.form(" Not Buy AirForce1Ambush Price"):
                not_buy_ambush_price = st.number_input(f"**At equal prices (\${price}), you prefer the Option 2 Air Force 1 Ambush**.\n\nNow, please fill out a price for the **Option 1 Air Force 1 Ambush** at which you would DEFINITELY choose **Option 1 Air Force 1**", value=None, min_value=price+1, max_value=10000, step=1)
                if st.form_submit_button("please confirm your choice"):
                    st.session_state["not_buy_ambush_question"] = not_buy_ambush_price
                    st.rerun()

    if st.session_state["not_buy_ambush_question"] is not None and st.session_state["verify_not_buy_ambush_question"] is None:
        with (st.form(" Verify Not Buy Ambush Price")):
            if "Option 1" in st.session_state["same_price_question"]:
                verify_not_buy_ambush = st.radio(f"Q3. Can you confirm that you would chose **Option 2 Air Force 1 Ambush at \${st.session_state["not_buy_ambush_question"]}** price given **Option 1 Air Force 1 at \${price}** ?", ("Yes, I confirm that I would definitely choose option 2", "No, I cannot confirm that I would definitely choose option 2"))
            else:
                verify_not_buy_ambush = st.radio(f"Q3. Can you confirm that you would chose **Option 1 Air Force 1 at \${price}** if **Option 2 Air Force 1 Ambush is at \${st.session_state["not_buy_ambush_question"]}** price?", ("Yes, I confirm that I would definitely choose option 1", "No, I cannot confirm that I would definitely choose option 1"))
            if st.form_submit_button("please confirm your choice"):
                if "Yes" in verify_not_buy_ambush:
                    # st.write("Move Forward")
                    st.session_state["verify_not_buy_ambush_question"] = verify_not_buy_ambush
                    st.rerun()
                else:
                    # st.write("Go back to question2")
                    st.session_state["not_buy_ambush_question"] = None
                    st.warning("You have not chosen a correct price for Option 2 Air force 1 Ambush then. Please try again.")
                    if st.form_submit_button("Try Again"):
                        st.rerun()
    if st.session_state["verify_not_buy_ambush_question"] is not None and st.session_state["indifference_question"] is None:
        if "Option 1" in st.session_state["same_price_question"]:
            st.write(f"Based on the previous answers \n\n  - You chose the **Air Force 1** when the prices of both sneakers is \${price}\n\n  - You chose the **Air Force 1 Ambush** when the price of the **Air Force 1 Ambush is** \${st.session_state["not_buy_ambush_question"]} while the price of the **Air Force 1 is** \${price}")
            with st.form(" Indifference question"):
                indifference_number = st.number_input(f"Therefore, there is a price between \${st.session_state["not_buy_ambush_question"]} and \${price} for the Air Force 1 Ambush where you are indifferent between the two sneakers. [i.e. you cannot choose between them]. Please fill out that price below \n\n", value=None, min_value=st.session_state["not_buy_ambush_question"], max_value=price, step=1)
                if st.form_submit_button("please confirm your choice"):
                    st.session_state["indifference_question"] = indifference_number
                    st.rerun()
        else:
            st.write(f"Based on the previous answers \n\n  - You chose the **Air Force 1 Ambush** when the prices of both sneakers is \${price}\n\n  - You chose the **Air Force 1** when the price of the **Air Force 1 Ambush is** \${st.session_state["not_buy_ambush_question"]} while the price of the **Air Force 1 is** \${price}")
            with st.form(" Indifference question"):
                indifference_number = st.number_input(f"Therefore, there is a price between \${price} and \${st.session_state["not_buy_ambush_question"]} for the Air Force 1 Ambush where you are indifferent between the two sneakers. [i.e. you cannot choose between them]. Please fill out that price below \n\n", value=None, min_value=price, max_value=st.session_state["not_buy_ambush_question"], step=1)
                if st.form_submit_button("please confirm your choice"):
                    st.session_state["indifference_question"] = indifference_number
                    st.rerun()
    if st.session_state["indifference_question"] is not None and st.session_state["verify_indifference_question"] is None:
        with st.form(" verify indifference question"):
            st.write(f"Price for Option 1 Air Force 1 is \${price} and Option 2 Air Force 1 Ambush is at \${st.session_state["indifference_question"]}")
            st.write(f"Please confirm that at this price you are indifferent between the two options")
            if st.form_submit_button("please confirm your choice"):
                st.session_state["verify_indifference_question"] = True
                st.rerun()
    if st.session_state["verify_indifference_question"] is not None and st.session_state["verify_indifference_question_partA"] is None:
        with st.form(" Verify Indifference question partA"):
            st.write(
                f"Price for Option 1 Air Force 1 is \${price} and Option 2 Air Force 1 Ambush is at \${st.session_state["indifference_question"]}")
            verify_indifferenceA = st.radio("Q5 A. Can the program select option 2 for you? Are you OK with that?", ("Yes, I am ", "No, I prefer Option 1"))
            if st.form_submit_button("Submit"):
                if "Yes" in verify_indifferenceA:
                    # st.write("Move Forward")
                    st.session_state["verify_indifference_question_partA"] = verify_indifferenceA
                    st.rerun()
                else:
                    st.warning(f"‘Hmm....Since you prefer option 1, you are apparently not quite indifferent between the two options. Hence the selected price of {st.session_state["indifference_question"]} is too high for you to be indifferent. So think this through a bit more and please input a price at which you are truly indifferent between the two options.")
                    st.session_state["indifference_question"] = None
                    st.session_state["verify_indifference_question"] = None
                    if st.form_submit_button("try again"):
                        st.rerun()
    if st.session_state["verify_indifference_question_partA"] is not None and st.session_state["verify_indifference_question_partB"] is None:
        with st.form(" Verify Indifference question partB"):
            st.write(
                f"Price for Option 1 Air Force 1 is \${price} and Option 2 Air Force 1 Ambush is at \${st.session_state["indifference_question"]}")
            verify_indifferenceB = st.radio("Q5 B. Can the program select option 1 for you? Are you OK with that?", ("Yes, I am", "No, I prefer Option 2"))
            if st.form_submit_button("please confirm your choice"):
                if "Yes" in verify_indifferenceB:
                    # st.write("Move Forward")
                    st.session_state["verify_indifference_question_partB"] = verify_indifferenceB
                    st.rerun()
                else:
                    st.warning(f"‘Hmm....Since you prefer option 1, you are apparently not quite indifferent between the two options. Hence the selected price of {st.session_state["indifference_question"]} is too low for you to be indifferent. So think this through a bit more and please input a price at which you are truly indifferent between the two options.")
                    st.session_state["indifference_question"] = None
                    st.session_state["verify_indifference_question"] = None
                    st.session_state["verify_indifference_question_partA"] = None
                    if st.form_submit_button("try again"):
                        st.rerun()
    if st.session_state["verify_indifference_question_partB"] is not None:
        return True