import pyarrow as pa

from image_search.config.config import cfg

FIELD_IMAGE_VECTOR = "image_vector"
FIELD_TEXT_VECTOR = "text_vector"
FIELD_IMAGE_NAME = "image_name"
FIELD_IMAGE_DESCRIPTION = "image_description"
FIELD_CREATE_TIMESTAMP = "create_timestamp"
FIELD_UPDATE_TIMESTAMP = "update_timestamp"

schema = pa.schema(
    [
        pa.field(FIELD_IMAGE_VECTOR, pa.list_(pa.float32(), cfg.image_vector_size)),
        pa.field(FIELD_TEXT_VECTOR, pa.list_(pa.float32(), cfg.text_vector_size)),
        pa.field(FIELD_IMAGE_NAME, pa.string()),
        pa.field(FIELD_IMAGE_DESCRIPTION, pa.string()),
        pa.field(FIELD_CREATE_TIMESTAMP, pa.timestamp("ms")),
        pa.field(FIELD_UPDATE_TIMESTAMP, pa.timestamp("ms")),
    ]
)
