import kue from 'kue';

const queue = kue.createQueue();
const job_data = {
    phoneNumber: '014567822',
    message: 'A new message',
};

const create_job = queue.create('push_notification_code', job_data).save(error => {
  if (!error) {
    console.log(`Notification job created: ${create_job.id}`);
  }
});

create_job.on('complete', () => console.log('Notification job completed'));
create_job.on('failed', () => console.log('Notification job failed'));
