import pandas as pd

ratings_new_data_types = {
#    "ID": "str",
    "USER_ID": "str",
    "ISBN": "str",
    "RATING": "str",
}

ratings = pd.read_csv("L1\\book_ratings_cleaned.csv", sep=";", on_bad_lines="warn", dtype=ratings_new_data_types, quotechar='"', encoding="utf-8")


users_types = {
#    "ID": "str",
    "USER_ID": "str",
    "EMAIL": "str",
    "PASSWORD": "str",
}



users = pd.DataFrame()
users["USER_ID"] = ratings["USER_ID"].unique()

user_count = len(users)
user_emails = [f"test_user_{num}" for num in range(1, user_count+1)]
users["EMAIL"] = user_emails

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

users["PASSWORD_HASH"] = get_password_hash("string")
users["DISABLED_BOOLEAN"] = True
print(f"the users table: {users}")

users.to_csv("L1\\users_cleaned.csv", sep=";", encoding="utf-8", index=False)
