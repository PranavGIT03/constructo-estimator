#!/usr/bin/env python3
from app import app

if __name__ == '__main__':
    print("Starting Constructo application...")
    print("Visit: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)