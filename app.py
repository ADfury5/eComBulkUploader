#To automate the bulk upload of product data to eCommerce platforms, reducing both time and effort required in managing large inventories.
import pandas as pd
import requests
import os
import json
import time

# Configuration
API_URL = "https://ecommerce-platform.com/api/v1/products"  # Replace with actual API endpoint
API_KEY = "your_api_key_here"  # Replace with your API key
IMAGE_UPLOAD_URL = "https://ecommerce-platform.com/api/v1/images"  # Replace with image upload endpoint

# Reading product data from CSV
def read_product_data(file_path):
    # Use pandas to read CSV data into a dataframe
    df = pd.read_csv(file_path)
    return df

# Uploading images to the platform
def upload_image(image_path):
    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"Image file {image_path} not found!")
        return None
    
    # API request to upload the image
    with open(image_path, 'rb') as image_file:
        files = {'file': image_file}
        headers = {'Authorization': f'Bearer {API_KEY}'}
        response = requests.post(IMAGE_UPLOAD_URL, headers=headers, files=files)
        
        if response.status_code == 200:
            # Return the uploaded image URL
            return response.json()['image_url']
        else:
            print(f"Failed to upload image {image_path}. Status code: {response.status_code}")
            return None

# Post product data to eCommerce platform
def post_product(product_data):
    headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
    
    # Sending a POST request to create the product
    response = requests.post(API_URL, headers=headers, data=json.dumps(product_data))
    
    if response.status_code == 201:
        print(f"Successfully created product: {product_data['name']}")
    else:
        print(f"Failed to create product: {product_data['name']}. Status code: {response.status_code}")
        print("Response:", response.text)

# Main function to process and upload product data
def bulk_upload_products(csv_file):
    # Read the product data from CSV
    product_data = read_product_data(csv_file)

    # Moving through each product row in the dataframe
    for index, row in product_data.iterrows():
        # Prepare product details
        product_info = {
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "sku": row['sku'],
            "stock_quantity": row['stock_quantity'],
            "category": row['category']
        }

        # Uploading product image and get the URL
        image_url = upload_image(row['image_path'])
        if image_url:
            product_info['image_url'] = image_url
        
        # Posting the product data to the platform
        post_product(product_info)
        
        # Stopping to avoid hitting rate limits
        time.sleep(1)

if __name__ == "__main__":
    # Give path to the CSV file with product data
    csv_file_path = "product_data.csv"
    
    # Using the bulk upload function
    bulk_upload_products(csv_file_path)
