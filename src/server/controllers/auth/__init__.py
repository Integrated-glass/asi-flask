from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import (
  jwt_required, create_access_token, get_jwt_identity, get_raw_jwt, create_refresh_token, jwt_refresh_token_required
)

from app import db, jwt

auth = Blueprint("auth", __name__, url_prefix="/auth")

blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
  jti = decrypted_token['jti']
  return jti in blacklist


@auth.route("/register", methods=["POST"])
def register():
  data = request.json
  email = data["email"]
  hashed_password = data["password"]
  role = data["role"]

  user_id = db.session.execute(
    'insert into "user" (email, hashed_password) VALUES (:email, :hashed_password) RETURNING id',
    {"email": email, "hashed_password": hashed_password}).scalar()
  db.session.commit()

  payload = {
    "email": email,
    "role": role,
    "user_id": user_id
  }
  token = create_refresh_token(identity=payload)
  return jsonify(access_token=token), 200


@auth.route("/registration_finish", methods=["POST"])
@jwt_refresh_token_required
def registration_finish():
  current_user = get_jwt_identity()
  data = request.json
  role = current_user['role']
  user_id = current_user['user_id']
  if role == 'entrepreneur':
    first_name = data['first_name']
    last_name = data['last_name']
    patronymic = data['patronymic']
    bio = data['bio']

    db.session.execute("""
      insert into public.entrepreneur (first_name, last_name, patronymic, bio, user_id) VALUES 
      (:first_name, :last_name, :patronymic, :bio, :user_id)
    """, {"first_name": first_name, "last_name": last_name, "bio": bio, "user_id": user_id, "patronymic": patronymic})
  elif role == 'investor':
    name = data['name']
    link = data['link']
    min_investment = data['min_investment']
    max_investment = data['max_investment']
    bio = data['bio']

    db.session.execute("""
      insert into public.investor (name, link, min_investment, max_investment, user_id) VALUES 
      (:name, :link, :min_investment, :max_investment, :user_id)
    """, {"name": name, "link": link, "min_investment": min_investment, "max_investment": max_investment,
          "user_id": user_id, "bio":bio})

  db.session.commit()
  jti = get_raw_jwt()['jti']  # revoking current token
  blacklist.add(jti)

  payload = {
    "role": role,
    "user_id": user_id
  }
  token = create_access_token(identity=payload)
  return jsonify(access_token=token), 200


@auth.route("/login", methods=["POST"])
def login():
  data = request.json
  email = data["email"]
  hashed_password = data["password"]
  role = data["role"]
  res = None
  if role == 'entrepreneur':
    res = db.session.execute(
      """
      select exists(
        select *
        from public.user as u
        join public.entrepreneur as e
          on e.user_id = u.id
        where u.email = :email
          and u.hashed_password = :hashed_password
      )
      """,
      {"email": email,
       "hashed_password": hashed_password}
    ).scalar()
  elif role == 'investor':
    res = db.session.execute(
      """
      select exists(
        select *
        from public.user as u
        join public.investor as e
          on e.user_id = u.id
        where u.email = :email
          and u.hashed_password = :hashed_password
      )
      """,
      {"email": email,
       "hashed_password": hashed_password}
    ).scalar()
  if res is None:
    return jsonify(msg="email or password is incorrect"), 401

  payload = {
    "user_id": email,
    "role": role
  }
  token = create_access_token(identity=payload)
  return jsonify(access_token=token), 200
