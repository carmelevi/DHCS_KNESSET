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
    topicsToIgnore_f = "topicsToIgnore.txt"
    speakers_f = "relSpeakers.json"

    # MACROS
    ACTIVITY_SPEAKER = '2'

    # STATIC VARS
    nodes_lst = []
    edge_list = []
    speaker_list_codes = []

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
    def createSpeakersList():
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
                    if not int(row_current[9]) == 9999:
                        if int(row_current[9]) not in Project.speaker_list_codes:
                            Project.speaker_list_codes.append(int(row_current[9]))
            i += 1

        # speakersLines = []
        # with open(Project.speakers_f, 'r') as speakersFile:
        #     for line in speakersFile:
        #         speakersLines.append(line.split('\n')[0].decode("UTF-8"))
        #
        # tmp = {}
        # for line in speakersLines:
        #     tmp[int(line.split('\t')[0])] = line.split('\t')[1]
        #
        # with open('./relSpeakers.json', 'a+') as f1:
        #     for x in Project.speaker_list_codes:
        #         f1.write(str(x) + "\t")
        #         f1.write(tmp[x].encode("UTF-8"))
        #         f1.write("\n")

    # --------------------------------------------------------------------------------
    @staticmethod
    def createNodes():

        for node in Project.speakers:
            node_dict = {}
            node_dict["group"] = 1
            node_dict["name"] = node
            Project.nodes_lst.append(node_dict)

    # --------------------------------------------------------------------------------
    @staticmethod
    def createEdgesDict():

        # Make 'Topics To Ignore' list
        with open(Project.topicsToIgnore_f, 'r') as topicsToIgnoreFile:
            for line in topicsToIgnoreFile:
                Project.topicsToIgnore_lst.append(line.split('\n')[0].decode("UTF-8"))

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
            row_next = metaDataLines[i + 1].split('\t')

            if row_current[7] == Project.ACTIVITY_SPEAKER:
                if not Project().isTopicToIgnore(row_current[8]):
                    speakers_lst = [int(row_current[9])]

                    # Check if it's still the same topic
                    while row_current[7] == row_next[7]:
                        speakers_lst.append(int(row_next[9]))
                        i += 1
                        row_current = metaDataLines[i].split('\t')
                        row_next = metaDataLines[i + 1].split('\t')

                    speakers_set = set(speakers_lst)
                    speakers_set.discard(9999)
                    speakers_lst = list(speakers_set)

                    if not len(speakers_lst) == 1:
                        all_couples = [frozenset([speakers_lst[k], speakers_lst[j]]) for k in range(len(speakers_lst)) for j in range(k + 1, len(speakers_lst))]

                        for couple in all_couples:
                            if couple not in Project.edges_dict:
                                Project.edges_dict[couple] = 1
                            else:
                                Project.edges_dict[couple] += 1
            i += 1

    # --------------------------------------------------------------------------------
    def isTopicToIgnore(self, topic):
        return topic in Project.topicsToIgnore_lst

    # --------------------------------------------------------------------------------
    @staticmethod
    def createEdges():
        for key, val in Project.edges_dict.iteritems():
            edge_dict = {}
            edge_dict["source"] = Project.speakers.index(list(key)[0])
            edge_dict["target"] = Project.speakers.index(list(key)[1])
            edge_dict["value"] = val
            Project.edge_list.append(edge_dict)

    # --------------------------------------------------------------------------------
    @staticmethod
    def createNetworkJSON():
        network = {}
        network['nodes'] = Project.nodes_lst
        network['links'] = Project.edge_list
        with open('./network.json', 'a+') as f1:
            f1.write(str(network))

# --------------------------------------------------------------------------------
if __name__ == "__main__":
    Project.createSpeakers()
    Project.createSpeakersList()
    Project.createNodes()
    Project.createEdgesDict()
    Project.createEdges()
    Project.createNetworkJSON()
    print "END"

