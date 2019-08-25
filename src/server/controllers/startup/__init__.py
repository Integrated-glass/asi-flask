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
  select e.first_name, e.last_name, e.patronymic, e.bio, e.id as enterpreneur_id, d.document_name, d.file, d.id as document_id,
         s.id as startup_id, s.name as startup_name, s.description, s.logo, s.money_requirement, t.id as tag_id, t.name as tag_name
  from startup as s
  join entrepreneur as e
    on s.owner_id = e.id
  join document as d
    on d.id = s.document_id
  left join startup_tag as st 
    on s.id = st."StartupID"
  left join tag as t
    on st."TagID" = t.id
  where s.id = :startup_id
    and (d.type = 'Business plan' or d.type is null);
  """, {"startup_id": id}).fetchall()

  if result:
    res = {
      "owner": {
        "first_name": result[0][0],
        "last_name": result[0][1],
        "patronymic": result[0][2],
        "bio": result[0][3],
        "id": result[0][4]
      },
      "document": {
        "name": result[0][5],
        "link": result[0][6],
        "id": result[0][7]
      },
      "startup": {
        "id": result[0][8],
        "name": result[0][9],
        "description": result[0][10],
        "logo": result[0][11],
        "money_requirement": float(result[0][12])
      },
      "tags": [{"tag_id": r[13], "tag_name": r[14]} for r in result]
    }
  else:
    res = {}

  return jsonify(res)
