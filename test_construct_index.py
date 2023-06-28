import unittest
from unittest import mock

from construct_index import *


class ConstructIndexTest(unittest.TestCase):
    @mock.patch.dict(os.environ, {"MAX_INPUT_SIZE": "4096", "NUM_INPUTS": "512", "MAX_CHUNK_OVERLAP": "20", "CHUNK_SIZE_LIMIT": "600", "TEMPERATURE": "0.7", "MODEL_NAME": "gpt-3.5-turbo"})
    def test_will_get_model_restrictions_from_env(self):
        model_restrictions = get_model_config_from_env()
        expected_model_restrictions = ModelConfig(4096, 512, 20, 600, 0.7, "gpt-3.5-turbo")
        self.assertEqual(expected_model_restrictions, model_restrictions)

    def test_will_use_default_restrictions_if_not_available_from_env(self):
        model_restrictions = get_model_config_from_env()
        expected_model_restrictions = ModelConfig(2048, 512, 28, 300, 0.6, "gpt-3.5-turbo")
        self.assertEqual(expected_model_restrictions, model_restrictions)

    @mock.patch.dict(os.environ, {"OPENAI_API_KEY": "someKey"})
    def test_get_llm_generates_openapi_llm_with_right_properties(self):
        config = ModelConfig(2048, 512, 28, 300, 0.6, "gpt-3.5-turbo")
        llm = get_llm(config)
        self.assertEqual("gpt-3.5-turbo", llm.model_name)
        self.assertEqual(0.6, llm.temperature)
        self.assertEqual(512, llm.max_tokens)

    @unittest.SkipTest
    def test_get_vector_index(self):
        documents = SimpleDirectoryReader("test_files").load_data()
        index = get_vector_index(documents)
        self.assertEqual(index, GPTSimpleVectorIndex.load_from_disk("test_expect/index.json"))

if __name__ == '__main__':
    unittest.main()
