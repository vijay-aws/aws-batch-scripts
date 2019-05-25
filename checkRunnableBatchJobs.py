""" This script will get all the jobs which are stuck in RUNNABLE state """
#!/usr/bin/env python
import sys
import boto3

def get_all_jobqueues():
	""" Get all the Job queues """
	client = boto3.client('batch')
	response = client.describe_job_queues()
	queues = response['jobQueues']
	myqueues = []
	for queue in queues:
		myqueues.append(str(queue['jobQueueArn']))
	return myqueues

def get_all_runnable_jobs():
	""" Get all the runnable jobs under each queue """
	client = boto3.client('batch')
	myjobqueues = get_all_jobqueues()
	myrunnablejobs = {}
	for jobqueue in myjobqueues:
		queuejobs = client.list_jobs(jobQueue=jobqueue, jobStatus="RUNNABLE")
		jobs = queuejobs['jobSummaryList']
		for job in jobs:
			myrunnablejobs["jobQueueName"] = jobqueue
			myrunnablejobs["status"] = job['status']
			myrunnablejobs["jobId"] = job['jobId']
	return myrunnablejobs

def main():
	""" Main Function """
	result = get_all_runnable_jobs()
	if result:
		print("Below are the jobs stuck in RUNNABLE state", result)
		sys.exit(1)
	else:
		sys.exit(0)

if __name__ == '__main__':
	main()
