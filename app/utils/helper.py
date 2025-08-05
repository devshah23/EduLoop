import json
from fastapi.encoders import jsonable_encoder


get_assignment_cache_key=lambda assignment_id: f"assignment:{assignment_id}"

def convert_to_redis_data(schema,data):
    serialized =jsonable_encoder(schema.model_validate(data).model_dump())
    return json.dumps(serialized)

get_class_cache_key=lambda class_id: f"class:{class_id}"

