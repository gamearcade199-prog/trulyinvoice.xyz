echo "🔍 Checking Git Status..."
git status --porcelain
echo ""
echo "📝 Recent Commits:"
git log --oneline -3
echo ""
echo "🌐 Remote Configuration:"
git remote -v
echo ""
echo "🚀 Attempting Push:"
git push origin main