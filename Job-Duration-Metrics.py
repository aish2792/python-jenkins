import jenkins
import matplotlib.pyplot as plt
import matplotlib
import time
from datetime import datetime
import numpy as np
import sys, getopt


class DurationMetrics:
    username = ''
    password = ''
    server = None
    buildDurations = []
    buildTimeStamps = []
    totalNumberBuilds = 0.0
    totalDuration = 0.0

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def calculateAverageDuration(self):
        averageDuration = (self.totalDuration / self.totalNumberBuilds)
        print("Average Build Duration: %.2f" % averageDuration)


    def connectToJenkins(self):
        """  Connect to jenkins """
        self.server = jenkins.Jenkins('http://localhost:8080', self.username, self.password)
        user = self.server.get_whoami() # get the user name
        version = self.server.get_version() # get the version of jenkins
        print("Hello %s from jenkins %s" %(user["fullName"], version))


    def getJobDuration(self):
         
        jenkinJobs = self.server.get_all_jobs() # return a list of all jobs on jenkins
        print(jenkinJobs)

        """ get specific job info """
        myJob = self.server.get_job_info("python-test", 0, True) # name of the job, depth = 0 (details), Fetch_all_builds = True (if false, fetches 100 builds)

        """ get specific build info """
        myJobBuilds = myJob.get("builds")

        for build in myJobBuilds:
            buildNumber = build.get("number")
            buildInfo = self.server.get_build_info("python-test", buildNumber )
            buildTimeStamp = buildInfo.get("timestamp")
            buildDuration = (buildInfo('duration')) / 1000
            self.buildTimeStamps.append(buildTimeStamp)
            self.buildDurations.append(buildDuration)

            self.totalDuration += buildDuration
            self.totalNumberBuilds += 1.0
        
        # print(self.buildTimeStamps)
        # print(self.buildDurations)


def plotJobDuration(self):
    #TODO: plot job durations

    dateTimeObjs = self.convertTimeStamps()
    dates = matplotlib.dates.date2num(dateTimeObjs)
    npArr = self.runningMean()
    # plt.plot_date(dates, self.buildDurations, '-')
    plt.plot_date(dates[:-9], npArr, '-')
    plt.xlabel("Time Of Execution")
    plt.ylabel("Build Duration (Seconds)")
    plt.title("Build Durations Over Time")
    plt.gcf().auto_fmt_xdate()

    #using convolution to take running mean
    plt.show()


def convertTimeStamps(self):
    dates = []
    for timestamp in self.buildTimeStamps:
        dateTimeObj = datetime.fromtimestamp((timestamp / 1000))
        dates.append(dateTimeObj)
    
    return dates

def runningMean(self):
    npArr = np.convolve(self.buildDurations, np.ones((10, ))/10, mode='valid')
    return npArr

def main(argv):
    username = ''
    password = ''

    try:
        opts, args = getopt.getopt(argv, "hu:p:", ["username=", "password="])
    except getopt.GetoptError:
        print("python Job-Duration-Metrics.py -u <username> -p <password>")
        sys.exit(2)
    
    for opt,arg in opts:
        if opt == '-h':
            print("python Job-Duration-Metrics.py -u <username> -p <password>")
            sys.exit()
        elif opt == '-u':
            username = arg
        elif opt == '-p':
            password = arg



    durationMetrics = DurationMetrics(username, password)
    durationMetrics.connectToJenkins()
    durationMetrics.getJobDuration()
    durationMetrics.calculateAverageDuration()
    durationMetrics.plotJobDuration()

if __name__ == '__main__':
    main(sys.argv[1:])

