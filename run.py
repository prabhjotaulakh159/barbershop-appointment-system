from project import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=5009, debug=True)
