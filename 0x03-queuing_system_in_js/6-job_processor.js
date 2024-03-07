import kue from 'kue';

const que = kue.createQueue();

function sendNotification (phoneno, mes) {
  console.log(`Sending notification to ${phoneno}, with message: ${mes}`);
}

que.process('push_notification_code', (job) => {
  sendNotification(job.data.phoneno, job.data.mes);
});
