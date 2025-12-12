import os
import sys
import uvicorn


def run(env: str):
    os.environ["APP_ENV"] = env
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
        reload=(env == "dev"),
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: api [dev|production]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "dev":
        run("dev")
    elif command == "production":
        run("production")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
