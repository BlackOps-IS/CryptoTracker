# 🚀 CryptoTracker Deployment Guide

## Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/BlackOps-IS/CryptoTracker.git
cd CryptoTracker
```

2. **Set up Python environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
ETHERSCAN_API_KEY=your_etherscan_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
```
Open your browser to: http://localhost:5000
```

---

## Production Deployment

### Option 1: Docker Deployment (Recommended)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data static templates

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  cryptotracker:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

Deploy:
```bash
docker-compose up -d
```

### Option 2: Cloud Platform Deployment

#### Heroku
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Set environment variables
heroku config:set ETHERSCAN_API_KEY=your_key
heroku config:set FLASK_SECRET_KEY=your_secret

# Deploy
git push heroku main
```

#### AWS EC2
```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clone repository
git clone https://github.com/BlackOps-IS/CryptoTracker.git
cd CryptoTracker

# Set up application
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your API keys

# Set up systemd service
sudo nano /etc/systemd/system/cryptotracker.service
```

Add to service file:
```ini
[Unit]
Description=CryptoTracker Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/CryptoTracker
Environment="PATH=/home/ubuntu/CryptoTracker/venv/bin"
ExecStart=/home/ubuntu/CryptoTracker/venv/bin/python app.py

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl start cryptotracker
sudo systemctl enable cryptotracker
```

#### DigitalOcean App Platform
```bash
# Create app.yaml
runtime: python
name: cryptotracker
services:
  - name: web
    github:
      repo: BlackOps-IS/CryptoTracker
      branch: main
    run_command: python app.py
    envs:
      - key: ETHERSCAN_API_KEY
        value: ${ETHERSCAN_API_KEY}
```

### Option 3: Traditional VPS

```bash
# Install Nginx
sudo apt install nginx

# Configure Nginx
sudo nano /etc/nginx/sites-available/cryptotracker
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/cryptotracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Environment Variables

### Required
- `ETHERSCAN_API_KEY` - Your Etherscan API key (get from https://etherscan.io/apis)
- `FLASK_SECRET_KEY` - Secret key for Flask sessions

### Optional
- `BSCSCAN_API_KEY` - For BSC support
- `POLYGONSCAN_API_KEY` - For Polygon support
- `ETHEREUM_RPC_URL` - Custom RPC endpoint
- `FLASK_ENV` - Set to 'production' for production
- `FLASK_DEBUG` - Set to 'False' for production
- `PORT` - Port to run on (default: 5000)

---

## Security Considerations

### Production Checklist
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use strong `FLASK_SECRET_KEY`
- [ ] Enable HTTPS (use Let's Encrypt)
- [ ] Set up firewall rules
- [ ] Configure rate limiting
- [ ] Enable CORS properly
- [ ] Set up monitoring and logging
- [ ] Regular security updates
- [ ] Backup database regularly

### SSL/TLS Setup (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Monitoring & Maintenance

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Logs
```bash
# View application logs
tail -f /var/log/cryptotracker/app.log

# View Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Backup
```bash
# Backup database
cp data/cryptotracker.db backups/cryptotracker_$(date +%Y%m%d).db

# Backup configuration
tar -czf config_backup.tar.gz .env config.py
```

---

## Scaling

### Horizontal Scaling
Use a load balancer with multiple instances:
```yaml
# docker-compose.yml for scaling
version: '3.8'

services:
  cryptotracker:
    build: .
    deploy:
      replicas: 3
    environment:
      - FLASK_ENV=production

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - cryptotracker
```

### Database Optimization
For high traffic, consider:
- PostgreSQL instead of SQLite
- Redis for caching
- Database connection pooling

---

## Troubleshooting

### Common Issues

**Port already in use**
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

**Permission denied**
```bash
# Fix permissions
chmod +x app.py
chown -R $USER:$USER .
```

**Module not found**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**API rate limiting**
- Get a paid Etherscan API key
- Implement caching
- Add request delays

---

## Performance Optimization

### Caching
Implement Redis caching:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

### Database Indexing
```sql
CREATE INDEX idx_address ON transactions(address);
CREATE INDEX idx_timestamp ON transactions(timestamp);
```

### CDN
Use a CDN for static assets:
- Cloudflare
- AWS CloudFront
- Fastly

---

## Support

For deployment issues:
- Check the [GitHub Issues](https://github.com/BlackOps-IS/CryptoTracker/issues)
- Read the [Documentation](README.md)
- Contact: support@blackops-is.com

---

**Happy Deploying! 🚀**