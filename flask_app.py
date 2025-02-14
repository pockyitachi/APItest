from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database
users = {}
id_counter = 1


@app.route('/users', methods=['POST'])
def create_user():
    global id_counter
    data = request.json
    user = {
        'id': id_counter,
        'name': data.get('name'),
        'email': data.get('email')
    }
    users[id_counter] = user
    id_counter += 1
    return jsonify(user), 201


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    data = request.json
    users[user_id]['name'] = data.get('name', users[user_id]['name'])
    users[user_id]['email'] = data.get('email', users[user_id]['email'])
    return jsonify(users[user_id]), 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    del users[user_id]
    return jsonify({'message': 'User deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
