from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def print_args():
    lines = []
    for (k, v) in request.args.items():
        lines.append("%s=%s" % (k, v))
    return "<br>".join(lines)

if __name__ == "__main__":
    app.run(port=4003, debug=True)
