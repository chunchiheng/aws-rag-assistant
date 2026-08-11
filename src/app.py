import streamlit as st

from rag import ask_question


st.set_page_config(
    page_title="AWS Documentation Assistant",
    page_icon="☁️",
)


st.title("AWS Documentation Assistant")

st.write(
    "Ask questions about AWS documentation."
)


query = st.text_input(
    "Ask a question:"
)


if st.button("Ask"):

    if not query.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching AWS documentation..."):

            answer, sources = ask_question(query)


        st.subheader("Answer")

        st.write(answer)


        st.subheader("Sources")

        for source in sources:

            st.write(f"- {source}")