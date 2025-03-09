import streamlit as st

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRql_3vokMRun7lTAq3x0CzjdLxzZ6zIcAUTA&s");
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


def remove_top_white():
    st.markdown(
        """
            <style>
                    .stAppHeader {
                        background-color: rgba(255, 255, 255, 0.0);  /* Transparent background */
                        visibility: visible;  /* Ensure the header is visible */
                    }

                   .block-container {
                        padding-top: 1rem;
                        padding-bottom: 0rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
            </style>
            """,
        unsafe_allow_html=True,
    )
