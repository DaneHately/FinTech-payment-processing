const express = require('express');
const fs = require('fs');
const axios = require('axios');
const app = express();

app.use(express.json());

// GET /pay endpoint
app.get('/pay', (req, res) => {
    fs.appendFileSync('/var/log/app.log', 'Payment Form accessed\n');
    res.send('Payment Form');
});

// POST /pay endpoint
app.post('/pay', async (req, res) => {
    try {
        const response = await axios.post('http://internal-FinTech-Internal-ALB-986761868.us-west-2.elb.amazonaws.com:3000/process', {
            id: 'tx_' + Date.now(),
            amount: 100.00,
            status: 'processed'
        });
        fs.appendFileSync('/var/log/app.log', 'Payment sent to App Tier\n');
        res.json(response.data);
    } catch (error) {
        fs.appendFileSync('/var/log/app.log', 'Error: ' + error.message + '\n');
        res.status(500).send('Error processing payment');
    }
});

// Start the server
app.listen(3000, () => console.log('Running'));
