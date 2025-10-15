# 🚀 Kidoo Preschool - Production Deployment Guide

This guide will help you deploy your Kidoo Preschool website to production with all necessary security, performance, and monitoring configurations.

## 📋 Prerequisites

### Server Requirements
- **OS**: Ubuntu 20.04+ or CentOS 8+ (recommended)
- **RAM**: Minimum 2GB, Recommended 4GB+
- **Storage**: Minimum 20GB SSD
- **CPU**: 2+ cores
- **Network**: Static IP address

### Software Requirements
- Docker & Docker Compose
- Git
- SSL Certificate (Let's Encrypt recommended)

## 🔧 Step-by-Step Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo apt install git -y
```

### 2. Clone and Configure

```bash
# Clone your repository
git clone <your-repo-url> kidoo-production
cd kidoo-production

# Copy environment files
cp backend/env.production.example backend/.env.production
cp frontend/env.production.example frontend/.env.production
```

### 3. Configure Environment Variables

Edit `backend/.env.production`:

```bash
# Django Settings
SECRET_KEY=your-super-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com

# Database Configuration
DB_NAME=kidoo_production
DB_USER=kidoo_user
DB_PASSWORD=your-secure-database-password
DB_HOST=db
DB_PORT=5432

# CORS Settings
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@kidoopreschool.com

# Redis Configuration
REDIS_URL=redis://redis:6379/1
```

Edit `frontend/.env.production`:

```bash
# API Configuration
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENVIRONMENT=production

# Analytics (optional)
REACT_APP_GOOGLE_ANALYTICS_ID=your-ga-id

# Other configurations
GENERATE_SOURCEMAP=false
```

### 4. SSL Certificate Setup

```bash
# Install Certbot
sudo apt install certbot -y

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy certificates to project
sudo mkdir -p ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem
sudo chown -R $USER:$USER ssl/
```

### 5. Deploy with Docker

```bash
# Make deployment script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### 6. Post-Deployment Configuration

#### Change Admin Password
```bash
docker-compose -f docker-compose.production.yml exec web python manage.py changepassword admin
```

#### Populate Sample Data (Optional)
```bash
docker-compose -f docker-compose.production.yml exec web python manage.py populate_sample_data --settings=kidoo_preschool.settings_production
```

## 🔒 Security Checklist

### ✅ Completed in Production Setup
- [x] Debug mode disabled
- [x] Secret key configured
- [x] Allowed hosts restricted
- [x] HTTPS enforced
- [x] Security headers configured
- [x] Rate limiting implemented
- [x] CORS properly configured
- [x] Static files served securely

### 🔧 Additional Security Measures

#### Firewall Configuration
```bash
# Configure UFW firewall
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

#### Database Security
```bash
# Create database user with limited privileges
sudo -u postgres psql
CREATE USER kidoo_user WITH PASSWORD 'secure_password';
CREATE DATABASE kidoo_production OWNER kidoo_user;
GRANT ALL PRIVILEGES ON DATABASE kidoo_production TO kidoo_user;
\q
```

## 📊 Monitoring and Maintenance

### 1. Log Monitoring
```bash
# View application logs
docker-compose -f docker-compose.production.yml logs -f web

# View nginx logs
docker-compose -f docker-compose.production.yml logs -f nginx
```

### 2. Database Backups
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose -f docker-compose.production.yml exec -T db pg_dump -U kidoo_user kidoo_production > backup_$DATE.sql
gzip backup_$DATE.sql
EOF

chmod +x backup.sh

# Schedule daily backups
echo "0 2 * * * /path/to/your/project/backup.sh" | crontab -
```

### 3. SSL Certificate Renewal
```bash
# Create renewal script
cat > renew_ssl.sh << 'EOF'
#!/bin/bash
sudo certbot renew --quiet
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem
sudo chown -R $USER:$USER ssl/
docker-compose -f docker-compose.production.yml restart nginx
EOF

chmod +x renew_ssl.sh

# Schedule monthly renewal check
echo "0 3 1 * * /path/to/your/project/renew_ssl.sh" | crontab -
```

## 🚀 Performance Optimization

### 1. Enable Gzip Compression
Already configured in nginx.conf

### 2. Static File Caching
Already configured with proper cache headers

### 3. Database Optimization
```bash
# Connect to database and run optimization
docker-compose -f docker-compose.production.yml exec db psql -U kidoo_user -d kidoo_production
```

### 4. CDN Setup (Optional)
Consider using CloudFlare or AWS CloudFront for static assets.

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml build
docker-compose -f docker-compose.production.yml up -d

# Run migrations if needed
docker-compose -f docker-compose.production.yml exec web python manage.py migrate --settings=kidoo_preschool.settings_production
```

### Health Checks
```bash
# Check application health
curl -f http://localhost/health/ || echo "Application is down!"

# Check database connection
docker-compose -f docker-compose.production.yml exec web python manage.py check --database default --settings=kidoo_preschool.settings_production
```

## 📱 Domain and DNS Configuration

### DNS Records
```
A     yourdomain.com        -> YOUR_SERVER_IP
A     www.yourdomain.com    -> YOUR_SERVER_IP
A     api.yourdomain.com    -> YOUR_SERVER_IP
CNAME www                  -> yourdomain.com
```

### Nginx Configuration Update
Update `nginx.conf` with your actual domain name:
```nginx
server_name yourdomain.com www.yourdomain.com;
```

## 🆘 Troubleshooting

### Common Issues

#### 1. Database Connection Error
```bash
# Check database container
docker-compose -f docker-compose.production.yml ps db

# Check database logs
docker-compose -f docker-compose.production.yml logs db
```

#### 2. Static Files Not Loading
```bash
# Recollect static files
docker-compose -f docker-compose.production.yml exec web python manage.py collectstatic --noinput --settings=kidoo_preschool.settings_production
```

#### 3. SSL Certificate Issues
```bash
# Test SSL configuration
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

## 📞 Support

For deployment issues:
1. Check the logs: `docker-compose -f docker-compose.production.yml logs`
2. Verify environment variables
3. Check firewall and DNS settings
4. Ensure SSL certificates are valid

## 🎯 Production Checklist

- [ ] Server provisioned and configured
- [ ] Domain name registered and DNS configured
- [ ] SSL certificate installed
- [ ] Environment variables configured
- [ ] Database created and configured
- [ ] Application deployed successfully
- [ ] Admin password changed
- [ ] Firewall configured
- [ ] Backup strategy implemented
- [ ] Monitoring set up
- [ ] Performance optimization completed
- [ ] Security audit completed

Your Kidoo Preschool website is now ready for production! 🎉
