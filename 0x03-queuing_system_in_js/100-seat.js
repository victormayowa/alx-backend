import redis from 'redis';
import kue from 'kue';
import express from 'express';

const app = express();
const client = redis.createClient();
let reservationEnabled = true;
const PORT = 1245;

await client.connect();

function reserveSeat(number = 50) {
  client.set('available_seats', number);
}

async function getCurrentAvailableSeats() {
  return parseInt(await client.get('available_seats'));
}

app.get('/available_seats', async (req, res) => {
  res.send({ numberOfAvailableSeats: await getCurrentAvailableSeats() });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.send({ status: 'Reservation are blocked' });
    return;
  }

  const queue = kue.createQueue();
  const job = queue.create('reserve_seat', {});
  job.save((err) => {
    if (err) res.send({ status: 'Reservation failed' });
    else res.send({status: 'Reservation in process'});
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  }).on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });
});

app.get('/process', async (req, res) => {
  const queue = kue.createQueue();

  res.send({status: 'Queue processing'});

  const seats = await getCurrentAvailableSeats();
  const newSeats = seats - 1;

  queue.process('reserve_seat', (job, done) => {
    if (newSeats === 0) {
      reservationEnabled = false;
    } else if (newSeats < 0) {
      done(new Error('Not enough seats available'));
    }

    reserveSeat(newSeats);
    done();
  });
});

app.listen(PORT, (err) => {
  if (err) {
    console.log(`Error starting server on port ${PORT}`);
  } else {
    reserveSeat(50);
    console.log(`Listening on port ${PORT}`);
  }
});
