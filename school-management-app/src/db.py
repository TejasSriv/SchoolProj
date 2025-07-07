from sqlalchemy import create_engine, text

# Update with your actual credentials and database name
engine = create_engine("mysql+pymysql://root:Ambrane@#3344@localhost/School")

def check_user_credentials(username, password):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM users WHERE username=:username AND password=:password"),
            {"username": username, "password": password}
        )
        return result.fetchone() is not None