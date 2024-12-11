# FlipVision - Empowering Your AI E-commerce Experience 

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

1. Clone this repository:
   ```bash
   git clone https://github.com/SASIDEVIvenaram/FlipVision.git
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the development server:
   ```bash
   python manage.py runserver

# Website Features

FlipVision is built to simplify and enhance the online shopping experience for everyone. Here’s what you can expect:

## For Customers 
- **Easy Registration**: Sign up with essential details like your username, email, and address.
- **Product Browsing**: Explore packed and unpacked products with advanced filters like categories, price range, and sorting options.
- **Smart Wishlist**: Save your favorite items for future purchases.
- **Hassle-Free Checkout**: Quickly review your cart and finalize your orders.

## For Sellers 
- **Profile Setup**: Create and verify your seller profile, complete with GST and bank details.
- **Product Management**: Add, update, and feature your products with ease.
- **AI-Powered Validation**:
  - Freshness analysis for unpacked products (e.g., fruits, vegetables). 
  - Brand detection and expiry validation for packed goods. 
- **Order Handling**: Manage and update the status of customer orders seamlessly.

## For Admins 
- Oversee seller profiles and product listings.
- Ensure smooth platform operations.
- Manage and verify all order processes.

---

# Key Technologies

FlipVision is powered by:
- **Django Framework**: Backend and dynamic functionalities.
- **AI Models**:
  - Freshness Analysis for unpacked items like apples, bananas, and carrots. 
  - Brand and Expiry Detection for packed goods.
- **Responsive Design**: Optimized for both desktop and mobile views.

---

# How to Use

## Access the Website 
1. Open your browser and go to the FlipVision website.
2. Choose your role: Customer, Seller, or Admin.

## Customer Workflow 
1. **Register**: Fill out the form with your details.
2. **Log in**: Use your username and password.
3. **Shop**: Browse, add to cart, and proceed to checkout!

## Seller Workflow 
1. **Register**: Sign up as a seller and wait for admin verification.
2. **Add Products**: Upload images, set prices, and manage stock.
3. **Validate Products**: Use AI tools to ensure quality and freshness.
4. **Update Order Status**: Keep customers updated on their orders.

## Admin Workflow 
1. **Manage Users**: Verify seller profiles and approve listings.
2. **Oversee Orders**: Ensure smooth order fulfillment.

---

## AI-Powered Tools

### Freshness Analysis
Ensure the quality of unpacked products like fruits and vegetables using advanced AI detection.

### Brand & Expiry Detection
For packed products, verify brand authenticity and expiry dates to maintain customer trust.

---

## Why FlipVision?
- AI-powered tools for quality assurance. 
- Seamless workflows for Customers, Sellers, and Admins. 
- Enhanced shopping experience with smart filters and features. 

---

# Future Enhancements

We are constantly working to make FlipVision even better! Stay tuned for:
- Personalized recommendations. 
- Advanced analytics for sellers. 
- More AI tools for quality assurance. 

---
   
# Contributors

We welcome contributions to FlipVision! Feel free to fork this repo, create new features, or report bugs. Together, we can make FlipVision the best e-commerce platform out there!

 Explore FlipVision Now! 

Access the website: https://app.saveetha.in

# Connect With Us

Website: https://app.saveetha.in

Happy shopping and selling on FlipVision!
