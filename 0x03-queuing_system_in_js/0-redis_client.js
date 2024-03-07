import { createClient } from "redis";

const redis_client = createClient();
redis_client.on('error', err => {
  console.log(`Redis client not connected to the server: ${err}`);
});

await redis_client.connect();
if (redis_client.isReady) {
  console.log('Redis client connected to the server');
}
