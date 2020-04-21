# coding=utf-8
def register_user_helper(client):
    """Helper function to register user"""
    return client.post(
        "/register",
        data=dict(
            username="Ebodius",
            password="Crimsaurus",
            confirm_password="Crimsaurus",
            email_address="ebodius@example.com",
        ),
        follow_redirects=True,
    )


def login_user_helper(client):
    """Helper function to login user"""
    return client.post(
        "/", data=dict(username="Ebodius", password="Crimsaurus"), follow_redirects=True
    )
