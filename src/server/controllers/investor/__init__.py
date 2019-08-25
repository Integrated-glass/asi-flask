from flask import Blueprint, render_template

investorMod = Blueprint("investor", __name__, url_prefix="/investor")

from functools import reduce
import json
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from app import db, jwt
from server.common.utils.conversion import tuple_with_decimal_to_double


@investorMod.route("/<int:investor_id>", methods=["GET"])
# @jwt_required
def get_by_id(investor_id):
  investor_info = db.session.execute(
    """
    select i.name, i.link, i.bio, i.min_investment, i.max_investment, i.maximal_historical_investment, i.avatar
    from public.investor as i
    where i.id = :investor_id;
    """,
    {
      "investor_id": investor_id
    }
  )

  investor_history = db.session.execute(
    """
    select iih.project_name, iih.link, iih.money_invested
    from public.investor_investment_history as iih
    where iih.investor_id = :investor_id;
    """,
    {
      "investor_id": investor_id
    }
  )

  investor_tags = db.session.execute(
    """
    select t.id as tag_id, t.name
    from public.investor_tag as it
    join public.tag as t
      on it."TagID" = t.id
    where it."InvestorID" = :investor_id;
    """,
    {
      "investor_id": investor_id
    }
  )

  return {
    "investor": dict(zip(investor_info.keys(), tuple_with_decimal_to_double(investor_info.first()))),
    "history": dict(zip(investor_history.keys(), tuple_with_decimal_to_double(investor_history.first()))),
    "tags": dict(zip(investor_tags.keys(), investor_tags.first() or []))
  }


@investorMod.route("/getAll", methods=["GET"])
def get_all_investors():
  ids = db.session.execute("""
    select id from investor
  """).fetchall()

  result = []
  for x in ids:
    id = x[0]
    result.append(get_by_id(id))

  return jsonify(result)


@investorMod.route("", methods=["GET"])
# @jwt_required
def get_by_interests():
  tag_ids = list(map(int, request.args.getlist("tags")))
  investors_tags = db.session.execute(
    """
    select i.id as investor_id, i.name as investor_name, i.min_investment, i.max_investment, i.avatar, it."TagID", t.name as tag_name
    from public.investor as i
    left join public.investor_tag as it
      on i.id = it."InvestorID"
    left join public.tag as t
      on t.id = it."TagID"
    """
  )

  investors_tags = list(
    map(
      lambda x: dict(zip(investors_tags.keys(), x)),
      investors_tags.fetchall()
    )
  )

  if tag_ids:
    filter(lambda x: x, investors_tags)

  return jsonify(reduce(
    _investor_tags_reducer,
    investors_tags,
    []
  ))


def _investor_tags_reducer(running, cur):
  if cur["TagID"]:
    cur = {
      "investor_id": cur["investor_id"],
      "investor_name": cur["investor_name"],
      "min_investment": float(cur["min_investment"]),
      "max_investment": float(cur["max_investment"]),
      "avatar": cur["avatar"],
      "tags": [{
        "TagID": cur["TagID"],
        "tag_name": cur["tag_name"],
      }],
    }
  else:
    cur = {
      "investor_id": cur["investor_id"],
      "investor_name": cur["investor_name"],
      "min_investment": float(cur["min_investment"]),
      "max_investment": float(cur["max_investment"]),
      "avatar": cur["avatar"],
    }

  existing = list(filter(lambda x: x["investor_id"] == cur["investor_id"], running))

  if existing:
    existing[0]["tags"].append({
      "TagID": cur["tags"][0]["TagID"],
      "tag_name": cur["tags"][0]["tag_name"],
    })

    return running
  else:
    running.append(cur)
    return running
