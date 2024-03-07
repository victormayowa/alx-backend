import express from 'express';
import redis from 'redis';

const listProducts = [
  {id: 1, name: 'Suitcase 250', price: 50, stock: 4},
  {id: 2, name: 'Suitcase 450', price: 100, stock: 10},
  {id: 3, name: 'Suitcase 650', price: 350, stock: 2},
  {id: 4, name: 'Suitcase 1050', price: 550, stock: 5}
];

const PORT = 1245;
const app = express();
const redisClient = redis.createClient();

await redisClient.connect();

function getItemById (id) {
  return listProducts.find((item) => {
    return item.id === id;
  });
}

function reserveStockById (itemId, stock) {
  redisClient.set(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById (itemId) {
  return await redisClient.get(`item.${itemId}`);
}

app.listen(PORT, (err) => {
  if (err) console.log(`Error starting server on port ${PORT}`);
  else console.log(`Listening on port ${PORT}`);
});

app.get('/list_products', (req, res) => {
  const items = listProducts.map((item) => {
    return {
      itemId: item.id,
      itemName: item.name,
      price: item.price,
      initialAvailableQuantity: item.stock,
    };
  });

  res.send(items);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const reserved = await getCurrentReservedStockById(itemId);

  const item = getItemById(itemId);
  if (!item) {
    res.send({status: 'Product not found'});
    return;
  }

  res.send({
    itemId: item.id,
    itemName: item.name,
    price: item.price,
    initialAvailableQuantity: item.stock,
    currentQuantity: item.stock - Number(reserved)
  });
});

app.get('/reserve_product/:itemId', (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);

  if (!item) {
    res.send({status: 'Product not found'});
    return;
  }
  if (item.stock < 1) {
    res.send({status: 'Not enough stock available', itemId: itemId});
    return;
  }

  reserveStockById(itemId, 1);
  res.send({status: 'Reservation confirmed','itemId': itemId});
});
