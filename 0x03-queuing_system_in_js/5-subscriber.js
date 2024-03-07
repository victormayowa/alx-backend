import { createClient } from "redis";

const redis_client = createClient();
redis_client.on('error', error => {
  console.log(`Redis client not connected to the server: ${error}`);
});

redis_client.on('connect', () => {
  console.log('Redis client connected to the server');
});

await redis_client.connect();

await redis_client.subscribe('holberton school channel', async (message) => {
  console.log(message);
  if (message === 'KILL_SERVER') {
    await redis_client.unsubscribe('holberton school channel');
    await redis_client.quit();
  }
});
