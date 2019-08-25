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
    startup_description = {"name": x[1], "description": x[2], "logo": x[3], "money_requirement": float(x[4])}
    tags = db.session.execute("""
      select t.id, t.name
      from public.startup as s
      join public.startup_tag as st
        on s.id = st."StartupID"
      join public.tag as t
          on t.id = st."TagID"
      where s.id = :startup_id;
    """, {"startup_id": x[0]}).fetchall()
    startup_description.update({"tags": [dict(zip(y.keys(), y)) for y in tags], "id": x[0]})
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
    result.append({
      "id": x[0],
      "name": x[1],
      "description": x[2],
      "logo": x[3],
      "money_requirement": float(x[4])
    })
  return jsonify(result)


@startup.route("/get/<id>")
def get_by_id(id):
  id = int(id)
  result = db.session.execute("""
   select e.first_name, e.last_name, e.patronymic, e.bio, e.id, d.document_name, d.file, d.id ,
   s.id, s.name,s.description, s.logo, s.money_requirement
  from startup as s
  join entrepreneur as e
    on s.owner_id = e.id
  join document as d
    on d.id = s.document_id
  where s.id = :startup_id
    and d.type = 'Business plan'
  """, {"startup_id": id}).first()
  res = {
    "owner": {
      "first_name": result[0],
      "last_name": result[1],
      "patronymic": result[2],
      "bio": result[3],
      "id": result[4]
    },
    "document": {
      "name": result[5],
      "link": result[6],
      "id": result[7]
    },
    "startup": {
      "id": result[8],
      "name": result[9],
      "description": result[10],
      "logo": result[11],
      "money_requirement": float(result[11])
    }
  }
  res = dict(zip(result.keys(), result))
  res.update({"money_requirement": float(res["money_requirement"])})
  return jsonify(res)
