from os import path, listdir, environ

BUILDING_RTD = environ.get("RCUTE_AI_RTD") == "1"

RESOURCES = path.join(path.dirname(__file__), '../resources')
def resource(file):
    return path.join(RESOURCES, file)

def hotword_model_list_snowboy():
    return listdir(resource('snowboy/hotword_models'))

def hotword_list_snowboy():
    return [w.split('/')[-1].split('.')[0] for w in hotword_model_list()]

import logging
logger = logging.getLogger('rcute-ai')

