# 📝 OS1B Project Description 
### 🧾Abstract:  
Software developers frequently exhibit a deficit in security expertise, thereby exposing the systems, tools, and software they design to significant security vulnerabilities. This project aims to develop a knowledge base system aiming to systematically summarise the essential security skills required by software developers.  The project will utilize a dataset derived from a published research study. This dataset, compiled from developer discussion forums (Stack Overflow and GitHub), comprises 772 questions (386 + 386) concerning security challenges encountered by software developers across 15 programming languages, including Java, PHP, JavaScript, C/C++, and Python.  Generative AI models and Natural Language Processing Techniques will be employed to analyse the dataset and extract actionable recommendations for resolving the identified security challenges. These extracted recommendations will be used to the design of a knowledge base system intended to support software developers in addressing security concerns.


### 🧑‍💻 Group Members: 
- Cong Deng a1155047
- Sheng Wang a1903948
- Tianhua Zhang a1915934
- Xin Wei a1912958
- Yifan Gu a1909803

🧑‍💼 Supervised by: **Dr Orvila Sarker**


# 🔐 Augmented Security Knowledge Hub
An AI-powered platform to help developers understand and solve security-related coding challenges by leveraging semantic search, classification, and large language models.

### 🌟 Project Overview

This project is developed as part of the MCI coursework. It aims to assist developers in resolving security-related programming questions by:

- **Classifying** question types (e.g., how-to, conceptual, debugging)
- **Retrieving** relevant Stack Overflow posts using semantic similarity
- **Analyzing** sentiment and security topics
- **Generating** summaries using a lightweight local LLM (e.g., LLaMA 3 via Ollama)

### 🧩 Features

- Natural language question input
- AI classifier to categorize question intent
- LDA-based topic extraction
- Semantic similarity search on a curated Stack Overflow dataset
- LLM-generated summaries for quick insights
- Web-based user interface (React + Tailwind CSS)
- FastAPI backend with modular architecture

### 🧰 Tech Stack

| Layer        | Technology                       |
|--------------|----------------------------------|
| Frontend     | React, Tailwind CSS              |
| Backend      | FastAPI, Python, LangChain       |
| Embeddings   | Sentence-Transformers (MiniLM)   |
| LLM          | LLaMA 3 (via Ollama)             |
| Deployment   | cloud-based sever                |

### 🧪 Testing
- Backend unit tests: pytest

- API testing: Postman / curl

- End-to-end test: manual input → output validation

### 🗃️ Project Structure
```
📁 root/code/
├── 🧩 rag-frontend/                        → React + Tailwind UI
├── 🖥️ rag-backend/                         → FastAPI backend
├── 📊 rag-backend/data/                    → Stack Overflow data
├── 🧠 rag-backend/app/pipeline/            → MiniLM + LDA
├── 🧠 rag-experiment/langchain_version/    → LLM
├── 📄 README.md                            → Docs
|
📁 root/docs/                               → Project Management Docs
```
##### 🕒 [Minutes/](https://github.cs.adelaide.edu.au/MCI-Project-2025/OS1B/tree/main/docs/Minutes/) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; → Team Meeting Records

##### 🗓️ [Timelines/](https://github.cs.adelaide.edu.au/MCI-Project-2025/OS1B/tree/main/docs/Timelines/)  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; → Team Member Timeline Records                          

&nbsp;

### 🗺️ Roadmap
| Phase         | Scrum Master     | Timeline | Objective                                                                                  | Status      |
|---------------|------------------|----------|--------------------------------------------------------------------------------------------|-------------|
|  Sprint 1   |      -           | Week 1   | Understand the dataset structure and perform preprocessing on Stack Overflow data           |   ✅   |
|  Sprint 2   |    Cong Deng     | Week 2   | Design and run ChatGPT prompts to extract challenges and required skills                    |   ✅   |
|  Sprint 3   |    Sheng Wang    | Week 3   | Build and train an SVM classifier to categorize question types & try to use Bert for unsupervised learning       |   ✅   |
|  Sprint 4   |    Tianhua Zhang | Week 4   | Pitch Presentation & Cluster and validate ChatGPT answers into sub-categories                                    |   ✅   |
|  Sprint 5   |    Xin Wei       | Week 5   | Build up the pipeline & Business Case Documentation                                                              |   ✅   |
|  Sprint 6   |    Yifan Gu      | Week 6   | Import documentation and run the pipeline                                                   |   ✅   |
|  Sprint 7   |    Cong Deng     | Week 7   | Record and analyse the results & Milestone 1 - Product Demo Delivery                        |   ✅   |
|  Sprint 8   |    Sheng Wang    | Week 8   | Testing Plan                                                        |  ✅  |
|  Sprint 9   |    Tianhua Zhang | Week 9   | UI/UX Interface Design & Prepare final testing                                              |   ✅   |
|  Sprint 10  |    Xin Wei       | Week 10  | Debugging & Bug fix                                                                         |   ✅   |
|  Sprint 11  |    Yifan Gu      | Week 11  | Product Testing                                                                             |   ✅   |
|  Sprint 12  |    Cong Deng     | Week 12  | Final Product Delivery & Report                                                             |   ✅   |

> 📝 *Status key:* ✅ Completed · ⏳ In Progress · 🔜 Not Started · 🧠 Final Stage
---
## 🏁🔚 The Project has been successfully completed. Thanks to all group members and our supervisor! -- 15th June
