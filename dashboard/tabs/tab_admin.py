
# tab_admin.py
# Admin User Management - Tab 4

import streamlit as st
import requests


def render_admin(token, username):

    st.subheader("👑 Admin User Management")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    if st.session_state.role != "admin":
        st.error("Admin only")
        return

    # === Add New User ===
    st.subheader("➕ Add New User")

    new_username = st.text_input("New username")
    new_password = st.text_input("New password", type="password")
    new_user_role = st.selectbox("Role for new user", ["viewer", "admin"])

    if st.button("Create User"):

        create_response = requests.post(
            "http://127.0.0.1:8000/register",
            params={
                "username": new_username,
                "password": new_password,
                "role": new_user_role
            },
            headers=headers
        )

        if create_response.status_code == 200:
            st.success(f"User {new_username} created successfully")
            st.rerun()
        else:
            st.error(create_response.text)

    st.divider()

    # === Existing Users ===
    st.subheader("👥 Existing Users")

    response = requests.get(
        "http://127.0.0.1:8000/users",
        headers=headers
    )

    if response.status_code != 200:
        st.error("Unable to load users")
        return

    users = response.json()

    for user in users:

        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])

        with col1:
            st.write(user["username"])

        with col2:
            selected_role = st.selectbox(
                "Role",
                ["viewer", "admin"],
                index=0 if user["role"] == "viewer" else 1,
                key=f"role_{user['username']}"
            )

        with col3:
            if st.button("Update", key=f"update_{user['username']}"):

                update_response = requests.put(
                    f"http://127.0.0.1:8000/users/{user['username']}/role",
                    params={"role": selected_role},
                    headers=headers
                )

                if update_response.status_code == 200:
                    st.success(f"{user['username']} updated")
                    st.rerun()
                else:
                    st.error("Update failed")

        with col4:
            if user["username"] == username:
                st.caption("Current user")
            else:
                if st.button("Delete", key=f"delete_{user['username']}"):

                    delete_response = requests.delete(
                        f"http://127.0.0.1:8000/users/{user['username']}",
                        headers=headers
                    )

                    if delete_response.status_code == 200:
                        st.success(f"{user['username']} deleted")
                        st.rerun()
                    else:
                        st.error("Delete failed")
                        