from flask import Flask
import matplotlib; matplotlib.use('Agg')
import matplotlib.pylab as plt
import networkx as nx
import numpy as np
import twitter
import os
import json

app = Flask(__name__)

GRAPH_FILENAME = '/tmp/graph.png'

auth = twitter.OAuth(
    os.getenv('TWITTER_TOKEN'),
    os.getenv('TWITTER_TOKENSECRET'),
    os.getenv('TWITTER_CONSUMERTOKEN'),
    os.getenv('TWITTER_CONSUMERSECRET')
)
twitter_api = twitter.Twitter(auth=auth)
twitter_upload = twitter.Twitter(domain='upload.twitter.com', auth=auth)

@app.route('/')
def post():
    g = nx.random_graphs.erdos_renyi_graph(n=np.random.randint(10,30), p=0.2)
    nx.draw_spring(g)
    plt.savefig(GRAPH_FILENAME, dpi=600)

    with open(GRAPH_FILENAME, "rb") as f:
        image_data = f.read()
    image_id = twitter_upload.media.upload(media=image_data)["media_id_string"]

    res = twitter_api.statuses.update(status="", media_ids=image_id)
    return json.dumps(res)

if __name__ == '__main__':
    app.run()
