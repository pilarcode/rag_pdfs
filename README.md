# Career Assistant
Chatbot to answer questions about pdfs

![caption](app\assets\screen-capture.gif)


# Run the app

```bash
cd app
python app_entrypoint.py
```
To interact with the assistant, we recommend running the backend app and then opening one of the UIs developed in this project in your browser.
e.g., http://localhost:8046


# Deployment 

To generate the containerized app and run it on-prem or on a VM, follow these steps:

1. Build the Docker image:

```bash
docker build -t app .
```

2. Run the Docker container:

```bash
docker run -it -p 8046:8046 app
```

