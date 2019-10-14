from findit import init_app

app = init_app()

if app and __name__ == '__main__':
    app.run(debug=True)
