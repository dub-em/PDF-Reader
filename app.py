import pandas as pd
import streamlit as st
import camelot, weaviate
from weaviate.util import generate_uuid5
from streamlit_extras.add_vertical_space import add_vertical_space
from config import settings
 
# Sidebar contents
with st.sidebar:
    st.title('PDF Reader')
    st.markdown('''
    ## About
    This app is an PDF Reader that extract tables and loads its content into a Vector Database built using:
    - [Streamlit](https://streamlit.io/)
    - [Weaviate](https://weaviate.io/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
 
    ''')
    add_vertical_space(5)
    
 
def main():
    st.header("PDF Table Reader 💬")
 
 
    # upload a PDF file
    orig_file = st.file_uploader("Upload your PDF", type='pdf')
 
    # st.write(pdf)
    if orig_file is not None:
        file = orig_file.getvalue()
        with open('./uploadedpdf1.pdf', 'wb') as f: 
            f.write(file)
        tables = './uploadedpdf1.pdf'
        tables = camelot.read_pdf(tables)

        df = tables[0].df
        df.columns = list(df.iloc[0,:])
        columns = [column.replace(" ","") for column in df.columns]
        df.columns = columns
        df.drop([0], axis=0, inplace=True)
        df

        auth_config = weaviate.AuthApiKey(api_key=settings.weaviate_apikey)  # Replace w/ your Weaviate instance API key

        # Instantiate the client
        client = weaviate.Client(
            url=settings.weaviate_url, # Replace w/ your Weaviate cluster URL
            auth_client_secret=auth_config,
            additional_headers={
                "X-OpenAI-Api-Key": settings.openai_key, # Replace with your OpenAI key
                }
        )

        store_name = orig_file.name[:-4]
        
        properties = []
        for i in df.columns:
            new_property = {"name": str(i), "dataType":["text"]}
            properties.append(new_property)
        
        class_obj = {
            # Class definition
            "class": str(store_name),

            # Property definitions
            "properties": properties,

            # Specify a vectorizer
            "vectorizer": "text2vec-openai",

            # Module settings
            "moduleConfig": {
                "text2vec-openai": {
                    "vectorizeClassName": False,
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text"
                },
            },
        }

        client.schema.create_class(class_obj)

        for i in range(df.shape[0]):
            data_object = {}
            for key in data_object.keys():
                data_object[key] = df[key][i+1]
            client.data_object.create(
                data_object=data_object,
                class_name=str(store_name),
                uuid='12345678-e64f-5d94-90db-c8cfa3fc123'+str(i+1),
            )

        status = client.query.aggregate(str(store_name)).with_meta_count().do()
        st.write(f'{status}')

 
if __name__ == '__main__':
    main()