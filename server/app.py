from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

from services.usage.get_usage import get_usage

app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/usage")
async def usage():
    try:
        usage_data = await get_usage()
        return {"usage": usage_data}
    except httpx.RequestError as err:
        raise HTTPException(status_code=500, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(err)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
