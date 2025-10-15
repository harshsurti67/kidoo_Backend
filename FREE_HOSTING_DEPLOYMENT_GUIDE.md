# 🆓 Free Hosting Deployment Guide for Kidoo Preschool

This guide will help you deploy your Kidoo Preschool website completely FREE using modern hosting platforms with PostgreSQL databases.

## 🎯 Best Free Hosting Options

### 1. **Render** (Recommended) ⭐
- **Frontend**: Static site hosting
- **Backend**: Web service with Python support
- **Database**: Free PostgreSQL database
- **Limitations**: Apps sleep after 15 minutes of inactivity
- **URL**: https://render.com

### 2. **Railway** (Alternative)
- **Full-stack**: Supports both frontend and backend
- **Database**: Free PostgreSQL database
- **Limitations**: $5 credit monthly (usually enough for small apps)
- **URL**: https://railway.app

### 3. **Vercel** (Frontend only)
- **Frontend**: Excellent for React apps
- **Backend**: Serverless functions (limited)
- **Database**: External database required
- **URL**: https://vercel.com

## 🚀 Option 1: Deploy with Render (Recommended)

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for free hosting deployment"
   git push origin main
   ```

### Step 2: Deploy Backend to Render

1. **Go to [Render.com](https://render.com)** and sign up with GitHub
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the backend service**:
   - **Name**: `kidoo-backend`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     cd backend && pip install -r requirements_free.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```bash
     cd backend && gunicorn kidoo_preschool.wsgi:application
     ```

5. **Add Environment Variables**:
   ```
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=kidoo-backend.onrender.com
   DJANGO_SETTINGS_MODULE=kidoo_preschool.settings_free
   ```

6. **Click "Create Web Service"**

### Step 3: Create PostgreSQL Database

1. **Click "New +" → "PostgreSQL"**
2. **Configure database**:
   - **Name**: `kidoo-db`
   - **Database**: `kidoo_production`
   - **User**: `kidoo_user`
3. **Copy the database URL** and add it to your backend environment variables:
   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

### Step 4: Run Database Migrations

1. **Go to your backend service**
2. **Click "Shell"**
3. **Run migrations**:
   ```bash
   cd backend
   python manage.py migrate --settings=kidoo_preschool.settings_free
   python manage.py createsuperuser --settings=kidoo_preschool.settings_free
   ```

### Step 5: Deploy Frontend to Render

1. **Click "New +" → "Static Site"**
2. **Connect your GitHub repository**
3. **Configure the frontend**:
   - **Name**: `kidoo-frontend`
   - **Build Command**: 
     ```bash
     cd frontend && npm install && npm run build
     ```
   - **Publish Directory**: `frontend/build`

4. **Add Environment Variables**:
   ```
   REACT_APP_API_URL=https://kidoo-backend.onrender.com/api
   REACT_APP_ENVIRONMENT=production
   ```

5. **Click "Create Static Site"**

### Step 6: Update CORS Settings

1. **Go to your backend service**
2. **Add environment variable**:
   ```
   CORS_ALLOWED_ORIGINS=https://kidoo-frontend.onrender.com
   ```
3. **Redeploy the backend**

## 🚂 Option 2: Deploy with Railway

### Step 1: Deploy to Railway

1. **Go to [Railway.app](https://railway.app)** and sign up with GitHub
2. **Click "New Project" → "Deploy from GitHub repo"**
3. **Select your repository**
4. **Railway will automatically detect your project structure**

### Step 2: Configure Environment Variables

Add these environment variables in Railway dashboard:
```
SECRET_KEY=your-super-secret-key-here
DEBUG=False
DJANGO_SETTINGS_MODULE=kidoo_preschool.settings_free
REACT_APP_API_URL=https://your-app.railway.app/api
```

### Step 3: Add PostgreSQL Database

1. **Click "New" → "Database" → "PostgreSQL"**
2. **Railway will automatically set DATABASE_URL**

### Step 4: Deploy

Railway will automatically build and deploy your application!

## 🎨 Option 3: Frontend on Vercel + Backend on Render

### Deploy Frontend to Vercel

1. **Go to [Vercel.com](https://vercel.com)** and sign up with GitHub
2. **Import your repository**
3. **Configure build settings**:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Add Environment Variables**:
   ```
   REACT_APP_API_URL=https://kidoo-backend.onrender.com/api
   ```

5. **Deploy!**

## 📊 Database Setup and Management

### Accessing Your PostgreSQL Database

#### Option 1: Using Render Dashboard
1. Go to your database service
2. Click "Connect" to get connection details
3. Use any PostgreSQL client (pgAdmin, DBeaver, etc.)

#### Option 2: Using Command Line
```bash
# Connect to your database
psql "postgresql://user:password@host:port/database"

# Run SQL commands
\dt  # List tables
\q   # Quit
```

### Populate Sample Data

1. **Access your backend shell** (Render: Shell tab, Railway: Deploy logs)
2. **Run the populate command**:
   ```bash
   cd backend
   python manage.py populate_sample_data --settings=kidoo_preschool.settings_free
   ```

## 🔧 Configuration Files Created

I've created these files for free hosting:

### Backend Files:
- `backend/requirements_free.txt` - Optimized dependencies for free hosting
- `backend/kidoo_preschool/settings_free.py` - Free hosting Django settings
- `backend/env.free.example` - Environment variables template

### Frontend Files:
- `frontend/env.production.free.example` - Frontend environment variables

### Deployment Files:
- `render.yaml` - Render deployment configuration
- `railway.json` - Railway deployment configuration

## 🌐 Custom Domain Setup (Optional)

### For Render:
1. **Go to your service settings**
2. **Click "Custom Domains"**
3. **Add your domain**
4. **Update DNS records** as instructed

### For Railway:
1. **Go to your project settings**
2. **Click "Domains"**
3. **Add custom domain**
4. **Configure DNS** as shown

## 📱 Mobile App Considerations

If you plan to create a mobile app later:
- Your API will be accessible at: `https://kidoo-backend.onrender.com/api`
- CORS is already configured for web access
- Add mobile app domains to CORS_ALLOWED_ORIGINS when needed

## 🔍 Monitoring and Maintenance

### Health Checks
- **Backend**: `https://kidoo-backend.onrender.com/health/`
- **Frontend**: Your main website URL

### Logs
- **Render**: Go to your service → "Logs" tab
- **Railway**: Go to your project → "Deployments" → Click deployment → "View Logs"

### Database Backups
Most free hosting platforms provide automatic backups, but you can also:
```bash
# Create manual backup
pg_dump "postgresql://user:password@host:port/database" > backup.sql
```

## 💡 Tips for Free Hosting

### Performance Optimization:
1. **Enable gzip compression** (already configured)
2. **Optimize images** before uploading
3. **Use CDN** for static assets (Render provides this automatically)

### Cost Management:
1. **Monitor usage** in your hosting dashboard
2. **Optimize database queries** to reduce resource usage
3. **Use caching** for frequently accessed data

### Scaling:
- **Render**: Upgrade to paid plan for better performance
- **Railway**: Add more resources as needed
- **Vercel**: Upgrade for more bandwidth and features

## 🆘 Troubleshooting

### Common Issues:

#### 1. "App is sleeping" (Render)
- **Solution**: First visit after inactivity takes 30-60 seconds
- **Prevention**: Use a monitoring service to ping your app

#### 2. Database Connection Errors
- **Check**: DATABASE_URL environment variable
- **Verify**: Database service is running
- **Test**: Connection string format

#### 3. CORS Errors
- **Check**: CORS_ALLOWED_ORIGINS includes your frontend URL
- **Verify**: Frontend is making requests to correct API URL

#### 4. Static Files Not Loading
- **Check**: STATIC_ROOT and STATIC_URL settings
- **Verify**: collectstatic command ran successfully

## 🎉 Success Checklist

- [ ] Backend deployed and accessible
- [ ] Database created and connected
- [ ] Migrations run successfully
- [ ] Frontend deployed and accessible
- [ ] API calls working from frontend
- [ ] Admin panel accessible
- [ ] Sample data populated
- [ ] Custom domain configured (optional)
- [ ] SSL certificate working
- [ ] Performance optimized

## 📞 Support

### Free Hosting Support:
- **Render**: [Community Forum](https://community.render.com)
- **Railway**: [Discord Community](https://discord.gg/railway)
- **Vercel**: [GitHub Discussions](https://github.com/vercel/vercel/discussions)

### Your Project:
- Check the logs first
- Verify environment variables
- Test API endpoints individually
- Use browser developer tools for frontend issues

---

**🎊 Congratulations!** Your Kidoo Preschool website is now live on free hosting with a PostgreSQL database! 

Your website will be accessible at:
- **Frontend**: `https://kidoo-frontend.onrender.com`
- **Backend API**: `https://kidoo-backend.onrender.com/api`
- **Admin Panel**: `https://kidoo-backend.onrender.com/admin`
