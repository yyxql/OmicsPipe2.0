#!/usr/bin/env python

from omics_pipe.parameters.default_parameters import default_parameters
from omics_pipe.utils import *
p = Bunch(default_parameters)


def cufflinks_miRNA(sample, cufflinks_miRNA_flag):
    '''Runs cufflinks to assemble .bam files from TopHat. Takes parameter MIRNA_GTF.
    
    input: 
        accepted_hits.bam
    output: 
        transcripts.gtf
    citation: 
        Trapnell C, et al. Transcript assembly and quantification by RNA-Seq reveals unannotated transcripts and isoform switching during cell differentiation  Nature Biotechnology doi:10.1038/nbt.1621
    link: 
        http://cufflinks.cbcb.umd.edu/ 
    parameters from parameters file: 
        TOPHAT_RESULTS:
            
        CUFFLINKS_RESULTS:
        
        miRNA_GTF:
        
        GENOME:
        
        CUFFLINKS_OPTIONS:
        
        CUFFLINKS_VERSION:
        '''
    spawn_job(jobname = 'cufflinks_miRNA', SAMPLE = sample, LOG_PATH = p.LOG_PATH, RESULTS_EMAIL = p.RESULTS_EMAIL, SCHEDULER = p.SCHEDULER, walltime = "120:00:00", queue = p.QUEUE, nodes = 1, ppn = 8, memory = "15gb", script = "/cufflinks_drmaa.sh", args_list = [sample,p.TOPHAT_RESULTS,p.CUFFLINKS_RESULTS,p.miRNA_GTF,p.GENOME,p.CUFFLINKS_OPTIONS,p.CUFFLINKS_VERSION])
    job_status(jobname = 'cufflinks_miRNA', resultspath = p.CUFFLINKS_RESULTS, SAMPLE = sample, outputfilename = sample + "/transcripts.gtf", FLAG_PATH = p.FLAG_PATH)
    return


if __name__ == '__main__':
    cufflinks_miRNA(sample, cufflinks_miRNA_flag)
    sys.exit(0)