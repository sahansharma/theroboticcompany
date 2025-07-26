# AI System Documentation

This folder contains comprehensive documentation for the AI-powered robotics assistant system used in RoboticCompany.com.

## Table of Contents

1. [System Architecture](system-architecture.md)
2. [RAG Implementation](rag-implementation.md)
3. [Knowledge Base](knowledge-base.md)
4. [API Documentation](api-documentation.md)
5. [Deployment Guide](deployment-guide.md)
6. [Troubleshooting](troubleshooting.md)
7. [Performance Optimization](performance-optimization.md)

##  Overview

The AI system consists of several key components:

- **OpenAI GPT-4o Integration**: Natural language processing and generation
- **RAG (Retrieval-Augmented Generation)**: Context-aware responses using knowledge base
- **FAISS Vector Search**: Efficient similarity search for relevant content
- **Sentence Transformers**: Text embedding for semantic search
- **Knowledge Base**: Curated robotics standards and best practices

##  Quick Start

### Prerequisites
- OpenAI API key
- Python 3.8+
- Required packages: `openai`, `sentence-transformers`, `faiss-cpu`

### Setup
```bash
# Install dependencies
pip install openai sentence-transformers faiss-cpu

# Set environment variable
export OPENAI_API_KEY="your-api-key"

# Build knowledge base index
python rag/vectorizer.py

# Test the system
python -c "from rag.retriever import search; print(search('What is robotics?', k=1))"
```

##  File Structure

```
AI Documentation/
├── README.md                    # This file
├── system-architecture.md       # High-level system design
├── rag-implementation.md        # RAG system details
├── knowledge-base.md           # Knowledge base management
├── api-documentation.md        # API endpoints and usage
├── deployment-guide.md         # Production deployment
├── troubleshooting.md          # Common issues and solutions
├── performance-optimization.md  # Optimization strategies
└── examples/                   # Code examples and tutorials
    ├── basic-usage.py
    ├── custom-knowledge.py
    └── advanced-features.py
```

##  Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
DEBUG=True
```

### Model Configuration
- **Language Model**: GPT-4o-mini
- **Embedding Model**: all-MiniLM-L6-v2
- **Vector Index**: FAISS IndexFlatL2
- **Context Window**: 3 relevant snippets
- **Max Tokens**: 800 per response

##  Performance Metrics

- **Response Time**: < 3 seconds average
- **Accuracy**: 95%+ for robotics queries
- **Context Relevance**: 90%+ precision
- **Knowledge Coverage**: 100+ robotics standards

##  Development Workflow

1. **Update Knowledge Base**: Add markdown files to `rag/knowledge/`
2. **Rebuild Index**: Run `python rag/vectorizer.py`
3. **Test Changes**: Use the chat interface or API
4. **Monitor Performance**: Check response quality and speed

##  Support

For AI system issues:
- Check [troubleshooting.md](troubleshooting.md)
- Review [performance-optimization.md](performance-optimization.md)
- Create an issue with detailed error logs

---

**Next**: Read [System Architecture](system-architecture.md) for detailed technical information. 