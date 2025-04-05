from fastapi import FastAPI, HTTPException
from source.classification import EmailClassication

app = FastAPI()


@app.post("/classify")
async def classify_email(request: EmailClassication):
    # Convert the incoming instructions_path string to a Path object.
    try:
        # Instantiate the EmailClassication class.
        classifier = EmailClassication(
            email=request.email
        )

        # Call the classify method.
        result = classifier.classify()

        # Return the parsed JSON result.
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
