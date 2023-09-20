import pkg from 'pg';
const { Client } = pkg;

const client = new Client({
  user: 'postgres',
  host: 'postgres', // should use container name as the host
  database: 'postgres',
  password: '1234',
  port: 5432,
});

client.connect();

function makeTable() {
  const createTableQuery = `
    CREATE TABLE IF NOT EXISTS chatroom (
      msg_id SERIAL PRIMARY KEY,
      order_num INTEGER,
      sender_id INTEGER,
      body TEXT,
      send_time TEXT
    )
  `;

  client.query(createTableQuery, (err, result) => {
    if (err) {
      console.error('Error creating table:', err);
    } else {
      console.log('Table "chatroom" created or already exists.');
    }
  });
}

export function saveMessageToDB(message) {
  const sendTime = new Date();

  const insertQuery = `
    INSERT INTO chatroom (order_num, sender_id, body, send_time)
    VALUES ($1, $2, $3, $4)
    RETURNING msg_id
  `;

  const values = [message.order_num, message.sender_id, message.body, sendTime];

  client.query(insertQuery, values, (err, result) => {
    if (err) {
      console.error('Error inserting message:', err);
    } else {
      console.log(`A row has been inserted with msg_id ${result.rows[0].msg_id}`);
    }
  });
}

makeTable();
