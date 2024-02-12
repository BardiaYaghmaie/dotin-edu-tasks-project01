from fastapi import FastAPI
import os

app = FastAPI()


@app.post("/echo/{message}")
async def echo(message: str):
    filepath = f"./var/lib/echo_api/{message}"
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write(message)

        return message

    except Exception as e:
        print(f"Error writing file: {e}")
        return "Error: Could not write message to file."


def main():
    import uvicorn

    uvicorn.run("echo_api:app", host="127.0.0.1", port=8080, reload=True)


if __name__ == "__main__":
    main()
