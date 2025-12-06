from controlador.app import app, db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Base de datos lista")

    app.run(debug=True)
