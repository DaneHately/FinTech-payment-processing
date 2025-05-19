import boto3
from flask import Flask, request
import logging
import json

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(
    filename='/var/log/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Initialize S3 client
try:
    s3 = boto3.client('s3')
except Exception as e:
    logging.error(f"Failed to initialize boto3 S3 client: {e}")
    raise

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        logging.info(f"Received JSON: {data}")

        # Ensure 'id' exists in the data
        if not data or 'id' not in data:
            raise ValueError("Missing 'id' in request data")

        # Put object to S3
        response = s3.put_object(
            Bucket='fintech-payment-pipeline',
            Key=f"transactions/{data['id']}.json",
            Body=json.dumps(data)
        )

        logging.info(f"S3 response: {response}")
        return {"status": "Processed"}

    except Exception as e:
        logging.error("Error processing request", exc_info=True)
        return {"error": str(e)}, 500

@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
