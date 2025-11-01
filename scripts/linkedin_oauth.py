#!/usr/bin/env python3
"""
LinkedIn OAuth Helper Script

Helps you get LinkedIn API credentials interactively.
"""

import requests
import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse

def get_credentials():
    """Interactive LinkedIn OAuth flow"""

    print("🔐 LinkedIn OAuth Setup")
    print("=" * 50)
    print()
    print("You'll need:")
    print("1. Client ID from your LinkedIn App")
    print("2. Client Secret from your LinkedIn App")
    print()
    print("Get these from: https://www.linkedin.com/developers/apps")
    print()

    client_id = input("Enter your LinkedIn Client ID: ").strip()
    client_secret = input("Enter your LinkedIn Client Secret: ").strip()

    if not client_id or not client_secret:
        print("❌ Client ID and Secret are required")
        return

    redirect_uri = "http://localhost:8080/callback"

    # Step 1: Authorization URL
    auth_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'w_member_social'
    }

    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(auth_params)}"

    print()
    print("=" * 50)
    print("Step 1: Authorize the application")
    print("=" * 50)
    print()
    print("Opening browser to LinkedIn authorization page...")
    print()
    print("If browser doesn't open, visit this URL manually:")
    print(auth_url)
    print()

    # Try to open browser
    try:
        webbrowser.open(auth_url)
    except:
        pass

    print("After authorizing, you'll be redirected to:")
    print("http://localhost:8080/callback?code=...")
    print()
    print("The page will show an error (that's normal).")
    print("Just copy the FULL redirect URL from your browser.")
    print()

    redirect_url = input("Paste the full redirect URL here: ").strip()

    if not redirect_url:
        print("❌ Redirect URL is required")
        return

    # Extract code from URL
    try:
        parsed = urlparse(redirect_url)
        code = parse_qs(parsed.query).get('code', [None])[0]

        if not code:
            print("❌ Could not extract authorization code from URL")
            return
    except Exception as e:
        print(f"❌ Error parsing URL: {e}")
        return

    # Step 2: Exchange code for token
    print()
    print("=" * 50)
    print("Step 2: Exchanging code for access token")
    print("=" * 50)
    print()

    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri
    }

    try:
        response = requests.post(
            'https://www.linkedin.com/oauth/v2/accessToken',
            data=token_data
        )

        if response.status_code != 200:
            print(f"❌ Failed to get access token: {response.status_code}")
            print(response.text)
            return

        token_info = response.json()
        access_token = token_info['access_token']
        expires_in = token_info['expires_in']

        print("✅ Access token obtained!")
        print(f"   Expires in: {expires_in // 86400} days")
        print()

    except Exception as e:
        print(f"❌ Error getting access token: {e}")
        return

    # Step 3: Get person URN
    print("=" * 50)
    print("Step 3: Getting your LinkedIn Person URN")
    print("=" * 50)
    print()

    try:
        response = requests.get(
            'https://api.linkedin.com/v2/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        if response.status_code != 200:
            print(f"❌ Failed to get profile: {response.status_code}")
            print(response.text)
            return

        profile = response.json()
        person_id = profile['id']
        person_urn = f"urn:li:person:{person_id}"

        print("✅ Profile retrieved!")
        print(f"   Name: {profile.get('localizedFirstName')} {profile.get('localizedLastName')}")
        print()

    except Exception as e:
        print(f"❌ Error getting profile: {e}")
        return

    # Step 4: Test posting
    print("=" * 50)
    print("Step 4: Testing posting capability")
    print("=" * 50)
    print()

    test_post = input("Post a test message to LinkedIn? (y/n) [y]: ").strip().lower()

    if test_post != 'n':
        try:
            post_data = {
                "author": person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": "🤖 Test post from RAG Showroom automation setup. If you see this, the integration works!"
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            response = requests.post(
                'https://api.linkedin.com/v2/ugcPosts',
                json=post_data,
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json',
                    'X-Restli-Protocol-Version': '2.0.0'
                }
            )

            if response.status_code == 201:
                print("✅ Test post successful!")
                print("   Check your LinkedIn profile to see it")
            else:
                print(f"⚠️  Test post failed: {response.status_code}")
                print(response.text)

        except Exception as e:
            print(f"⚠️  Test post error: {e}")

    print()
    print("=" * 50)
    print("✅ Setup Complete!")
    print("=" * 50)
    print()
    print("Your credentials:")
    print("-" * 50)
    print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
    print(f"LINKEDIN_URN={person_urn}")
    print("-" * 50)
    print()
    print("Add these to GitHub secrets:")
    print()
    print(f"  gh secret set LINKEDIN_ACCESS_TOKEN")
    print(f"  # Paste: {access_token}")
    print()
    print(f"  gh secret set LINKEDIN_URN")
    print(f"  # Paste: {person_urn}")
    print()
    print("⚠️  IMPORTANT: Token expires in ~60 days")
    print("   Set a reminder to refresh before expiration")
    print()

if __name__ == "__main__":
    try:
        get_credentials()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
