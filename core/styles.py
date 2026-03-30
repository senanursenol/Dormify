import streamlit as st


def _inject(css: str) -> None:
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def load_base_styles() -> None:
    _inject(
        """
        #MainMenu, footer, header {
            visibility: hidden;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .stButton > button {
            width: 100%;
            border: none;
            font-weight: 700;
            transition: all 0.25s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
        }

        [data-testid="collapsedControl"] {
            display: none;
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="stSidebarNav"] {
            display: none;
        }
        """
    )


def load_app_background() -> None:
    _inject(
        """
        .stApp {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 25%, #bfdbfe 50%, #93c5fd 75%, #60a5fa 100%);
        }

        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 25%, #bfdbfe 50%, #93c5fd 75%, #60a5fa 100%);
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        """
    )


def load_soft_background() -> None:
    _inject(
        """
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f8fafc 0%, #eef4ff 50%, #dbeafe 100%);
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        """
    )


def load_main_card_styles() -> None:
    _inject(
        """
        .main-card {
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 3rem 2.5rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.10);
            max-width: 440px;
            margin: 80px auto;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.4);
        }

        .custom-card, .modern-menu-card {
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.10);
            border: 1px solid rgba(255,255,255,0.4);
            margin-bottom: 20px;
        }

        .menu-item-pill {
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            color: #166534;
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 0.9rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .afiyet-text {
            color: #15803d;
            font-size: 0.75rem;
            font-weight: 800;
            margin-top: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-align: center;
        }

        .logo {
            font-size: 2rem;
            font-weight: 700;
            color: #3b82f6;
            margin-bottom: 1rem;
        }

        .title {
            text-align: center;
            font-size: 1.8rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            text-align: center;
            color: #64748b;
            font-size: 1rem;
            margin-bottom: 2rem;
        }

        .support {
            margin-top: 1.5rem;
            color: #64748b;
            font-size: 0.95rem;
        }

        .divider {
            text-align: center;
            color: #94a3b8;
            margin: 1.5rem 0 1rem 0;
            font-size: 0.9rem;
        }
        """
    )


def load_login_page_styles() -> None:
    _inject(
        """
        .block-container {
            max-width: 700px;
        }

        .bg-blur-1, .bg-blur-2 {
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            z-index: -1;
            animation: floatBlob 8s ease-in-out infinite;
        }

        .bg-blur-1 {
            width: 220px;
            height: 220px;
            background: rgba(59, 130, 246, 0.18);
            top: 10%;
            left: 10%;
        }

        .bg-blur-2 {
            width: 180px;
            height: 180px;
            background: rgba(96, 165, 250, 0.16);
            bottom: 12%;
            right: 12%;
            animation-delay: 2s;
        }

        @keyframes floatBlob {
            0%, 100% {
                transform: translateY(0px) translateX(0px);
            }
            50% {
                transform: translateY(-14px) translateX(8px);
            }
        }

        .login-card {
            background: rgba(255, 255, 255, 0.94);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255,255,255,0.55);
            border-radius: 26px;
            padding: 42px 30px 28px 30px;
            box-shadow: 0 20px 50px rgba(15, 23, 42, 0.12);
            margin-bottom: 16px;
        }

        .icon-wrap {
            display: flex;
            justify-content: center;
            margin-bottom: 12px;
        }

        .icon-box {
            width: 70px;
            height: 70px;
            border-radius: 20px;
            background: linear-gradient(135deg, #3b82f6, #60a5fa);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            color: white;
            box-shadow: 0 12px 28px rgba(59,130,246,0.30);
        }

        .title {
            text-align: center;
            font-size: 1.7rem;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 6px;
        }

        .subtitle {
            text-align: center;
            color: #64748b;
            font-size: 0.95rem;
            margin-bottom: 24px;
        }

        .field-label {
            font-size: 0.88rem;
            font-weight: 600;
            color: #334155;
            margin-bottom: 6px;
            margin-top: 8px;
        }

        .stTextInput > div > div > input {
            height: 48px;
            border-radius: 12px;
            border: 1px solid #dbe2ea;
            background: white;
            font-size: 0.96rem;
        }

        .stButton > button {
            height: 52px;
            border-radius: 14px;
            font-size: 1rem;
            background: linear-gradient(135deg, #3b82f6, #60a5fa);
            color: white;
            box-shadow: 0 10px 24px rgba(59,130,246,0.28);
            margin-top: 10px;
        }

        .back-btn .stButton > button {
            background: white !important;
            color: #2563eb !important;
            border: 1.5px solid #bfdbfe !important;
            box-shadow: 0 8px 18px rgba(148,163,184,0.12) !important;
            margin-top: 8px;
        }

        .info-note {
            margin-top: 16px;
            text-align: center;
            color: #64748b;
            font-size: 0.86rem;
            line-height: 1.5;
        }

        @media (max-width: 768px) {
            .login-card {
                padding: 34px 20px 24px 20px;
            }

            .title {
                font-size: 1.5rem;
            }
        }
        """
    )


def render_login_background_blobs() -> None:
    st.markdown(
        """
        <div class="bg-blur-1"></div>
        <div class="bg-blur-2"></div>
        """,
        unsafe_allow_html=True,
    )


def load_student_panel_styles() -> None:
    _inject(
        """
        .block-container {
            padding-top: 0.8rem;
            padding-bottom: 2rem;
            max-width: 1280px;
        }

        .topbar-wrap {
            background: rgba(255,255,255,0.96);
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 14px 22px;
            box-shadow: 0 4px 18px rgba(15,23,42,0.05);
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            min-height: 82px;
        }

        div[data-testid="stPopover"] > button {
            width: 100%;
            height: 48px;
            border-radius: 999px;
            border: none !important;
            background: linear-gradient(135deg, #2563eb, #60a5fa) !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            box-shadow: 0 10px 24px rgba(59,130,246,0.22);
            padding: 0 18px !important;
        }

        .welcome-wrap {
            text-align: center;
            margin: 20px 0 34px 0;
        }

        .welcome-title {
            font-size: 2.15rem;
            font-weight: 800;
            color: #1f2937;
            margin-bottom: 8px;
        }

        .welcome-subtitle {
            color: #64748b;
            font-size: 1.05rem;
        }

        .feature-card {
            background: rgba(255,255,255,0.96);
            border: 1px solid #eef2f7;
            border-radius: 28px;
            padding: 36px 28px;
            box-shadow: 0 14px 40px rgba(15,23,42,0.10);
            text-align: center;
            min-height: 255px;
        }

        .icon-badge {
            width: 82px;
            height: 82px;
            border-radius: 22px;
            background: linear-gradient(135deg, #60a5fa, #3b82f6);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
            margin: 0 auto 20px auto;
            box-shadow: 0 12px 30px rgba(59,130,246,0.24);
        }

        .card-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 12px;
        }

        .card-text {
            color: #64748b;
            font-size: 1rem;
            line-height: 1.8;
            margin: 0 auto 20px auto;
        }

        .menu-btn .stButton > button {
            background: white;
            color: #2563eb;
            border: 1.5px solid #bfdbfe;
            box-shadow: 0 8px 18px rgba(148,163,184,0.12);
            margin-top: 6px;
        }

        .primary-btn .stButton > button {
            background: linear-gradient(135deg, #60a5fa, #3b82f6);
            color: white;
            box-shadow: 0 10px 24px rgba(59,130,246,0.28);
            height: 52px;
            border-radius: 16px;
        }

        .info-box {
            margin-top: 18px;
            background: rgba(239,246,255,0.9);
            border: 1px solid #dbeafe;
            border-radius: 16px;
            padding: 14px 16px;
            color: #1e3a8a;
            font-size: 0.95rem;
            text-align: center;
        }
        """
    )


def load_student_fault_styles() -> None:
    _inject(
        """
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 760px;
        }

        .header-card {
            background: rgba(255,255,255,0.96);
            border: 1px solid #eef2f7;
            border-radius: 24px;
            padding: 2.2rem 2rem;
            box-shadow: 0 12px 40px rgba(15,23,42,0.08);
            text-align: center;
            margin-bottom: 1.4rem;
        }

        .header-icon {
            width: 72px;
            height: 72px;
            background: linear-gradient(135deg, #ef4444, #f87171);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem auto;
            font-size: 1.7rem;
            color: white;
            box-shadow: 0 10px 28px rgba(239,68,68,0.25);
        }

        .header-title {
            font-size: 1.7rem;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 0.45rem;
        }

        .header-subtitle {
            color: #64748b;
            font-size: 1rem;
            line-height: 1.6;
        }

        .form-shell {
            background: rgba(255,255,255,0.96);
            border: 1px solid #eef2f7;
            border-radius: 24px;
            padding: 1.8rem 1.6rem 1.2rem 1.6rem;
            box-shadow: 0 12px 40px rgba(15,23,42,0.08);
            margin-bottom: 1rem;
        }

        .field-label {
            font-size: 0.96rem;
            font-weight: 700;
            color: #334155;
            margin-top: 0.2rem;
            margin-bottom: 0.5rem;
        }

        .stTextInput > div > div > input,
        .stTextArea textarea {
            border-radius: 14px !important;
            border: 1.8px solid #dbe2ea !important;
            background: white !important;
            font-size: 1rem !important;
        }

        .stTextArea textarea {
            min-height: 180px !important;
            line-height: 1.6 !important;
        }

        .stButton > button {
            height: 52px;
            border-radius: 14px;
            font-size: 1rem;
        }

        .success-card {
            text-align: center;
            padding: 2.6rem 2rem;
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border: 2px solid #bbf7d0;
            border-radius: 24px;
            box-shadow: 0 10px 35px rgba(16,185,129,0.12);
            margin-top: 0.6rem;
            margin-bottom: 1rem;
        }

        .success-icon {
            font-size: 3.8rem;
            margin-bottom: 0.8rem;
        }

        .success-title {
            font-size: 1.45rem;
            font-weight: 800;
            color: #166534;
            margin-bottom: 0.65rem;
        }

        .success-text {
            color: #047857;
            font-size: 1rem;
            line-height: 1.7;
        }

        .info-box {
            margin-top: 0.8rem;
            background: rgba(239,246,255,0.92);
            border: 1px solid #dbeafe;
            border-radius: 16px;
            padding: 14px 16px;
            color: #1e3a8a;
            font-size: 0.95rem;
            text-align: center;
        }
        """
    )


def load_student_notifications_styles() -> None:
    _inject(
        """
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 950px;
        }

        .back-btn .stButton > button {
            width: auto;
            min-width: 220px;
            padding: 0 24px;
            height: 48px;
            border-radius: 14px;
            background: rgba(255,255,255,0.95);
            color: #374151;
            border: 2px solid #e5e7eb;
            font-weight: 700;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }

        .back-btn .stButton > button:hover {
            border-color: #3b82f6;
            color: #3b82f6;
        }

        .stat-card {
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 1.5rem 1rem;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.06);
            border: 1px solid rgba(255,255,255,0.6);
            margin-bottom: 1rem;
        }

        .stat-icon {
            font-size: 1.8rem;
            margin-bottom: 0.6rem;
        }

        .stat-number {
            font-size: 2rem;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 0.2rem;
        }

        .stat-label {
            color: #64748b;
            font-size: 0.95rem;
            font-weight: 600;
        }

        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
            color: #64748b;
            background: rgba(255,255,255,0.95);
            border-radius: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            margin-top: 1rem;
        }

        .empty-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }

        .native-badge {
            display: inline-block;
            width: 100%;
            text-align: center;
            padding: 0.4rem 0.65rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            white-space: nowrap;
            margin-top: 0.1rem;
        }

        .native-badge.pending {
            background: #fef3c7;
            color: #d97706;
        }

        .native-badge.solved {
            background: #d1fae5;
            color: #047857;
        }

        .native-badge.cancelled {
            background: #fee2e2;
            color: #dc2626;
        }

        .card-gap {
            height: 0.25rem;
        }

        .stContainer {
            margin-top: 1rem;
        }

        .stButton > button {
            border-radius: 12px;
            font-weight: 700;
        }

        /* X butonu */
        div[data-testid="stColumn"]:nth-child(2) .stButton > button {
            width: 34px !important;
            min-width: 34px !important;
            height: 34px !important;
            min-height: 34px !important;
            padding: 0 !important;
            border-radius: 8px !important;
            background: #ef4444 !important;
            color: white !important;
            border: none !important;
            font-size: 0.9rem !important;
            font-weight: 800 !important;
            box-shadow: none !important;
        }

        div[data-testid="stColumn"]:nth-child(2) .stButton > button:hover {
            background: #dc2626 !important;
            transform: none !important;
        }

        /* İptal butonu */
        div[data-testid="stColumn"] .stButton > button {
            min-height: 34px !important;
            height: 34px !important;
            font-size: 0.82rem !important;
            border-radius: 10px !important;
        }

        /* İptal için yazıya göre genişlik */
        div[data-testid="stColumn"]:last-child .stButton > button {
            width: auto !important;
            min-width: 72px !important;
            padding: 0.2rem 0.8rem !important;
        }
        """
    )


def load_landing_styles() -> None:
    load_base_styles()
    load_app_background()
    load_main_card_styles()


def load_student_login_styles() -> None:
    load_base_styles()
    load_soft_background()
    load_login_page_styles()


def load_student_panel_page_styles() -> None:
    load_base_styles()
    load_soft_background()
    load_student_panel_styles()


def load_student_fault_page_styles() -> None:
    load_base_styles()
    load_soft_background()
    load_student_fault_styles()


def load_student_notifications_page_styles() -> None:
    load_base_styles()
    load_soft_background()
    load_student_notifications_styles()