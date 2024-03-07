import redis from "redis";

const redis_client = redis.createClient();
redis_client.on('error', err => {
  console.log(`Redis client not connected to the server: ${err}`);
});

await redis_client.connect();
if (redis_client.isReady) {
  console.log('Redis client connected to the server');
}

async function setNewSchool (schoolName, value) {
  const res = await redis_client.SET(schoolName, value);
  console.log(`Reply: ${res}`);
}

async function displaySchoolValue (schoolName) {
  console.log(await redis_client.get(schoolName));
}

await displaySchoolValue('Holberton');
await setNewSchool('HolbertonSanFrancisco', '100');
await displaySchoolValue('HolbertonSanFrancisco'); 
