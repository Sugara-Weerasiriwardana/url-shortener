from pydantic import BaseModel

class URLBase(BaseModel):
    long_url: str

class URLCreate(URLBase):
    pass

class URLInfo(URLBase):
    short_code: str
    clicks: int

    class Config:
        orm_mode = True
