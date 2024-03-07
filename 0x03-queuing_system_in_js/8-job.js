import kue from 'kue';

export function createPushNotificationsJobs (jobs, que) {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  for (const job_data of jobs) {
    const job = que.create('push_notification_code_3', job_data)
    job.save(error => {
      if (!error) {
        console.log(`Notification job created: ${job.id}`);
      }
    });

    job.on('complete', (res) => {
      console.log(`Notification job ${job.id} completed`)
    });
    job.on('failed', (error) => {
      console.log(`Notification job ${job.id} failed: ${error}`)
    })
    job.on('progress', (progress, data) => {
      console.log(`Notification job ${job.id} ${progress}% complete`)
    });
  }
}
