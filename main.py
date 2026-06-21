if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True, port=8000, host="127.0.0.1")
