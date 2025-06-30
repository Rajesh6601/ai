from configparser import ConfigParser
import os


class Config:
    def __init__(self, config_file=None):
        self.config = ConfigParser()
        
        # Default values as fallback
        self.defaults = {
            "PAGE_TITLE": "LangGraph: Build Stateful Agentic AI graph",
            "LLM_OPTIONS": "Groq",
            "USECASE_OPTIONS": "Basic Chatbot",
            "GROQ_MODEL_OPTIONS": "llama3-8b-8192, llama3-70b-8192, gemma2-9b-it"
        }
        
        # Determine config file path
        if config_file is None:
            # Get the directory of this current file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(current_dir, "uiconfigfile.ini")
        
        # Try to read the config file
        try:
            files_read = self.config.read(config_file)
            if not files_read:
                print(f"Warning: Could not read config file at {config_file}. Using default values.")
                self._load_defaults()
        except Exception as e:
            print(f"Error reading config file: {e}. Using default values.")
            self._load_defaults()
    
    def _load_defaults(self):
        """Load default values into the config parser"""
        self.config.add_section("DEFAULT")
        for key, value in self.defaults.items():
            self.config.set("DEFAULT", key, value)

    def get_llm_options(self):
        value = self.config["DEFAULT"].get("LLM_OPTIONS", self.defaults["LLM_OPTIONS"])
        return value.split(", ") if value else ["Groq"]
    
    def get_usecase_options(self):
        value = self.config["DEFAULT"].get("USECASE_OPTIONS", self.defaults["USECASE_OPTIONS"])
        return value.split(", ") if value else ["Basic Chatbot"]

    def get_groq_model_options(self):
        value = self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS", self.defaults["GROQ_MODEL_OPTIONS"])
        return value.split(", ") if value else ["llama3-8b-8192", "llama3-70b-8192", "gemma2-9b-it"]
    
    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE", self.defaults["PAGE_TITLE"])
