from fastapi import FastAPI
from prefect import flow
import uvicorn


app = FastAPI()


@flow(name="GET_ROOT", flow_run_name="efef")
async def flow_for_root():
    return {"message": f"Hello"}


@app.get("/")
async def say_hello():
    return await flow_for_root()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
