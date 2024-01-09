# 🤖💭
Chatbot to answer questions about pdfs

## 🟦 Development

### 👉 Create a repository

```bash
$ git init .
```
and link it to the cloud repo. e.g.:
```bash
$ git remote add origin https://github.com/pilarcode/rag_pdfs.git
$ git branch -M main
$ git push -uf origin main
```

### 👉 Set up a dev environment

Navigate to the root directory of the repository and create a new conda environment for development:

```bash
conda create -n pdfrag python=3.11 -y && conda activate pdfrag

```
### 👉 Manage dependencies with Poetry

1. Install poetry

```bash
pip install poetry
```

2. Create the .toml file and main dependencies

```bash
poetry init
```

3. Add more dependencies to the toml file.

```bash
poetry add <package>
```

4. Update dependencies to the latest version if needed.

```bash
poetry update
```

5. Build the whl package with poetry

```bash
poetry build
```

6. Copy the whl file in the dist directory to the root directory

```bash
cp dist/pdfrag-0.1.0-py3-none-any.whl  app/.
```

7. Edit the requirements.txt and install all the dependencies:

```bash
pip install -r app/requirements.txt

```

### 👉 Run the app

```bash
cd app
python app_entrypoint.py
```


## 🟦 Deployment 

To generate the containerized app and run it on-prem or on a VM, follow these steps:

1. Build the Docker image:

```bash
docker build -t pdfrag .
```

2. Run the Docker container:

```bash
docker run -it -p 8046:8046 pdfrag
```


3. Tag the Docker image:

```bash
docker tag pdfrag <your-registry-path>/pdfrag
```

4. Push the Docker image to your cloud Container/Artifact Registry. i.e.:

```bash
docker push <your-registry-path>/pdfrag
```

Replace `<your-registry-path>` with the path to your Container Registry.



## 🟦 UI 

To interact with the assistant, we recommend running the backend app and then opening one of the UIs developed in this project in your browser.
e.g., http://localhost:8046


