from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # bisa diakses dari device lain di jaringan yang sama
        port=5000,
        debug=True
    )