from datetime import datetime, time, timedelta
from typing import List, Optional
from uuid import UUID

from fastapi import Body, Cookie, FastAPI, Header

app = FastAPI()

# Cookie & Header Definition
@app.get("/items/")
async def read_items(
    ads_id: Optional[str] = Cookie(None), # Cookie definition
    user_agent: Optional[str] = Header(None), # Declare Header parameters
    strange_header: Optional[str] = Header(None, convert_underscores=False), # Automatic conversion
    x_token: Optional[List[str]] = Header(None) # Duplicate headers
    ):
    return {
        "ads_id": ads_id, 
        "User_agent":user_agent, 
        "Strange_header":strange_header, 
        "X-Token values": x_token
        }

# Extra Datatypes
@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Optional[datetime] = Body(None),
    end_datetime: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after: Optional[timedelta] = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }

