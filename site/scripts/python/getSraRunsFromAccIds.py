#!/usr/bin/env python
import shutil, os, argparse, sys, stat
import requests
import csv, io







class SRAUtils:
    @staticmethod
    def getSraUrlFromRunAccession(accesion):
        if not type(accesion) is str:
            raise Exception("Error in getSraUrlFromRunAccession: accesion should be str, not " + str(type(accesion)))
        if len(accesion) < 7:
            raise Exception("Error in getSraUrlFromRunAccession: accession should be least 7 character long, not " + str(len(accesion)) + ", for " + str(accesion))
        
        if not accesion.startswith("ERR") and not accesion.startswith("SRR"):
            raise Exception("Error in getSraUrlFromRunAccession: accession should start with either ERR or SRR, not " + str(accesion[0:3]) )
        
        template = "ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/{PREFIX}/{PREFIX}{PREFIXNUMS}/{ACCESION}/{ACCESION}.sra"
        return template.format(PREFIX = accesion[0:3], PREFIXNUMS = accesion[3:6], ACCESION = accesion)

    @staticmethod
    def getRunsFromSampleAcc(sample):
        if not sample.startswith("ERS") and not sample.startswith("SRS"):
            raise Exception("sample should start with ERS or SRS, not: " + sample)
        payload = {"save": "efetch","db": "sra","rettype" : "runinfo", "term" : sample };
        r = requests.get('http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi', params=payload)
        if 200 ==  r.status_code:
            if r.text.isspace():
                raise Exception("Got blank string from " + str(r.url ))
            else:
                reader_list = csv.DictReader(io.StringIO(r.text))
                runIds = []
                for row in reader_list:
                    if sample == str(row.get('Sample')):
                        runIds.append(str(row.get('Run')))
                if 0 == len(runIds):
                    raise Exception('Found %d entries in SRA for "%s" when expecting at least 1' % (len(runIds), sample))
                else:        
                    return runIds
        else:
            raise Exception("Error in downloading from " + str(r.url) + " got response code " + str(r.status_code))
        
    @staticmethod
    def getRunsFromProjectAcc(project):
        if not project.startswith("ERP") and not project.startswith("SRP"):
            raise Exception("project should start with ERP or SRP, not: " + project)
        payload = {"save": "efetch","db": "sra","rettype" : "runinfo", "term" : project };
        r = requests.get('http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi', params=payload)
        if 200 ==  r.status_code:
            if r.text.isspace():
                raise Exception("Got blank string from " + str(r.url ))
            else:
                reader_list = csv.DictReader(io.StringIO(r.text))
                runIds = []
                for row in reader_list:
                    if project == str(row.get('SRAStudy')):
                        runIds.append(str(row.get('Run')))
                if 0 == len(runIds):
                    raise Exception('Found %d entries in SRA for "%s" when expecting at least 1' % (len(runIds), project))
                else:        
                    return runIds
        else:
            raise Exception("Error in downloading from " + str(r.url) + " got response code " + str(r.status_code))
        
    @staticmethod
    def getRunsFromExperimentAcc(experiment):
        if not experiment.startswith("ERX") and not experiment.startswith("SRX"):
            raise Exception("experiment should start with ERX or SRX, not: " + experiment)
        payload = {"save": "efetch","db": "sra","rettype" : "runinfo", "term" : experiment };
        r = requests.get('http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi', params=payload)
        if 200 ==  r.status_code:
            if r.text.isspace():
                raise Exception("Got blank string from " + str(r.url ))
            else:
                reader_list = csv.DictReader(io.StringIO(r.text))
                runIds = []
                for row in reader_list:
                    if experiment == str(row.get('Experiment')):
                        runIds.append(str(row.get('Run')))
                if 0 == len(runIds):
                    raise Exception('Found %d entries in SRA for "%s" when expecting at least 1' % (len(runIds), experiment))
                else:        
                    return runIds
        else:
            raise Exception("Error in downloading from " + str(r.url) + " got response code " + str(r.status_code))
    
    @staticmethod
    def getRunsFromSRAIdentifier(identifier):
        if identifier.startswith("ERX") or identifier.startswith("SRX"):
            return SRAUtils.getRunsFromExperimentAcc(identifier)
        elif identifier.startswith("ERP") or identifier.startswith("SRP"):
            return SRAUtils.getRunsFromProjectAcc(identifier)
        elif identifier.startswith("ERS") or identifier.startswith("SRS"):
            return SRAUtils.getRunsFromSampleAcc(identifier)
        elif identifier.startswith("ERR") or identifier.startswith("SRR"):
            return [identifier]
        else:
            raise Exception("Error, unrecognized prefix for sra Identifier " + str(identifier))

def parse_args_sraIdentifier():
    parser = argparse.ArgumentParser()
    parser.add_argument('--identifiers', type=str, required =True)
    return parser.parse_args()

def runGetRunsFromSampleAcc():
    args = parse_args_sraIdentifier()
    identifiers = args.identifiers.split(",")
    sys.stdout.write(str("identifier") + "\t" + str("run") + "\t" + "url" + "\n")
    for identifier in identifiers:
        runs = SRAUtils.getRunsFromSRAIdentifier(identifier)
        for run in runs:
            if not None == run:
                sys.stdout.write(str(identifier) + "\t" + str(run) + "\t" + SRAUtils.getSraUrlFromRunAccession(str(run)) + "\n")
    
if __name__ == "__main__":
    runGetRunsFromSampleAcc()
