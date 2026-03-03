import streamlit as st

st.set_page_config(page_title="🤖 AI Computer Chatbot", page_icon="🤖")

st.title("🤖 AI Computer FAQ Chatbot")
st.write("Ask anything about computers")

# -----------------------------------
# CONNECT USING STREAMLIT CONNECTION
# -----------------------------------
conn = st.connection("my_example_connection")

TABLE = "COMPUTER_TABLE"

user_input = st.chat_input("Type your question...")

if user_input:

    st.chat_message("user").write(user_input)

    # ✅ SAFE parameterized query
    query = """
        SELECT RESPONSE
        FROM COMPUTER_TABLE
        WHERE LOWER(INPUT) = LOWER(%s)
    """

    result = conn.query(query, params=(user_input,))

    # -----------------------------
    # IF FOUND IN DATABASE
    # -----------------------------
    if not result.empty:
        answer = result.iloc[0]["RESPONSE"]

    # -----------------------------
    # IF NOT FOUND → USE AI
    # -----------------------------
    else:
        ai_query = f"""
        SELECT SNOWFLAKE.CORTEX.COMPLETE(
            'snowflake-arctic',
            'Explain clearly: {user_input}'
        ) AS RESPONSE;
        """

        ai_result = conn.query(ai_query)
        answer = ai_result.iloc[0]["RESPONSE"]

    st.chat_message("assistant").write(answer)