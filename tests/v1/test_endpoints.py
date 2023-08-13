import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
import logging

from src.v1.endpoints import router, call_language_model, get_bot_response

class TestMain(unittest.TestCase):

    def setUp(self):
        self.app = TestClient(router)
        logging.getLogger().setLevel(logging.WARNING)

    @patch('src.v1.endpoints.LLMChain')
    @patch('src.v1.endpoints.VertexAI')
    @patch('src.v1.endpoints.PromptTemplate')
    def test_call_vertexai(self, MockPromptTemplate, MockVertexAI, MockLLMChain):
        mock_chain = MockLLMChain.return_value
        mock_chain.run.return_value = 'Test response'
        with patch('src.v1.endpoints.config.get', return_value='vertex'):
            response = call_language_model('test_input')
        self.assertEqual(response, 'Test response')
        
    @patch('src.v1.endpoints.LLMChain')
    @patch('src.v1.endpoints.OpenAI')
    @patch('src.v1.endpoints.PromptTemplate')
    def test_call_openai(self, MockPromptTemplate, MockOpenAI, MockLLMChain):
        mock_chain = MockLLMChain.return_value
        mock_chain.run.return_value = 'Test response'
        with patch('src.v1.endpoints.config.get', return_value='openai'):
            with patch('src.v1.endpoints.token_cost', return_value=1):
                response = call_language_model('test_input')
        self.assertEqual(response, 'Test response')

    @patch('src.v1.endpoints.call_language_model')
    def test_get_bot_response_hello(self, mock_call_language_model):
        mock_call_language_model.return_value = 'Hi there!'
        response = get_bot_response('hello')
        self.assertEqual(response, 'Hi there!')

    def test_get_bot_response_name(self):
        response = get_bot_response('what is your name?')
        self.assertEqual(response, 'My name is Chat Bot!')

    @patch('src.v1.endpoints.call_language_model')
    def test_get_bot_response_other(self, mock_call_language_model):
        mock_call_language_model.return_value = 'Language model response'
        response = get_bot_response('other_input')
        self.assertEqual(response, 'Language model response')

    def test_handle_request_get(self):
        response = self.app.get('/')
        self.assertEqual(response.json(), {'error': 'Only POST requests are allowed'})

    @patch('src.v1.endpoints.get_bot_response')
    def test_handle_request_post(self, mock_get_bot_response):
        mock_get_bot_response.return_value = 'Bot response'
        response = self.app.post('/', json={'user_input': 'test_input'})
        self.assertEqual(response.json(), {'bot_response': 'Bot response'})

    @patch('src.v1.endpoints.EmbeddingSource')
    def test_get_embedding_source(self, MockEmbeddingSource):
        mock_get_source = MockEmbeddingSource.return_value.get_source
        mock_get_source.return_value = 'Test response'
        response = self.app.post('/get_embedding_sources', json={'query': 'test_query', 'num_results': 5})
        self.assertEqual(response.json(), {'embedding_source': 'Test response'})

    @patch('src.v1.endpoints.call_language_model')
    @patch('src.v1.endpoints.EmbeddingSource')
    def test_synthesize_response(self, MockEmbeddingSource, mock_call_language_model):
        mock_get_source = MockEmbeddingSource.return_value.get_source
        mock_get_source.return_value = [{'source': 'test_source', 'content': 'test_content'}]
        mock_call_language_model.return_value = 'Language model response'
        response = self.app.post('/synthesize_response', json={'query': 'test_query', 'num_results': 5})
        self.assertEqual(response.json(), {'bot_response': 'Language model response\n\nPossibly Related Sources:\n<a href="#">test_source</a>'})

    #TODO
    def test_spend_limit_exceeded(self):
                assert True == True

if __name__ == "__main__":
    unittest.main()
