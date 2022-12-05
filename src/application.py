from flask import Flask, Response, request
from datetime import datetime
import json
from team_resource import TeamResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__)

CORS(app)


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Starter-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/team/course_id=<course_id>/limit=<limit>&offset=<offset>", methods=["get"])
def browse_all_team(course_id, limit, offset):
    result = TeamResource.browse_all_team(course_id, limit, offset)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/team/team_captain_uni=<team_captain_uni>&course_id=<course_id>", methods=["get"])
def browse_team_info_by_input(course_id, team_captain_uni):
    result = TeamResource.browse_team_info_by_input(course_id, team_captain_uni)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/team/add/team_name=<team_name>&team_captain_uni=<team_captain_uni>&team_captain=<team_captain>&course_id=<course_id>&number_needed=<number_needed>&team_message=<team_message>",
           methods=["POST", "GET"])
def add_team(team_name, team_captain_uni, team_captain, course_id, number_needed=0, team_message=""):
    result, message = TeamResource.add_team(team_name, team_captain_uni, team_captain, course_id, number_needed, team_message)
    if result:
        rsp = Response("Team CREATED", status=200, content_type="text/plain")
    else:
        rsp = Response(message, status=404, content_type="text/plain")
    return rsp

@app.route("/team/edit/team_name=<team_name>&team_captain_uni=<team_captain_uni>&team_captain=<team_captain>&course_id=<course_id>&number_needed=<number_needed>&team_message=<team_message>",
           methods=["POST", "GET"])
def edit_team(team_name, team_captain_uni, team_captain, course_id, number_needed=0, team_message=""):
    result= TeamResource.edit_team(team_name, team_captain_uni, team_captain, course_id, number_needed, team_message)
    if result:
        rsp = Response("Team UPDATED", status=200, content_type="text/plain")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/team/delete/team_id=<team_id>&team_captain_uni=<team_captain_uni>&course_id=<course_id>",
           methods=["POST", "GET"])
def delete_team(team_captain_uni, course_id,team_id):
    result = TeamResource.delete_team(team_captain_uni, course_id,team_id)
    if result:
        rsp = Response("DELETE SUCCESS", status=200, content_type="application.json")
    else:
        rsp = Response("No existed Preference is found!", status=404, content_type="text/plain")
    return rsp

@app.route("/team/team_member/team_id=<team_id>&course_id=<course_id>", methods=["get"])
def browse_all_team_member(team_id, course_id):
    result = TeamResource.get_all_team_member(team_id, course_id)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/team/add_member/uni=<uni>&student_name=<student_name>&team_id=<team_id>&course_id=<course_id>", methods=["get"])
def add_team_member(uni, student_name, team_id, course_id):
    result, message = TeamResource.add_team_member(uni, student_name, team_id, course_id)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response(message, status=404, content_type="text/plain")
    return rsp

@app.route("/team/delete_member/uni=<uni>&team_id=<team_id>&course_id=<course_id>",
           methods=["POST", "GET"])
def delete_team_member(uni,  team_id, course_id):
    result = TeamResource.delete_team_member(uni, team_id, course_id)
    if result:
        rsp = Response("DELETE SUCCESS", status=200, content_type="application.json")
    else:
        rsp = Response("No existed Preference is found!", status=404, content_type="text/plain")
    return rsp


@app.route("/team/find_my_teammate/uni=<uni>&course_id=<course_id>", methods=["get"])
def find_my_teammate(uni, course_id):
    result = TeamResource.find_my_teammate(uni, course_id)
    print(result)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=2233)
