from marshmallow import Schema, fields
from src.schema.accelerometer_schema import AccelerometerSchema
from src.schema.gps_schema import GpsSchema
from src.schema.height_schema import HeightSchema


class AggregatedDataSchema(Schema):
    accelerometer = fields.Nested(AccelerometerSchema)
    gps = fields.Nested(GpsSchema)
    height = fields.Nested(HeightSchema)
    time = fields.DateTime('iso')
