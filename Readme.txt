如何启动网页:
1. 配置虚拟环境
terminal输入
python3 -m venv venv
source venv/bin/activate

2.装一些库
pip install -r requirements.txt

3.导入py
export FLASK_APP=app.py
4.然后flask run 启动

注意: windows用户将 export 替换为 set
