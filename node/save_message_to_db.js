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
      id SERIAL PRIMARY KEY,
      group_id INTEGER,
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
    INSERT INTO chatroom (group_id, order_num, sender_id, body, send_time)
    VALUES ($1, $2, $3, $4, $5)
    RETURNING group_id
  `;

  const values = [message.group_id, message.order_num, message.sender_id, message.body, sendTime];

  client.query(insertQuery, values, (err, result) => {
    if (err) {
      console.error('Error inserting message:', err);
    } else {
      console.log(`A message has been sent with to group ${result.rows[0].group_id}`);
    }
  });
}

makeTable();
