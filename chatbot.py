import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Computer FAQ Chatbot",
    page_icon="🤖"
)

st.title("🤖 AI Computer FAQ Chatbot")
st.write("Ask anything about computers")

# -----------------------------
# Snowflake Connection
# -----------------------------
conn = st.connection("my_example_connection")

TABLE = "COMPUTER_DB.COMPUTER_SCHEMA.COMPUTER_TABLE"

# -----------------------------
# Chat Input
# -----------------------------
user_input = st.chat_input("Type your question...")

if user_input:

    st.chat_message("user").write(user_input)

    try:
        # ✅ FIXED: Use ? instead of %s
        query = f"""
            SELECT RESPONSE
            FROM {TABLE}
            WHERE LOWER(INPUT) = LOWER(?)
        """

        result = conn.query(query, params=[user_input])

        # -----------------------------
        # If found in FAQ table
        # -----------------------------
        if not result.empty:
            answer = result.iloc[0]["RESPONSE"]

        # -----------------------------
        # If NOT found → Use Cortex
        # -----------------------------
        else:
            ai_query = """
                SELECT SNOWFLAKE.CORTEX.COMPLETE(
                    'mistral-large',
                    ?
                ) AS RESPONSE
            """

            ai_result = conn.query(
                ai_query,
                params=[f"Explain clearly: {user_input}"]
            )

            answer = ai_result.iloc[0]["RESPONSE"]

    except Exception as e:
        answer = f"⚠️ Error: {str(e)}"

    st.chat_message("assistant").write(answer)