from flask import Blueprint, render_template
testMod = Blueprint("test", __name__, url_prefix="/test")


@testMod.route("/", methods=["GET"])
def test():
  return "Hello world"
