---
title: Prompt Injection Detector
emoji: 🛡️
sdk: docker
app_port: 8501
---

# Machine Learning-Based Prompt Injection Detection

A CYBERSEC 520 final project investigating direct prompt injection detection using traditional machine learning.

## Models
- TF-IDF + Logistic Regression
- TF-IDF + Linear SVM

## Datasets
- Primary: NeurAlchemy Prompt Injection Dataset
- Secondary: Wambosec Prompt Injections

## Application
Users can enter a text prompt and select a classification model.

The application returns:
- Benign
- Potential Prompt Injection

## Limitations
The models may miss unfamiliar prompt injection attempts or incorrectly flag legitimate requests.

Cross-dataset evaluation showed reduced performance on Wambosec compared with NeurAlchemy.

This is a research prototype, not a production-grade security enforcement system.
