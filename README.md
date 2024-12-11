# Flipkart Grid 6.O Robotic Challenge

# FlipVision in Action!

Watch this demo video to see FlipVision in action! 

[![FlipVision Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

# Project Overview
This AI-powered solution is designed to detect product brand names, assess freshness levels, and extract expiry dates from product images. The system combines advanced object detection and text recognition technologies to deliver accurate and actionable insights.
# Key Features
### 1. Brand Name Detection
Uses YOLO to detect product logos and text regions.
Extracts brand names, product type, and flavor details using PaddleOCR.
### 2. Freshness Detection
Identifies unpacked products and assesses their appearance using YOLO.
Predicts freshness levels based on visual cues like color and texture.
Estimates the remaining shelf life using lifespan prediction models.
### 3. Expiry Date Detection
Utilizes YOLO for bounding regions containing expiry dates.
Combines Faster R-CNN with ResNet45 for high-accuracy text extraction.
Verifies and parses date-like patterns (e.g., "DD/MM/YYYY") using DMY detection.
# Future Scope
1.Improving model efficiency, speed, and accuracy.
# Technologies and Tools Used
1.YOLO (You Only Look Once): For object detection and bounding box creation.
2.PaddleOCR: For extracting and recognizing text from images.
3.Faster R-CNN with ResNet45: For precise text extraction and validation.
4.Django: A Python-based web framework used to develop a scalable and user-friendly web application.
5.NoSQL Database (e.g., MongoDB): To store and retrieve unstructured data efficiently, such as extracted text and image metadata.
6.Business Logic Implementation: For integrating AI models with real-world workflows, such as freshness prediction and expiry validation, ensuring actionable results.
7.Python: Core programming language for building and integrating AI models.
# Installation
