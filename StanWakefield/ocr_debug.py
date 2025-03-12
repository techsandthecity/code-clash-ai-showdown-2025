#!/usr/bin/env python3
"""
OCR Debugging Tool for SEC Tournament Predictor
This script helps debug OCR extraction from statistical images
"""

import os
import sys
from PIL import Image
import pytesseract
import argparse

def extract_text(image_path):
    """Extract text from an image using pytesseract OCR"""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}")
        return ""

def main():
    parser = argparse.ArgumentParser(description='Debug OCR extraction from SEC stats images')
    parser.add_argument('--image', type=str, help='Path to image file to process', default=None)
    parser.add_argument('--dir', type=str, help='Directory containing images to process', default='stats')
    parser.add_argument('--output', type=str, help='Path to save OCR output', default=None)
    args = parser.parse_args()
    
    if args.image:
        # Process single image
        print(f"Processing image: {args.image}")
        text = extract_text(args.image)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(text)
            print(f"OCR output saved to {args.output}")
        else:
            print("\nOCR Output:")
            print("===========")
            print(text)
            
    elif args.dir:
        # Process all images in directory
        if not os.path.isdir(args.dir):
            print(f"Error: Directory {args.dir} does not exist")
            return
            
        if args.output and not os.path.isdir(args.output):
            os.makedirs(args.output)
            
        for filename in os.listdir(args.dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(args.dir, filename)
                print(f"Processing image: {file_path}")
                text = extract_text(file_path)
                
                if args.output:
                    output_file = os.path.join(args.output, f"{os.path.splitext(filename)[0]}.txt")
                    with open(output_file, 'w') as f:
                        f.write(text)
                    print(f"OCR output saved to {output_file}")
                else:
                    print("\nOCR Output for {}:".format(filename))
                    print("======================={}".format("=" * len(filename)))
                    print(text)
                    print("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    main() 