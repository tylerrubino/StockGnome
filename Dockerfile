# Stage 1: Build frontend
FROM node:18 AS build-stage

WORKDIR /code

COPY ./frontend /code/frontend

WORKDIR /code/frontend

# Installing packages
RUN npm install

# Building the frontend
RUN npm run build

# Stage 2: Build backend
FROM python:3.10.6

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /code

# Copying requirements and installing dependencies
COPY ./backend /code/backend

# Install the required packages
RUN pip install -r ./backend/requirements.txt

# Copy the frontend build to the Django project
COPY --from=build-stage ./code/frontend/dist /code/backend/static
COPY --from=build-stage ./code/frontend/dist/index.html /code/backend/main/templates/index.html

# Expose the port
EXPOSE 80

# Add entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set working directory and start app
WORKDIR /code/backend
ENTRYPOINT ["/entrypoint.sh"]
