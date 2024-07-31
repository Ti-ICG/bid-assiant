# 标书助手的后端

### 1.安装开发包

```
poetry install 
```

### 2.启动 Server

将本项目以可编辑方式安装到当前 Python 环境：

```
pip install -e .
```

命令行运行：

```
bid_assistant server
```

版本查看：

```
bid_assistant -V
```

swagger页面：

> http://0.0.0.0:8000/docs


### 3.打包

```
poetry build
```
