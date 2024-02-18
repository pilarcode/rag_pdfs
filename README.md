# Career Assistant
Chatbot to answer questions about the book [How women rise](https://www.amazon.es/How-Women-Rise-Habits-Holding/dp/1847942253/ref=asc_df_1847942253/?tag=googshopes-21&linkCode=df0&hvadid=301100039962&hvpos=&hvnetw=g&hvrand=10334737450623775220&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=20267&hvtargid=pla-640107206623&psc=1&mcid=486d76258ee533a596d70bec4171c4f2)

![demo](https://github.com/pilarcode/rag_pdfs/blob/main/app/assets/screen-capture.gif)

# Run the app

```bash
cd app
python app_entrypoint.py
```
To interact with the assistant,open  http://localhost:8046 in your browser 


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

