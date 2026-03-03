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
session = conn.session()

TABLE = "COMPUTER_DB.COMPUTER_SCHEMA.COMPUTER_TABLE"

# -----------------------------
# Chat Input
# -----------------------------
user_input = st.chat_input("Type your question...")

if user_input:

    st.chat_message("user").write(user_input)

    try:
        # ✅ SAFE parameterized query (prevents SQL injection)
        query = f"""
            SELECT RESPONSE
            FROM {TABLE}
            WHERE LOWER(INPUT) = LOWER(%s)
        """

        result = session.sql(query, params=[user_input]).collect()

        # -----------------------------
        # If found in FAQ table
        # -----------------------------
        if result:
            answer = result[0]["RESPONSE"]

        # -----------------------------
        # If NOT found → Use Snowflake Cortex AI
        # -----------------------------
        else:
            ai_query = """
                SELECT SNOWFLAKE.CORTEX.COMPLETE(
                    'mistral-large',
                    %s
                ) AS RESPONSE
            """

            ai_result = session.sql(
                ai_query,
                params=[f"Explain clearly: {user_input}"]
            ).collect()

            answer = ai_result[0]["RESPONSE"]

    except Exception as e:
        answer = "⚠️ Something went wrong. Please check logs."

    st.chat_message("assistant").write(answer)