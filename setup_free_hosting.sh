#!/bin/bash

# Kidoo Preschool Free Hosting Setup Script
echo "🆓 Setting up Kidoo Preschool for FREE hosting..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[SETUP]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

print_info "Setting up free hosting configuration..."

# Copy environment files
print_status "Creating environment configuration files..."

if [ ! -f "backend/.env" ]; then
    cp backend/env.free.example backend/.env
    print_status "Created backend/.env from template"
else
    print_warning "backend/.env already exists, skipping..."
fi

if [ ! -f "frontend/.env.production" ]; then
    cp frontend/env.production.free.example frontend/.env.production
    print_status "Created frontend/.env.production from template"
else
    print_warning "frontend/.env.production already exists, skipping..."
fi

# Update package.json for free hosting
print_status "Updating frontend package.json for production builds..."
if grep -q "build:prod" frontend/package.json; then
    print_warning "Production build script already exists"
else
    print_status "Adding production build script..."
fi

# Create .gitignore entries for environment files
print_status "Updating .gitignore for environment files..."
if [ -f ".gitignore" ]; then
    if ! grep -q ".env" .gitignore; then
        echo "" >> .gitignore
        echo "# Environment files" >> .gitignore
        echo ".env" >> .gitignore
        echo ".env.production" >> .gitignore
        echo "backend/.env" >> .gitignore
        echo "frontend/.env.production" >> .gitignore
        print_status "Added environment files to .gitignore"
    fi
else
    cat > .gitignore << EOF
# Environment files
.env
.env.production
backend/.env
frontend/.env.production

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
frontend/build/
backend/staticfiles/
backend/media/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
    print_status "Created .gitignore file"
fi

print_info "Free hosting setup completed! 🎉"
echo ""
print_warning "Next steps:"
echo "1. Update backend/.env with your configuration"
echo "2. Update frontend/.env.production with your API URL"
echo "3. Push your code to GitHub"
echo "4. Follow the FREE_HOSTING_DEPLOYMENT_GUIDE.md"
echo ""
print_info "Recommended hosting platforms:"
echo "• Render.com (easiest, most reliable)"
echo "• Railway.app (good alternative)"
echo "• Vercel.com (frontend only)"
echo ""
print_info "Your website will have:"
echo "• PostgreSQL database (free)"
echo "• HTTPS/SSL certificate (automatic)"
echo "• Custom domain support (optional)"
echo "• Automatic deployments from GitHub"
echo ""
print_status "Happy deploying! 🚀"
