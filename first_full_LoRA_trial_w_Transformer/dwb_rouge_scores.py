import itertools
from itertools import combinations
import rouge_score
from rouge_score import rouge_scorer, scoring
import re
import sys

def dwb_rouge_n(system, reference, n):
    '''
    ROUGE-N : N-Grams implementation
    
    ref = "https://web.archive.org/web/20240530230949/" + \\
          "https://www.bomberbot.com/machine-learning/" + \\
          "skip-bigrams-in-system/"
    
    @needs  itertools     `pip install itertools`
    
    @param  system      string   The hypothesis
    @param  reference   string   The truth
    @param  n           string   The "n" in "n-gram", i.e.
                                  the number of words in
                                  each grouping
    
    @returns  dict in form {"recall": recall,
                            "precision": precision,
                            "f-measure": f_measure}
    
    Example:
      >>> import rouge_n
      >>>
      >>> system = "The cat was found under the bed."
      >>> reference = "The cat was hidden under the bed."
      >>>
      >>> print(dwb_rouge_n(system, reference, 1)) # ROUGE-1
      {'recall': 0.8571428571428571, 'precision': 1.0, \\
       'f-measure': 0.9230769230769231}
      >>> print(dwb_rouge_n(system, reference, 2)) # ROUGE-2
      {'recall': 0.6, 'precision': 0.5, 'f-measure': 0.5454545454545455}
    '''
    
    sys_ngrams = list(itertools.ngrams(system.split(), n))
    ref_ngrams = list(itertools.ngrams(reference.split(), n))
    
    overlaps = set(sys_ngrams) & set(ref_ngrams)
    recall = len(overlaps) / len(ref_ngrams)
    precision = len(overlaps) / len(sys_ngrams)
    
    if precision + recall == 0:
        f_measure = 0
    else:
        f_measure = 2 * precision * recall / (precision + recall)
    ##endof:  if/else precision + recall == 0
    return {"recall": recall, "precision": precision, "f-measure": f_measure}
##endof:  dwb_rouge_n(system, reference, n)



def dwb_lcs(X, Y): 
    '''
    Longest common subsequence
    
    ref = "https://web.archive.org/web/20240530230949/" + \\
          "https://www.bomberbot.com/machine-learning/" + \\
          "skip-bigrams-in-system/"
    
    @param X  list  the words from the first sequence, space-delimited
    @param Y  list  the words from the second sequence, space-delimited
    
    @return   int   length of the longest common subsequence
    
    
    Example:
      >>> import dwb_lcs
      >>>
      >>> seq_1 = "The quick dog jumps over the lazy fox.".split()
      >>> seq_2 = "The quick brown fox jumps over the lazy dog.".split()
      >>>
      >>> dwb_lcs(seq_1, seq_2)
      6
    '''
    
    m = len(X) 
    n = len(Y) 
    
    L = [[None]*(n+1) for i in range(m+1)] 
    
    for i in range(m+1): 
        for j in range(n+1): 
            if i == 0 or j == 0: 
                L[i][j] = 0
            elif X[i-1] == Y[j-1]: 
                L[i][j] = L[i-1][j-1]+1
            else: 
                L[i][j] = max(L[i-1][j], L[i][j-1])
            ##endof:  if
        ##endof:  for j
    ##endof:  for i
    return L[m][n] 
##endof:  dwb_lcs(X, Y)

def dwb_rouge_L(system, reference):
    '''
    ROUGE-L : Longest Common Subsequence implementation
    
    ref = "https://web.archive.org/web/20240530230949/" + \\
          "https://www.bomberbot.com/machine-learning/" + \\
          "skip-bigrams-in-system/"
    
    @needs  dwb_lcs
    
    @param  system      string   The hypothesis
    @param  reference   string   The truth
    
    @returns  dict in form {"recall": recall,
                            "precision": precision,
                            "f-measure": f_measure}
    
    
    Example:
      >>> import dwb_rouge_L, dwb_lcs
      >>>
      >>> system = "The quick dog jumps over the lazy fox."
      >>> reference = "The quick brown fox jumps over the lazy dog."
      >>>
      >>> print(dwb_rouge_L(system, reference))
      {'recall': 0.7777777777777778, 'precision': 0.875, 'f-measure': 0.823529411764706}
    '''
    
    sys_len = len(system.split())
    ref_len = len(reference.split())
    lcs_len = dwb_lcs(system.split(), reference.split())
    
    recall = lcs_len / ref_len
    precision = lcs_len / sys_len
    
    if precision + recall == 0:
        f_measure = 0
    else:
        f_measure = 2 * precision * recall / (precision + recall)
    ##endof:  if/else
    
    return {"recall": recall, "precision": precision, "f-measure": f_measure}
##endof:  dwb_rouge_L(system, reference)


def dwb_skipngrams(sequence, n=2):
    '''
    Returns the set of skip n-grams
    
    ref = "https://web.archive.org/web/20240530230949/" + \\
          "https://www.bomberbot.com/machine-learning/" + \\
          "skip-bigrams-in-system/"
    
    @param  sequence    list     The input to be ngram-med, i.e.
                                 a list of words, space delimited
    @param  n           int      The 'n' in skip ngrams
                                                 ^
    
    @needs  itertools
    
    @returns  set of skip ngrams in the form (if we imagine bigrams)
                                  {(word1, word2), 
                                   (word1, word3), ...}
                   If it is the empty set (the set has length 0),
                   the set will be returned, but a notice will
                   be output (via stdout) that the set is empty.
    
    
    Examples:
      >>> import dwb_skipngrams
      >>>
      >>> my_str = "Lorem ipsum dolor sit amet"
      >>> my_seq = my_str.split()
      >>>
      >>> dwb_skipngrams(my_sequence, 2)
      {('Lorem', 'amet'),
       ('Lorem', 'dolor'),
       ('Lorem', 'ipsum'),
       ('Lorem', 'sit'),
       ('dolor', 'amet'),
       ('dolor', 'sit'),
       ('ipsum', 'amet'),
       ('ipsum', 'dolor'),
       ('ipsum', 'sit'),
       ('sit', 'amet')}
      >>>
      >>> dwb_skipngrams(my_sequence, 3)
      {('Lorem', 'dolor', 'amet'),
       ('Lorem', 'dolor', 'sit'),
       ('Lorem', 'ipsum', 'amet'),
       ('Lorem', 'ipsum', 'dolor'),
       ('Lorem', 'ipsum', 'sit'),
       ('Lorem', 'sit', 'amet'),
       ('dolor', 'sit', 'amet'),
       ('ipsum', 'dolor', 'amet'),
       ('ipsum', 'dolor', 'sit'),
       ('ipsum', 'sit', 'amet')}
      >>>
      >>> dwb_skipngrams(my_sequence, 4)
      {('Lorem', 'dolor', 'sit', 'amet'),
       ('Lorem', 'ipsum', 'dolor', 'amet'),
       ('Lorem', 'ipsum', 'dolor', 'sit'),
       ('Lorem', 'ipsum', 'sit', 'amet'),
       ('ipsum', 'dolor', 'sit', 'amet')}
      >>>
      >>> dwb_skipngrams(my_sequence, 5)
      {('Lorem', 'ipsum', 'dolor', 'sit', 'amet')}
      >>>
      >>> dwb_skipngrams(my_sequence, 6)
      #  !! Notice: you are receiving the empty set !!
      set()
    '''
    
    set_to_return = \
      set(itertools.combinations(sequence, n))
    
    if not len(set_to_return):
        print("  !! Notice: you are receiving the empty set !!")
    ##endof:  if not len(set_to_return)
    
    return set_to_return
    
##endof:  dwb_skipngrams(sequence, n=2)

def dwb_rouge_s(system, reference, n=2):
    '''
    ROUGE-S : Skip Bigrams implementation
              Extended to Skip Ngrams implementation
    
    ref = "https://web.archive.org/web/20240530230949/" + \\
          "https://www.bomberbot.com/machine-learning/" + \\
          "skip-bigrams-in-system/"
    
    @param  system      string   The hypothesis
    @param  reference   string   The truth
    @param  n           int      The 'n' in skip ngrams
                                                 ^
    
    @needs : dwb_skipngrams
    
    @returns  dict in form {"recall": recall,
                            "precision": precision,
                            "f-measure": f_measure}     
    
    
    Example
      >>> import dwb_skipngrams, dwb_rouge_s
      >>>
      >>> system = "The quick dog jumps over the lazy fox."
      >>> reference = "The quick brown fox jumps over the lazy dog."  
      >>>
      >>> print(dwb_rouge_s(system, reference))
      {'recall': 0.35, 'precision': 0.4166666666666667, \\
       'f-measure': 0.38095238095238093}
    '''
    
    sys_skipngrams = skipngrams(system.split(), n)
    ref_skipngrams = skipngrams(reference.split(), n)
    
    overlaps = sys_skipngrams & ref_skipngrams
    recall = len(overlaps) / len(ref_skipngrams)
    precision = len(overlaps) / len(sys_skipngrams)
    
    if precision + recall == 0:
        f_measure = 0
    else:
        f_measure = 2 * precision * recall / (precision + recall)
    ##endof:  if/else
    
    return {"recall": recall, "precision": precision, "f-measure": f_measure}
##endof:  dwb_rouge_s(system, reference, n=2)


def dwb_rouge_Lsum(system, reference):
    '''
    ROUGE-Lsum : Whatever
    
    @param  system      string   The hypothesis
    @param  reference   string   The truth
    
    @returns  dict in form {"recall": recall,
                            "precision": precision,
                            "f-measure": f_measure}     
    
    
    Example
      >>> import dwb_rouge_Lsum
      >>>
      >>> system = ("The quick dog jumps over the lazy fox. "
                    "That quick dog is not lazy. "
                    "That lazy fox is quick."
          )
      >>> reference = ("The quick dog jumps over the lazy fox. "
                       "That quick dog is not lazy. "
                       "That lazy fox is quick."
          )  
      >>>
      >>> print(dwb_rouge_Lsum(system, reference))
      {'recall': 1, 'precision': 1, 'f-measure': 1}
    '''
    
    rls_scorer = rouge_scorer.RougeScorer(rouge_types=['rougeLsum'])
    this_ref = reference
    this_pred = system
    rls_scores = rls_scorer.score(this_ref, this_pred)
    
    recall = rls_scores.recall
    precision = rls_scores.precision
    f_measure = rls_scores.fmeasure
    
    return {"recall": recall, "precision": precision, "f-measure": f_measure}
##endof:  dwb_rouge_Lsum(system, reference, n=2)



def score_multiple_pred_ref(
                  prediction_list, 
                  reference_list, 
                  rouge_type='rouge_s',
                  do_aggregate=True
):
    '''
    Use the agregator from google-research/rouge
       ( `rouge_score.scoring.BootsrapAggregator` )
    as it's clarified in
       "github.com/huggingface/datasets/blob/" + \\
       "main/metrics/rouge/rouge.py
    the latter being the deprecated and
    soon-to-be-removed method.
    '''
    
    if use_aggregator:
        aggregator = scoring.BootstrapAggregator()
    else:
        scores = []
    ##endof:  if

    for pred, ref in zip(prediction_list, reference_list):
        score_label = rouge_type
        score_values = None
        if ( score_label == 'rouge_s' or
             score_label == 'rouge_S' or
             score_label == 'rougeS'
        ):
            score_values = dwb_rouge_s(pred, ref)
        elif ( score_label == 'rouge_L' or
               score_label == 'rougeL' or
               score_label == 'rouge_l'
        ):
            score_values = dwb_rouge_L(pred, ref)
        elif (score_label == 'rouge_Lsum' or
              score_label == 'rougeLsum'
        ):
            score_values = dwb_rouge_Lsum
        else:
            rouge_n_regex = r"^rouge[_]?(?P<nvalue>[0-9]+)$"
            if re.match(rouge_n_regex, score_label):
                searcher = re.search(rouge_n_regex, score_label)
                rouge_n_nvalue = searcher.group('nvalue')
                if rouge_n_value == 0:
                    zero_exception_str = \
                      f"There is no '{score_label}' score.\n"
                    raise ValueError(zero_exception_str)
                elif rouge_n_value > 9:
                    big_exception_str = \
                      f"There is a '{score_label}' score,\n" + \
                      "but at some point, you'll run out of\n" + \
                      "memory, so I'm making the cutoff at 9.\n"
                    raise ValueError(big_exception_str)
            else:
                not_supported_exception_str = \
                  f"Your '{score_label}' (rouge?) score is" + \
                  "not supported by this module.\n"
                raise ValueError(not_supported_exception_str)
            ##endof:  if/elif/else with re
        ##endof:  if/elif/else <rouge_s or rouge_L or rouge_Lsum or ...>
        
        this_precision = score_values['precision']
        this_recall = score_values['recall']
        this_f_measure = score_values['f-measure']
        
        score = scoring.Score(this_precision,
                              this_recall,
                              this_f_measure
        )
        
        if use_aggregator:
            aggregator.add_scores(score)
        else:
            scores.append(score)
        ##endof:  if/esle
    ##endof:  for
    
    if use_aggregator:
        result = aggregator.aggregate()
    else:
        result = {}
        for key in scores[0]:
            result[key] = [score[key] for score in scores]
        ##endof:  for key in scores[0]
    ##endof:  if/else
        
    return result
##endof:  score_multiple_pred_ref(<params>)