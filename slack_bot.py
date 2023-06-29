import os
import ssl

import certifi
from gpt_index import GPTSimpleVectorIndex, LLMPredictor
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

from construct_index import IndexMaker, get_model_config_from_env, get_hf_llm_2, get_llm

ssl_context = ssl.create_default_context(cafile=certifi.where())

def filter_channels(list_channels, channel_names):
    list_ids = []
    for channel in list_channels:
        if channel["is_member"] and channel["name"] in channel_names:
            list_ids.append(channel["id"])
    return list_ids
def get_app():
    client = WebClient(token=os.environ["SLACK_BOT_TOKEN"], ssl=ssl_context)
    app = App(client=client)
    model_config = get_model_config_from_env()

    @app.message("gpt index channels")
    def index_workspace(message, say):
        full_message = str(message["text"]).split("gpt index channels ")
        channels_to_keep = full_message[1].split(" ")
        list_channels = app.client.conversations_list().get("channels")
        list_ids = filter_channels(list_channels, channels_to_keep)
        index = IndexMaker.get_hf_index_from_slack(list_ids) if model_config.local else IndexMaker.get_index_from_slack(list_ids)
        index.save_to_disk("workspace_index.json")
        say("Workspace has been indexed: use query command to query it")

    @app.message("gpt index workspace")
    def index_workspace(message, say):

        list_channels = app.client.conversations_list().get("channels")
        list_ids = []
        for channel in list_channels:
            if channel["is_member"]:
                list_ids.append(channel["id"])
        index = IndexMaker.get_hf_index_from_slack(list_ids) if model_config.local else IndexMaker.get_index_from_slack(list_ids)
        index.save_to_disk("workspace_index.json")
        say("Workspace has been indexed: use query command to query it")

    @app.message("gpt query")
    def gpt_query(message, say):
        split_on_query = str(message["text"]).split("gpt query")
        actual_query = split_on_query[1]
        index = local_model() if model_config.local else open_ai_model()
        response = index.query(actual_query)
        say(response.response)

    def local_model():
        model = get_hf_llm_2(model_config)
        index = GPTSimpleVectorIndex.load_from_disk('workspace_index.json', llm_predictor=LLMPredictor(llm=model),
                                                    embed_model=IndexMaker.get_hf_embeddings())
        return index


    def open_ai_model():
        model = get_llm(model_config)
        index = GPTSimpleVectorIndex.load_from_disk('workspace_index.json', llm_predictor=LLMPredictor(llm=model))
        return index
    return app
