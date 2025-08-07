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
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /code

# Copying requirements and installing dependencies
COPY ./backend /code/backend

# Install the required packages
RUN pip install -r ./backend/requirements.txt

# Copy the frontend build to the Django project
COPY --from=build-stage ./code/frontend/build /code/backend/static
COPY --from=build-stage ./code/frontend/build/static /code/backend/static
COPY --from=build-stage ./code/frontend/build/index.html /code/backend/main/templates/index.html

# Run Django migrations
RUN python /code/backend/manage.py migrate

# Collect static files
RUN python /code/backend/manage.py collectstatic --noinput

# Expose the port
EXPOSE 80

WORKDIR /code/backend/

# Run the application
CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:8000"]