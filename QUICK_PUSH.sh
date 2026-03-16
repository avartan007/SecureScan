#!/bin/bash

# 🚀 GITHUB READY - ONE SHOT PUSH COMMAND
# Run this from the project directory to push to GitHub

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🛡️  File Security Scanner - GitHub Push"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Stage any uncommitted changes
echo "📝 Staging changes..."
git add -A

# Check if there are changes to commit
if ! git diff --cached --quiet; then
    echo "✅ Found changes to commit"
    git commit -m "chore: final cleanup and GitHub ready"
else
    echo "✅ Nothing new to stage"
fi

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
git push origin main -u

if [ $? -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ✅ SUCCESS! Project pushed to GitHub!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📍 Repository URL:"
    echo "   $(git remote get-url origin)"
    echo ""
    echo "🎯 What you get:"
    echo "   ✨ Modern Flask web app"
    echo "   🎨 Glassmorphic black/orange UI"
    echo "   🔒 VirusTotal API integration"
    echo "   🌐 3-page responsive design"
    echo "   📚 Complete documentation"
    echo "   🚀 Heroku & Render configs"
    echo ""
else
    echo ""
    echo "❌ Push failed!"
    echo "   Make sure you have:"
    echo "   1. GitHub account and repository created"
    echo "   2. Remote configured: git remote add origin <your-repo-url>"
    echo "   3. Valid credentials/SSH keys"
    exit 1
fi
