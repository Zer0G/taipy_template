# Taipy Web Application Template

A template for creating web applications using Taipy and Plotly. This template provides a basic structure for building interactive data visualization web applications.

## Features

- Interactive web interface built with Taipy
- Dynamic data visualization using Plotly
- Sample time series data generation
- Responsive layout
- Production-ready deployment configuration

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git

## Local Development Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd taipy_webapp
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
taipy_webapp/
├── main.py           # Main application file
├── wsgi.py          # WSGI entry point for production
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## Production Deployment on Ubuntu VPS

### Option 1: Direct Deployment

### 1. Server Preparation

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install python3.11 python3.11-venv python3-pip nginx -y
```

### 2. Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/taipy_app
sudo chown $USER:$USER /var/www/taipy_app

# Clone repository (or copy files)
cd /var/www/taipy_app
git clone <your-repository-url> .

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Systemd Service Setup

Create a systemd service file:
```bash
sudo nano /etc/systemd/system/taipy.service
```

Add the following content:
```ini
[Unit]
Description=Taipy Web Application
After=network.target

[Service]
User=your_username
WorkingDirectory=/var/www/taipy_app
Environment="PATH=/var/www/taipy_app/venv/bin"
ExecStart=/var/www/taipy_app/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:gui
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4. Nginx Configuration

Create Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/taipy
```

Add the following content:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/taipy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL Setup (Recommended)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

### 6. Start the Application

```bash
sudo systemctl start taipy
sudo systemctl enable taipy
```

### 7. Monitoring

Check application status:
```bash
sudo systemctl status taipy
```

View logs:
```bash
sudo journalctl -u taipy
```

## Important Notes

1. Replace `your_username` with your actual VPS username
2. Replace `your_domain.com` with your actual domain name
3. Ensure your domain's DNS is pointing to your VPS IP address
4. Configure firewall rules to allow traffic on ports 80 and 443
5. If using a cloud provider, configure their security groups/firewall rules

## Security Considerations

1. Keep your system and packages updated
2. Use strong passwords
3. Configure firewall rules appropriately
4. Use SSL/TLS for secure connections
5. Regularly monitor logs for suspicious activity

## Troubleshooting

1. Check application logs:
```bash
sudo journalctl -u taipy
```

2. Check Nginx logs:
```bash
sudo tail -f /var/log/nginx/error.log
```

3. Verify service status:
```bash
sudo systemctl status taipy
sudo systemctl status nginx
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Your chosen license]

## Contact

[Your contact information]

### Option 2: Docker-based Deployment

#### 1. Server Preparation

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Docker and Docker Compose
sudo apt install docker.io docker-compose -y

# Add your user to the docker group
sudo usermod -aG docker $USER

# Log out and log back in for the group changes to take effect
```

#### 2. Create Docker Configuration Files

Create a `Dockerfile`:
```bash
nano Dockerfile
```

Add the following content:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
```

Create a `docker-compose.yml`:
```bash
nano docker-compose.yml
```

Add the following content:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    restart: always
    volumes:
      - .:/app
    environment:
      - PYTHONUNBUFFERED=1

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
```

Create an Nginx configuration file:
```bash
nano nginx.conf
```

Add the following content:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://web:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 3. Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/taipy_app
sudo chown $USER:$USER /var/www/taipy_app

# Clone repository (or copy files)
cd /var/www/taipy_app
git clone <your-repository-url> .

# Create SSL directory
mkdir ssl
```

#### 4. SSL Setup (Recommended)

```bash
# Install Certbot
sudo apt install certbot -y

# Obtain SSL certificate
sudo certbot certonly --standalone -d your_domain.com

# Copy SSL certificates to the application directory
sudo cp /etc/letsencrypt/live/your_domain.com/fullchain.pem /var/www/taipy_app/ssl/
sudo cp /etc/letsencrypt/live/your_domain.com/privkey.pem /var/www/taipy_app/ssl/
```

Update the `nginx.conf` to include SSL:
```nginx
server {
    listen 80;
    server_name your_domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your_domain.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;

    location / {
        proxy_pass http://web:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 5. Start the Application

```bash
# Build and start the containers
docker-compose up -d

# View logs
docker-compose logs -f
```

#### 6. Monitoring

Check container status:
```bash
docker-compose ps
```

View logs:
```bash
docker-compose logs -f
```

#### 7. Updating the Application

```bash
# Pull latest changes
git pull

# Rebuild and restart containers
docker-compose down
docker-compose up -d --build
```

#### 8. Backup and Restore

To backup your application:
```bash
# Backup data
tar -czf taipy_backup.tar.gz /var/www/taipy_app

# Restore data
tar -xzf taipy_backup.tar.gz -C /var/www/taipy_app
```

## Important Notes

1. Replace `your_username` with your actual VPS username
2. Replace `your_domain.com` with your actual domain name
3. Ensure your domain's DNS is pointing to your VPS IP address
4. Configure firewall rules to allow traffic on ports 80 and 443
5. If using a cloud provider, configure their security groups/firewall rules

## Security Considerations

1. Keep your system and packages updated
2. Use strong passwords
3. Configure firewall rules appropriately
4. Use SSL/TLS for secure connections
5. Regularly monitor logs for suspicious activity

## Troubleshooting

1. Check application logs:
```bash
sudo journalctl -u taipy
```

2. Check Nginx logs:
```bash
sudo tail -f /var/log/nginx/error.log
```

3. Verify service status:
```bash
sudo systemctl status taipy
sudo systemctl status nginx
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Your chosen license]

## Contact

[Your contact information] 
