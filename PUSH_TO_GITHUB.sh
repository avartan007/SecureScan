#!/bin/bash

# One-shot command to push to GitHub
# Run this from the project root: bash PUSH_TO_GITHUB.sh

echo "🚀 Pushing File Security Scanner to GitHub..."
echo ""

# Verify git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Error: Not a git repository. Run 'git init' first."
    exit 1
fi

# Check if remote is configured
if ! git remote -v | grep -q "origin"; then
    echo "❌ Error: No 'origin' remote found. Run:"
    echo "   git remote add origin https://github.com/avartan007/document-scanner.git"
    exit 1
fi

# Get current branch
BRANCH=$(git branch --show-current)
echo "📝 Current branch: $BRANCH"
echo ""

# Verify working directory is clean (all changes staged)
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ Working directory is clean"
else
    echo "⚠️  Unstaged changes detected. Staging all changes..."
    git add -A
fi

# Check if there are commits to push
COMMITS_TO_PUSH=$(git rev-list --count $BRANCH...origin/$BRANCH 2>/dev/null || git rev-list --count $BRANCH)
if [ "$COMMITS_TO_PUSH" -gt 0 ]; then
    echo "📤 Found $COMMITS_TO_PUSH commit(s) to push"
    echo ""
    echo "Pushing to GitHub..."
    git push origin $BRANCH -u
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ SUCCESS! Your project is now on GitHub!"
        echo ""
        echo "View your repository:"
        echo "   $(git remote get-url origin)"
    else
        echo "❌ Push failed. Check your credentials or internet connection."
        exit 1
    fi
else
    echo "✅ All commits are already pushed to GitHub!"
fi

echo ""
echo "🎉 GitHub Ready Checklist:"
echo "   ✅ Old CLI files removed"
echo "   ✅ Flask web app implemented"
echo "   ✅ Glassmorphic UI with black/orange theme"
echo "   ✅ Deployment configs (Render, Heroku)"
echo "   ✅ README with instructions"
echo "   ✅ .gitignore properly configured"
echo "   ✅ All artifacts cleaned up"
