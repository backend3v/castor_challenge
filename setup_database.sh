#!/bin/bash

# Castor Challenge Database Setup Script
# This script sets up the complete database environment

echo "🚀 Setting up Castor Challenge Database..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

print_status "Docker is running"

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose down

# Remove existing volumes (optional - uncomment if you want fresh start)
# print_warning "Removing existing database volumes..."
# docker volume rm castor_challenge_mysql_data 2>/dev/null || true

# Start MySQL container
print_status "Starting MySQL container..."
docker-compose up -d mysql

# Wait for MySQL to be ready
print_status "Waiting for MySQL to be ready..."
sleep 10

# Check if MySQL is ready
max_attempts=30
attempt=1
while [ $attempt -le $max_attempts ]; do
    if docker exec castor_mysql mysqladmin ping -h localhost -u root -prootpassword --silent; then
        print_status "MySQL is ready!"
        break
    fi
    echo -n "."
    sleep 2
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    print_error "MySQL failed to start properly"
    exit 1
fi

# Verify database and tables
print_status "Verifying database setup..."
docker exec castor_mysql mysql -u castor_user -pcastor_password -e "USE castor_db; SHOW TABLES;"
if [ $? -eq 0 ]; then
    print_status "Database setup completed successfully!"
else
    print_error "Database setup failed"
    exit 1
fi 