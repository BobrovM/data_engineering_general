# Dockerfile (vibecoded)
FROM apache/airflow:3.3.1-python3.14

# Switch to root to install system packages
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
        gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && CHROME_VERSION=$$(google-chrome --version | awk '{print $$3}') \
    && CHROME_MAJOR=$$(echo "$$CHROME_VERSION" | cut -d. -f1) \
    && DRIVER_VERSION=$$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$$CHROME_MAJOR") \
    && wget -q "https://storage.googleapis.com/chrome-for-testing-public/$$DRIVER_VERSION/linux64/chromedriver-linux64.zip" \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64 chromedriver-linux64.zip \
    \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user for security
USER airflow
# Install Python packages
RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    selenium \
    webdriver-manager