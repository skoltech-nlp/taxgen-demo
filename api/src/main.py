#!flask/bin/python
from flask import Flask, jsonify, request, abort, send_file
import fasttext
from nltk.corpus import wordnet as wn
from helpers import get_graph_with_node, predict_new_nodes


ft = fasttext.load_model("cc.en.300.bin")

all_lemmas = list(wn.all_lemma_names('n'))
app = Flask(__name__)


@app.route('/images/<node_id>', methods=['GET'])
def get_image(node_id):
    filename = 'coton.jpeg'
    return send_file(filename, mimetype='image/jpeg')


@app.route('/initial', methods=['GET', 'POST'])
def get_initial_graph():
    return get_centered_graph("entity.n.01")


@app.route('/centered', methods=['GET', 'POST'])
def get_centered_graph(start_node=None):
    if (request.json and 'start_node' in request.json) or start_node is not None:
        if start_node is None:
            start_node = request.json.get('start_node')
        return jsonify(get_graph_with_node(start_node))
    else:
        abort(400)


@app.route('/generate', methods=['GET', 'POST'])
def generate_subgraph():
    if not request.json or 'start_node' not in request.json:
        abort(400)
    start_node = request.json.get('start_node')
    return jsonify(predict_new_nodes(ft, start_node, all_lemmas=all_lemmas))


if __name__ == '__main__':
    app.run(port=8888, host='0.0.0.0', debug=True, use_reloader=False)
