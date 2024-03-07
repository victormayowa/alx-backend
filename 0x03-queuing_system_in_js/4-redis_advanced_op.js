import redis from "redis";

const redis_client = redis.createClient();
redis_client.on('error', error => {
  console.log(`Redis client not connected to the server: ${error}`);
});

await redis_client.connect();
if (redis_client.isReady) {
  console.log('Redis client connected to the server');
}

console.log(`Reply: ${await redis_client.hSet('HolbertonSchools', 'Portland', 50)}`);
console.log(`Reply: ${await redis_client.hSet('HolbertonSchools', 'Seatle', 80)}`);
console.log(`Reply: ${await redis_client.hSet('HolbertonSchools', 'New York', 20)}`);
console.log(`Reply: ${await redis_client.hSet('HolbertonSchools', 'Bogota', 20)}`);
console.log(`Reply: ${await redis_client.hSet('HolbertonSchools', 'Cali', 40)}`);
console.log(`Reply: ${await redis_client.hSet('HolbertonSchools', 'Paris', 2)}`);

console.log(await redis_client.hGetAll('HolbertonSchools'))
