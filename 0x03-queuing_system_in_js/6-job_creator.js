import kue from 'kue';

const que = kue.createQueue();
const data = {
    phoneNumber: '014567822',
    message: 'A new message',
};

const create_job = que.create('push_notification_code', data).save(error => {
  if (!error) {
    console.log(`Notification job created: ${create_job.id}`);
  }
});

create_job.on('complete', () => console.log('Notification job completed'));
create_job.on('failed', () => console.log('Notification job failed'));
