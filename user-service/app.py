from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 设置数据库连接地址
DB_URI = 'mysql://root:123@db:3306/deathstar'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
# 是否追踪数据库修改，一般不开启, 会影响性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 是否显示底层执行的SQL语句
app.config['SQLALCHEMY_ECHO'] = True
# 初始化db，关联flask项目
db = SQLAlchemy(app)


# 定义模型，映射user表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # 假设user表还有其他字段，这里也需要一一映射


@app.route('/query', methods=['POST'])
def query_database():
    data = request.json.get('input')

    # 使用模型来查询
    user = User.query.filter_by(name=data).first()

    # 将查询到的用户信息转换为字典
    if user:
        user_info = {
            'id': user.id,
            'name': user.name,
            # 包含其他字段...
        }
        return jsonify(user_info)
    else:
        return jsonify({'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)