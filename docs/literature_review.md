# Deep Literature Review: AutoML & RAG in Support Ticket Intelligence

This review provides an in-depth analysis of the technologies and methodologies used in modern automated customer support systems, focusing on the transition from traditional ML to AutoML and Generative AI with RAG.

## 1. Evolution of Support Ticket Classification

Customer support ticketing has moved through several distinct phases:
- **Phase 1: Rule-Based Systems**: Early systems used keyword matching and regex to route tickets. While fast, they struggled with linguistic nuances and misspellings.
- **Phase 2: Statistical Machine Learning**: The introduction of SVMs, Naive Bayes, and Random Forests allowed for semantic understanding. TF-IDF and Bag-of-Words were the standard vectorization techniques.
- **Phase 3: Deep Learning (NLP)**: Models like Word2Vec and later BERT (Bidirectional Encoder Representations from Transformers) enabled context-aware embeddings, significantly improving accuracy in multi-class classification.
- **Phase 4: Agentic AI & RAG**: The current state-of-the-art involves Large Language Models (LLMs) that don't just classify, but reason and retrieve relevant information to provide actionable solutions.

## 2. Automated Machine Learning (AutoML) in Support

AutoML aims to automate the end-to-end process of applying machine learning to real-world problems.
- **Hyperparameter Optimization (HPO)**: Using Bayesian Optimization to find the best settings for models like XGBoost or LightGBM.
- **Neural Architecture Search (NAS)**: Automating the design of neural networks for specific NLP tasks.
- **AutoML for Support**: Tools like Auto-Sklearn or H2O.ai can be used to quickly benchmark traditional models against a dataset like the 200k synthetic tickets used here, ensuring the "baseline" metadata (Queue, Priority) is as accurate as possible before moving to GenAI.

## 3. Retrieval-Augmented Generation (RAG) Deep Dive

RAG addresses the two biggest flaws of LLMs: hallucinations and lack of domain-specific/current knowledge.
- **Semantic Retrieval**: Instead of keyword matching, vector embeddings (e.g., Ada-002, GTE-Large) capture the "meaning" of a ticket.
- **The "Contextual Grounding" Effect**: By providing top-k historical tickets to the LLM, we ensure that the "Action" suggested is one that has been successfully used in the past.
- **Ref**: *Borgeaud et al. (2022)* - Improving language models by retrieving from trillions of tokens.

## 4. Multi-Label vs. Multi-Stage Architectures

A critical design choice is whether to use one large model for everything or a multi-stage approach.
- **The Argument for Multi-Stage**: Metadata (Team, Priority) is stable and requires low latency. Generative tasks (Action, Resolution) require high reasoning. Separating them allows for:
    - **Efficiency**: Cheap ML models run first.
    - **Relevance**: LLMs only run when complex reasoning is needed.
    - **Explainability**: Each stage of the pipeline can be audited independently.

## 5. Metrics for Success

A "Deep" support system must be evaluated on more than just "Accuracy":
- **F1-Score**: Crucial for imbalanced classes (e.g., rare but critical security tickets).
- **Mean Time to Resolution (MTTR)**: The ultimate business metric. Does the AI actually speed up the human agent?
- **Retrieval Mean Reciprocal Rank (MRR)**: Measures how well the RAG system finds the *best* historical case.
- **Human-in-the-Loop Approval Rate**: How often do agents use the AI-suggested "Action" without changes?

## 6. Conclusion for the Current Project

The proposed architecture aligns with these findings by:
1.  Using **Optimized ML** for established labels (Speed & Reliability).
2.  Implementing **RAG** for Action suggestion (Knowledge & Context).
3.  Focusing on **Critical Incidents** through prioritized retrieval, ensuring high-stakes tickets get the most detailed "Action" suggestions.
