# Implementation of the project

An .env file with environment variables is required for the project to work. Create it with this content and substitute your values.

# Database PostgreSQL
POSTGRES_DB=

POSTGRES_USER=

POSTGRES_PASSWORD=

POSTGRES_PORT=

SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}

# JWT authentication
SECRET_KEY=

ALGORITHM=

# Email service
MAIL_USERNAME=

MAIL_PASSWORD=

MAIL_FROM=

MAIL_PORT=

MAIL_SERVER=

# Redis
REDIS_HOST=

REDIS=

# Cloud Storage
CLOUDINARY_NAME=

CLOUDINARY_API_KEY=

CLOUDINARY_API_SECRET=

# Starting databases

docker-compose up -d

# Launching the application

uvicorn main:app --reload