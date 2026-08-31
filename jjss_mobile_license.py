import streamlit as st
from datetime import datetime

st.set_page_config(page_title="JJSS Login", page_icon="J", layout="centered")

# Shared server-process store so client and admin sessions can see
# the same login requests during this test.
if "JJSS_LOGIN_REQUESTS" not in st.session_state:
    st.session_state.JJSS_LOGIN_REQUESTS = {}

# Use module-level shared storage rather than st.session_state.
# Streamlit sessions have separate session_state dictionaries.
try:
    LOGIN_REQUESTS
except NameError:
    LOGIN_REQUESTS = {}

ADMIN_KEY = "JJSS-ADMIN"

st.title("JJSS LOGIN")

if st.query_params.get("admin") == ADMIN_KEY:
    st.header("JJSS ADMIN")

    pending = [
        phone for phone, data in LOGIN_REQUESTS.items()
        if data["status"] == "pending"
    ]

    if not pending:
        st.info("No pending login requests.")
    else:
        for phone in pending:
            st.write(f"**{phone}**")
            c1, c2 = st.columns(2)

            if c1.button("ACCEPT", key=f"accept_{phone}"):
                LOGIN_REQUESTS[phone]["status"] = "approved"
                st.rerun()

            if c2.button("REJECT", key=f"reject_{phone}"):
                LOGIN_REQUESTS[phone]["status"] = "rejected"
                st.rerun()

    st.stop()

phone = st.text_input("Phone Number")

if st.button("REQUEST ACCESS", use_container_width=True):
    phone = phone.strip()

    if not phone:
        st.error("Enter your phone number.")
    else:
        LOGIN_REQUESTS[phone] = {
            "status": "pending",
            "requested_at": datetime.now().isoformat(timespec="seconds"),
        }
        st.success("ACCESS REQUEST SENT")
        st.info("Waiting for JJSS Admin approval.")

if phone:
    current = LOGIN_REQUESTS.get(phone)

    if current:
        if current["status"] == "approved":
            st.success("LOGIN APPROVED")
            st.write("JJSS access is approved.")
        elif current["status"] == "rejected":
            st.error("ACCESS DENIED")
        else:
            st.info("WAITING FOR ADMIN APPROVAL")
            st.caption("Refresh this page after the admin accepts.")

