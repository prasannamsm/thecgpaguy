from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    authoring_db_path: str = "./data/authoring.db"
    runtime_db_path: str = "./data/runtime.db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
