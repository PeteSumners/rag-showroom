# LinkedIn API Setup Guide

This guide will help you get LinkedIn API credentials to enable automated posting.

## Overview

You need two pieces of information:
1. **LinkedIn Access Token** - OAuth 2.0 token with `w_member_social` scope
2. **LinkedIn Person URN** - Your unique LinkedIn identifier

## Step-by-Step Setup

### Step 1: Create a LinkedIn App

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Click **"Create app"**
3. Fill in the required information:
   - **App name**: RAG Showroom (or your preferred name)
   - **LinkedIn Page**: Select your LinkedIn Page (or create one)
   - **Privacy policy URL**: Can use your GitHub repo URL
   - **App logo**: Optional
4. Check the agreement box and click **"Create app"**

### Step 2: Request API Access

1. In your app dashboard, go to the **"Products"** tab
2. Find **"Share on LinkedIn"** product
3. Click **"Request access"**
4. Fill out the application:
   - Explain you're building an automated content sharing system
   - Mention it's for sharing technical RAG pattern demonstrations
   - Be specific and honest about your use case
5. Submit and **wait for approval** (typically 1-3 days)

⚠️ **Important**: You cannot proceed until LinkedIn approves your access.

### Step 3: Configure OAuth 2.0

Once approved:

1. Go to the **"Auth"** tab in your app
2. Note down:
   - **Client ID**
   - **Client Secret**
3. Add a redirect URL:
   - For testing: `http://localhost:8080/callback`
   - Click **"Update"**

### Step 4: Generate Access Token

#### Option A: Manual Token Generation (Quick Testing)

For testing, you can generate a token manually:

1. Construct authorization URL:
```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8080/callback&scope=w_member_social
```

2. Open this URL in your browser
3. Grant permissions
4. You'll be redirected to `http://localhost:8080/callback?code=YOUR_CODE`
5. Copy the `code` parameter

6. Exchange code for access token using curl:
```bash
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=YOUR_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=http://localhost:8080/callback"
```

7. Response will contain your access token:
```json
{
  "access_token": "YOUR_ACCESS_TOKEN",
  "expires_in": 5184000
}
```

⚠️ **Note**: Manual tokens expire after 60 days. For production, implement OAuth refresh tokens.

#### Option B: Using Python Script (Recommended)

I can create a helper script:

```python
# linkedin_auth.py
import http.server
import socketserver
import urllib.parse
import requests

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "http://localhost:8080/callback"

# Step 1: Visit this URL
print(f"Visit this URL to authorize:")
print(f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=w_member_social")

# Step 2: Paste the code from redirect
code = input("\nEnter the code from redirect URL: ")

# Step 3: Exchange for token
response = requests.post(
    "https://www.linkedin.com/oauth/v2/accessToken",
    data={
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI
    }
)

token_data = response.json()
print(f"\nAccess Token: {token_data['access_token']}")
print(f"Expires in: {token_data['expires_in']} seconds")
```

### Step 5: Get Your Person URN

With your access token, get your LinkedIn URN:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://api.linkedin.com/v2/me
```

Response:
```json
{
  "id": "ABC123xyz",
  "localizedFirstName": "Your Name",
  ...
}
```

Your URN is: `urn:li:person:ABC123xyz` (use the `id` field)

### Step 6: Test Your Credentials

Test posting to LinkedIn:

```bash
curl -X POST https://api.linkedin.com/v2/ugcPosts \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -d '{
    "author": "urn:li:person:YOUR_ID",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
      "com.linkedin.ugc.ShareContent": {
        "shareCommentary": {
          "text": "Test post from RAG Showroom automation"
        },
        "shareMediaCategory": "NONE"
      }
    },
    "visibility": {
      "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
  }'
```

If successful, you'll get a 201 response and see the post on your LinkedIn profile.

### Step 7: Add to GitHub Secrets

Once you have both credentials:

```bash
# Using GitHub CLI
gh secret set LINKEDIN_ACCESS_TOKEN
# Paste your token when prompted

gh secret set LINKEDIN_URN
# Enter: urn:li:person:YOUR_ID
```

Or use the setup script:
```bash
./setup-secrets.sh
```

## Troubleshooting

### "Application cannot access this API"
- Your app hasn't been approved for "Share on LinkedIn" product
- Wait for LinkedIn to approve your access request

### "Invalid access token"
- Token may have expired (60-day expiration)
- Generate a new token using the OAuth flow

### 403 Forbidden when posting
- Check your token has `w_member_social` scope
- Verify the URN format is correct: `urn:li:person:YOUR_ID`

### Posts not appearing
- Check LinkedIn's rate limits (throttling)
- Verify the post was created (check HTTP response)
- Look for the post in your LinkedIn profile's Activity

## Production Considerations

### Token Refresh (Important!)

Manual tokens expire after 60 days. For production:

1. **Store refresh token** (included in OAuth response)
2. **Implement token refresh** before expiration:

```python
def refresh_access_token(refresh_token):
    response = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )
    return response.json()
```

3. **Update GitHub secret** when token refreshes

### Rate Limits

LinkedIn API has rate limits:
- **Personal posts**: 100 per day
- **Throttling**: Space posts by 10+ minutes

For daily automation (1 post/day), you're well within limits.

### Monitoring

1. Check GitHub Actions logs for posting errors
2. Verify posts appear on LinkedIn
3. Monitor token expiration (set calendar reminder for 50 days)

## Alternative: Selenium Fallback

If you can't get API access, you can modify `scripts/post_linkedin.py` to use Selenium:

```python
# Selenium-based posting (not recommended but works)
from selenium import webdriver

def post_with_selenium(username, password, content):
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")
    # Log in and post using browser automation
    # (Implementation details in script)
```

⚠️ **Warning**: Selenium is against LinkedIn's ToS for automation. Use at your own risk.

## Summary Checklist

- [ ] Created LinkedIn App
- [ ] Requested "Share on LinkedIn" API access
- [ ] Got approval from LinkedIn
- [ ] Generated OAuth access token with `w_member_social` scope
- [ ] Retrieved LinkedIn person URN
- [ ] Tested posting with curl/Python
- [ ] Added `LINKEDIN_ACCESS_TOKEN` to GitHub secrets
- [ ] Added `LINKEDIN_URN` to GitHub secrets
- [ ] Set calendar reminder for token refresh (50 days)

## Need Help?

- [LinkedIn API Documentation](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin)
- [OAuth 2.0 Guide](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication)
- Check GitHub Issues for common problems
