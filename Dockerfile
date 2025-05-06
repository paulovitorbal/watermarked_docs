# Use the official Python image as the base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container work directory
COPY . /app

# Install any dependencies required by the project
# (assuming they are listed in requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the desired port (if the application uses one, otherwise omit)
#EXPOSE 8000

# Set the command to run your Python script
CMD ["python", "telegram_bot.py"]