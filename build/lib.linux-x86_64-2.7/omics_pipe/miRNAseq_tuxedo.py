#!/usr/bin/env python

#from sumatra.projects import load_project
#from sumatra.parameters import build_parameters
#from sumatra.decorators import capture
from ruffus import *
import sys 
import os
import time
import datetime 
import drmaa
from omics_pipe.utils import *
from omics_pipe.modules.fastqc import fastqc
from omics_pipe.modules.tophat_miRNA import tophat_miRNA
from omics_pipe.modules.cufflinks_miRNA import cufflinks_miRNA
from omics_pipe.modules.cuffmerge_miRNA import cuffmerge_miRNA
from omics_pipe.modules.cuffmergetocompare_miRNA import cuffmergetocompare_miRNA
from omics_pipe.modules.cuffdiff_miRNA import cuffdiff_miRNA
from omics_pipe.modules.RNAseq_report_tuxedo import RNAseq_report_tuxedo
from omics_pipe.modules.fastq_length_filter_miRNA import fastq_length_filter_miRNA
from omics_pipe.modules.cutadapt_miRNA import cutadapt_miRNA


from omics_pipe.parameters.default_parameters import default_parameters 
p = Bunch(default_parameters)

os.chdir(p.WORKING_DIR)
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d %H:%M")    

print p

for step in p.STEPS:
    vars()['inputList_' + step] = []
    for sample in p.SAMPLE_LIST:
        vars()['inputList_' + step].append([sample, "%s/%s_%s_completed.flag" % (p.FLAG_PATH, step, sample)])
    print vars()['inputList_' + step]

for step in p.STEPS_DE:
    vars()['inputList_' + step] = []
    vars()['inputList_' + step].append([step, "%s/%s_completed.flag" % (p.FLAG_PATH, step)])
    print vars()['inputList_' + step]
     
@parallel(inputList_cutadapt_miRNA)
@check_if_uptodate(check_file_exists)
def run_cutadapt_miRNA(sample, cutadapt_miRNA_flag):
    cutadapt_miRNA(sample, cutadapt_miRNA_flag)
    return

@parallel(inputList_fastq_length_filter_miRNA)
@check_if_uptodate(check_file_exists)
@follows(run_cutadapt_miRNA)
def run_fastq_length_filter_miRNA(sample, fastq_length_filter_miRNA_flag):
    fastq_length_filter_miRNA(sample, fastq_length_filter_miRNA_flag)
    return

@parallel(inputList_fastqc_miRNA)
@check_if_uptodate(check_file_exists)
@follows(run_fastq_length_filter_miRNA)
def run_fastqc(sample, fastqc_flag):
    fastqc(sample, fastqc_flag)
    return

@parallel(inputList_tophat_miRNA)
@check_if_uptodate(check_file_exists)
@follows(run_fastq_length_filter_miRNA)   
def run_tophat_miRNA(sample, tophat_miRNA_flag):
    tophat_miRNA(sample, tophat_miRNA_flag)
    return


@parallel(inputList_cufflinks_miRNA)
@check_if_uptodate(check_file_exists)
@follows(run_tophat_miRNA)
def run_cufflinks_miRNA(sample, cufflinks_miRNA_flag):
    cufflinks_miRNA(sample, cufflinks_miRNA_flag)
    return

@parallel(inputList_cuffmerge_miRNA)
@check_if_uptodate(check_file_exists)
@follows(run_cufflinks_miRNA)
def run_cuffmerge_miRNA(step, cuffmerge_miRNA_flag):
    cuffmerge_miRNA(step, cuffmerge_miRNA_flag)
    return

@parallel(inputList_cuffmergetocompare_miRNA)
@check_if_uptodate(check_file_exists)
@follows(run_cuffmerge_miRNA)
def run_cuffmergetocompare_miRNA(step, cuffmergetocompare_miRNA_flag):
    cuffmergetocompare_miRNA(step, cuffmergetocompare_miRNA_flag)
    return

@check_if_uptodate(check_file_exists)
@parallel(inputList_cuffdiff_miRNA)
@follows(run_cuffmergetocompare_miRNA)
def run_cuffdiff_miRNA(step, cuffdiff_miRNA_flag):
    cuffdiff_miRNA(step, cuffdiff_miRNA_flag)
    return

@check_if_uptodate(check_file_exists)
@parallel(inputList_RNAseq_report_tuxedo)
@follows(run_cuffdiff_miRNA)
def run_RNAseq_report_tuxedo(step, RNAseq_report_tuxedo_flag):
    RNAseq_report_tuxedo(step, RNAseq_report_tuxedo_flag)
    return


@parallel(inputList_last_function)
@check_if_uptodate(check_file_exists)
@follows(run_fastqc, run_RNAseq_report_tuxedo)
def last_function(sample, last_function_flag):
    print "PIPELINE HAS FINISHED SUCCESSFULLY!!! YAY!"
    pipeline_graph_output = p.FLAG_PATH + "/pipeline_" + sample + "_" + str(date) + ".pdf"
    pipeline_printout_graph (pipeline_graph_output,'pdf', step, no_key_legend=False)
    stage = "last_function"
    flag_file = "%s/%s_%s_completed.flag" % (p.FLAG_PATH, stage, sample)
    open(flag_file, 'w').close()
    return   


if __name__ == '__main__':

    pipeline_run(p.STEP, multiprocess = p.PIPE_MULTIPROCESS, verbose = p.PIPE_VERBOSE, gnu_make_maximal_rebuild_mode = p.PIPE_REBUILD)


