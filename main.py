import os


from dotenv import load_dotenv
load_dotenv()


def run_streamlit():
    os.system("streamlit run ui/app.py")

if __name__ == "__main__":
    run_streamlit()