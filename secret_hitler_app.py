import streamlit as st
import random
import secrets

st.set_page_config(page_title="Secret Hitler: Code-Based Reveal", layout="centered")

# Initialize session state
if 'roles' not in st.session_state:
    st.session_state.roles = []
if 'names' not in st.session_state:
    st.session_state.names = []
if 'role_map' not in st.session_state:
    st.session_state.role_map = {}
if 'revealed_codes' not in st.session_state:
    st.session_state.revealed_codes = set()

# Helper to generate roles
@st.experimental_singleton
def get_roles(n):
    liberal_count = {5: 3, 6: 4, 7: 4, 8: 5, 9: 5, 10: 6}[n]
    fascist_count = n - liberal_count - 1
    roles = ["Liberal"] * liberal_count + ["Fascist"] * fascist_count + ["Hitler"]
    random.shuffle(roles)
    return roles

st.title("🔒 Secret Hitler: Code-Based Role Reveal")

# Host setup phase
if not st.session_state.role_map:
    st.header("🎲 Host Setup")
    player_count = st.number_input("Number of players (5–10)", min_value=5, max_value=10, step=1)
    if player_count and st.button("Generate Names Inputs"):
        st.session_state.names = ["" for _ in range(player_count)]

    # Collect player names
    if st.session_state.names:
        st.subheader("✏️ Enter Player Names")
        for i in range(len(st.session_state.names)):
            st.session_state.names[i] = st.text_input(f"Name for Player {i+1}", key=f"name_{i}")

        if all(name.strip() for name in st.session_state.names):
            if st.button("🎲 Generate Roles & Codes"):
                roles = get_roles(len(st.session_state.names))
                codes = []
                for name, role in zip(st.session_state.names, roles):
                    code = f"{secrets.randbelow(10000):04d}"
                    codes.append(code)
                    st.session_state.role_map[code] = (name, role)
                st.session_state.roles = roles
                st.success("Roles and access codes generated!")

    # Show table of codes for host
    if st.session_state.role_map:
        st.subheader("🔑 Player Access Codes (Host Only)")
        st.write("Provide each player only their code privately.")
        table = [[name, code] for code, (name, _) in st.session_state.role_map.items()]
        st.table(table)

# Player reveal phase
else:
    st.header("👤 Player Access")
    code = st.text_input("Enter your 4-digit access code")
    if st.button("Reveal My Role"):
        if code in st.session_state.role_map:
            if code in st.session_state.revealed_codes:
                st.error("This code has already been used.")
            else:
                name, role = st.session_state.role_map[code]
                st.success(f"Hello {name}! Your role is **{role}**")
                # Show teammates
                if role == "Fascist":
                    teammates = []
                    for c, (n, r) in st.session_state.role_map.items():
                        if r == "Fascist" and c != code:
                            teammates.append(n)
                        if r == "Hitler":
                            teammates.append(f"{n} (Hitler)")
                    st.info(f"Your teammates are: {', '.join(teammates)}")
                elif role == "Hitler":
                    # Hitler info
                    if len(st.session_state.roles) <= 6:
                        pals = [n for c, (n, r) in st.session_state.role_map.items() if r == "Fascist"]
                        st.info(f"Fascist teammate(s): {', '.join(pals)}")
                    else:
                        st.info("You don\'t know who the fascists are.")
                st.session_state.revealed_codes.add(code)
        else:
            st.error("Invalid code. Check with the host.")

    # Next game button when all revealed
    if len(st.session_state.revealed_codes) == len(st.session_state.role_map):
        st.markdown("---")
        if st.button("🔁 Next Game (Same Players)"):
            # Reset but keep names
            st.session_state.roles = []
            st.session_state.role_map = {}
            st.session_state.revealed_codes = set()
            # Clear singleton cache for roles
            get_roles.clear()
            st.experimental_rerun()
