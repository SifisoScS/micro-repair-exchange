# 🛠️ Micro-Repair Exchange

*A community platform for repairing instead of replacing.*

## 🌟 Vision

Restoring dignity through repair. Instead of throwing things away, communities log small repair needs and connect with neighbors who have the skills to fix them. It's about building trust, reducing waste, and celebrating everyday acts of care.

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Firebase account
- Streamlit account (for deployment)

### 2. Local Development

```bash
# Clone and setup
git clone <repository-url>
cd micro-repair-exchange

# Install dependencies
pip install -r requirements.txt

# Set up Firebase
1. Go to Firebase Console (console.firebase.google.com)
2. Create a new project
3. Enable Firestore Database
4. Go to Project Settings > Service Accounts
5. Generate new private key
6. Copy the credentials to .streamlit/secrets.toml

# Run locally
streamlit run app.py
