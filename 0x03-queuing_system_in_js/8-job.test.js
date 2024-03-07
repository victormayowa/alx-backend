import { expect } from 'chai';
import mocha from 'mocha';
import kue from 'kue';
import { createPushNotificationsJobs } from './8-job.js';

const que = kue.createQueue();

describe('createPushNotificationsJobs', () => {
  before(() => {
    que.testMode.enter();
  });
  afterEach(() => {
    que.testMode.clear();
  });
  after(() => {
    que.testMode.exit();
  });

  it('error thrown when jobs is not an array', (done) => {
    expect(() => createPushNotificationsJobs('string', que))
      .to.throw(Error, 'Jobs is not an array');
    done();
  });

  it('3 jobs created successfully', () => {
    const jobs = [
      {name: 'job 1'},
      {name: 'job 2'},
      {name: 'job 3'}
    ];

    createPushNotificationsJobs(jobs, que);

    expect(que.testMode.jobs.length).to.equal(3);
    expect(que.testMode.jobs[0].type).to.be.equal('push_notification_code_3');
    expect(que.testMode.jobs[0].data.name).to.be.equal('job 1');
    expect(que.testMode.jobs[1].type).to.be.equal('push_notification_code_3');
    expect(que.testMode.jobs[1].data.name).to.be.equal('job 2');
  });
});
