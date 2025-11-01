#!/usr/bin/env python3
"""
LinkedIn posting script - posts demo showcase to LinkedIn
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

def load_linkedin_post():
    """Load the generated LinkedIn post"""
    today = datetime.now().strftime("%Y-%m-%d")
    post_file = Path(f"outputs/{today}/linkedin_post.md")

    with open(post_file, 'r', encoding='utf-8') as f:
        return f.read()

def load_screenshot():
    """Load the screenshot image"""
    today = datetime.now().strftime("%Y-%m-%d")
    screenshot_file = Path(f"outputs/{today}/screenshots/terminal_output.png")

    if not screenshot_file.exists():
        print(f"WARNING: Screenshot not found at {screenshot_file}")
        return None

    with open(screenshot_file, 'rb') as f:
        return f.read()

def upload_image(access_token, person_urn, image_data):
    """Upload image to LinkedIn and get asset URN"""

    # Step 1: Register upload
    register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"

    register_payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": person_urn,
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(register_url, json=register_payload, headers=headers)

    if response.status_code != 200:
        print(f"ERROR: Failed to register upload: {response.text}")
        return None

    upload_info = response.json()
    upload_url = upload_info['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    asset_urn = upload_info['value']['asset']

    # Step 2: Upload image
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "image/png"
    }

    response = requests.put(upload_url, data=image_data, headers=headers)

    if response.status_code != 201:
        print(f"ERROR: Failed to upload image: {response.text}")
        return None

    return asset_urn

def post_to_linkedin(access_token, person_urn, post_text, image_asset_urn=None):
    """Post to LinkedIn"""

    url = "https://api.linkedin.com/v2/ugcPosts"

    # Build post payload
    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_text
                },
                "shareMediaCategory": "NONE" if not image_asset_urn else "IMAGE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    # Add image if available
    if image_asset_urn:
        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
            {
                "status": "READY",
                "description": {
                    "text": "RAG pattern demonstration with colored ASCII art"
                },
                "media": image_asset_urn,
                "title": {
                    "text": "RAG Pattern Demo"
                }
            }
        ]
        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("✅ Successfully posted to LinkedIn")
        return True
    else:
        print(f"❌ Failed to post to LinkedIn: {response.status_code}")
        print(response.text)
        return False

def main():
    """Main execution"""
    print("📱 Posting to LinkedIn...")

    # Get credentials from environment
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    person_urn = os.getenv('LINKEDIN_URN')

    if not access_token or not person_urn:
        print("ERROR: LINKEDIN_ACCESS_TOKEN and LINKEDIN_URN environment variables must be set")
        print("Skipping LinkedIn post (dry run mode)")
        sys.exit(0)  # Don't fail the workflow, just skip posting

    # Load post content
    post_text = load_linkedin_post()
    print("✓ Post content loaded")

    # Load screenshot
    image_data = load_screenshot()
    image_asset_urn = None

    if image_data:
        print("✓ Screenshot loaded, uploading to LinkedIn...")
        image_asset_urn = upload_image(access_token, person_urn, image_data)
        if image_asset_urn:
            print(f"✓ Image uploaded: {image_asset_urn}")

    # Post to LinkedIn
    success = post_to_linkedin(access_token, person_urn, post_text, image_asset_urn)

    if success:
        print("✅ LinkedIn post complete")
    else:
        print("❌ LinkedIn post failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
