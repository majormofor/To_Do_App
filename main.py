from webite import create_app

app = create_app()

if __name__ == '__main__': # needed before the app is ran
    app.run(debug=False, host = 0.0.0.0) # debug = true -- automatically restart server
