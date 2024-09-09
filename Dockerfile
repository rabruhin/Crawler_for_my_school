# 使用 Python 官方映像檔
FROM python:3.9-slim

# 安裝 Chrome 和 ChromeDriver
RUN apt-get update && apt-get install -y wget gnupg unzip \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/93.0.4577.15/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 將應用程式檔案複製到容器中
COPY . /app

# 設置工作目錄
WORKDIR /app

# 安裝 Python 依賴
RUN pip install -r requirements.txt

# 啟動 Flask 應用
CMD ["python", "app.py"]
