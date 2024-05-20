import json
import os

from flask import Flask, jsonify, request
from src.agent_crew import AgentCrew
from src.feed import get_following_feed

app = Flask(__name__)


@app.route("/feed/<int:fid>", methods=["GET"])
def feed(fid):
    if fid is None:
        return jsonify({"error": "Please provide 'fid' parameter."}), 400

    feed_file_path = os.path.join(os.getcwd(), "data", f"{fid}_feed.json")
    if os.path.exists(feed_file_path):
        os.remove(feed_file_path)

    casts = get_following_feed(fid)
    print(f"casts {len(casts)}\n")

    filtered_casts = []
    for cast in casts:
        if "embeds" in cast and len(cast["embeds"]) > 0:
            continue  # filter out images

        temp_keys = list(cast.keys())
        for key in temp_keys:
            if key != "text":
                del cast[key]

        filtered_casts.append(cast)

    with open(feed_file_path, "w") as f:
        f.write(json.dumps(filtered_casts))

    return jsonify(filtered_casts)


@app.route("/process_feed/<int:fid>", methods=["GET"])
def process(fid):
    if fid is None:
        return jsonify({"error": "Please provide 'fid' parameter."}), 400

    # fid = int(request.args.get("fid"))

    casts = os.path.join(os.getcwd(), "data", f"{fid}_feed.json")

    if not os.path.exists(casts):
        return jsonify({"error": "User feed not found"}), 404

    interests = request.args.getlist("interests")

    print(f"casts {casts} {type(casts)} interests {interests} {type(interests)}\n")

    # casts_list = [{"text": cast} for cast in casts]

    result = AgentCrew.kickoff(
        inputs={"fid": fid, "casts": casts, "interests": interests}
    )

    return jsonify({"result": result})


if __name__ == "__main__":

    PORT = 4000

    app.run(port=PORT, host="0.0.0.0", debug=True)
