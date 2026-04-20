from django.apps import apps

def get_all_custom_models():
    custom_models=[]

    default_model={'LogEntry','Permission','Group','User','ContentType','Session','Upload'}

    for model in apps.get_models():
        if model.__name__ not in default_model:
            custom_models.append(model.__name__)
    return custom_models