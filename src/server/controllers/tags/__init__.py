from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import (
  jwt_required, create_access_token, get_jwt_identity, get_raw_jwt, create_refresh_token, jwt_refresh_token_required
)

from app import db, jwt

tag = Blueprint("tag", __name__, url_prefix="/tags")


@tag.route("/getAll", methods=["GET"])
def get_all_tags():
  data = db.session.execute("""
    select id, name from tag
  """).fetchall()
  data = [dict(zip(x.keys(), x)) for x in data]
  return jsonify(data)
