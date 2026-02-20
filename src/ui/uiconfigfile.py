from configparser import ConfigParser
import os

class Config:
    def __init__(self,config_file="./src/ui/uiconfigfile.ini"):
        self.config = ConfigParser()
        self.config.read(config_file)

    def _split_csv(self, value):
        return [item.strip() for item in value.split(',') if item.strip()]

    def get_llm_options(self):
        return self._split_csv(self.config['DEFAULT'].get('LLM_OPTIONS',''))
    
    def get_usecase_options(self):
        return self._split_csv(self.config['DEFAULT'].get('USECASE_OPTIONS',''))
    
    def get_groq_model_options(self):
        return self._split_csv(self.config['DEFAULT'].get('GROQ_Model_OPTIONS',''))
    
    def get_page_title(self):
        return self.config['DEFAULT'].get('PAGE_TITLE','LangGraph: Build Stateful Agentic AI LangGraph')
