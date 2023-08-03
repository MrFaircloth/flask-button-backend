# Use a base Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container's working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container's working directory
COPY . .

# Expose the port on which the Python app will listen (replace 8000 with your app's port)
EXPOSE 5005

# Command to run the Python application (replace 'app.py' with your app's main Python file)
CMD ["python", "button/app.py"]

# Build:
# docker build -t button:0.0.1 .

# Example Usage: 
# docker run -d \
#   --name button_api \ 
#   --restart=always
#   -p 5005:5005 \
#   -v $(pwd)/db_data:/app/db_data \
#   -e DATABASE_URL='sqlite:////app/db_data/button_data.db' \
#   -e GROUPME_BOT_ID='1234' \
#   button:0.0.1 
