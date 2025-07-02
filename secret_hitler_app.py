import streamlit as st
import random

st.set_page_config(page_title="Secret Hitler Role Assigner", layout="centered")

if "roles" not in st.session_state:
    st.session_state.roles = []
if "player_names" not in st.session_state:
    st.session_state.player_names = []
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
        st.session_state.player_names = [""] * player_count
        st.success("Roles generated! Now enter player names below:")

# Get player names
if st.session_state.roles and st.session_state.player_names:
    st.subheader("✏️ Enter Player Names")
    for i in range(len(st.session_state.player_names)):
        st.session_state.player_names[i] = st.text_input(
            f"Name for Player {i+1}",
            value=st.session_state.player_names[i],
            key=f"name_input_{i}"
        )

    st.header("🕵️ Role Reveal (One by One)")

    for i in range(len(st.session_state.roles)):
        player_name = st.session_state.player_names[i].strip() or f"Player {i+1}"

        # Require previous player to finish
        if i > 0 and (i - 1) not in st.session_state.viewed_players:
            st.warning(f"Wait for the previous player before {player_name} can continue.")
            continue

        if i in st.session_state.viewed_players:
            st.markdown(f"✅ {player_name} has viewed their role.")
            continue

        if st.session_state.revealed_player == i:
            role = st.session_state.roles[i]
            st.subheader(f"🧑 {player_name}, your role is: **{role}**")

            if role == "Fascist":
                teammates = []
                for j, r in enumerate(st.session_state.roles):
                    if j == i:
                        continue
                    if r == "Fascist":
                        teammates.append(st.session_state.player_names[j] or f"Player {j+1}")
                    elif r == "Hitler":
                        teammates.append((st.session_state.player_names[j] or f"Player {j+1}") + " (Hitler)")
                st.info(f"Your teammates are: {', '.join(teammates)}")

            elif role == "Hitler":
                if len(st.session_state.roles) <= 6:
                    teammates = [st.session_state.player_names[j] or f"Player {j+1}"
                                 for j, r in enumerate(st.session_state.roles) if r == "Fascist"]
                    st.info(f"The fascist(s) are: {', '.join(teammates)}")
                else:
                    st.info("You don't know who the fascists are.")

            if st.button("🔒 Hide and lock", key=f"hide_{i}"):
                st.session_state.viewed_players.add(i)
                st.session_state.revealed_player = None
                st.rerun()

        else:
            if st.button(f"Reveal role for {player_name}", key=f"reveal_{i}"):
                st.session_state.revealed_player = i
                st.rerun()

# Offer option to play again with same settings
if st.session_state.roles and len(st.session_state.viewed_players) == len(st.session_state.roles):
    st.markdown("---")
    if st.button("🔁 Next Game with Same Players"):
        st.session_state.roles = get_roles(len(st.session_state.roles))
        st.session_state.revealed_player = None
        st.session_state.viewed_players = set()
        st.success("New roles generated. Start revealing again!")
        st.rerun()

