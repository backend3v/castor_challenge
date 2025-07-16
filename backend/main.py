from dotenv import load_dotenv
load_dotenv()

from app.application import Application

if __name__ == "__main__":
    app = Application()
    app.run() 