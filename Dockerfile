FROM python:3.9

# Copy only the requirements file first to leverage caching
ADD requirements.txt .
RUN pip3 install -r requirements.txt

# Now, copy the entire application code
COPY . .

# Install the Google Cloud SDK
RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    apt-get update && \
    apt-get install -y google-cloud-sdk

ENV PYTHONPATH "/${PYTHONPATH}"

CMD ["/bin/bash"]