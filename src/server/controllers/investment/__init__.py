from flask import Blueprint, render_template

investment = Blueprint("investment", __name__, url_prefix="/investment")

from functools import reduce
import json
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from app import db, jwt
from server.common.utils.conversion import tuple_with_decimal_to_double
import datetime


@investment.route("/getAll", methods=["GET"])
def get_all_investments():
  investments = db.session.execute("""
    select id, name, description, start_date, end_date, link, min_money, max_money, logo, type from investment
  """).fetchall()
  result = []
  for x in investments:
    program = dict(zip(x.keys(), x))
    program.update({
      "min_money": float(program["min_money"]),
      "max_money": float(program["max_money"]),
      "start_date": program["start_date"].strftime('%Y-%m-%d'),
      "end_date": program["end_date"].strftime('%Y-%m-%d'),
      "type": {"government": "Государственный", "private": "Частный"}[program["type"]]
    })

    result.append(program)

  return jsonify(result), 200
