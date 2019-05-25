""" This script will get all the jobs which are stuck in RUNNABLE state """
#!/usr/bin/env python
import sys
import boto3
from pprint import pprint
import datetime
import argparse


def get_all_jobqueues():
	""" Get all the Job queues """
	client = boto3.client('batch')
	response = client.describe_job_queues()
	queues = response['jobQueues']
	myqueues = []
	for queue in queues:
		myqueues.append(str(queue['jobQueueArn']))
	return myqueues

def get_all_runnable_jobs(sec):
	""" Get all the runnable jobs under each queue """
	client = boto3.client('batch')
	myjobqueues = get_all_jobqueues()
	allrunnablejobs = []
	for jobqueue in myjobqueues:
		myrunnablejob = {}
		queuejobs = client.list_jobs(jobQueue=jobqueue, jobStatus="RUNNABLE")
		jobs = queuejobs['jobSummaryList']
		if jobs:
			for job in jobs:
				myrunnablejob["jobQueueName"] = jobqueue
				myrunnablejob["status"] = job['status']
				myrunnablejob["jobId"] = job['jobId']
				unixtimestamp = job['createdAt']
				currenttime = datetime.datetime.now()
				readable = datetime.datetime.fromtimestamp(unixtimestamp/1000.0)
				myrunnablejob["JobStuckInSeconds"] = (currenttime - readable).seconds
				if myrunnablejob["JobStuckInSeconds"] > sec:
					allrunnablejobs.append(myrunnablejob)
	return allrunnablejobs

def main():
	""" Main Function """
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--seconds", help="Pass the number of seconds to check the RUNNABLE jobs:", type=int, required=True)
	args = parser.parse_args()

	result = get_all_runnable_jobs(args.seconds)
	if result:
		print("Below are the jobs stuck in RUNNABLE state for more than {0} seconds".format(args.seconds))
		pprint(result)
		sys.exit(1)
	else:
		sys.exit(0)

if __name__ == '__main__':
	main()
