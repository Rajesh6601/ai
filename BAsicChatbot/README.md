# BAsicChatbot - LangGraph Agentic AI Chatbot

A sophisticated conversational AI chatbot built with LangGraph, Streamlit, and Groq LLM, featuring persistent chat memory, web scraping capabilities, and specialized tools for company information retrieval.

## 🚀 Features

- **Conversational AI**: Powered by Groq's high-performance language models
- **Chat Memory**: Persistent conversation history within sessions
- **Multiple Model Support**: Choose from various Groq models (llama3-8b-8192, llama3-70b-8192, gemma2-9b-it)
- **Web Interface**: Clean and intuitive Streamlit-based UI
- **Session Management**: Unique thread-based conversation sessions
- **Real-time Streaming**: Live response streaming for better user experience
- **🆕 LinkedIn Integration**: Enhanced company information retrieval including LinkedIn profile data
- **🆕 Advanced Web Scraping**: Multi-source content extraction with intelligent fallback mechanisms
- **🆕 LinkedIn Posts Handling**: Specialized queries for LinkedIn activity and posts
- **Tool Integration**: Himalaya Enterprises search tool for comprehensive company information
- **Vector Search**: Semantic search across multiple web sources using OpenAI embeddings
- **Configurable**: Easy configuration through INI files and environment variables
- **Extensible Architecture**: Modular design for easy feature additions
- **🆕 Error Handling**: Robust service outage detection and user-friendly error messages

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
- **OpenAI Embeddings**: Vector embeddings for semantic search
- **ChromaDB**: Vector database for similarity search
- **BeautifulSoup**: HTML parsing and content extraction
- **Python-dotenv**: Environment variable management
- **Requests**: HTTP client for web scraping
- **Python 3.8+**: Core programming language

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API key (Get it from [Groq Console](https://console.groq.com/keys))
- OpenAI API key (Get it from [OpenAI Platform](https://platform.openai.com/api-keys))
- Virtual environment (recommended)

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

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   GROQ_API_KEY=your-groq-api-key-here
   OPENAI_API_KEY=your-openai-api-key-here
   ```
   
   Or set them as environment variables:
   ```bash
   export GROQ_API_KEY="your-groq-api-key-here"
   export OPENAI_API_KEY="your-openai-api-key-here"
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

### 5. Himalaya Enterprises Tool (`tools/webloader_tool.py`)
- **🆕 LinkedIn Integration**: Direct access to Himalaya Enterprises LinkedIn profile
- **Multi-URL Web Scraping**: Loads content from multiple Himalaya Enterprises web pages
- **Advanced Text Extraction**: Uses BeautifulSoup for clean content extraction
- **🆕 LinkedIn Posts Handling**: Specialized detection and handling of LinkedIn posts queries
- **Vector Search**: Creates searchable embeddings using OpenAI embeddings and Chroma
- **Comprehensive Coverage**: Searches across About, Products, Contact, Projects, and LinkedIn
- **🆕 Smart Fallback Mechanism**: Graceful handling with structured fallback content
- **🆕 Environment Variable Support**: Automatic loading of API keys from .env file

#### Supported URLs:
- `https://www.himalayaentp.com/index.php/about/` - Company information
- `https://www.himalayaentp.com/index.php/product-2/` - Product details
- `https://www.himalayaentp.com/index.php/contact/` - Contact information
- `https://www.himalayaentp.com/index.php/projects/` - Project portfolio
- **🆕** `https://www.linkedin.com/in/himalaya-enterprises-34a0141a9/` - LinkedIn profile

#### LinkedIn Features:
- **Profile Information**: Company overview, specializations, and professional services
- **Professional Network**: Information about industry connections and partnerships
- **Posts Query Detection**: Automatically detects queries about "latest post", "recent updates", etc.
- **Structured Response**: Provides clear guidance when LinkedIn posts cannot be directly accessed
- **Fallback Content**: Comprehensive LinkedIn profile information with guidance for accessing live posts

## 🎨 Features in Detail

### Chat Memory
- **Session-based**: Each browser session maintains its own conversation history
- **Thread Isolation**: Unique thread IDs prevent conversation mixing
- **Persistent Storage**: Messages persist across page refreshes within the same session

### 🆕 LinkedIn Integration
- **Profile Access**: Retrieves comprehensive LinkedIn profile information
- **Posts Query Handling**: Intelligent detection of LinkedIn posts queries
- **Educational Response**: Provides clear guidance when live posts cannot be accessed
- **Professional Information**: Company specializations, network details, and contact information

### 🆕 Enhanced Web Scraping
- **Multi-source Content**: Aggregates information from 5+ web sources
- **Intelligent Fallback**: Structured content when direct extraction fails
- **Content Normalization**: Advanced text cleaning and formatting
- **Vector Search**: Semantic search across all collected content

### 🆕 Service Reliability
- **API Outage Detection**: Monitors Groq service availability
- **Error Recovery**: Graceful handling of temporary service interruptions
- **User Guidance**: Clear instructions during service outages
- **Retry Mechanisms**: Built-in retry logic for transient failures

### Error Handling
- **Robust Configuration Loading**: Fallback to default values if config fails
- **API Error Management**: Graceful handling of API failures
- **User-friendly Error Messages**: Clear feedback for configuration issues
- **🆕 Environment Variable Support**: Automatic loading from .env files

### User Experience
- **Real-time Responses**: Streaming text display for immediate feedback
- **Clean Interface**: Intuitive chat-like interface
- **Responsive Design**: Works well on different screen sizes
- **🆕 Enhanced Query Processing**: Specialized handling for different query types

## 🆕 Latest Updates (v2.0)

### LinkedIn Integration Enhancement
- **LinkedIn Profile Integration**: Added comprehensive LinkedIn profile data extraction
- **Posts Query Detection**: Intelligent handling of LinkedIn posts queries
- **Structured Fallback**: Professional guidance when live posts cannot be accessed
- **Enhanced Vector Search**: Expanded search across 5+ sources including LinkedIn

### Web Scraping Improvements
- **Multi-source Content**: Aggregates information from website and LinkedIn
- **Advanced Text Extraction**: Improved content cleaning and normalization
- **Intelligent Fallback**: Graceful handling when direct extraction fails
- **Environment Variable Support**: Automatic loading of API keys from .env file

### Service Reliability
- **API Outage Detection**: Monitors Groq service availability
- **Error Recovery**: Graceful handling of temporary service interruptions
- **User Guidance**: Clear instructions during service outages
- **Enhanced Error Messages**: More informative error handling

### Developer Tools
- **Test Scripts**: Comprehensive testing tools for functionality verification
- **Debug Support**: Enhanced logging and debugging capabilities
- **Configuration Management**: Improved environment variable handling

## 🔍 Troubleshooting

### Common Issues

1. **"Please enter your GROQ API key"**
   - Ensure you have a valid Groq API key
   - Enter the key in the sidebar input field
   - Check if GROQ_API_KEY is set in your .env file

2. **🆕 "The api_key client option must be set" (OpenAI)**
   - Ensure you have a valid OpenAI API key
   - Check if OPENAI_API_KEY is set in your .env file
   - Verify the .env file is in the project root directory

3. **🆕 "Service unavailable" (Groq 503 error)**
   - Check [Groq Status](https://groqstatus.com/) for service outages
   - Wait for service restoration
   - The application will provide guidance during outages

4. **Configuration errors**
   - Check if `uiconfigfile.ini` exists and is properly formatted
   - The application will use default values if config fails

5. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)
   - Activate your virtual environment

6. **🆕 LinkedIn content not loading**
   - LinkedIn has anti-scraping measures
   - The tool provides fallback content and guidance
   - Visit LinkedIn profile directly for latest posts

### 🆕 Testing Tools

The project includes test scripts to verify functionality:

```bash
# Test basic tool functionality
python test_himalaya_tool.py

# Test LinkedIn integration
python test_linkedin_integration.py

# Test LinkedIn posts queries
python test_linkedin_posts.py
```

### Debug Mode
Enable debug output by checking the terminal/console for detailed logs during operation.

## 🚧 Future Enhancements

- **Multi-modal Support**: Image and document processing
- **Enhanced LinkedIn Integration**: Real-time LinkedIn API integration
- **Advanced Tool Integration**: Web search, calculator, and other specialized tools
- **Custom Agents**: Specialized agents for different domains
- **Export Conversations**: Save chat history to files
- **User Authentication**: Multi-user support with individual histories
- **Advanced Memory**: Long-term memory across sessions
- **🆕 Service Monitoring**: Real-time API health monitoring
- **🆕 Multi-company Support**: Extend tool to support multiple companies
- **🆕 Social Media Integration**: Extend to other social platforms

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
- **OpenAI**: For powerful embedding models and API
- **Streamlit**: For the intuitive web app framework
- **LangChain Community**: For comprehensive LLM integration tools
- **ChromaDB**: For efficient vector database capabilities
- **BeautifulSoup**: For robust HTML parsing and content extraction

## 📞 Support

For support, questions, or feature requests:
- Create an issue in the repository
- Check the troubleshooting section above
- Review the Groq documentation for API-related issues

---

**Built with ❤️ using LangGraph, Streamlit, Groq, OpenAI, and ChromaDB**
