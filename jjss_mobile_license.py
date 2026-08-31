import streamlit as st
import requests

st.set_page_config(
    page_title="JJSS Login",
    page_icon="J",
    layout="centered"
)

GOOGLE_APPS_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbz2xaN6-t-fXJs4i0qf6tMjmoszZ15v8AP2DEt4KFernxbRsYLaOf9Y-CabpQYR4ZoP/"
    "exec"
)

API_KEY = "JJSS-LICENSING-TEST-2026"
ADMIN_KEY = "JJSS-ADMIN"


# ============================================================
# BROKER LIST
# ============================================================

BROKERS = [
    "Zerodha",
    "Upstox",
    "Angel One",
    "Choice Broking",
    "Dhan",
    "Groww",
    "FYERS",
    "5paisa",
    "ICICI Direct",
    "Kotak Neo",
    "Motilal Oswal",
    "Nuvama",
    "Shoonya / Finvasia",
    "Alice Blue",
    "IIFL Securities",
    "Axis Direct",
    "Anand Rathi",
    "Geojit",
    "Mastertrust",
    "Flattrade",
    "Indiabulls"
]


# ============================================================
# API FUNCTION
# ============================================================

def call_api(action, phone=""):
    try:

        if action in ("request", "approve", "reject"):

            response = requests.post(
                GOOGLE_APPS_SCRIPT_URL,
                json={
                    "key": API_KEY,
                    "action": action,
                    "phone": phone
                },
                timeout=15
            )

        else:

            response = requests.get(
                GOOGLE_APPS_SCRIPT_URL,
                params={
                    "key": API_KEY,
                    "action": action,
                    "phone": phone
                },
                timeout=15
            )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "ok": False,
            "error": str(e)
        }


# ============================================================
# TITLE
# ============================================================

st.title("JJSS LOGIN")


# ============================================================
# JJSS ADMIN
# ============================================================

if st.query_params.get("admin") == ADMIN_KEY:

    st.header("JJSS ADMIN")

    result = call_api("pending")

    if not result.get("ok"):

        st.error("Unable to connect to JJSS License Database.")
        st.stop()

    pending = result.get("pending", [])

    if not pending:

        st.info("No pending login requests.")

    else:

        for phone in pending:

            st.write(f"**{phone}**")

            c1, c2 = st.columns(2)

            if c1.button(
                "ACCEPT",
                key=f"accept_{phone}"
            ):

                result = call_api(
                    "approve",
                    phone
                )

                if result.get("ok"):

                    st.rerun()

                else:

                    st.error(
                        "Unable to approve request."
                    )

            if c2.button(
                "REJECT",
                key=f"reject_{phone}"
            ):

                result = call_api(
                    "reject",
                    phone
                )

                if result.get("ok"):

                    st.rerun()

                else:

                    st.error(
                        "Unable to reject request."
                    )

    st.stop()


# ============================================================
# JJSS USER LOGIN
# ============================================================

phone = st.text_input(
    "Phone Number",
    key="phone"
)


if st.button(
    "REQUEST ACCESS",
    use_container_width=True
):

    phone = phone.strip()

    if not phone:

        st.error(
            "Enter your phone number."
        )

    else:

        result = call_api(
            "request",
            phone
        )

        if result.get("ok"):

            st.success(
                "ACCESS REQUEST SENT"
            )

            st.info(
                "Waiting for JJSS Admin approval."
            )

        else:

            st.error(
                "Unable to send access request."
            )


# ============================================================
# CHECK CURRENT STATUS
# ============================================================

if phone:

    phone = phone.strip()

    result = call_api(
        "status",
        phone
    )

    if result.get("ok"):

        status = result.get(
            "status",
            ""
        )

        if status == "approved":

            st.success(
                "LOGIN APPROVED"
            )

            st.write(
                "JJSS access is approved."
            )

            # ==================================================
            # DEMAT ACCOUNT
            # ==================================================

            st.header("DEMAT ACCOUNT")

            selected_broker = st.selectbox(
                "Select Broker",
                BROKERS,
                key="selected_broker"
            )

            st.write(
                f"Selected Broker: **{selected_broker}**"
            )

            client_id = st.text_input(
                "Client ID / User ID",
                key="broker_client_id"
            )

            api_key = st.text_input(
                "API Key",
                key="broker_api_key",
                type="password"
            )

            api_secret = st.text_input(
                "API Secret",
                key="broker_api_secret",
                type="password"
            )

            if st.button(
                "CONNECT DEMAT ACCOUNT",
                use_container_width=True
            ):

                if not client_id:

                    st.error(
                        "Enter Client ID / User ID."
                    )

                elif not api_key:

                    st.error(
                        "Enter API Key."
                    )

                elif not api_secret:

                    st.error(
                        "Enter API Secret."
                    )

                else:

                    st.success(
                        f"{selected_broker} selected."
                    )

                    st.info(
                        "Broker connection setup ready."
                    )

        elif status == "rejected":

            st.error(
                "ACCESS DENIED"
            )

        elif status == "pending":

            st.info(
                "WAITING FOR ADMIN APPROVAL"
            )

            st.caption(
                "Refresh this page after the admin accepts."
            )
