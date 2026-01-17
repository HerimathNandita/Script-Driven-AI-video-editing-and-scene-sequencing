# Methodology / ML Models Used / Enhancements

## 🔷 Machine Learning Models Integrated (NEW – MAJOR PROJECT)

To enhance real-world applicability and intelligence, the proposed system integrates multiple machine learning models at different stages of the automated film editing pipeline. These models enable intelligent understanding of scripts, videos, emotions, and scene relevance.

### 1. Script Understanding Model (NLP)

A natural language processing model is used to analyze the screenplay and extract semantic information such as scene boundaries, dialogues, and emotional context. Lightweight text-based models such as TF-IDF and word embeddings are used for dialogue similarity analysis, while transformer-based models are considered conceptually for advanced semantic understanding.

### 2. Speech-to-Text Model for Dialogue Matching

Audio tracks are extracted from video clips and processed using a speech-to-text model to convert spoken dialogues into text. The extracted dialogues are compared with script dialogues using similarity measures, improving scene alignment accuracy. This approach reflects real-world AI-assisted media processing techniques.

### 3. Emotion Recognition Model

A pre-trained facial emotion recognition model is used to detect dominant emotional expressions from video frames. Emotions such as happiness, sadness, anger, and neutrality are identified and mapped to script-defined emotional cues, enabling emotion-aware scene sequencing.

### 4. Visual Feature Extraction Model

A convolutional neural network (CNN)-based visual feature extractor is used to analyze background characteristics such as color contrast, brightness, and scene tone. These features help maintain visual continuity and aesthetic consistency in the final edited video.

### 5. Scene Ranking and Confidence Scoring Model

A lightweight machine learning classifier is used to rank candidate video clips for each script scene based on dialogue similarity, emotional alignment, and visual features. The model generates a confidence score for each match, improving explainability and decision transparency.

## 🔷 Advantages of Using ML Models

- Improves accuracy of scene matching
- Enables intelligent dialogue and emotion understanding
- Adds explainable AI through confidence scoring
- Aligns the system with real-world AI media tools
- Enhances project depth and innovation

## 🔷 Real-World Relevance of ML Integration

The integration of machine learning models makes the system closer to real-world AI-assisted video editing platforms used in media production. Similar ML-based techniques are employed in professional tools for rough-cut generation, content analysis, and automated storytelling. The proposed system demonstrates a prototype-level implementation suitable for academic and experimental use.

## 🔷 Final Improved Idea (System Overview)

This project proposes an emotion-aware, AI-driven film editing system that combines script analysis, video emotion recognition, and live user emotion feedback. The system allows users to either upload a screenplay file or manually enter script text. Raw video clips are analyzed to detect emotional and visual features. Additionally, the system captures live facial expressions through a webcam to identify the user’s current emotional state, which is used as a preference signal during scene selection and sequencing. By combining script intent, video emotions, and live user feedback, the system generates a personalized, coherent edited film. This approach reflects real-world AI-assisted media production workflows and enhances user involvement in the editing process.
