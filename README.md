# 爬虫环境部署，需要安装docker
# docker拉取Splash镜像
sudo docker pull scrapinghub/splash
# 启动容器
sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash
# 现在可以通过0.0.0.0:8050(http),8051(https),5023 (telnet)来访问Splash了。

# 安装依赖包，在根目录
pip install -r requirements.txt

# 修改./spider/spiders/sentiment.py中关于数据库的配置

# 后台运行main.py
python main.py>>spider.log &