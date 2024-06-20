#!/usr/env/bin python3
# -*- coding: utf-8 -*-
#
##############################################################################
'''
@file : dwb_text_utils_data_rep.py
@author : David BLACK  (GitHub @bballdave025, Hugging Face @thebballdave025)
@since : 2024-05-21

This module isn't runnable - it only provides imports. The following
imports, in fact.

@usage  from dwb_text_utils_data_rep import 
        from dwb_text_utils_data_rep import 
        from dwb_text_utils_data_rep import 
        from dwb_text_utils_data_rep import 
        from dwb_text_utils_data_rep import 
        from dwb_text_utils_data_rep import 

For the examples, the following strings are useful

my_str = ("The quick brown fox jumps over the lazy dog.\n"
          "Lorem ipsum dolor sit amet,\n"
          "consectetur\n"
          "adipiscing\n"
          "elit,\n"
          "sed do eiusmod tempor incidunt ut labore et "
          "dolore magna aliqua. Ut enim ad minim veniam,"
          "quis nostrund exercitation ullamco laboris "
          "laboris nisi ut aliquip ex ea\n"
          "commodo consequat.\n"
          "Greeking with Sokal's Postmodernism Generator: "
          "transgressing the bounderies towards a "
          "transformative hermeneutics of quantum gravity.\n"
          "Oh, Francium Fluoride and holoalphabetic "
          "Hamburgefonstivs.\n"
)

this_str = ( 
        "ETAOIN! SHRDLU! CMFWYP!\n"
        "  New York, July 18.---Here are two\n"
        "reasons why bailiffs, judges, presecu-\n"
        "tors and court stenographers die\n"
        "young.\n"
        "John Ziampettisledibetci was fined\n"
        "$1 for owning an unmuzzled dog.\n"
        "Robert Tyzyczhowzswiski is ask-\n"
        "ing the court to change his cogno-\n"
        "men.\n"
        "\n
        "On the Insert tab, the galleries include items "
        "that are designed to coordinate with the overall "
        "look of your document.\n"
)

that_str = (
        "This pangram contains four As, one B, two Cs, one D, thirty Es, "
        "six Fs, five Gs, seven Hs, eleven Is, one J, one K, two Ls, two "
        "Ms, eighteen Ns, fifteen Os, two Ps, one Q, five Rs, "
        "twenty-seven Ss, eighteen Ts, two Us, seven Vs, eight Ws, two "
        "Xs, three Ys, & one Z. "
        "Pack my box with five dozen liquor jugs. "
        "Ciyesh yeshchyo etikh myagkikh frantsuzkikh bulok, da vypei zhe "
        "chayu. "
        "Would a citrus live in the jungles of the sount? Yes, "
        "but a fake specimen! "
        "Mr Jock, TV quiz PhD, bags few lynx. "
        "Blowzy night-frumps vex'd Jack Q. "
        "Waltz, bad nymph, for quick jigs vex. "
        "Glib jocks quiz nymph to vex dwarf. "
        "Sphinx of black quartz, judge my vow. "
        "How quickly daft jumping zebras vex! "
        "The five boxing wizards jump quickly. "
        "Jackdaws love my big sphinx of quartz. "
        "Iroha: "
        "The leaves may shine with colored gloss / "
        "But they will fall, forever lost / "
        "In this false world, what soul, I ask / "
        "May hope in timelessness to last / "
        "Today I cross these mountain depths" /
        "With no vain dreams or drunkenness."
        "Iroha nihoeto / Chirinuru wo / "
        "Wakayo tareso / Tsune naramu / "
        "Uwi no okuyama / Kefu koete / "
        "Asaki yume mishi / Wefi mo sesun"
)

other_str = (
  "Li Europan lingues es membres del sam familie. Lor separat existentie es un myth. Por scientie, musica, sport etc, litot Europa usa li sam vocabular. Li lingues differe solmen in li grammatica, li pronunciation e li plu commun vocabules. Omnicos directe al desirabilite de un nov lingua franca: On refusa continuar payar custosi traductores."
  "At solmen va esser necessi far uniform grammatica, pronunciation e plu commun paroles. Ma quande lingues coalesce, li grammatica del resultant lingue es plu simplic e regulari quam ti del coalescent lingues. Li nov lingua franca va esser plu simplic e regulari quam li existent Europan lingues. It va esser tam simplic quam Occidental in fact, it va esser Occidental. A un Angleso it va semblar un simplificat Angles, quam un skeptic Cambridge amico dit me que Occidental es."

'''
##############################################################################


##-----------
## IMPORTS
##-----------
import os
import csv
import json
import pandas as pd  # requires `pip install pandas`


def wc(filename, do_print=True):
  '''
  Mimics part of the behavior of the `bash` command, `wc`.
  
  @todo  Get things ready for UnicodeDammit, so we make sure everything
         gets put in as utf-8
  
  @param   str   filename  A string representing the filename whose length
                           in lines, words, and characters will be given
  
  @return  tuple   A tuple with the format:
                      (n_lines, n_words, n_chars)
  
  @result       The lengths get output in the format
                        n_lines: {n_lines}
                        n_words: {n_words}
                        n_chars: {n_chars}
                  if the 'do_print' boolean has a 'True' value
  
    Examples:
    
      >>> from dwb_text_utils_data_rep import wc
      >>> my_str = ("The quick brown fox jumps over the lazy dog.\n"
                    "Lorem ipsum dolor sit amet,\n"
                    "consectetur\n"
                    "adipiscing\n"
                    "elit,\n"
                    "sed do eiusmod tempor incidunt ut labore et "
                    "dolore magna aliqua. Ut enim ad minim veniam,"
                    "quis nostrund exercitation ullamco laboris "
                    "laboris nisi ut aliquip ex ea\n"
                    "commodo consequat.\n"
                    "Greeking with Sokal's Postmodernism Generator: "
                    "transgressing the bounderies towards a "
                    "transformative hermeneutics of quantum gravity.\n"
                    "Oh, Francium Fluoride and holoalphabetic "
                    "Hamburgefonstivs.\n"
          )
      >>> with open("my_file.txt", 'w', encoding='utf-8') as fh:
            fh.write(my_str)
          ##endof:  with open ... fh
      >>>
      >>> l, w, c = wc("my_file.txt")
      
      >>> _, _, only_char_about_char = wc("my_file.txt", do_print=False)
      
      >>> line_count, word_count, _ = wc("my_file.txt", do_print=False)
      
      >>> wc("my_file.txt")
      
      >>> _, _, _ = wc("my_file.txt")
      
  '''
  
  n_lines = 0
  n_words = 0
  n_chars = 0
  
  with open(filename, 'r', encoding='utf-8') as f:
    for line in f:
      words = line.split()
      
      n_lines += 1
      n_words += len(words)
      n_chars += len(line)
      
    ##endof:  for line in f
    
  ##endof for line in f
  
  print("n_lines: " + str(n_lines))
  print("n_words: " + str(n_words))
  print("n_chars: " + str(n_chars))
  
##endof:  wc(filename)


def head(n_lines, filename, do_print=True):
  '''
  Mimics part of the behavior of the `bash` command, `head`.
  
  @todo  Get things ready for UnicodeDammit, so we make sure everything
         gets put in as utf-8
  
  @param n_lines         The number of lines. It will be the  n_lines
                         first lines.
  
  @param filename        A string representing the filename whose first lines
                         will be found.
  
  @return    str  A string representing the first  n_lines  lines of the file.
  
  @result                A string representing the first  n_lines  lines of
                         the file represented by  filename  will print out,
                         if  do_print  has the value of  True
  
    Examples:
      >>> from dwb_text_utils_data_rep import head
      >>>
      >>> this_str = ( 
             "ETAOIN! SHRDLU! CMFWYP!\n"
             "  New York, July 18.---Here are two\n"
             "reasons why bailiffs, judges, presecu-\n"
             "tors and court stenographers die\n"
             "young.\n"
             "John Ziampettisledibetci was fined\n"
             "$1 for owning an unmuzzled dog.\n"
             "Robert Tyzyczhowzswiski is ask-\n"
             "ing the court to change his cogno-\n"
             "men.\n"
             "\n
             "On the Insert tab, the galleries include items "
             "that are designed to coordinate with the overall "
             "look of your document.\n"
  '''
  
  str_to_return = ''
  
  with open(filename, 'r', encoding='utf-8') as ifh:
    for i in range(n_lines):
      #  getting rid of the linefeed character at the end.
      #+ it also gets rid of any trailing whitespace, which
      #+ is probably not what I want to do
      # @todo  Only take off the trailing linefeed
      this_line = next(ifh).rstrip()
      
      if do_print:
        print(this_line)
      ##endof:  if do_print
      
      str_to_return += this_line + '\n'
  ##endof:  with open ... ifh # Input File Handle
  
  return str_to_return
  
##endof:  head(n_lines, filename, do_print=True)


def first_n_chars_in_file(n_chars, filename, do_print=True):
  '''
  Yes, huge problems with big files and running out of memory
  (fix with buffering, as per the reference). Also a problems
  with asking for more characters than there are in the file.
  (simple tests or a try/catch could fix that)
    ref="https://stackoverflow.com/questions/2988211"
    arch_ref="https://web.archive.org/web/20240521233914/" + \
                 "https://stackoverflow.com/questions/2988211/" + \
                 "how-can-i-read-a-single-character-at-a-time-" + \
                 "from-a-file-in-python"
  
    Examples:
      >>> 
      >>> that_str = (
           "This pangram contains four As, one B, two Cs, one D, thirty Es, "
           "six Fs, five Gs, seven Hs, eleven Is, one J, one K, two Ls, two "
           "Ms, eighteen Ns, fifteen Os, two Ps, one Q, five Rs, "
           "twenty-seven Ss, eighteen Ts, two Us, seven Vs, eight Ws, two "
           "Xs, three Ys, & one Z. "
           "Pack my box with five dozen liquor jugs. "
           "Ciyesh yeshchyo etikh myagkikh frantsuzkikh bulok, da vypei zhe "
           "chayu. "
           "Would a citrus live in the jungles of the sount? Yes, "
           "but a fake specimen! "
           "Mr Jock, TV quiz PhD, bags few lynx. "
           "Blowzy night-frumps vex'd Jack Q. "
           "Waltz, bad nymph, for quick jigs vex. "
           "Glib jocks quiz nymph to vex dwarf. "
           "Sphinx of black quartz, judge my vow. "
           "How quickly daft jumping zebras vex! "
           "The five boxing wizards jump quickly. "
           "Jackdaws love my big sphinx of quartz. "
           "Iroha: "
           "The leaves may shine with colored gloss / "
           "But they will fall, forever lost / "
           "In this false world, what soul, I ask / "
           "May hope in timelessness to last / "
           "Today I cross these mountain depths" /
           "With no vain dreams or drunkenness."
           "Iroha nihoeto / Chirinuru wo / "
           "Wakayo tareso / Tsune naramu / "
           "Uwi no okuyama / Kefu koete / "
           "Asaki yume mishi / Wefi mo sesun"
      )
  '''
  with open(filename, 'r', encoding='utf-8') as f:
    file_contents = f.read()
    print(file_contents[:n_chars])
  ##endof:  with open ... f
##endof:  first_n_chars_in_file


def csv2json_bare_builtins(csv_fname, json_fname):
  with open(csv_fname, 'r', encoding='utf-8') as c_fh:
    with open(json_fname, 'w', encoding='utf-8') as j_fh:
      ## fieldnames = ("id", "dialogue", "summary") 
      ##         # we have the fieldnames in the header
      reader = csv.DictReader(c_fh) #, fieldnames)
      out = json.dumps([ row for row in reader ])
      j_fh.write(out)
    ##endof:  with open ... j_fh
  ##endof:  with open ... c_fh
##endof:  csv2json_bare_builtins(csv_fname, json_fname)


def csv2json_better_builtins_indent(csv_fname, json_fname):
  with open(csv_fname, 'r', encoding='utf-8') as c_fh:
    with open(json_fname, 'w', encoding='utf-8') as j_fh:
      reader = csv.DictReader(c_fh)
      out = json.dumps([ row for row in reader ], indent=2)
      j_fh.write(out)
    ##endof:  with open ... j_fh
  ##endof:  with open ... c_fh
##endof:  csv2json_better_builtins_indent


def csv2json_overkill_builtins_robust(csv_fname, json_fname):
  with open(csv_fname, 'r', encoding='utf-8') as c_fh:
    with open(json_fname, 'w', encoding='utf-8') as j_fh:
      reader = csv.DictReader(c_fh)
      
      #  the  sort_keys  option could have something
      #+ to make matching the tutorial easier (with
      #+ switched header order, as we'll see
      out = json.dumps([ row for row in reader ], 
                       sort_keys=False,
                       indent=2,
                       separators=(',', ': ')
      )
      j_fh.write(out)
    ##endof:  with open ... j_fh
  ##endof:  with open ... c_fh
##endof:  csv2json_overkill_builtins_robust


## Pandas
def csv2json_pandas_basic(csv_fname, json_fname):
  frame_from_csv = pd.DataFrame(pd.read_csv(csv_fname, 
                                            sep=',', 
                                            header=0,
                                            index_col=False
                                )
                   )
  #  header=0,  b/c 0th row, the top one, 
  #+ has our field names
  frame_from_csv.to_json(json_fname, 
                         orient="records"
  ) 
  #  orient="records" gets the order as  "key": "value"
  #+ coming from                       header :  value in the CSV
##endof:  csv2json_pandas_basic


