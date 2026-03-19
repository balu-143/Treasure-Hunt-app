# Use official Python image
FROM python:3.10-slim
ENV PORT=5000
# Set the working directory inside the container
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .
EXPOSE 5000

# Default command to run the game
# Replace src/game.py with your actual entry point
CMD ["python", "src/Treasure-webapp.py"]
