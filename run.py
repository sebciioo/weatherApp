from app import create_app

app = create_app()

"""
    Main application input file.
"""

if __name__ == '__main__':
    app.run(debug=True)
