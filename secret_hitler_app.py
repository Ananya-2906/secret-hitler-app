import streamlit as st
import random

st.set_page_config(page_title="Secret Hitler Role Assigner", layout="centered")

if "roles" not in st.session_state:
    st.session_state.roles = []
if "revealed_player" not in st.session_state:
    st.session_state.revealed_player = None
if "viewed_players" not in st.session_state:
    st.session_state.viewed_players = set()

def get_roles(n):
    liberal_count = {5: 3, 6: 4, 7: 4, 8: 5, 9: 5, 10: 6}[n]
    fascist_count = n - liberal_count - 1
    roles = ["Liberal"] * liberal_count + ["Fascist"] * fascist_count + ["Hitler"]
    random.shuffle(roles)
    return roles

st.title("🎭 Secret Hitler Role Distributor")

if not st.session_state.roles:
    player_count = st.number_input("Number of players (5–10):", min_value=5, max_value=10, step=1)
    if st.button("🎲 Generate Roles"):
        st.session_state.roles = get_roles(player_count)
        st.success("Roles generated! Hand the device to each player to view their role.")

if st.session_state.roles:
    st.header("🕵️ Player Role Reveal")

for i in range(len(st.session_state.roles)):
    player_label = f"Player {i+1}"
    
    # Check if previous player has locked their role
    if i > 0 and (i - 1) not in st.session_state.viewed_players:
        st.warning(f"Please wait for Player {i} to finish before {player_label} can view.")
        continue

    if i in st.session_state.viewed_players:
        st.markdown(f"✅ {player_label} has seen their role.")
        continue

    if st.session_state.revealed_player == i:
        role = st.session_state.roles[i]
        st.subheader(f"🧑 {player_label}, your role is: **{role}**")

        if role == "Fascist":
            teammates = []
            for j, r in enumerate(st.session_state.roles):
                if j == i:
                    continue
                if r == "Fascist":
                    teammates.append(f"Player {j+1}")
                elif r == "Hitler":
                    teammates.append(f"Player {j+1} (Hitler)")
            st.info(f"Your teammates are: {', '.join(teammates)}")

        elif role == "Hitler":
            if len(st.session_state.roles) <= 6:
                teammates = [j+1 for j, r in enumerate(st.session_state.roles) if r == "Fascist"]
                st.info(f"The fascist(s) are: Player(s): {', '.join(map(str, teammates))}")
            else:
                st.info("You don't know who the fascists are.")

        if st.button("🔒 Hide and lock", key=f"hide_{i}"):
            st.session_state.viewed_players.add(i)
            st.session_state.revealed_player = None
            st.rerun()

    else:
        if st.button(f"Reveal role for {player_label}", key=f"reveal_{i}"):
            st.session_state.revealed_player = i
            st.rerun()

