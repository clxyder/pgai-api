from pydantic import BaseModel, Field


class Response(BaseModel):
    message: str = Field(
        ..., json_schema_extra=(dict(description="Message", example="Hello V1"))
    )


class UserSchema(BaseModel):
    name: str = Field(..., json_schema_extra=(dict(description="name", example="name")))
