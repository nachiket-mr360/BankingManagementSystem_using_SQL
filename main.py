import streamlit as st
import time
import textwrap
from datetime import datetime
from CLI_main import BankSystem, Audit


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="MyBank | Banking Management System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": None,
    }
)


# ============================================================
# PROFESSIONAL FINTECH UI
# ============================================================
st.markdown(textwrap.dedent("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #07121f;
    --surface: #0d1b2d;
    --surface-2: #12233a;
    --border: #21334a;
    --text: #f5f7fa;
    --muted: #9aaabd;
    --primary: #19c99a;
    --primary-dark: #0fae88;
    --cyan: #2bc6df;
    --danger: #ef6b7a;
    --warning: #f3b53f;
}

* { box-sizing: border-box; }

html, body, .stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
.main,
.block-container {
    background: transparent !important;
}

.block-container {
    width: 100% !important;
    max-width: 1380px !important;
    padding: 24px clamp(14px, 2.4vw, 34px) 42px !important;
}

[data-testid="stHeader"] {
    background: rgba(7,18,31,.92) !important;
}

[data-testid="stToolbar"] { display: none; }

h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
}

p, label, [data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}

/* -------------------- HERO -------------------- */

.hero {
    position: relative;
    overflow: hidden;
    min-height: 205px;
    padding: 34px clamp(24px, 4vw, 52px);
    margin-bottom: 26px;
    border: 1px solid #1d6d69;
    border-radius: 22px;
    background:
        linear-gradient(120deg, rgba(19,64,66,.68), rgba(9,30,45,.96) 60%),
        #0b1c2b;
    box-shadow: 0 16px 42px rgba(0,0,0,.20);
}

.hero::before {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    right: -120px;
    top: -145px;
    border-radius: 50%;
    background: rgba(25,201,154,.08);
}

.hero::after {
    content: "";
    position: absolute;
    width: 190px;
    height: 190px;
    left: -95px;
    bottom: -130px;
    border: 1px solid rgba(43,198,223,.16);
    border-radius: 50%;
}

.hero-content {
    position: relative;
    z-index: 1;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    width: fit-content;
    padding: 7px 12px;
    margin-bottom: 15px;
    border: 1px solid rgba(25,201,154,.45);
    border-radius: 999px;
    background: rgba(25,201,154,.07);
    color: #58e0ba;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .65px;
    text-transform: uppercase;
}

.hero h1 {
    margin: 0 !important;
    font-size: clamp(31px, 4.2vw, 53px) !important;
    line-height: 1.08 !important;
    letter-spacing: -1.7px;
    background: linear-gradient(90deg, #61e2ba, #35c9df);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 800px;
    margin: 13px 0 0;
    color: #aab9ca !important;
    font-size: 14px;
    line-height: 1.65;
}

/* -------------------- AUTH -------------------- */

.auth-surface {
    min-height: 420px;
    padding: 30px;
    border: 1px solid var(--border);
    border-radius: 20px;
    background: linear-gradient(145deg, #102239, #0b192b);
}

.auth-title {
    margin: 0 0 8px;
    color: var(--text);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 27px;
    font-weight: 700;
}

.auth-copy {
    color: #aab9ca;
    line-height: 1.7;
    font-size: 14px;
}

.feature-list {
    display: grid;
    gap: 15px;
    margin-top: 28px;
}

.feature {
    display: flex;
    align-items: flex-start;
    gap: 12px;
}

.feature-icon {
    display: grid;
    place-items: center;
    width: 32px;
    height: 32px;
    flex: 0 0 32px;
    border: 1px solid rgba(25,201,154,.18);
    border-radius: 9px;
    background: rgba(25,201,154,.07);
}

.feature-text strong {
    display: block;
    margin-bottom: 3px;
    color: #eaf0f6;
    font-size: 13px;
}

.feature-text span {
    display: block;
    color: #899bb0;
    font-size: 12px;
    line-height: 1.5;
}

.login-panel {
    padding: 26px;
    border: 1px solid var(--border);
    border-radius: 20px;
    background: #0d1b2d;
}

.login-title {
    color: #5ee0bb;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 27px;
    font-weight: 700;
}

.login-copy {
    margin: 5px 0 22px;
    color: #899bb0;
    font-size: 13px;
}

/* -------------------- ACCOUNT CREATED -------------------- */

.account-created {
    padding: 18px 20px;
    margin-bottom: 22px;
    border: 1px solid rgba(25,201,154,.34);
    border-radius: 16px;
    background: #0d282b;
}

.account-created-label {
    color: #62dfba;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .6px;
}

.account-created-number {
    display: block;
    margin: 8px 0;
    color: #e9fff8;
    font-family: monospace;
    font-size: 25px;
    font-weight: 700;
    letter-spacing: 1px;
    overflow-wrap: anywhere;
}

.account-created-note {
    color: #e2b458;
    font-size: 12px;
}

.account-created-bottom {
    margin-top: -10px;
    border-top: 0;
    border-radius: 0 0 16px 16px;
}

div[data-testid="stCodeBlock"] {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

div[data-testid="stCodeBlock"] pre {
    border: 1px solid rgba(25,201,154,.34) !important;
    border-top: 0 !important;
    border-radius: 0 !important;
    background: #102c30 !important;
    color: #e9fff8 !important;
    padding: 13px 16px !important;
}

div[data-testid="stCodeBlock"] code {
    color: #e9fff8 !important;
    font-family: 'Space Grotesk', monospace !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
}

/* -------------------- HEADINGS -------------------- */

.page-heading {
    display: flex;
    align-items: center;
    gap: 11px;
    margin: 5px 0 4px;
    color: var(--text);
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(24px, 2.8vw, 31px);
    font-weight: 700;
}

.page-heading::before {
    content: "";
    width: 4px;
    height: 28px;
    border-radius: 4px;
    background: linear-gradient(#19c99a, #2bc6df);
}

.page-subtitle {
    margin: 0 0 20px;
    color: #8799ad;
    font-size: 13px;
}

/* -------------------- CARDS -------------------- */

.surface {
    padding: 25px;
    border: 1px solid var(--border);
    border-radius: 18px;
    background: #0d1b2d;
    box-shadow: 0 14px 35px rgba(0,0,0,.13);
}

.surface-title {
    margin-bottom: 7px;
    color: var(--text);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 700;
}

.surface-copy {
    color: #91a2b5;
    font-size: 13px;
    line-height: 1.65;
}

/* -------------------- METRICS -------------------- */

.metric {
    height: 100%;
    padding: 21px;
    border: 1px solid var(--border);
    border-radius: 17px;
    background: #0d1b2d;
    box-shadow: 0 12px 28px rgba(0,0,0,.13);
    transition: transform .18s ease, border-color .18s ease;
}

.metric:hover {
    transform: translateY(-3px);
    border-color: #28516a;
}

.metric-label {
    color: #899bb0;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .75px;
    text-transform: uppercase;
}

.metric-value {
    margin-top: 8px;
    color: #51dbb2;
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(25px, 3vw, 34px);
    font-weight: 700;
}

.metric-value.cyan { color: #45cce2; }
.metric-value.orange { color: #f29a45; }

/* -------------------- BUTTONS -------------------- */

div[data-testid="stButton"] > button {
    width: 100%;
    min-height: 45px;
    border: 1px solid rgba(25,201,154,.25) !important;
    border-radius: 11px !important;
    background: linear-gradient(90deg, #15b98f, #109db8) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    box-shadow: none !important;
    transition: transform .16s ease, filter .16s ease;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px);
    filter: brightness(1.07);
}

div[data-testid="stButton"] > button p {
    color: #ffffff !important;
}

/* -------------------- INPUTS -------------------- */

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    min-height: 47px !important;
    background: #14243a !important;
    border: 1px solid #30445d !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    font-size: 14px !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: #25caa0 !important;
    box-shadow: 0 0 0 2px rgba(25,201,154,.12) !important;
}

div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stNumberInput"] input::placeholder {
    color: #71839a !important;
}

div[data-testid="stNumberInput"] button {
    background: #1b2c43 !important;
    color: #b8c6d6 !important;
    border: none !important;
}

/* -------------------- TABS -------------------- */

div[data-testid="stTabs"] [role="tablist"] {
    gap: 4px;
    border-bottom: 1px solid #1c2c40;
}

div[data-testid="stTabs"] button {
    color: #91a1b4 !important;
    font-weight: 600 !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #5fe0bc !important;
}

/* -------------------- SIDEBAR -------------------- */

[data-testid="stSidebar"] {
    background: #06111e !important;
    border-right: 1px solid #15263a;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 20px 14px !important;
}

.sidebar-brand {
    margin-bottom: 16px;
    color: #5ee0bb;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 700;
}

.sidebar-account {
    padding: 14px;
    border: 1px solid #1a2b3f;
    border-radius: 13px;
    background: #0b1929;
}

.sidebar-name {
    color: #f3f6f9;
    font-size: 14px;
    font-weight: 700;
}

.sidebar-number {
    margin-top: 6px;
    color: #42c8df;
    font-family: monospace;
    font-size: 10px;
    overflow-wrap: anywhere;
}

.sidebar-status {
    margin-top: 9px;
    color: #54dcb5;
    font-size: 10px;
    font-weight: 700;
}

.sidebar-divider {
    height: 1px;
    margin: 16px 0;
    background: #17283b;
}

[data-testid="stSidebar"] div[data-testid="stButton"] > button {
    min-height: 42px !important;
    margin: 2px 0 !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    color: #a9b8c8 !important;
    box-shadow: none !important;
    text-align: left !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
    background: #10263a !important;
    border-color: #1b4050 !important;
    color: #e9f3f8 !important;
    transform: none;
}

/* -------------------- TRANSACTIONS -------------------- */

.transaction {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 15px 17px;
    margin-bottom: 9px;
    border: 1px solid #1a2a3e;
    border-radius: 13px;
    background: #0c1a2b;
}

.transaction-main {
    min-width: 0;
}

.transaction-action {
    color: #e7edf4;
    font-size: 13px;
    font-weight: 700;
}

.transaction-time {
    margin-top: 4px;
    color: #71839a;
    font-size: 10px;
}

.transaction-amount {
    white-space: nowrap;
    font-family: monospace;
    font-size: 15px;
    font-weight: 700;
}

/* -------------------- NOTICES -------------------- */

.notice {
    padding: 13px 15px;
    border: 1px solid #1d3e4b;
    border-radius: 11px;
    background: #0b202b;
    color: #9cc3ce;
    font-size: 12px;
    line-height: 1.55;
}

.danger-zone {
    padding: 18px;
    border: 1px solid rgba(239,107,122,.22);
    border-radius: 14px;
    background: rgba(239,107,122,.055);
}

.danger-zone-title {
    color: #f29aa5;
    font-weight: 700;
}

.danger-zone-copy {
    margin-top: 5px;
    color: #9aa9ba;
    font-size: 12px;
    line-height: 1.6;
}

/* -------------------- FOOTER -------------------- */

.footer {
    margin-top: 35px;
    padding-top: 18px;
    border-top: 1px solid #15263a;
    color: #617389;
    font-size: 10px;
    text-align: center;
}

/* -------------------- RESPONSIVE -------------------- */

@media (max-width: 1000px) {
    .block-container {
        padding: 20px 18px 35px !important;
    }

    .hero {
        min-height: 190px;
    }

    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
    }

    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        min-width: min(100%, 360px) !important;
        flex: 1 1 360px !important;
    }
}

@media (max-width: 700px) {
    .block-container {
        padding: 14px 12px 30px !important;
    }

    .hero {
        min-height: 175px;
        padding: 25px 20px;
        border-radius: 18px;
    }

    .hero h1 {
        font-size: 31px !important;
        letter-spacing: -1px;
    }

    .hero p {
        font-size: 12px;
    }

    .auth-surface,
    .login-panel,
    .surface {
        padding: 19px;
        border-radius: 16px;
    }

    .transaction {
        align-items: flex-start;
        flex-direction: column;
    }

    .transaction-amount {
        align-self: flex-end;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
"""), unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "account": None,
    "pin": None,
    "page": "Dashboard",
    "created_account_number": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# DATABASE
# ============================================================
@st.cache_resource
def get_bank():
    return BankSystem()


try:
    bank = get_bank()
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()


# ============================================================
# HELPERS
# ============================================================
def money(value):
    return f"₹{float(value):,.2f}"


def refresh_account():
    if st.session_state.account and st.session_state.pin:
        fresh = bank.read_account(
            st.session_state.account.get_account_number(),
            st.session_state.pin
        )
        if fresh:
            st.session_state.account = fresh


def get_logs():
    if not st.session_state.account:
        return []

    return bank.get_single_audit_logs(
        st.session_state.account.get_account_number()
    ) or []


def do_login(account_number, pin):
    account = bank.read_account(
        account_number.strip(),
        pin.strip()
    )

    if account:
        st.session_state.account = account
        st.session_state.pin = pin.strip()
        st.session_state.page = "Dashboard"
        st.session_state.created_account_number = None
        st.toast("Welcome back. Login successful.")
        time.sleep(.35)
        st.rerun()

    st.error("Invalid account number or PIN.")


def do_logout():
    st.session_state.account = None
    st.session_state.pin = None
    st.session_state.page = "Dashboard"
    st.toast("You have been logged out.")
    time.sleep(.25)
    st.rerun()


# ============================================================
# HERO
# ============================================================
st.markdown(textwrap.dedent("""
<div class="hero">
    <div class="hero-content">
        <div class="hero-badge">🔐 Secure Banking Platform</div>
        <h1>🏦 Banking Management System</h1>
        <p>
            A clean digital banking experience for account management,
            secure transactions, live balances, and complete activity history.
        </p>
    </div>
</div>
"""), unsafe_allow_html=True)


# ============================================================
# AUTHENTICATION SCREEN
# ============================================================
if not st.session_state.account:

    # This placeholder intentionally comes BEFORE the form.
    # Therefore a newly-created account number appears above the form,
    # not below it.
    created_placeholder = st.empty()

    if st.session_state.created_account_number:
        # Keep the success message as HTML, but render the account number
        # with st.code() so Streamlit provides its built-in Copy button.
        created_placeholder.markdown("""
        <div class="account-created" style="margin-bottom:10px;">
            <div class="account-created-label">✓ ACCOUNT CREATED SUCCESSFULLY</div>
        </div>
        """, unsafe_allow_html=True)

        st.code(
            str(st.session_state.created_account_number),
            language=None
        )

        st.markdown("""
        <div class="account-created account-created-bottom">
            <div class="account-created-note">
                ⚠ Save this account number securely. You need it to sign in.
            </div>
        </div>
        """, unsafe_allow_html=True)

    auth_left, auth_right = st.columns(
        [1.05, 1],
        gap="large"
    )

    with auth_left:
        st.markdown(
        """
        <div class="auth-surface">
            <div class="auth-title">Banking without the clutter.</div>
            <div class="auth-copy">
                Everything important is available from one focused dashboard.
                No unnecessary screens, no confusing visual hierarchy.
            </div>
            <div class="feature-list">
                <div class="feature">
                    <div class="feature-icon">🔐</div>
                    <div class="feature-text">
                        <strong>PIN-protected access</strong>
                        <span>Secure authentication using your existing banking backend.</span>
                    </div>
                </div>
                <div class="feature">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-text">
                        <strong>Instant transactions</strong>
                        <span>Deposit and withdraw funds directly from your account.</span>
                    </div>
                </div>
                <div class="feature">
                    <div class="feature-icon">📊</div>
                    <div class="feature-text">
                        <strong>Clear financial overview</strong>
                        <span>Balance, deposits, withdrawals and recent activity at a glance.</span>
                    </div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🧾</div>
                    <div class="feature-text">
                        <strong>Complete activity history</strong>
                        <span>Review the audit records generated by your banking system.</span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    with auth_right:
        login_tab, create_tab = st.tabs(["🔐 Sign In", "✨ Create Account"])

        with login_tab:
            st.markdown(textwrap.dedent("""
            <div class="login-panel">
                <div class="login-title">Welcome back</div>
                <div style="color:#8191a5;font-size:13px;margin-bottom:20px;">
                    Sign in to access your banking dashboard.
                </div>
            """), unsafe_allow_html=True)

            account_number = st.text_input(
                "Account Number",
                placeholder="Enter your account number",
                key="login_account"
            )

            pin = st.text_input(
                "4-digit PIN",
                type="password",
                max_chars=4,
                placeholder="••••",
                key="login_pin"
            )

            if st.button(
                "Sign In Securely  →",
                use_container_width=True,
                type="primary",
                key="signin_button"
            ):
                if not account_number.strip():
                    st.warning("Enter your account number.")
                elif len(pin) != 4 or not pin.isdigit():
                    st.warning("PIN must contain exactly 4 digits.")
                else:
                    with st.spinner("Verifying your credentials..."):
                        time.sleep(.35)
                        do_login(account_number, pin)

            st.markdown("</div>", unsafe_allow_html=True)

        with create_tab:
            st.markdown(textwrap.dedent("""
            <div class="login-panel">
                <div class="login-title">Open a new account</div>
                <div style="color:#8191a5;font-size:13px;margin-bottom:20px;">
                    Create your account in a few seconds.
                </div>
            """), unsafe_allow_html=True)

            name = st.text_input(
                "Full Name",
                placeholder="Enter your name",
                key="create_name"
            )

            new_pin = st.text_input(
                "Create 4-digit PIN",
                type="password",
                max_chars=4,
                placeholder="••••",
                key="create_pin"
            )

            confirm_pin = st.text_input(
                "Confirm PIN",
                type="password",
                max_chars=4,
                placeholder="••••",
                key="confirm_pin"
            )

            if st.button(
                "Create Account  →",
                use_container_width=True,
                type="primary",
                key="create_button"
            ):
                if not name.strip():
                    st.warning("Name cannot be empty.")
                elif len(new_pin) != 4 or not new_pin.isdigit():
                    st.warning("PIN must contain exactly 4 digits.")
                elif new_pin != confirm_pin:
                    st.error("PINs do not match.")
                else:
                    with st.spinner("Creating your account..."):
                        time.sleep(.35)
                        new_account = bank.create_account(
                            name.strip(),
                            new_pin
                        )

                    if new_account:
                        st.session_state.created_account_number = (
                            new_account.get_account_number()
                        )
                        created_placeholder.empty()
                        st.rerun()
                    else:
                        st.error("Account creation failed.")

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(textwrap.dedent("""
    <div class="footer">
        MyBank • Python + PostgreSQL • Streamlit
    </div>
    """), unsafe_allow_html=True)

    st.stop()


# ============================================================
# LOGGED-IN STATE
# ============================================================
account = st.session_state.account


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand">🏦 MyBank</div>',
        unsafe_allow_html=True
    )

    st.markdown(textwrap.dedent(f"""
    <div class="sidebar-account">
        <div class="sidebar-name">{account.get_name()}</div>
        <div class="sidebar-number">{account.get_account_number()}</div>
        <div class="sidebar-status">● SESSION ACTIVE</div>
    </div>
    """), unsafe_allow_html=True)

    navigation = {
        "Overview": "Dashboard",
        "Deposit": "Deposit",
        "Withdraw": "Withdraw",
        "Transactions": "Transactions",
        "Account Settings": "Account",
    }

    for label, page in navigation.items():
        icon = {
            "Overview": "⌂",
            "Deposit": "＋",
            "Withdraw": "−",
            "Transactions": "▤",
            "Account Settings": "⚙",
        }[label]

        if st.button(
            f"{icon}  {label}",
            use_container_width=True,
            key=f"sidebar_{page}"
        ):
            st.session_state.page = page
            st.rerun()

    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True
    )

    refresh_col, logout_col = st.columns(2)

    with refresh_col:
        if st.button(
            "↻ Refresh",
            use_container_width=True,
            key="sidebar_refresh"
        ):
            refresh_account()
            st.toast("Account data refreshed.")
            time.sleep(.25)
            st.rerun()

    with logout_col:
        if st.button(
            "Logout",
            use_container_width=True,
            key="sidebar_logout"
        ):
            do_logout()


# ============================================================
# DASHBOARD
# ============================================================
if st.session_state.page == "Dashboard":

    refresh_account()
    account = st.session_state.account
    logs = get_logs()

    st.markdown(
        f'<div class="page-heading">Welcome back, {account.get_name()}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="page-subtitle">'
        f'Account {account.get_account_number()} · '
        f'{datetime.now().strftime("%d %b %Y, %I:%M %p")}'
        f'</div>',
        unsafe_allow_html=True
    )

    balance = account.get_balance()

    deposits = sum(
        float(log["amount"] or 0)
        for log in logs
        if "deposit" in str(log["action"]).lower()
    )

    withdrawals = sum(
        float(log["amount"] or 0)
        for log in logs
        if "withdraw" in str(log["action"]).lower()
    )

    metric_1, metric_2, metric_3 = st.columns(
        3,
        gap="medium"
    )

    with metric_1:
        st.markdown(textwrap.dedent(f"""
        <div class="metric">
            <div class="metric-label">Available Balance</div>
            <div class="metric-value">{money(balance)}</div>
        </div>
        """), unsafe_allow_html=True)

    with metric_2:
        st.markdown(textwrap.dedent(f"""
        <div class="metric">
            <div class="metric-label">Total Deposited</div>
            <div class="metric-value cyan">{money(deposits)}</div>
        </div>
        """), unsafe_allow_html=True)

    with metric_3:
        st.markdown(textwrap.dedent(f"""
        <div class="metric">
            <div class="metric-label">Total Withdrawn</div>
            <div class="metric-value orange">{money(withdrawals)}</div>
        </div>
        """), unsafe_allow_html=True)

    st.markdown(
        '<div class="page-heading" style="margin-top:34px;">Quick Actions</div>',
        unsafe_allow_html=True
    )

    action_1, action_2, action_3 = st.columns(
        3,
        gap="medium"
    )

    with action_1:
        if st.button(
            "Deposit Money  →",
            use_container_width=True,
            key="dashboard_deposit"
        ):
            st.session_state.page = "Deposit"
            st.rerun()

    with action_2:
        if st.button(
            "Withdraw Money  →",
            use_container_width=True,
            key="dashboard_withdraw"
        ):
            st.session_state.page = "Withdraw"
            st.rerun()

    with action_3:
        if st.button(
            "View Transactions  →",
            use_container_width=True,
            key="dashboard_transactions"
        ):
            st.session_state.page = "Transactions"
            st.rerun()

    st.markdown(
        '<div class="page-heading" style="margin-top:34px;">Recent Activity</div>',
        unsafe_allow_html=True
    )

    if logs:
        for index, log in enumerate(logs[:6]):
            action = str(log["action"])
            amount = float(log["amount"] or 0)
            timestamp = log["time_stamp"]

            if hasattr(timestamp, "strftime"):
                timestamp = timestamp.strftime(
                    "%d %b %Y · %I:%M %p"
                )

            lower_action = action.lower()

            if "deposit" in lower_action:
                icon = "↑"
                color = "#55e0b6"
                sign = "+"
            elif "withdraw" in lower_action:
                icon = "↓"
                color = "#fb923c"
                sign = "−"
            elif "deleted" in lower_action:
                icon = "×"
                color = "#fb7185"
                sign = ""
            else:
                icon = "•"
                color = "#4bd7ef"
                sign = ""

            st.markdown(textwrap.dedent(f"""
            <div class="transaction" style="animation-delay:{index * .05}s;">
                <div class="transaction-main">
                    <div class="transaction-action">
                        <span style="color:{color};font-size:18px;">{icon}</span>
                        &nbsp;{action}
                    </div>
                    <div class="transaction-time">{timestamp}</div>
                </div>
                <div class="transaction-amount" style="color:{color};">
                    {sign}{money(amount)}
                </div>
            </div>
            """), unsafe_allow_html=True)
    else:
        st.markdown(textwrap.dedent("""
        <div class="notice">
            No activity yet. Your deposits, withdrawals and account actions
            will appear here.
        </div>
        """), unsafe_allow_html=True)


# ============================================================
# DEPOSIT
# ============================================================
elif st.session_state.page == "Deposit":

    st.markdown(
        '<div class="page-heading">Deposit Funds</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Add money to your account securely.</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(
        [1.15, .85],
        gap="large"
    )

    with left:
        st.markdown(textwrap.dedent("""
        <div class="surface">
            <div class="surface-title">Deposit amount</div>
            <div class="surface-copy" style="margin-bottom:18px;">
                Enter the amount you want to add to your current balance.
            </div>
        """), unsafe_allow_html=True)

        amount = st.number_input(
            "Amount (₹)",
            min_value=1.0,
            step=100.0,
            format="%.2f",
            key="deposit_amount"
        )

        if st.button(
            "Deposit Securely  →",
            use_container_width=True,
            type="primary",
            key="deposit_submit"
        ):
            with st.spinner("Processing deposit..."):
                time.sleep(.35)
                success = bank.deposit(
                    account.get_account_number(),
                    st.session_state.pin,
                    amount
                )

            if success:
                refresh_account()
                st.toast(
                    f"{money(amount)} deposited successfully."
                )
                time.sleep(.35)
                st.rerun()
            else:
                st.error("Deposit failed. Please try again.")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        refresh_account()
        st.markdown(textwrap.dedent(f"""
        <div class="metric">
            <div class="metric-label">Current Balance</div>
            <div class="metric-value">{money(account.get_balance())}</div>
        </div>
        <div style="height:14px;"></div>
        <div class="notice">
            Your transaction will be recorded in the existing audit table.
        </div>
        """), unsafe_allow_html=True)


# ============================================================
# WITHDRAW
# ============================================================
elif st.session_state.page == "Withdraw":

    st.markdown(
        '<div class="page-heading">Withdraw Funds</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Withdraw available funds from your account.</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(
        [1.15, .85],
        gap="large"
    )

    with left:
        st.markdown(textwrap.dedent("""
        <div class="surface">
            <div class="surface-title">Withdrawal amount</div>
            <div class="surface-copy" style="margin-bottom:18px;">
                You can withdraw only an amount that is available in your balance.
            </div>
        """), unsafe_allow_html=True)

        amount = st.number_input(
            "Amount (₹)",
            min_value=1.0,
            step=100.0,
            format="%.2f",
            key="withdraw_amount"
        )

        if st.button(
            "Withdraw Securely  →",
            use_container_width=True,
            type="primary",
            key="withdraw_submit"
        ):
            refresh_account()

            if amount > account.get_balance():
                st.error(
                    f"Insufficient balance. Available: "
                    f"{money(account.get_balance())}"
                )
            else:
                with st.spinner("Processing withdrawal..."):
                    time.sleep(.35)
                    success = bank.withdraw(
                        account.get_account_number(),
                        st.session_state.pin,
                        amount
                    )

                if success:
                    refresh_account()
                    st.toast(
                        f"{money(amount)} withdrawn successfully."
                    )
                    time.sleep(.35)
                    st.rerun()
                else:
                    st.error("Withdrawal failed. Please try again.")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        refresh_account()
        st.markdown(textwrap.dedent(f"""
        <div class="metric">
            <div class="metric-label">Available Balance</div>
            <div class="metric-value">{money(account.get_balance())}</div>
        </div>
        <div style="height:14px;"></div>
        <div class="notice">
            Withdrawals cannot exceed your current available balance.
        </div>
        """), unsafe_allow_html=True)


# ============================================================
# TRANSACTIONS
# ============================================================
elif st.session_state.page == "Transactions":

    st.markdown(
        '<div class="page-heading">Transaction History</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">A complete view of your account activity.</div>',
        unsafe_allow_html=True
    )

    logs = get_logs()

    if not logs:
        st.markdown(textwrap.dedent("""
        <div class="surface">
            <div class="surface-title">No transactions yet</div>
            <div class="surface-copy">
                Your account activity will appear here after your first transaction.
            </div>
        </div>
        """), unsafe_allow_html=True)
    else:
        for index, log in enumerate(logs):
            action = str(log["action"])
            amount = float(log["amount"] or 0)
            timestamp = log["time_stamp"]

            if hasattr(timestamp, "strftime"):
                timestamp = timestamp.strftime(
                    "%d %B %Y · %I:%M:%S %p"
                )

            lower_action = action.lower()

            if "deposit" in lower_action:
                icon = "↑"
                color = "#55e0b6"
                sign = "+"
            elif "withdraw" in lower_action:
                icon = "↓"
                color = "#fb923c"
                sign = "−"
            elif "balance" in lower_action:
                icon = "•"
                color = "#4bd7ef"
                sign = ""
            else:
                icon = "•"
                color = "#aab7c8"
                sign = ""

            st.markdown(textwrap.dedent(f"""
            <div class="transaction" style="animation-delay:{index * .035}s;">
                <div class="transaction-main">
                    <div class="transaction-action">
                        <span style="color:{color};font-size:20px;">{icon}</span>
                        &nbsp;{action}
                    </div>
                    <div class="transaction-time">{timestamp}</div>
                </div>
                <div class="transaction-amount" style="color:{color};">
                    {sign}{money(amount)}
                </div>
            </div>
            """), unsafe_allow_html=True)


# ============================================================
# ACCOUNT SETTINGS
# ============================================================
elif st.session_state.page == "Account":

    st.markdown(
        '<div class="page-heading">Account Settings</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Manage your profile and account security.</div>',
        unsafe_allow_html=True
    )

    info_tab, name_tab, pin_tab, close_tab = st.tabs([
        "Account Info",
        "Update Name",
        "Change PIN",
        "Close Account",
    ])

    with info_tab:
        refresh_account()

        st.markdown(textwrap.dedent("""
        <div class="surface">
            <div class="surface-title">Account information</div>
        """), unsafe_allow_html=True)

        info_1, info_2 = st.columns(2, gap="large")

        with info_1:
            st.markdown(
                f"**Account Holder**  \n"
                f"<span style='color:#5ee7bd;font-size:19px;font-weight:700;'>"
                f"{account.get_name()}</span>",
                unsafe_allow_html=True
            )

        with info_2:
            st.markdown(
                f"**Account Number**  \n"
                f"<span style='color:#4bd7ef;font-family:monospace;"
                f"font-size:17px;font-weight:700;overflow-wrap:anywhere;'>"
                f"{account.get_account_number()}</span>",
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            f"**Current Balance**  \n"
            f"<span style='color:#55e0b6;font-size:27px;font-weight:700;'>"
            f"{money(account.get_balance())}</span>",
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with name_tab:
        st.markdown(textwrap.dedent("""
        <div class="surface">
            <div class="surface-title">Update your name</div>
            <div class="surface-copy" style="margin-bottom:18px;">
                Change the account holder name stored in your account.
            </div>
        """), unsafe_allow_html=True)

        new_name = st.text_input(
            "New Name",
            value=account.get_name(),
            key="new_account_name"
        )

        if st.button(
            "Save Name",
            use_container_width=True,
            type="primary",
            key="update_name"
        ):
            if not new_name.strip():
                st.warning("Name cannot be empty.")
            else:
                account.set_name(new_name.strip())

                if bank.update_account(account):
                    Audit.log_action(
                        account.get_account_number(),
                        account.get_name(),
                        "Account Info Updated",
                        0.0
                    )
                    refresh_account()
                    st.toast("Account name updated.")
                    time.sleep(.35)
                    st.rerun()
                else:
                    st.error("Could not update the account.")

        st.markdown("</div>", unsafe_allow_html=True)

    with pin_tab:
        st.markdown(textwrap.dedent("""
        <div class="surface">
            <div class="surface-title">Change your PIN</div>
            <div class="surface-copy" style="margin-bottom:18px;">
                Your new PIN must contain exactly four digits.
            </div>
        """), unsafe_allow_html=True)

        old_pin = st.text_input(
            "Current PIN",
            type="password",
            max_chars=4,
            key="old_pin"
        )

        new_pin = st.text_input(
            "New 4-digit PIN",
            type="password",
            max_chars=4,
            key="new_pin"
        )

        confirm_pin = st.text_input(
            "Confirm New PIN",
            type="password",
            max_chars=4,
            key="confirm_new_pin"
        )

        if st.button(
            "Update PIN",
            use_container_width=True,
            type="primary",
            key="update_pin"
        ):
            if old_pin != st.session_state.pin:
                st.error("Current PIN is incorrect.")
            elif len(new_pin) != 4 or not new_pin.isdigit():
                st.error("New PIN must contain exactly 4 digits.")
            elif new_pin != confirm_pin:
                st.error("New PINs do not match.")
            else:
                account.set_pin(new_pin)

                if bank.update_account(account):
                    Audit.log_action(
                        account.get_account_number(),
                        account.get_name(),
                        "PIN Updated",
                        0.0
                    )
                    st.session_state.pin = new_pin
                    st.toast("PIN updated successfully.")
                    time.sleep(.35)
                    st.rerun()
                else:
                    st.error("Could not update the PIN.")

        st.markdown("</div>", unsafe_allow_html=True)

    with close_tab:
        st.markdown(textwrap.dedent("""
        <div class="danger-zone">
            <div class="danger-zone-title">Permanent account closure</div>
            <div class="danger-zone-copy">
                Closing your account permanently removes the account and its
                audit records using your existing backend logic. This action
                cannot be undone.
            </div>
        </div>
        """), unsafe_allow_html=True)

        st.write("")

        confirm_delete = st.checkbox(
            "I understand that this action cannot be undone.",
            key="confirm_delete"
        )

        delete_pin = st.text_input(
            "Enter your PIN to confirm",
            type="password",
            max_chars=4,
            key="delete_pin"
        )

        if st.button(
            "Permanently Close Account",
            use_container_width=True,
            key="delete_account"
        ):
            if not confirm_delete:
                st.warning("Please confirm the checkbox first.")
            elif delete_pin != st.session_state.pin:
                st.error("Incorrect PIN.")
            else:
                with st.spinner("Closing account securely..."):
                    time.sleep(.5)
                    success = bank.delete_account(
                        account.get_account_number(),
                        st.session_state.pin
                    )

                if success:
                    st.session_state.account = None
                    st.session_state.pin = None
                    st.session_state.page = "Dashboard"
                    st.toast(
                        "Account closed successfully."
                    )
                    time.sleep(.5)
                    st.rerun()
                else:
                    st.error("Could not close the account.")


# ============================================================
# FOOTER
# ============================================================
st.markdown(textwrap.dedent("""
<div class="footer">
    <strong style="color:#8292a7;">MyBank</strong>
    &nbsp;·&nbsp; Banking Management System
    &nbsp;·&nbsp; Python + PostgreSQL + Streamlit
</div>
"""), unsafe_allow_html=True)