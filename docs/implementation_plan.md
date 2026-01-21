# Refined ML Architecture: 5 Models + RAG

Based on the "real" dataset ([customer_support_tickets.csv](file:///C:/Users/SRINATH/Desktop/data science/machine learing/ml project/data/raw/customer_support_tickets.csv)) and the provided visual analysis, we will implement the following hybrid architecture.

## User Review Required

> [!IMPORTANT]
> - **Team Mapping**: Per your visualization, we will use `Ticket Channel` as the label for the **Team** model.
> - **Payments Model**: Since "Payments" is not a direct column, we will implement a binary classifier or a sub-category detection focusing on "Billing inquiry" and "Refund request" types. Please confirm if this approach meets your requirement.
> - **Groq for "Action"**: The `Action` field will be purely generative, using RAG to fetch context from the `Resolution` column of historical tickets.

## Proposed Changes

### 1. Data Processing
- Merge `Ticket Subject` and `Ticket Description` into a single feature text.
- Clean text: Lowercase, remove special characters, and handle templates like `{product_purchased}`.

### 2. The 5 Models (Traditional ML)
We will use Optimized SVM/LinearSVC for the following:
- **Type**: 5 categories (Technical issue, Billing, etc.)
- **Priority**: 4 categories (Low, Medium, High, Critical)
- **Team**: 4 categories (Social media, Chat, Email, Phone) - *as per your "Ticket Channels (Teams)" plot.*
- **Payments**: Binary classification (Is this a payment/billing related ticket?)
- **TTR**: Regression for `Time to Resolution`.

### 3. The RAG System (GenAI)
For the **Action** suggestion:
- **Vector Store**: FAISS with HuggingFace embeddings.
- **Retrieval**: Find top 3 `Ticket Description` -> `Resolution` pairs.
- **LLM**: Use **Groq** (e.g., Llama-3-70b) to generate a step-by-step "Action Suggestion" based on the current ticket and retrieved resolutions.

---

### [NEW] notebooks/hybrid_rag_tickets.ipynb
A clean, documented notebook implementing the full pipeline from scratch.

## Verification Plan

### Automated Tests
- **RAG Consistency**: Verify the LLM uses retrieved context in Its "Action" field.
- **Model performance**: Standard classification reports for the 4 classifiers.

### Manual Verification
- Testing with specific "Critical" cases as highlighted in your request.
