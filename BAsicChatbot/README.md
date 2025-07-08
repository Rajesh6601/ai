# BAsicChatbot - LangGraph Agentic AI Chatbot

A sophisticated conversational AI chatbot built with LangGraph, Streamlit, and Groq LLM, featuring persistent chat memory and a user-friendly web interface.

## 🚀 Features

- **Conversational AI**: Powered by Groq's high-performance language models
- **Chat Memory**: Persistent conversation history within sessions
- **Multiple Model Support**: Choose from various Groq models (llama3-8b-8192, llama3-70b-8192, gemma2-9b-it)
- **Web Interface**: Clean and intuitive Streamlit-based UI with proper prompt-response flow
- **Session Management**: Unique thread-based conversation sessions
- **Real-time Processing**: Efficient message processing and display
- **Tool Integration**: Himalaya Enterprises search tool for comprehensive company information
- **Multi-URL Web Scraping**: Advanced content extraction from multiple web pages
- **Vector Search**: Intelligent search across company content using embeddings
- **Fallback Mechanisms**: Robust error handling and content extraction
- **Configurable**: Easy configuration through INI files
- **Extensible Architecture**: Modular design for easy feature additions

## 🏗️ Architecture

The project follows a modular architecture with clear separation of concerns :

```
BAsicChatbot/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
└── src/
    └── langgraphagenticai/
        ├── main.py                # Core application logic
        ├── graph/
        │   └── graph_builder.py   # LangGraph workflow builder
        ├── LLMS/
        │   └── groqllm.py        # Groq LLM integration
        ├── nodes/
        │   └── basic_chatbot_node.py  # Chatbot processing node
        ├── state/
        │   └── state.py          # State management
        ├── tools/                # Future tool integrations
        └── ui/
            ├── uiconfigfile.py   # Configuration management
            ├── uiconfigfile.ini  # UI configuration
            └── streamlitui/
                ├── loadui.py     # UI components loader
                └── display_result.py  # Result display handler
```

## 🛠️ Technology Stack

- **LangGraph**: Workflow orchestration and state management
- **LangChain**: LLM integration and conversation handling
- **Groq**: High-performance language model inference
- **Streamlit**: Web application framework
- **Python 3.8+**: Core programming language

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API key (Get it from [Groq Console](https://console.groq.com/keys))

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd BAsicChatbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (Optional)**
   ```bash
   export GROQ_API_KEY="your-groq-api-key-here"
   ```

## 🎯 Usage

### Running the Application

1. **Start the Streamlit application**
   ```bash
   streamlit run app.py
   ```

2. **Access the application**
   - Open your browser and navigate to `http://localhost:8501`

### Using the Chatbot

1. **Configure Settings** (in the sidebar):
   - Select LLM provider (Groq)
   - Choose your preferred model
   - Enter your Groq API key
   - Select use case (Basic Chatbot)

2. **Start Chatting**:
   - Type your message in the chat input field
   - Press Enter to send
   - The AI will respond with streaming text

3. **Manage Chat History**:
   - View previous messages in the chat interface
   - Use "🗑️ Clear Chat History" button to reset the conversation

## ⚙️ Configuration

### UI Configuration (`src/langgraphagenticai/ui/uiconfigfile.ini`)

```ini
[DEFAULT]
PAGE_TITLE = LangGraph: Build Stateful Agentic AI graph
LLM_OPTIONS = Groq
USECASE_OPTIONS = Basic Chatbot
GROQ_MODEL_OPTIONS = llama3-8b-8192, llama3-70b-8192, gemma2-9b-it
```

### Supported Models

- **llama3-8b-8192**: Fast and efficient for general conversations
- **llama3-70b-8192**: More capable model for complex tasks
- **gemma2-9b-it**: Balanced performance and capability

## 🔧 Core Components

### 1. Graph Builder (`graph_builder.py`)
- Constructs LangGraph workflows
- Manages conversation flow
- Implements memory persistence with MemorySaver

### 2. Chatbot Node (`basic_chatbot_node.py`)
- Processes user messages
- Invokes LLM for response generation
- Maintains conversation state

### 3. LLM Integration (`groqllm.py`)
- Handles Groq API integration
- Manages model selection and configuration
- Provides error handling for API calls

### 4. UI Components (`ui/streamlitui/`)
- **loadui.py**: Renders the user interface
- **display_result.py**: Handles response display and chat history

### 5. State Management (`state.py`)
- Defines conversation state structure
- Manages message history with LangGraph's `add_messages`

### 6. Himalaya Enterprises Tool (`tools/webloader_tool.py`)
- **Multi-URL Web Scraping**: Loads content from multiple Himalaya Enterprises web pages
- **Advanced Text Extraction**: Uses BeautifulSoup for clean content extraction
- **Vector Search**: Creates searchable embeddings using OpenAI embeddings and Chroma
- **Comprehensive Coverage**: Searches across About, Products, Contact, and Projects pages
- **Fallback Mechanism**: Graceful handling when primary extraction fails

#### Supported URLs:
- `https://www.himalayaentp.com/index.php/about/` - Company information
- `https://www.himalayaentp.com/index.php/product-2/` - Product details
- `https://www.himalayaentp.com/index.php/contact/` - Contact information
- `https://www.himalayaentp.com/index.php/projects/` - Project portfolio

## 🎨 Features in Detail

### Chat Memory
- **Session-based**: Each browser session maintains its own conversation history
- **Thread Isolation**: Unique thread IDs prevent conversation mixing
- **Persistent Storage**: Messages persist across page refreshes within the same session

### Error Handling
- **Robust Configuration Loading**: Fallback to default values if config fails
- **API Error Management**: Graceful handling of API failures
- **User-friendly Error Messages**: Clear feedback for configuration issues

### User Experience
- **Real-time Responses**: Streaming text display for immediate feedback
- **Clean Interface**: Intuitive chat-like interface
- **Responsive Design**: Works well on different screen sizes

## 🔍 Troubleshooting

### Common Issues

1. **"Please enter your GROQ API key"**
   - Ensure you have a valid Groq API key
   - Enter the key in the sidebar input field

2. **Configuration errors**
   - Check if `uiconfigfile.ini` exists and is properly formatted
   - The application will use default values if config fails

3. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)

### Debug Mode
Enable debug output by checking the terminal/console for detailed logs during operation.

## 🚧 Future Enhancements

- **Multi-modal Support**: Image and document processing
- **Tool Integration**: Web search, calculator, and other tools
- **Custom Agents**: Specialized agents for different domains
- **Export Conversations**: Save chat history to files
- **User Authentication**: Multi-user support with individual histories
- **Advanced Memory**: Long-term memory across sessions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangGraph Team**: For the excellent workflow orchestration framework
- **Groq**: For providing high-performance LLM inference
- **Streamlit**: For the intuitive web app framework
- **LangChain Community**: For comprehensive LLM integration tools

## 📞 Support

For support, questions, or feature requests:
- Create an issue in the repository
- Check the troubleshooting section above
- Review the Groq documentation for API-related issues

---

**Built with ❤️ using LangGraph, Streamlit, and Groq**
