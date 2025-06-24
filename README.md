# 🤖 ZOKO-Shopify AI Middleware

> **Enterprise-grade AI-powered WhatsApp integration with Shopify e-commerce platform**

A production-ready middleware solution that seamlessly connects ZOKO (WhatsApp Business API), OpenAI's GPT-4, and Shopify's e-commerce platform. Features real-time translation, intelligent product recommendations, conversational memory, and multi-language broadcast capabilities.

## 📋 Table of Contents

- [🚀 Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Technology Stack](#️-technology-stack)
- [📦 Installation & Setup](#-installation--setup)
- [🐳 Docker Deployment](#-docker-deployment)
- [☁️ Google Cloud Deployment](#️-google-cloud-deployment)
- [🔧 Local Development](#-local-development)
- [📚 API Documentation](#-api-documentation)
- [🔐 Security & Authentication](#-security--authentication)
- [🌍 Multi-Language Support](#-multi-language-support)
- [📊 Monitoring & Logging](#-monitoring--logging)
- [🚨 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🚀 Features

### Core Capabilities
- **🤖 AI-Powered Chatbot**: GPT-4 integration for intelligent customer interactions
- **🛍️ Smart Product Recommendations**: AI-driven product suggestions based on user intent
- **🌍 Real-time Translation**: 35+ language support with automatic detection
- **💬 Conversational Memory**: Persistent chat history across sessions
- **📢 Multi-language Broadcasts**: Automated promotional campaigns
- **🔒 Enterprise Security**: API key authentication and rate limiting
- **📊 Production Monitoring**: Structured logging and health checks

### Technical Features
- **⚡ High Performance**: Async FastAPI with Gunicorn workers
- **🔄 Auto-scaling**: Cloud Run deployment with automatic scaling
- **🛡️ Fault Tolerance**: Retry mechanisms and graceful error handling
- **📈 Observability**: Comprehensive logging and metrics
- **🔧 Configuration Management**: Environment-based configuration
- **🐳 Containerized**: Production-ready Docker setup

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   WhatsApp      │    │   AI Middleware  │    │    Shopify      │
│   (via ZOKO)    │◄──►│   (FastAPI)      │◄──►│   (E-commerce)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   OpenAI GPT-4   │
                       │   (AI Engine)    │
                       └──────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Google Cloud   │
                       │   (Firestore)    │
                       └──────────────────┘
```

### Data Flow
1. **Customer Message** → ZOKO Webhook → AI Middleware
2. **Language Detection** → Translation (if needed)
3. **Intent Analysis** → Product Recommendation OR AI Chat
4. **Response Generation** → Translation → ZOKO → Customer
5. **Session Storage** → Firestore (conversation history)

## 🛠️ Technology Stack

### Backend Framework
- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation and settings management
- **Gunicorn** - Production WSGI server with Uvicorn workers

### AI & ML
- **OpenAI GPT-4** - Advanced language model for conversations
- **LangDetect** - Language detection and translation
- **Tenacity** - Retry mechanisms for API resilience

### Cloud Services
- **Google Cloud Run** - Serverless container platform
- **Google Cloud Firestore** - NoSQL document database
- **Google Cloud Storage** - Media file storage
- **Google Secret Manager** - Secure credential management

### External Integrations
- **ZOKO API** - WhatsApp Business API provider
- **Shopify Admin API** - E-commerce platform integration

### Development Tools
- **Docker** - Containerization
- **Google Cloud Build** - CI/CD pipeline
- **Python 3.11** - Runtime environment

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- Docker (for containerized deployment)
- Google Cloud CLI (for cloud deployment)
- Active accounts for:
  - OpenAI API
  - ZOKO WhatsApp Business
  - Shopify Store
  - Google Cloud Platform

### Environment Variables
Create a `.env` file in the project root:

```bash
# Google Cloud
PROJECT_ID=your-gcp-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key

# Shopify
SHOPIFY_API_KEY=your-shopify-api-key
SHOPIFY_API_PASSWORD=your-shopify-api-password
SHOPIFY_STORE_NAME=your-store-name

# ZOKO
ZOKO_API_KEY=your-zoko-api-key

# Application
API_KEY=your-secret-api-key
ENV=development
```

### Local Installation
```bash
# Clone the repository
git clone <repository-url>
cd automation

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 🐳 Docker Deployment

### Build Docker Image
```bash
# Build the production image
docker build -t ai-middleware .

# Verify the image was created
docker images | grep ai-middleware
```

### Run Container Locally
```bash
# Run with environment variables
docker run -d \
  --name ai-middleware \
  --env-file .env \
  -p 8080:8080 \
  ai-middleware

# Check container status
docker ps

# View logs
docker logs ai-middleware
```

### Docker Commands Reference
```bash
# Start container
docker start ai-middleware

# Stop container
docker stop ai-middleware

# Restart container
docker restart ai-middleware

# Remove container
docker rm ai-middleware

# View real-time logs
docker logs -f ai-middleware

# Execute commands in container
docker exec -it ai-middleware bash

# Check container health
docker inspect ai-middleware | grep Health -A 10
```

### Docker Configuration
The application uses a multi-stage Docker build for optimization:

```dockerfile
# Builder stage
FROM python:3.11-slim as builder
# Install build dependencies and create virtual environment

# Production stage
FROM python:3.11-slim
# Copy virtual environment and run as non-root user
```

**Key Features:**
- Multi-stage build for smaller image size
- Non-root user for security
- Health checks for monitoring
- Optimized layer caching

## ☁️ Google Cloud Deployment

### Prerequisites
```bash
# Install Google Cloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Authenticate and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### Service Account Setup
1. **Create Service Account:**
   ```bash
   gcloud iam service-accounts create ai-middleware-sa \
     --display-name="AI Middleware Service Account"
   ```

2. **Assign Roles:**
   ```bash
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:ai-middleware-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/datastore.user"
   
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:ai-middleware-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/storage.admin"
   ```

3. **Create and Download Key:**
   ```bash
   gcloud iam service-accounts keys create service-account.json \
     --iam-account=ai-middleware-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

### Secret Management
```bash
# Create secrets in Google Secret Manager
echo -n "your-openai-api-key" | gcloud secrets create openai-api-key --data-file=-
echo -n "your-shopify-api-key" | gcloud secrets create shopify-api-key --data-file=-
echo -n "your-shopify-password" | gcloud secrets create shopify-password --data-file=-
echo -n "your-shopify-store-name" | gcloud secrets create shopify-store --data-file=-
echo -n "your-zoko-api-key" | gcloud secrets create zoko-api-key --data-file=-
echo -n "your-api-key" | gcloud secrets create api-key --data-file=-
```

### Deploy with Cloud Build
```bash
# Deploy using the provided cloudbuild.yaml
gcloud builds submit --config cloudbuild.yaml .
```

### Manual Deployment
```bash
# Build and push image
docker build -t gcr.io/YOUR_PROJECT_ID/ai-middleware .
docker push gcr.io/YOUR_PROJECT_ID/ai-middleware

# Deploy to Cloud Run
gcloud run deploy ai-middleware \
  --image gcr.io/YOUR_PROJECT_ID/ai-middleware \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars "PROJECT_ID=YOUR_PROJECT_ID,ENV=production" \
  --set-secrets "OPENAI_API_KEY=openai-api-key:latest,SHOPIFY_API_KEY=shopify-api-key:latest,SHOPIFY_API_PASSWORD=shopify-password:latest,SHOPIFY_STORE_NAME=shopify-store:latest,ZOKO_API_KEY=zoko-api-key:latest,API_KEY=api-key:latest"
```

### Post-Deployment
After successful deployment, you'll receive a URL like:
```
https://ai-middleware-xxxxx-uc.a.run.app
```

**Test the deployment:**
```bash
curl https://ai-middleware-xxxxx-uc.a.run.app/
```

## 🔧 Local Development

### Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Development Commands
```bash
# Run tests
pytest

# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

### Project Structure
```
automation/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── logger.py            # Structured logging setup
│   ├── deps.py              # Dependency injection
│   ├── gcp.py               # Google Cloud operations
│   ├── openai_agent.py      # OpenAI integration
│   ├── zoko_client.py       # ZOKO API client
│   ├── shopify_client.py    # Shopify API client
│   ├── translation.py       # Language detection & translation
│   ├── recommendation.py    # Product recommendation engine
│   ├── broadcast.py         # Multi-language broadcasting
│   └── gunicorn_conf.py     # Production server configuration
├── templates.json           # Multi-language message templates
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── cloudbuild.yaml         # Google Cloud Build pipeline
└── README.md               # This documentation
```

## 📚 API Documentation

### Base URL
- **Local:** `http://localhost:8080`
- **Production:** `https://your-app-url.a.run.app`

### Authentication
All endpoints (except health check) require the `x-api-key` header:
```bash
curl -H "x-api-key: your-secret-api-key" https://your-app-url.a.run.app/test-gcp
```

### Endpoints

#### 1. Health Check
```http
GET /
```
**Response:**
```json
{
  "status": "ok"
}
```

#### 2. Test GCP Connectivity
```http
GET /test-gcp
```
**Headers:** `x-api-key: your-secret-api-key`

**Response:**
```json
{
  "message": "GCP OK"
}
```

#### 3. ZOKO Webhook
```http
POST /webhook/zoko
```
**Headers:** 
- `Content-Type: application/json`
- `x-api-key: your-secret-api-key`

**Request Body:**
```json
{
  "messages": [
    {
      "from": "1234567890",
      "text": {
        "body": "Hello, I need help with products"
      }
    }
  ]
}
```

**Response:**
```json
{
  "status": "processed"
}
```

#### 4. Broadcast Promotional Message
```http
POST /broadcast/promo
```
**Headers:** `x-api-key: your-secret-api-key`

**Response:**
```json
{
  "status": "broadcast_sent"
}
```

### Interactive Documentation
Access the interactive API documentation:
- **Swagger UI:** `https://your-app-url.a.run.app/docs`
- **ReDoc:** `https://your-app-url.a.run.app/redoc`

## 📱 ZOKO-WhatsApp Integration

### Prerequisites
- Active ZOKO account (https://zoko.io/)
- WhatsApp Business API approval
- Verified business phone number
- Production webhook URL (HTTPS required)

### Step 1: ZOKO Account Setup

#### 1.1 Create ZOKO Account
1. **Visit:** https://zoko.io/
2. **Sign up** for a ZOKO account
3. **Verify** your email and phone number
4. **Complete** business verification

#### 1.2 WhatsApp Business API Setup
```bash
# In ZOKO Dashboard:
1. Go to "WhatsApp" → "Get Started"
2. Select your business type
3. Provide business details:
   - Business name
   - Business address
   - Business description
   - Website URL
4. Upload required documents
5. Wait for approval (24-48 hours)
```

### Step 2: Get ZOKO API Credentials

#### 2.1 API Key Generation
```bash
# In ZOKO Dashboard:
1. Go to "Settings" → "API Keys"
2. Click "Generate New API Key"
3. Copy the API key (starts with 'zoko_')
4. Add to your .env file:
   ZOKO_API_KEY=zoko_your_api_key_here
```

#### 2.2 Webhook URL Setup
```bash
# Your webhook URL will be:
# Local: http://localhost:8080/webhook/zoko
# Production: https://your-app-url.a.run.app/webhook/zoko
```

### Step 3: Configure Webhook in ZOKO

#### 3.1 Set Webhook URL
```bash
# In ZOKO Dashboard:
1. Go to "Settings" → "Webhooks"
2. Add webhook URL: https://your-app-url.a.run.app/webhook/zoko
3. Select events:
   ✅ message_received
   ✅ message_delivered
   ✅ message_read
4. Set HTTP method: POST
5. Add headers:
   x-api-key: your-secret-api-key
6. Save webhook configuration
```

#### 3.2 Test Webhook
```bash
# Test webhook connectivity
curl -X POST \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-api-key" \
  -d '{
    "messages": [{
      "from": "1234567890",
      "text": {
        "body": "Hello, test message"
      }
    }]
  }' \
  https://your-app-url.a.run.app/webhook/zoko
```

### Step 4: WhatsApp Business Setup

#### 4.1 Phone Number Configuration
```bash
# In ZOKO Dashboard:
1. Go to "WhatsApp" → "Phone Numbers"
2. Add your business phone number
3. Verify the number via SMS/call
4. Set display name and business info
5. Configure business hours and away message
```

#### 4.2 Message Templates (Optional)
```bash
# Create message templates for:
1. Welcome messages
2. Product catalogs
3. Order confirmations
4. Customer support

# Template example:
"Hi {{1}}, welcome to {{2}}! 🎉 
How can we help you today?"
```

### Step 5: Integration Testing

#### 5.1 Test Message Flow
```bash
# 1. Send test message from WhatsApp
# 2. Check webhook receives it:
docker logs ai-middleware | grep "webhook"

# 3. Verify AI response:
docker logs ai-middleware | grep "OpenAI"

# 4. Check ZOKO sends response:
docker logs ai-middleware | grep "Sent text"
```

#### 5.2 Test Different Scenarios
```bash
# Test product recommendation
"recommend shoes for running"

# Test general chat
"Hello, how are you?"

# Test different languages
"Hola, necesito ayuda" (Spanish)
"Bonjour, je voudrais des informations" (French)
```

### Step 6: Production Deployment

#### 6.1 Update Environment Variables
```bash
# In your .env file:
ZOKO_API_KEY=zoko_your_production_api_key
API_KEY=your_production_api_key

# In Google Cloud Run:
gcloud run services update ai-middleware \
  --set-env-vars "ZOKO_API_KEY=zoko_your_key,API_KEY=your_key"
```

#### 6.2 SSL Certificate (Required for Production)
```bash
# Google Cloud Run provides HTTPS automatically
# Your webhook URL will be:
https://ai-middleware-xxxxx-uc.a.run.app/webhook/zoko
```

### Step 7: Monitoring and Analytics

#### 7.1 ZOKO Dashboard Analytics
```bash
# Monitor in ZOKO Dashboard:
1. Message delivery rates
2. Response times
3. Customer engagement
4. Template performance
5. Error rates
```

#### 7.2 Application Logs
```bash
# Monitor your application:
docker logs -f ai-middleware

# Or in Google Cloud:
gcloud logging read "resource.type=cloud_run_revision"
```

### Step 8: Advanced Features

#### 8.1 Rich Media Messages
```bash
# Send images, documents, videos
# Update zoko_client.py to support:
- send_image()
- send_document()
- send_video()
- send_audio()
```

#### 8.2 Interactive Messages
```bash
# Send buttons, quick replies
# Example carousel for products:
{
  "type": "interactive",
  "interactive": {
    "type": "product_list",
    "body": "Here are our products:",
    "action": {
      "button": "View Products",
      "sections": [...]
    }
  }
}
```

#### 8.3 Broadcast Messages
```bash
# Send promotional messages to all users
curl -X POST \
  -H "x-api-key: your-api-key" \
  https://your-app-url.a.run.app/broadcast/promo
```

### Step 9: Troubleshooting

#### 9.1 Common Issues
```bash
# Webhook not receiving messages:
1. Check webhook URL is correct
2. Verify API key in headers
3. Check SSL certificate (production)
4. Test webhook connectivity

# Messages not sending:
1. Verify ZOKO API key
2. Check message format
3. Ensure phone number is verified
4. Check rate limits

# AI responses not working:
1. Verify OpenAI API key
2. Check internet connectivity
3. Monitor OpenAI rate limits
4. Check application logs
```

#### 9.2 Debug Commands
```bash
# Test ZOKO API directly:
curl -H "Authorization: Bearer zoko_your_key" \
  https://api.zoko.io/v1/messages

# Check webhook logs:
docker logs ai-middleware | grep "zoko"

# Test OpenAI integration:
curl -H "x-api-key: your-key" \
  https://your-app-url.a.run.app/test-gcp
```

### Step 10: Best Practices

#### 10.1 Message Guidelines
```bash
# Follow WhatsApp Business Policy:
1. No spam or unsolicited messages
2. Respect business hours
3. Provide opt-out options
4. Use approved message templates
5. Maintain professional tone
```

#### 10.2 Performance Optimization
```bash
# Optimize for scale:
1. Implement message queuing
2. Add retry mechanisms
3. Cache frequent responses
4. Monitor API rate limits
5. Use async processing
```

### Quick Start Checklist
- [ ] Create ZOKO account
- [ ] Get WhatsApp Business approval
- [ ] Generate API key
- [ ] Configure webhook URL
- [ ] Test message flow
- [ ] Deploy to production
- [ ] Monitor performance
- [ ] Set up analytics

## 🔐 Security & Authentication

### API Key Authentication
The application uses API key authentication for all protected endpoints:

```python
# Middleware implementation
class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: StarletteRequest, call_next):
        if request.url.path == "/":
            return await call_next(request)
        api_key = request.headers.get("x-api-key")
        if api_key != API_KEY:
            return JSONResponse(
                status_code=401, 
                content={"detail": "Invalid API key"}
            )
        return await call_next(request)
```

### Rate Limiting
Built-in rate limiting prevents abuse:
- **Limit:** 30 requests per minute per IP
- **Window:** 60 seconds
- **Exemption:** Health check endpoint

### Security Best Practices
- ✅ Non-root Docker user
- ✅ Environment variable secrets
- ✅ Input validation with Pydantic
- ✅ CORS configuration
- ✅ Request size limits
- ✅ Error message sanitization

## 🌍 Multi-Language Support

### Supported Languages
The application supports **35+ languages** including:

| Language | Code | Example |
|----------|------|---------|
| English | `en` | "Hi {name}! 🎉 Check out our latest products..." |
| Spanish | `es` | "¡Hola {name}! 🎉 ¡Mira nuestros últimos productos..." |
| French | `fr` | "Salut {name}! 🎉 Découvrez nos derniers produits..." |
| German | `de` | "Hallo {name}! 🎉 Schauen Sie sich unsere neuesten Produkte..." |
| Arabic | `ar` | "مرحباً {name}! 🎉 تحقق من أحدث منتجاتنا..." |
| Chinese | `zh` | "你好 {name}! 🎉 查看我们最新的产品..." |
| Japanese | `ja` | "こんにちは {name}さん！🎉 最新商品をご覧いただき..." |
| Korean | `ko` | "안녕하세요 {name}님! 🎉 최신 제품을 확인하고..." |
| Czech | `cs` | "Ahoj {name}! 🎉 Podívejte se naše nejnovější produkty..." |
| Polish | `pl` | "Cześć {name}! 🎉 Sprawdź nasze najnowsze produkty..." |

### Language Detection
Automatic language detection using `langdetect`:
```python
def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        logger.info(f"Detected language: {lang} for text: {text}")
        return lang
    except Exception as e:
        logger.error(f"Language detection failed: {e}")
        return "en"
```

### Translation Pipeline
1. **Detect** user's language
2. **Translate** to English for AI processing
3. **Generate** AI response in English
4. **Translate** back to user's language
5. **Send** localized response

## 📊 Monitoring & Logging

### Structured Logging
All logs are in JSON format for easy parsing:

```json
{
  "level": "INFO",
  "time": "2025-06-23 23:58:24,509",
  "name": "main",
  "message": "Health check endpoint called"
}
```

### Log Categories
- **Application:** Main application events
- **API:** External API calls and responses
- **Translation:** Language detection and translation
- **Recommendation:** Product recommendation engine
- **Broadcast:** Multi-language broadcasting
- **GCP:** Google Cloud operations
- **ZOKO:** WhatsApp API interactions
- **Shopify:** E-commerce platform operations

### Health Monitoring
Built-in health checks:
```bash
# Docker health check
docker inspect ai-middleware | grep Health -A 10

# Application health endpoint
curl https://your-app-url.a.run.app/
```

### Performance Metrics
- Request/response times
- API call success rates
- Translation accuracy
- Memory and CPU usage
- Error rates and types

## 🚨 Troubleshooting

### Common Issues & Solutions

#### 1. Docker Container Won't Start
**Problem:** Container exits immediately
```bash
# Check logs
docker logs ai-middleware

# Common causes:
# - Missing environment variables
# - Port conflicts
# - Permission issues
```

**Solution:**
```bash
# Verify environment file
cat .env

# Check port availability
netstat -tulpn | grep 8080

# Run with explicit environment
docker run -d \
  --name ai-middleware \
  -e PROJECT_ID=your-project \
  -e OPENAI_API_KEY=your-key \
  -p 8080:8080 \
  ai-middleware
```

#### 2. GCP Authentication Errors
**Problem:** `DefaultCredentialsError: File /path/to/your/service-account.json was not found`

**Solution:**
```bash
# Set credentials path
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Or add to .env file
echo "GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json" >> .env

# For local development, the app will run without GCP
```

#### 3. Import Errors
**Problem:** `ModuleNotFoundError: No module named 'config'`

**Solution:**
```bash
# Ensure you're in the project root
cd /path/to/automation

# Install dependencies
pip install -r requirements.txt

# Run with correct Python path
PYTHONPATH=/path/to/automation uvicorn src.main:app --reload
```

#### 4. API Key Authentication Fails
**Problem:** `401 Unauthorized` responses

**Solution:**
```bash
# Verify API key in .env file
cat .env | grep API_KEY

# Test with correct header
curl -H "x-api-key: your-actual-api-key" \
  https://your-app-url.a.run.app/test-gcp
```

#### 5. Rate Limiting Issues
**Problem:** `429 Too Many Requests`

**Solution:**
```bash
# Wait 60 seconds before retrying
# Or implement exponential backoff in your client
```

#### 6. Cloud Run Deployment Fails
**Problem:** Build or deployment errors

**Solution:**
```bash
# Check build logs
gcloud builds log [BUILD_ID]

# Verify project configuration
gcloud config get-value project

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com
```

#### 7. Memory Issues
**Problem:** Container runs out of memory

**Solution:**
```bash
# Increase memory allocation
gcloud run deploy ai-middleware \
  --memory 2Gi \
  --cpu 2

# Or optimize the application
# - Reduce worker count
# - Implement connection pooling
# - Add caching layers
```

### Debug Mode
Enable debug logging:
```bash
# Set debug environment variable
export LOG_LEVEL=DEBUG

# Or add to .env file
echo "LOG_LEVEL=DEBUG" >> .env

# Restart container
docker restart ai-middleware
```

### Performance Optimization
```bash
# Monitor resource usage
docker stats ai-middleware

# Check application metrics
curl https://your-app-url.a.run.app/metrics

# Analyze logs for bottlenecks
docker logs ai-middleware | grep "ERROR\|WARNING"
```

## 🤝 Contributing

### Development Workflow
1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include docstrings for public APIs
- Write unit tests for new features
- Update documentation as needed

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_main.py

# Run with verbose output
pytest -v
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

### Getting Help
- **Documentation:** This README and API docs
- **Issues:** Create GitHub issues for bugs
- **Discussions:** Use GitHub Discussions for questions
- **Email:** Contact the development team

### Emergency Contacts
- **Production Issues:** [Emergency Contact]
- **Security Issues:** [Security Contact]
- **API Support:** [API Support Contact]

---

**Built with ❤️ for enterprise-grade AI integration**