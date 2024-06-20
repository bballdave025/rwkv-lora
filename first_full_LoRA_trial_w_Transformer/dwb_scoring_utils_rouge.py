#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##############################################################################
'''
@file : dwb_scoring_utils_rouge.py
@author : David BLACK  (GitHub @bballdave025, Hugging Face @thebballdave025)
@since : 2024-06-10  (functions in-line in Notebook weeks earlier)

This module isn't runnable - it only provides imports. Three imports, in
fact.

@usage  from dwb_scoring_utils_rouge import format_rouge_score_rough
        from dwb_scoring_utils_rouge import print_rouge_scores
        from dwb_scoring_utils_rouge import compute_google_rouge_score
'''
##############################################################################

import re
import rouge_score  # requires pip install rouge-score
from rouge_score import rouge_scorer, scoring


def compute_google_rouge_score(predictions, 
                               references, 
                               rouge_types=None, 
                               use_aggregator=True, 
                               use_stemmer=False):

    '''
    Figuring out the nice format of the deprecated method from
    the googleresearch/rouge method it claims to be calling.
    
    @ref:
     refurl1 = "https://github.com/google-research/google-research/" + \\
               "tree/master/rouge
     refurl2 = "https://web.archive.org/web/20240530231357/" + \\
               "https://pypi.org/project/rouge-score/"
     this is PyPI version 0.1.2 ( pip install rouge-score==0.1.2
     
     <strike>I can't see how to aggregate it, though I may have</strike>
     I _have_ found a resource at
     
       ref_gg_rg="https://github.com/huggingface/datasets/blob/" + \\
                 "main/metrics/rouge/rouge.py"
    
       arch_gg_rg="https://web.archive.org/web/20240603192938/" + \\
                  "https://github.com/huggingface/datasets/blob/" + \\
                  "main/metrics/rouge/rouge.py"
    
    @param    list  predictions  The list of prediction/hypothesis/system
                                 strings; it is assumed these will mostly
                                 be summaries. A list of length one is 
                                 perfectly acceptable.
    
    @param    list  references   The list of reference/truth strings; it 
                                 is assumed these will mostly be summaries.
                                 A list of length one is perfectly 
                                 acceptable
    
    @param    list  rouge_types  \[Optional\]
                                 The type of ROUGE score desired. The list
                                 may contain any combination of or all of
                                 {"rouge1", "rouge2", "rougeL", "rougeLsum"}
                                 If no value is passed in, the default will
                                 be all four.
    
    @param    bool  use_aggregator  Whether or not to use the aggregator
                                    provided by google research to combine
                                    multiple scores
    
    @param    bool  use_stemmer   Whether or not to use Porter Stemming
                                  (a linguistic thing that returns the
                                   roots of words - a sort of
                                   "un-inflection" tool (very non-technical
                                   term).
    
    @return   one of two things, depending on the value of use_aggregator:
            1) if use_aggregator=False
            list of scores in the format, e.g.
               [Score('rouge1',
               
    '''
    
    if rouge_types is None:
        rouge_types = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
    ##endof:  if rouge_types is None
    
    scorer = rouge_scorer.RougeScorer(rouge_types=rouge_types, 
                                      use_stemmer=use_stemmer
    )
    
    if use_aggregator:
        aggregator = scoring.BootstrapAggregator()
    else:
        scores = []
    ##endof:  if/else use_aggregator
    
    for ref, pred in zip(references, predictions):
        score = scorer.score(ref, pred)
        if use_aggregator:
            aggregator.add_scores(score)
        else:
            scores.append(score)
    ##endof:  for ref, pred in zip(references, predictions)

    result = "there-is-some-problem-" + \
             "in-compute_google_rouge_score"
                                     #  scoping (if we weren't
                                     #+ in Python) and having
                                     #+ a sort of error message
    
    if use_aggregator:
        result = aggregator.aggregate()
    else:
        result = {}
        for key in scores[0]:
            result[key] = [score[key] for score in scores]
        ##endof:  for key in scores[0]
    ##endof:  if/else use_aggregator
    
    return result
    
##endof:  compute_google_rouge_score


def format_rouge_score_rough(this_rouge_str):
    '''
    Make it look pretty
    
    @param    string  this_rouge_str : A string with the Google Research
                                       rouge score as it gets spat out.
    
    @return   string      A nicely formatted version of the input.
    '''
    
    rouge_ret_str = this_rouge_str
    
    rouge_ret_str = re.sub(r"([(,][ ]?)([0-9A-Za-z_]+[=])",
                            "\g<1>\n     \g<2>",
                           rouge_ret_str,
                           flags=re.I|re.M
    )
    
    rouge_ret_str = re.sub(r"(.)([)])$",
                            "\g<1>\n\g<2>",
                           rouge_ret_str
    )

    rouge_ret_str = rouge_ret_str.replace(
                                   "precision=",
                                   "     precision="
                                ).replace(
                                   "recall=",
                                   "     recall="
                                ).replace(
                                   "fmeasure=",
                                   "     fmeasure="
    )
    
    return rouge_ret_str
    
##endof:  format_rouge_score_rough(<params>)


def print_rouge_scores(result, sample_num_or_header=None):
    '''
    Output the nicely formatted score string to stdout
    (or wherever `print` is set up to output.
    
    @param   result   Either a `Score` object or an 
                      `Aggregated Score` object
    
    @param
    
    @result  A nicely formatted score with any important
             information gets printed out.
    '''
    
    print("\n\n---------- ROUGE SCORES ----------")
    if sample_num_or_header is None:
        print("  --------- dialogue ----------")
    elif type(sample_num_or_header) is int:
        print(f"  --------- dialogue {sample_num_or_header+1} " + \
               "----------")
    else:
        print(f"  --------- {sample_num_or_header} ----------")
    ##endof:  if/else sample_num is None
    print("ROUGE-1 results")
    rouge1_str = str(result['rouge1'])
    print(format_rouge_score_rough(rouge1_str))
    print("ROUGE-2 results")
    rouge2_str = str(result['rouge2'])
    print(format_rouge_score_rough(rouge2_str))
    print("ROUGE-L results")
    rougeL_str = str(result['rougeL'])
    print(format_rouge_score_rough(rougeL_str))
    print("ROUGE-Lsum results")
    rougeLsum_str = str(result['rougeLsum'])
    print(format_rouge_score_rough(rougeLsum_str))
##endof:  print_rouge_scores(<params>)
