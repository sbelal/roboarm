"""
Flask service test
"""

from flask import Flask, render_template, jsonify, abort, request, make_response, url_for
import roboarm


app = Flask(__name__)

#region error handlers

@app.errorhandler(404)
def not_found(error):
    '''
    Error 404 handling
    '''
    return make_response(jsonify({'error': str(error)}), 404)

@app.errorhandler(500)
def internal_error(error):
    '''
    Error 500 handling
    '''
    return make_response(jsonify({'error': 'Internal server error. Details: '+str(error)}), 500)

#endregion

#region service functions

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    """
    qwqeqw eqweq we qwe qwe
    """
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


@app.route('/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_single_task(task_id):
    """
    qwqeqw eqweq we qwe qwe
    """
    task = [task for task in tasks if task['id'] == task_id]
    if not task:
        abort(404)
    return jsonify({'task': make_public_task(task[0])})



@app.route('/api/v1.0/tasks', methods=['POST'])
def create_task():
    '''
    Some text
    '''
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201




@app.route('/api/v1.0/movearm', methods=['POST'])
def get_sentiment_score():
    '''
    Some text
    '''
    if not request.json:
        abort(400)
   
    if not 'motor0' in request.json:
        abort(400)
   
    if not 'motor1' in request.json:
        abort(400)
   
    if not 'motor2' in request.json:
        abort(400)
   
    m0 = int(request.json['motor0'])
    m1 = int(request.json['motor1'])
    m2 = int(request.json['motor2'])
    
    #roboarm.runRoboArm(arduino,[m0,m1,m2])
   
    return jsonify({'taskDone': str(m0) + " - " +str(m1) + " - " + str(m2) }), 200




@app.route('/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    '''
    blah blah
    '''
    task = [task for task in tasks if task['id'] == task_id]
    if not task:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and not isinstance(request.json['title'], str):
        abort(400)
    if 'description' in request.json and not isinstance(request.json['description'], str):
        abort(400)
    if 'done' in request.json and not isinstance(request.json['done'], bool):
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    '''
    blah blah
    '''
    task = [task for task in tasks if task['id'] == task_id]
    if not task:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

#endregion


def make_public_task(task):
    '''
    Helper
    '''
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_single_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


#region fake data
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]
#endregion


seq_length = 200



#arduino = roboarm.initRoboArm("COM4")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

