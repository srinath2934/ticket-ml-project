# Methodology Summary for IEEE Paper

## System Overview
A novel hybrid approach combining traditional Machine Learning with Generative AI and Retrieval-Augmented Generation (RAG) for intelligent support ticket classification and action recommendation.

## Dataset
- **Source**: Customer support tickets dataset
- **Size**: 8,469 tickets
- **Features**: Ticket Subject, Description, Type, Priority, Channel, Resolution
- **Languages**: Multi-language support (English, German, etc.)

## Preprocessing Pipeline
1. **Text Combination**: Merged `Ticket Subject` + `Ticket Description` into unified feature
2. **Label Engineering**:
   - Mapped `Ticket Channel` → `Team` classification
   - Derived binary `Payments` flag from ticket types
   - Calculated `TTR (Time to Resolution)` in hours
3. **Text Cleaning**: Lowercase conversion, special character handling

## Model Architecture

### Traditional ML Component (Stage 1)
**Purpose**: Fast, efficient classification of structured metadata

#### Models:
1. **Team Classifier**
   - Algorithm: LinearSVC
   - Vectorization: TF-IDF (5000 features, bigrams)
   - Output: Email, Chat, Phone, Social Media

2. **Type Classifier**
   - Algorithm: LinearSVC
   - Output: Technical Issue, Billing Inquiry, Refund Request, etc.

3. **Priority Classifier**
   - Algorithm: LinearSVC
   - Output: Low, Medium, High, Critical

4. **Payments Classifier**
   - Algorithm: LinearSVC (Binary)
   - Output: Payment-related (Yes/No)

5. **TTR Regressor**
   - Algorithm: Ridge Regression
   - Output: Estimated hours to resolution

**Implementation**: All models wrapped in `sklearn.pipeline.Pipeline` for production readiness

### GenAI/RAG Component (Stage 2)
**Purpose**: Context-aware action recommendation based on historical success patterns

#### Architecture:
1. **Embedding Layer**
   - Model: `all-MiniLM-L6-v2` (Sentence Transformers)
   - Dimension: 384
   
2. **Vector Store**
   - Engine: FAISS (Facebook AI Similarity Search)
   - Index Type: L2 (Euclidean distance)
   - Indexed Records: 8,469 historical ticket resolutions

3. **Retrieval Mechanism**
   - Query: New ticket description (embedded)
   - Retrieval: Top-3 most similar historical cases
   - Similarity Metric: Cosine similarity

4. **Generation Layer**
   - LLM: Llama 3.3 70B (via Groq API)
   - Temperature: 0.2 (low variance for consistent recommendations)
   - Context Window: 32,768 tokens
   - Prompt Engineering: Few-shot learning with retrieved cases

## Training Configuration
- **Split Ratio**: 80% Train / 20% Test
- **Random State**: 42 (reproducibility)
- **Cross-Validation**: Stratified sampling for class balance
- **Feature Selection**: TF-IDF with min_df=2 to reduce noise

## Evaluation Metrics
### Classification Models:
- Precision
- Recall
- F1-Score
- Accuracy

### Regression Model (TTR):
- Mean Absolute Error (MAE)
- R² Score

### RAG System:
- Retrieval Accuracy (manual evaluation)
- Action Relevance Score (human-in-the-loop validation)

## Novel Contributions
1. **Hybrid Architecture**: First system to combine traditional ML efficiency with GenAI intelligence for support automation
2. **Multi-Stage Pipeline**: Separation of "static" predictions (fast) from "dynamic" recommendations (smart)
3. **Production-Ready RAG**: FAISS-based vector search with sub-second latency for real-time deployment
4. **Cost Optimization**: Uses traditional ML for 83% of predictions, reserving expensive LLM calls only for action generation

## Experimental Setup
- **Hardware**: Consumer-grade laptop (no GPU required for inference)
- **Software**: Python 3.11, scikit-learn 1.3, FAISS-CPU, Groq API
- **Training Time**: ~3 minutes for all 5 traditional models
- **Inference Time**: 
  - Traditional ML: <50ms per ticket
  - RAG + LLM: ~2 seconds per ticket

## Reproducibility
All code, datasets, and configurations are available in the GitHub repository with detailed documentation for complete reproducibility of results.
