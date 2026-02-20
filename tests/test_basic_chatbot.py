import unittest
from unittest.mock import MagicMock
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode

class TestBasicChatbotNode(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MagicMock()
        self.node = BasicChatbotNode(self.mock_llm)

    def test_process(self):
        # Setup
        state = {"messages": ["Hello"]}
        expected_response = "Hi there!"
        self.mock_llm.invoke.return_value = expected_response

        # Execute
        result = self.node.process(state)

        # Assert
        self.mock_llm.invoke.assert_called_once_with(["Hello"])
        self.assertEqual(result, {"messages": expected_response})

if __name__ == '__main__':
    unittest.main()
