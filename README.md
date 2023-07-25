# PDF Table Reader 

### Purpose of this Project 
+ The project is aimed at implementing a pdf table reader, which parses a pdf file and extracts the tables within this file. The contents of the extracted table are then transformed using embeddings of open-source LLMs and then loaded unto a Vector Store.
+ Streamlit was used for the interactive front-end of this project, Weaviate was used for creating the Vector Store, but any other suitable clud platform can still be used. OpenAI was used for the embedding part of this app.