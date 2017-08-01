#!/usr/bin/python
import sys
import getopt
import codecs
from operator import itemgetter
import math
import json
import urllib2

class Project:

    # FILES
    knessetMetaData_f = "FilteredMetaData.csv"
    # knessetMetaData_f = "test.txt"
    topicsToIgnore_f = "topicsToIgnore.txt"
    speakers_f = "Speakersss.tsv"

    # MACROS
    ACTIVITY_SPEAKER = '2'

    # STATIC VARS
    nodes_lst = []
    edge_list = []

    speaker_and_topics = []
    topic_list = []

    edges_dict = {}
    topicsToIgnore_lst = []
    speakers = []

    def __init__(self):
        pass

    # --------------------------------------------------------------------------------
    @staticmethod
    def createSpeakers():

        speakersLines = []
        with open(Project.speakers_f, 'r') as speakersFile:
            for line in speakersFile:
                speakersLines.append(line.split('\n')[0].decode("UTF-8"))

        for line in speakersLines:
            speakerCode = int(line.split('\t')[0])
            Project.speakers.append(speakerCode)

    # --------------------------------------------------------------------------------
    @staticmethod
    def createNodes():

        i = 1
        for node in Project.speaker_and_topics:
            node_dict = {}

            if i <= 459:
                node_dict["group"] = 1
            else:
                node_dict["group"] = 2
            node_dict["name"] = node
            Project.nodes_lst.append(node_dict)
            i += 1

    # --------------------------------------------------------------------------------
    @staticmethod
    def createTopicsToIgnore():
        # Make 'Topics To Ignore' list
        with open(Project.topicsToIgnore_f, 'r') as topicsToIgnoreFile:
            for line in topicsToIgnoreFile:
                Project.topicsToIgnore_lst.append(line.split('\n')[0].decode("UTF-8"))

    # --------------------------------------------------------------------------------
    @staticmethod
    def createTopics():

        metaDataLines = []
        with open(Project.knessetMetaData_f, 'r') as metaDataFile:
            # Read a file from knessetMetaData
            # Split file to lines
            for line in metaDataFile:
                metaDataLines.append(line.split('\n')[0].decode("UTF-8"))

        i = 1
        N = len(metaDataLines) - 1
        while i < N:
            row_current = metaDataLines[i].split('\t')

            if row_current[7] == Project.ACTIVITY_SPEAKER:
                if not Project().isTopicToIgnore(row_current[8]):
                    if row_current[8] not in Project.topic_list:
                        Project.topic_list.append(row_current[8])
            i += 1

    # --------------------------------------------------------------------------------
    @staticmethod
    def createSpeakerAndTopics():
        Project.speaker_and_topics = Project.speakers + Project.topic_list

    # --------------------------------------------------------------------------------
    @staticmethod
    def initEdgesDict():
        for x in  Project.speakers:
            Project.edges_dict[x] = []

    # --------------------------------------------------------------------------------
    @staticmethod
    def createEdgesDict():

        metaDataLines = []
        with open(Project.knessetMetaData_f, 'r') as metaDataFile:
            # Read a file from knessetMetaData
            # Split file to lines
            for line in metaDataFile:
                metaDataLines.append(line.split('\n')[0].decode("UTF-8"))


        # Process the 8th value of the line- The Topic
        i = 1
        N = len(metaDataLines) - 1
        while i < N:
            row_current = metaDataLines[i].split('\t')

            if row_current[7] == Project.ACTIVITY_SPEAKER:
                if not int(row_current[9]) == 9999:
                    if not Project().isTopicToIgnore(row_current[8]):
                        if row_current[8] not in Project.edges_dict[int(row_current[9])]:
                            Project.edges_dict[int(row_current[9])].append(row_current[8])
            i += 1

    # --------------------------------------------------------------------------------
    def isTopicToIgnore(self, topic):
        return topic in Project.topicsToIgnore_lst

    # --------------------------------------------------------------------------------
    @staticmethod
    def createEdges():
        for key, val in Project.edges_dict.iteritems():
            for x in val:
                edge_dict = {}
                edge_dict["source"] = Project.speaker_and_topics.index(key)
                edge_dict["target"] =  Project.speaker_and_topics.index(x)
                edge_dict["value"] = 0
                Project.edge_list.append(edge_dict)

    # --------------------------------------------------------------------------------
    @staticmethod
    def createNetworkJSON():
        network = {}
        network['nodes'] = Project.nodes_lst
        network['links'] = Project.edge_list
        with open('./networkSpeakersTopics.json', 'a+') as f1:
            f1.write(str(network))

    # --------------------------------------------------------------------------------
    @staticmethod
    def exportTopics():
        with open('Topics.txt', 'a+') as f1:
            for x in Project.topic_list:
                f1.write(x.encode("UTF-8"))
                f1.write("\t2\n")

# --------------------------------------------------------------------------------
if __name__ == "__main__":
    Project.createSpeakers()
    Project.createTopicsToIgnore()
    Project.createTopics()
    Project.createSpeakerAndTopics()
    Project.createNodes()
    Project.initEdgesDict()
    Project.createEdgesDict()
    Project.createEdges()
    Project.exportTopics()
    Project.createNetworkJSON()
    print "END"

