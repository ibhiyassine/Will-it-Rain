import os
from dotenv import load_dotenv

class ENV:

    envInstance = None
    
    def __init__(self):
        # Load the .env file from the parent directory
        load_dotenv(dotenv_path="../.env")

        # Access environment variables
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        try:
            self.TIMESFM_CONTEXT = int( str( os.getenv("TIMESFM_CONTEXT") ) )
            self.TIMESFM_HORIZON = int( str( os.getenv("TIMESFM_HORIZON") ) )
        except:
            print("Cannot find desired environment values")


    @classmethod
    def getInstance(cls) -> "ENV":

        if cls.envInstance is None:
            cls.envInstance = ENV()
        return cls.envInstance



