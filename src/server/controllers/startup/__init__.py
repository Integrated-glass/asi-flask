from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import (
  jwt_required, create_access_token, get_jwt_identity, get_raw_jwt, create_refresh_token, jwt_refresh_token_required
)

from typing import List
from decimal import Decimal

from app import db, jwt

startup = Blueprint("startup", __name__, url_prefix="/startup")


@startup.route("/getAll", methods=["GET"])
def get_all_startups():
  data = db.session.execute("""
    select id, name, description, logo, money_requirement from startup
  """).fetchall()
  result = []
  for x in data:
    startup_description = {"name": x[1], "description": x[2], "logo": x[3], "money_requirement": x[4]}
    tags = db.session.execute("""
      select t.id, t.name
      from public.startup as s
      join public.startup_tag as st
        on s.id = st."StartupID"
      join public.tag as t
          on t.id = st."TagID"
      where s.id = :startup_id;
    """, {"startup_id": x[0]}).fetchall()
    startup_description.update({"tags": [dict(zip(y.keys(), y)) for y in tags]})
    result.append(startup_description)
  return jsonify(result)


@startup.route("/getByTags", methods=["GET"])
def get_by_tags():
  tags = list(request.json["tags"])  # type: List[str]
  data = db.session.execute("""
    select id, name, description, logo, "money_requirement" from startup where 
    "id"=(select "StartupID" from startup_tag where "TagID" in :tags)
  """, {"tags": tags}).fetchall()
  result = []
  for x in data:
    l = list(x)
    for y in range(len(x)):
      if isinstance(l[y], Decimal):
        l[y] = float(l[y])
    result.append( data(zip(x.keys(), l)))
  return jsonify(result)


@startup.route("/get/{id:int}")
def get_by_id(id: int):
  result = db.session.execute("""
    select id, name, description, logo, money_requirement from startup where id = :id
  """, {"id": id}).first()
  return jsonify(dict(zip(result.keys(), result)))
