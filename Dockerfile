FROM python:3.10.4

ENV TZ=Asia/Shanghai

WORKDIR /work

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

ENTRYPOINT ["python", "main.py"]