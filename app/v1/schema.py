from pydantic import BaseModel, Field


class Response(BaseModel):
    message: str = Field(
        ..., json_schema_extra=(dict(description="Message", example="Hello V1"))
    )


class UserSchema(BaseModel):
    name: str = Field(..., json_schema_extra=(dict(description="name", example="name")))


class MessageSchema(BaseModel):
    message: str = Field(
        ..., json_schema_extra=(dict(description="message", example="message"))
    )


class PageSchema(BaseModel):
    title: str = Field(
        ..., json_schema_extra=(dict(description="title", example="title"))
    )
    content: str = Field(
        ..., json_schema_extra=(dict(description="content", example="content"))
    )
