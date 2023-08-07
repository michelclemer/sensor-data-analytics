from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from main import CSVDataFile, NewItemCSV

app = APIRouter(prefix="/api", responses={404: {"description": "Not Found"}})


csv_instance = CSVDataFile("sensor.csv", "data_sensor.json")
DATA_FILTERED = csv_instance.get_data_json(
    csv_instance.csv_file_name, csv_instance.json_output_name
)


class Item(BaseModel):
    count: int
    entries: List[dict]


@app.get("/")
async def root():
    payload = {"count": len(DATA_FILTERED), "entries": DATA_FILTERED}
    return JSONResponse(content=payload, media_type="application/json")


@app.post("/create")
async def create(item: Item):
    new_item = NewItemCSV()

    try:
        output_dataframe = new_item.create_dataframe(item.entries)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    print("[+] Output dataframe")
    print(output_dataframe)
    print("")
    return item


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
