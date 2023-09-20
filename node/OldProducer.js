const http = require('http');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const apiUrl = 'http://localhost:8000'; // Replace with your server's API URL

const sendRequest = (jsonData) => {
  const data = JSON.stringify(jsonData);

  const options = {
    hostname: 'localhost', // Replace with your server's hostname
    port: 8000,            // Replace with your server's port
    path: '/your-endpoint', // Replace with your endpoint path
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': data.length,
    },
  };

  const req = http.request(options, (res) => {
    let responseData = '';

    res.on('data', (chunk) => {
      responseData += chunk;
    });

    res.on('end', () => {
      console.log('Request sent successfully');
      console.log('Response data:', responseData);
      rl.close();
    });
  });

  req.on('error', (error) => {
    console.error('Error sending request:', error.message);
    rl.close();
  });

  req.write(data);
  req.end();
};

rl.question('Enter a JSON request: ', (input) => {
  try {
    const jsonData = JSON.parse(input);
    sendRequest(jsonData);
  } catch (error) {
    console.error('Invalid JSON input:', error.message);
    rl.close();
  }
});
