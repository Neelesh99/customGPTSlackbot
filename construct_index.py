import os

from gpt_index import PromptHelper


class ModelConfig:
    def __init__(self, max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit, temperature, model_name):
        self.max_input_size = max_input_size
        self.num_outputs = num_outputs
        self.max_chunk_overlap = max_chunk_overlap
        self.chunk_size_limit = chunk_size_limit
        self.temperature = temperature
        self.model_name = model_name

    def __eq__(self, o: object) -> bool:
        if isinstance(o, ModelConfig):
            return self.chunk_size_limit == o.chunk_size_limit and self.max_chunk_overlap == o.max_chunk_overlap and self.num_outputs == o.num_outputs and self.max_input_size == o.max_input_size and self.temperature == o.temperature and self.model_name == o.model_name
        return False


def get_model_restrictions_from_env() -> ModelConfig:
    max_input_size_str = os.getenv("MAX_INPUT_SIZE") if "MAX_INPUT_SIZE" in os.environ else "2048"
    num_outputs_str = os.getenv("NUM_OUTPUTS") if "NUM_OUTPUTS" in os.environ else "512"
    max_chunk_overlap_str = os.getenv("MAX_CHUNK_OVERLAP") if "MAX_CHUNK_OVERLAP" in os.environ else "28"
    chunk_size_limit_str = os.getenv("CHUNK_SIZE_LIMIT") if "CHUNK_SIZE_LIMIT" in os.environ else "300"
    temperature_str = os.getenv("TEMPERATURE") if "TEMPERATURE" in os.environ else "0.6"
    model_name = os.getenv("MODEL_NAME") if "MODEL_NAME" in os.environ else "gpt-3.5-turbo"

    return ModelConfig(int(max_input_size_str), int(num_outputs_str), int(max_chunk_overlap_str),
                       int(chunk_size_limit_str), float(temperature_str), model_name)

def get_prompt_helper(model_restrictions: ModelConfig) -> PromptHelper:
    return PromptHelper(model_restrictions.max_input_size, model_restrictions.num_outputs, model_restrictions.max_chunk_overlap, chunk_size_limit=model_restrictions.chunk_size_limit)

class ConstructIndex:
    pass