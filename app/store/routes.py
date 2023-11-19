from app.store import bp
from flask import abort, request
from werkzeug.exceptions import HTTPException
import json
import sqlite3
from random import randint
from app.db import get_db_connection

# Route to insert store
@bp.route('/', methods=["POST"])
def store_post():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        data = request.get_json()
        user_name = data["username"]
        store_name = data["name"]
        data = store_name

        # Establish the connection and insert into database
        conn = get_db_connection()

        count = conn.execute(
            'SELECT COUNT(*) FROM stores WHERE username = ?;', (user_name,)).fetchall()
        if count[0][0] != 1:
            return "Invalid"

        # See if the store already exists
        count = conn.execute(
            'SELECT COUNT(*) FROM stores WHERE name LIKE ? and username = ?;', ('%' + store_name + '%', user_name)).fetchall()
        if count[0][0] == 1:
            return "Store already added"

        # Generate random store id
        is_valid_number = False
        while not is_valid_number:
            store_id = randint(1, 10000)
            count = conn.execute(
                'SELECT COUNT(*) FROM stores where store_id = ?;', (store_id,)).fetchall()

            # Check if the store_id already exists
            if count[0][0] == 0:
                is_valid_number = True
                break

        try:
            query = "INSERT INTO stores (store_id, name, username) VALUES (?,?,?)"

            conn.execute(query, (store_id, store_name, user_name))
            conn.commit()
            conn.close()

            data = "Inserted store successfully"
        except Exception as e:
            data = "Failed to insert store" + str(e)

    except Exception as e:
        print(e)
        data = str(e)
    return data


# Route to get store
@bp.route('/', methods=["GET"])
def store_get():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        data = request.get_json()
        user_name = data["username"]
        store_name = data["name"]
        store_id = data["store_id"]

        # Establish the connection and insert into database
        conn = get_db_connection()

        query = "SELECT COUNT(*) FROM stores WHERE username = ? and store_id = ?"

        count = conn.execute(query, (user_name, store_id)).fetchall()
        conn.commit()
        conn.close()
        if count[0][0] == 1:
            data = "Store found " + store_name
        elif count[0][0] == 0:
            data = "No store added"
        else:
            data = "Error in checking store" + store_name

    except Exception as e:
        print(e)
        data = str(e)
    return data