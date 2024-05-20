from flask import Flask, jsonify, request
from src.feed import get_following_feed
from src.agent_crew import AgentCrew

app = Flask(__name__)


@app.route("/feed/<int:fid>", methods=["GET"])
def feed(fid):
    if fid is None:
        return jsonify({"error": "Please provide 'fid' parameter."}), 400

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

    return jsonify(filtered_casts)


@app.route("/process_feed/<int:fid>", methods=["GET"])
def process(fid):
    if fid is None:
        return jsonify({"error": "Please provide 'fid' parameter."}), 400

    # fid = int(request.args.get("fid"))
    casts = request.args.getlist("casts")
    interests = request.args.getlist("interests")

    print(f"casts {casts} {type(casts)} interests {interests} {type(interests)}\n")

    casts_list = [{"text": cast} for cast in casts]

    result = AgentCrew.kickoff(
        inputs={"fid": fid, "casts": casts_list, "interests": interests}
    )

    return jsonify({"result": result})


if __name__ == "__main__":

    PORT = 4000

    app.run(port=PORT, host="0.0.0.0", debug=True)
