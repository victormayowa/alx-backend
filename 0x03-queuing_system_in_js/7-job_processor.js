import kue from 'kue';

const list = ['4153518780', '4153518781'];

const que = kue.createQueue();

function sendNotification (phoneNumber, message, job, done) {
  job.progress(0, 100);
  if (list.indexOf(phoneNumber) !== -1) {
    return done(new Error(`Phone number ${job.data.phoneNumber} is blacklisted`));
  };

  job.progress(50, 100);
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
  done();
}

que.process('push_notification_code_2', 2, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
