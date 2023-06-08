
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.5rpfgk8.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

# 저장
@app.route("/todo", methods=["POST"])
def todo_post():
    todo_receive = request.form['todo_give']

    todo_list = list(db.todo.find({}, {'_id': False}))
    count = len(todo_list) + 1
    doc = {
        'num':count,
        'todo' :todo_receive,
        'done' : 0
    }
    db.todo.insert_one(doc)
    return jsonify({'msg': '저장되었습니다!'})

# 수정
@app.route("/todo/update", methods=["POST"])
def todo_update():
	num_receive = int(request.form['num_give'])
	todo_receive = request.form['todo_give']
	
	db.todo.update_one({'num':num_receive},{'$set':{'todo':todo_receive}})
	return jsonify({'msg': '수정되었습니다!'})

# 삭제
@app.route("/todo/delete", methods=["POST"])
def todo_delete():
	num_receive = int(request.form['num_give'])
	
	db.todo.delete_one({'num':num_receive})
	return jsonify({'msg': '삭제되었습니다!'})

# 완료 
@app.route("/todo/success", methods=["POST"])
def todo_success():
	num_receive = request.form['num_give']
	
	db.todo.update_one({'num':int(num_receive)},{'$set':{'done':1}})
	return jsonify({'msg': 'DO 완료!'})

	
@app.route("/todo", methods=["GET"])
def todo_get():
	all_todo = list(db.todo.find({},{'_id':False}))	
	return jsonify({'result': all_todo})

if __name__ == '__main__':
		app.run('0.0.0.0', port=5000, debug=True)
		
 # 수정
