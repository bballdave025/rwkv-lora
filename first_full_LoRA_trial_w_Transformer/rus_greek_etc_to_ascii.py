#! /cygdrive/c/Users/Anast/.conda/envs/get-workouts-out/python -u
# -*- coding: utf-8 -*-


## I'm using a conda hack, so the shebang is a bit different that normal,
## Not '#!/usr/bin/python3 -u'
## I've done a `conda activate get-workouts-out`

##############################################################################
'''
@file: rus_greek_etc_to_ascii.py
@author : David Wallace Black
         uname: bballdave025; server: yahoo -d-o-t- com
       OR
         uname: thedavidwblack; server: gmail -d-o-t- com
@since :  2020-03-31
@ref : "https://www.ling.upenn.edu/courses/Spring_2003/" + \
       "ling538/UnicodeRanges.html"
       (archived)
       "https://web.archive.org/web/20200403204117/" + \
       "https://www.ling.upenn.edu/courses/Spring_2003/" + \
       "ling538/UnicodeRanges.html"
       (which is really just a nice way to get to specific pages also
        available via the official Unicode site, i.e.)
       "http://www.unicode.org/charts/PDF/"
         OR (with a different, thematically-and-alphabetically-sorted
         interface)
       "http://www.unicode.org/charts/"
       
Newest version on 2022-02-12
       
  A big usage example. Renaming a whole directory of files with
non-ASCII characters in the filename. This from `bash`, Cygwin
specifically.

bball@DESKTOP-64E7VFT /cygdrive/c/to_upload_tmp/non_ascii_in_ggiiff
$ find . -type f -print0 | 
  xargs -I'{}' -0 bash -c 'orig="{}"; 
    orig_fname_bare=$(echo "${orig}" | sed '"'"'s#^[.]/##g;'"'"' | 
      awk -F'"'"'.'"'"' '"'"'{NF--; print $0}'"'"'); 
    this_ext=$(echo "${orig}" | 
      awk -F'"'"'.'"'"' '"'"'{print $NF}'"'"');
    if ! [ "${this_ext}" = "pyc" -o "${this_ext}" = "py" -o \
           "${this_ext}" = "sh" -o "${this_ext}" = "out" ]; then 
     used_fname_bare=$(python3 -u rus_greek_etc_to_ascii.py \
       "${orig_fname_bare}" "True" "None"); 
     echo; echo "orig: ${orig}"; 
     echo "orig_fname_bare: ${orig_fname_bare}"; 
     echo "used_fname_bare: ${used_fname_bare}"; 
     echo "this_ext: ${this_ext}"; 
     echo " Moving ..."; 
     echo "mv \"${orig}\" \"${used_fname_bare}.${this_ext}\""; 
     mv "${orig}" "${used_fname_bare}.${this_ext}" && 
       echo -e "         ...\n          ... success" || 
       echo -e "         ...\n          ... FAILURE"; 
    fi;' | tee moving_non_ascii_$(date +'%s').out
       
'''
##############################################################################

import sys
import re
import unicodedata
import jamo

from bs4 import UnicodeDammit

dwb_fh_is_found = True ## Innocent until proven guilty
try:
  import dwb_fh_spec
except ImportError:
  dwb_fh_is_found = False
  pass
##endof:  try/except <import dwb_fh_spec>


def main(input_str, is_best=False, resolution=None):
  '''
  Easy command-line access to the glyph-to-ascii-pronunciation method
  '''
  
  return run(input_str, is_best, resolution)
  
##endof:  main(input_str)


def run(input_str, is_best=False, resolution=None):
  '''
  Easy-to-remember method name for the glyph-to-ascii-pronunciation method
  '''
  
  return dwb_to_ascii(input_str, is_best, resolution)
  
##endof:  run(input_str)

def dwb_to_ascii(input_str, is_best=False, resolution=None):
  '''
  Glyph (in various alphabetical scripts) to ascii repr of pronunciation
  '''
  
  ##  REMEMBER THAT IF ANY DEBUGGING IS GOING FOR THIS PYTHON SCRIPT,
  ##+ IT WILL CAUSE PROBLEMS FOR THE CALLING SCRIPT, WHICH JUST
  ##+ EXPECTS A NORMALIZED FILENAME!
  ##  P.S. Other debug is in the if-called-from-command-line at
  ##+ the end of this file.
  
  debug_process = False
  
  # # testing input string for another encoding.
  # try:
    # input_str.encode('utf-8')
  # except TypeError as te:
    # print("in the error", file=sys.stderr)
    # print(str(te), file=sys.stderr)
    # input_swear = UnicodeDammit.detwingle(input_str)
    # input_str = input_swear.decode("utf-8")
  # finally:
    # print("Fixed broken window pains, all in REAL utf-8 Unicode.",
          # file=sys.stderr)
    
  
  processing_str = input_str
  
  # Get rid of bad spaces
  processing_str = processing_str.translate(str.maketrans(' ', '_'))
  
  if debug_process:
    try:
      print("(a) input_str:      " + input_str)
    except UnicodeEncodeError as uee:
      print("UnicodeEncodeError", file=sys.stderr)
      print(str(uee), file=sys.stderr)
      input_swear = UnicodeDammit(input_str)
      orig_enc = input_swear.original_encoding
      print("original encoding: " + str(orig_enc), file=sys.stderr)
    finally:
      print("Hopefully, things are better.", file=sys.stderr)
    ##endof:  try/except/finally
    print("    processing_str: " + processing_str, file=sys.stderr)
    print("    is_best:        " + str(is_best), file=sys.stderr)
    print("    resolution:     " + str(resolution), file=sys.stderr)
  ##endof:  if debug_process
  
  # For youtube-dl
  qual_str = ''
  if is_best:
    qual_str = "bst"
  ##endof:  if is_best
  
  res_str = "res"
  if resolution is not None:
    res_str = str(resolution)
    res_str.replace('\r', '')
    res_str.replace('\n', '')
    if "720" in res_str or "1280" in res_str:
      res_str = "720"
    elif "1080" in res_str or "1920" in res_str:
      res_str = "1080"
    elif "2160" in res_str or "3840" in res_str:
      res_str = "4k"
    elif "480" in res_str and "852" in res_str:
      res_str = "480"
    elif "360" in res_str and "480" in res_str:
      res_str = "360"
    elif "480" in res_str:
      res_str = "480"
    elif "360" in res_str:
      res_str = "360"
    elif "240" in res_str or "352" in res_str:
      res_str = "240"
    elif "144" in res_str or "256" in res_str:
      res_str = "144"
    else:
      pass
    ##endof:  if/elif/else <res_str>
  ##endof:  if resolution is not None
  
  extra_info_str = qual_str + res_str + "mus"
  
  if debug_process:
     print("(a.5) extra_info_str: " + extra_info_str, file=sys.stderr)
  ##endof:  if debug_process
  
  is_new_sqr_brk_not_old_hyphen = True
  
  if is_new_sqr_brk_not_old_hyphen:
    processing_str = \
      re.sub(r"^(.*)[[]([A-Za-z0-9_-]{11})[]](_[^.])*([.])([a-z0-9]{3,5})$",
             r"\1_\2_" + extra_info_str + r"\4\5", 
             processing_str,
             flags=re.IGNORECASE)
  else:
    processing_str = \
      re.sub(r"^(.*)[-]([A-Za-z0-9_-]{11})(_[^.])*([.])([a-z0-9]{3,5})$",
             r"\1_\2_" + extra_info_str + r"\4\5", 
             processing_str,
             flags=re.IGNORECASE)
  ##endof:  if/else is_new_sqr_brk_not_old_hyphen
  
  if debug_process:
    print("(b) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  pre_yt_code_stuff = \
    re.sub(r"^(.*)([_][A-Za-z0-9_-]{11})([_][^.]+)([.])([a-z0-9]{3,5})$",
           r"\1", 
           processing_str,
           flags=re.IGNORECASE)
  
  pre_yt_code_stuff_pre = pre_yt_code_stuff
  
  yt_code_stuff_etc = \
    re.sub(r"^(.*)([_][A-Za-z0-9_-]{11})([_][^.]+)([.])([a-z0-9]{3,5})$",
           r"\2\3\4\5", 
           processing_str,
           flags=re.IGNORECASE)
  
  processing_str = pre_yt_code_stuff
  
  if debug_process:
    print("(c) processing_str" + processing_str, file=sys.stderr)
    print("    pre_yt_code_stuff: " + pre_yt_code_stuff, file=sys.stderr)
    print("    yt_code_stuff_etc: " + yt_code_stuff_etc, file=sys.stderr)
  ##endof:  if debug_process
  
  ## For the newline and carriage-return characters that keep getting in
  ## there. Adding some other possible control characters.
  processing_str = processing_str.replace('\r', '')
  processing_str = processing_str.replace('\n', '')
  processing_str = processing_str.replace('\t', '_')
  processing_str = processing_str.replace('\0', '')
  ## for other things found along the way.
  #processing_str = processing_str.replace('\r', '')
  #processing_str = processing_str.replace('\r', '')
  #processing_str = processing_str.replace('\r', '')
  #processing_str = processing_str.replace('\r', '')

  # Latin stuff
  processing_str = \
    processing_str.translate(str.maketrans(
      'ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöøùúûüýÿ', 
      'AAAAAACEEEEIIIIDNOOOOOxOUUUUYaaaaaaceeeeiiiinoooooouuuuyy'))
  
  processing_str = processing_str.replace('Æ', 'AE')
  processing_str = processing_str.replace('Þ', 'TH')
  processing_str = processing_str.replace('ß', 'ss')
  processing_str = processing_str.replace('æ', 'ae')
  processing_str = processing_str.replace('ð', 'th')
  processing_str = processing_str.replace('þ', 'th')
  
  ## More Latin, for later.
  #ĲĳŊŋŒœǀǁǂǃǄǅǆǇǈǉǊǋǌǢǣǼǽ
  #
  #
  
  # ƀƁƂƃƄƅƆƇƈƉƊƋƌƍƎƏƐƑƒƓƔƕƖƗƘƙƚƛƜƝƞƟƠơƢƣƤƥƦƧƨƩƪƫƬƭƮƯưƱƲƳƴƵƶƷƸƹƺƻƼƽƾƿ
  #
  
  #ǮǯǶǷ
  #
  
  # ɀɁɂɃɄɅɆɇɈɉɊɋɌɍɎɏ
  #
  
  # ȜȝȞȟȠȡȢȣȤȥ
  #
  
  # ȴȵȶȸȹ
  #
  
  processing_str = \
    processing_str.translate(str.maketrans(
      'ĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĴĵĶķĸĹĺĻļĽľĿŀ', 
      'AaAaAaCcCcCcCcDdDdEeEeEeEeEeGgGgGgGgHhHhIiIiIiIiIiJjKkkLlLlLlLl'))
  
  processing_str = \
    processing_str.translate(str.maketrans(
      'ŁłŃńŅņŇňŉŌōŎŏŐőŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſ',
      'LlNnNnNnnOoOoOoRrRrRrSsSsSsSsTtTtTtUuUuUuUuUuUuWwYyYZzZzZzs'))
  
  processing_str = \
    processing_str.translate(str.maketrans(
      'ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöøùúûüýÿ', 
      'AAAAAACEEEEIIIIDNOOOOOxOUUUUYaaaaaaceeeeiiiinoooooouuuuyy'))
  
  processing_str = \
    processing_str.translate(str.maketrans(
      'ǍǎǏǐǑǒǓǔǕǖǗǘǙǚǛǜǝǞǟǠǡǤǥǦǧǨǩǪǫǬǭ', 
      'AaIiOoUuUuUuUuUueAaAaGgGgKkOoOo'))
  
  processing_str = \
    processing_str.translate(str.maketrans(
      'ǸǹǺǻǾǿȀȁȂȃȄȅȆȇȈȉȊȋȌȍȎȏȐȑȒȓȔȕȖȗȘșȚț', 
      'NnAaOoAaAaEeEeIiIiOoOoRrRrUuUuSsTt'))
  
  processing_str = \
    processing_str.translate(str.maketrans(
      'ɃɄɆɇǰǴǵɈɉɊɋɌɍɎɏ', 
      'BUEejGgJjQqRrYy'))
  
  processing_str = \
    processing_str.translate(str.maketrans(
      'ȦȧȨȩȪȫȬȭȮȯȰȱȲȳȺȻȼȽȾȿ', 
      'AaEeOoOoOoOoYyACcLTs'))
  
  
  # ĲĳŊŋŒœǀǁǂǃǄǅǆǇǈǉǊǋǌǢǣǼǽ
  
  processing_str = processing_str.replace('Ĳ', 'IJ')
  processing_str = processing_str.replace('ĳ', 'ij')
  processing_str = processing_str.replace('Ŋ', 'NG')
  processing_str = processing_str.replace('ŋ', 'ng')
  processing_str = processing_str.replace('Œ', 'OE')
  processing_str = processing_str.replace('œ', 'oe')
  processing_str = processing_str.replace('Ǆ', 'DZ')
  processing_str = processing_str.replace('ǅ', 'Dz')
  processing_str = processing_str.replace('ǆ', 'dz')
  processing_str = processing_str.replace('Ǳ', 'DZ')
  processing_str = processing_str.replace('ǲ', 'Dz')
  processing_str = processing_str.replace('ǳ', 'dz')
  processing_str = processing_str.replace('Ǉ', 'LJ')
  processing_str = processing_str.replace('ǈ', 'Lj')
  processing_str = processing_str.replace('ǉ', 'lj')
  processing_str = processing_str.replace('ǋ', 'Nj')
  processing_str = processing_str.replace('ǌ', 'nj')
  processing_str = processing_str.replace('Ǣ', 'AE')
  processing_str = processing_str.replace('ǣ', 'ae')
  processing_str = processing_str.replace('Ǽ', 'AE')
  processing_str = processing_str.replace('ǽ', 'ae')
  
  if debug_process:
    print("(d) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  
  # Russian/Cyrillic
  # ЁёЖжХхЦцЧчШшЩщЪъЬьЮюЯя
  # 
  
  # # ЀЁЂЃЄЅІЇЈЉЊЋЌЍЎЏ
  
  
  # АБВГДЕЗИЙІКЛМНОПРСТУФЫЭабвгдезийіклмнопрстуфыэ
  # ABVGDEZIIIKLMNOPRSTUFYEabvgdeziiiklmnoprstufye
  
  # # ѐёђѓєѕіїјљњћќѝўџѠѡѢѣѤѥѦѧѨѩѪѫѬѭѮѯѰѱѲѳѴѵѶѷѸѹѺѻѼѽѾѿҀҁ
  # # ҂҃҄҅҆҇҈҉
  # # ҊҋҌҍҎҏҐґҒғҔҕҖҗҘҙҚқҜҝҞҟҠҡҢңҤҥҦҧҨҩҪҫҬҭҮүҰұҲҳҴҵҶҷҸҹҺһ
  # # ҼҽҾҿӀӁӂӃӄӅӆӇӈӉӊӋӌӍӎӏӐӑӒӓӔӕӖӗӘәӚӛӜӝӞӟӠӡӢӣӤӥӦӧӨөӪӫ
  # # ӬӭӮӯӰӱӲӳӴӵӶӷӸӹӺӻӼӽӾӿ
  
  processing_str = \
    processing_str.translate(str.maketrans(
      'АБВГДЕЗИЙІКЛМНОПРСТУФЫЭабвгдезийіклмнопрстуфыэ', 
      'ABVGDEZIIIKLMNOPRSTUFYEabvgdeziiiklmnoprstufye'))
  
  # ЁёЖжХхЦцЧчШшЩщЪъЬьЮюЯя
  
  processing_str = processing_str.replace('Ё', 'YO')
  processing_str = processing_str.replace('ё', 'yo')
  processing_str = processing_str.replace('Ж', 'ZH')
  processing_str = processing_str.replace('ж', 'zh')
  processing_str = processing_str.replace('Х', 'KH')
  processing_str = processing_str.replace('х', 'kh')
  processing_str = processing_str.replace('Ц', 'TS')
  processing_str = processing_str.replace('ц', 'ts')
  processing_str = processing_str.replace('Ч', 'CH')
  processing_str = processing_str.replace('ч', 'ch')
  processing_str = processing_str.replace('Ш', 'SH')
  processing_str = processing_str.replace('ш', 'sh')
  processing_str = processing_str.replace('Щ', 'SHCH')
  processing_str = processing_str.replace('щ', 'shch')
  processing_str = processing_str.replace('Ъ', '')
  processing_str = processing_str.replace('ъ', '')
  processing_str = processing_str.replace('Ь', '')
  processing_str = processing_str.replace('ь', '')
  processing_str = processing_str.replace('Ю', 'YU')
  processing_str = processing_str.replace('ю', 'yu')
  processing_str = processing_str.replace('Я', 'YA')
  processing_str = processing_str.replace('я', 'ya')
  
  if debug_process:
    print("(e) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  
  # Greek (and Coptic, according to the Unicode Block)
  #Including some accents, but not most letters I don't
  #recognize as Greek Alphabetical
  #
  #ΘθΦΧΨφχψϴ
  
  #'ΑΒΓΔΕΖΗΙΚΛΜΝΞΟΠΡΣΤΥΦΩ'
  #'AVGDEZEIKLMNXOPRSTUFO'
  
  #'αβγδεζηικλμνξοπρστυφω'
  #'avgdezeiklmnxoprstufo'
  
  #'ςΆΈΉΊΌΎΏΐΪΫάέήίΰϊϋόύώϐϑϒϓϔϕϖϱϲϳϵ϶'
  #'sAENIOUOiIUaeeiuiuouovdUUUforcjee'
  
  processing_str = \
    processing_str.translate(str.maketrans(
      'ΑΒΓΔΕΖΗΙΚΛΜΝΞΟΠΡΣΤΥΦΩαβγδεζηικλμνξοπρστυφω', 
      'AVGDEZEIKLMNXOPRSTUFOavgdezeiklmnxoprstufo'))
  
  processing_str = \
    processing_str.translate(str.maketrans(
      'ςΆΈΉΊΌΎΏΐΪΫάέήίΰϊϋόύώϐϒϓϔϕϖϱϲϳϵ϶', 
      'sAENIOUOiIUaeeiuiuouovUUUforcjee'))
  
  #ΘθΧχΨψϑϴ
  
  processing_str = processing_str.replace('Θ', 'TH')
  processing_str = processing_str.replace('θ', 'th')
  processing_str = processing_str.replace('Φ', 'F')
  processing_str = processing_str.replace('φ', 'f')
  processing_str = processing_str.replace('Χ', 'KH')
  processing_str = processing_str.replace('χ', 'kh')
  processing_str = processing_str.replace('Ψ', 'PS')
  processing_str = processing_str.replace('ψ', 'ps')
  processing_str = processing_str.replace('ϑ', 'th')
  processing_str = processing_str.replace('ϴ', 'th')
  
  
  if debug_process:
    print("(f) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  
  # # Armenian
  # #
  # #
  
  # #ԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖ
  # #
  
  # #աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆև
  # #
  
  # processing_str=$(echo "${processing_str}" | \
  # )
  
  # #
  
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  
  if debug_process:
    print("(g) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  
  # Hebrew
  #
  #* שיעורי ריקודי בטן * הופעות * חפלות * סדנאות *
                                             
  
  processing_str = processing_str.replace('־', '')
  processing_str = processing_str.replace('׀', '')
  processing_str = processing_str.replace('׆', '')
  processing_str = processing_str.replace('א', 'a')
  processing_str = processing_str.replace('ב', 'b')
  processing_str = processing_str.replace('ג', 'g')
  processing_str = processing_str.replace('ד', 'd')
  processing_str = processing_str.replace('ה', 'h')
  processing_str = processing_str.replace('ו', 'v')
  processing_str = processing_str.replace('ז', 'z')
  processing_str = processing_str.replace('ח', 'x')
  processing_str = processing_str.replace('ט', 't')
  processing_str = processing_str.replace('י', 'j')
  processing_str = processing_str.replace('ך', 'k')
  processing_str = processing_str.replace('כ', 'k')
  processing_str = processing_str.replace('ל', 'l')
  processing_str = processing_str.replace('ם', 'm')
  processing_str = processing_str.replace('מ', 'm')
  processing_str = processing_str.replace('ן', 'n')
  processing_str = processing_str.replace('נ', 'n')
  processing_str = processing_str.replace('ס', 's')
  processing_str = processing_str.replace('ע', 'a')
  processing_str = processing_str.replace('ף', 'p')
  processing_str = processing_str.replace('פ', 'p')
  processing_str = processing_str.replace('ץ', 'ts')
  processing_str = processing_str.replace('צ', 'ts')
  processing_str = processing_str.replace('ק', 'k')
  processing_str = processing_str.replace('ר', 'r')
  processing_str = processing_str.replace('ש', 's')
  processing_str = processing_str.replace('ת', 't')
  processing_str = processing_str.replace('װ', '')
  processing_str = processing_str.replace('ױ', '')
  processing_str = processing_str.replace('ײ', '')
  processing_str = processing_str.replace('׳', '')
  processing_str = processing_str.replace('״', '')
  
  #echo "לעבודה אבא הלך" | 
  
  if debug_process:
    print("(h) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  
  # Arabic
  # Ignoring vowel markings (or what I think are vowel markings) for now.
  # http://www.arabic-keyboard.org/arabic/arabic-alphabet.php
  # https://www.lexilogos.com/keyboard/arabic.htm
  # https://www.omniglot.com/writing/arabic.htm # come back to
  
  processing_str = processing_str.replace('،', '')
  processing_str = processing_str.replace('؍', '')
  processing_str = processing_str.replace('؎', '')
  processing_str = processing_str.replace('؏', '')
  processing_str = processing_str.replace('؛', '')
  processing_str = processing_str.replace('؞', '')
  processing_str = processing_str.replace('؟', '')
  processing_str = processing_str.replace('ء', '') #hamza
  processing_str = processing_str.replace('آ', 'a')
  processing_str = processing_str.replace('أ', 'a')
  processing_str = processing_str.replace('ؤ', 'w')
  processing_str = processing_str.replace('إ', 'a')
  processing_str = processing_str.replace('ئ', 'y')
  processing_str = processing_str.replace('ا', 'a')
  processing_str = processing_str.replace('ب', 'b')
  processing_str = processing_str.replace('ة', 'h')
  processing_str = processing_str.replace('ت', 't')
  processing_str = processing_str.replace('ث', 'th')
  processing_str = processing_str.replace('ج', 'j')
  processing_str = processing_str.replace('ح', 'h')
  processing_str = processing_str.replace('خ', 'kh')
  processing_str = processing_str.replace('د', 'd')
  processing_str = processing_str.replace('ذ', 'th')
  processing_str = processing_str.replace('ر', 'r')
  processing_str = processing_str.replace('ز', 'z')
  processing_str = processing_str.replace('س', 's')
  processing_str = processing_str.replace('ش', 'sh')
  processing_str = processing_str.replace('ص', 's')
  processing_str = processing_str.replace('ض', 'd')
  processing_str = processing_str.replace('ط', 't')
  processing_str = processing_str.replace('ظ', 'z')
  processing_str = processing_str.replace('ع', '3')
  processing_str = processing_str.replace('غ', 'gh')
  processing_str = processing_str.replace('ـ', '')
  processing_str = processing_str.replace('ف', 'f')
  processing_str = processing_str.replace('ق', 'q')
  processing_str = processing_str.replace('ك', 'k')
  processing_str = processing_str.replace('ل', 'l')
  processing_str = processing_str.replace('م', 'm')
  processing_str = processing_str.replace('ن', 'n')
  processing_str = processing_str.replace('ه', 'h')
  processing_str = processing_str.replace('و', 'w')
  processing_str = processing_str.replace('ى', 'y')
  processing_str = processing_str.replace('ي', 'y')
  processing_str = processing_str.replace('٠', '0')
  processing_str = processing_str.replace('١', '1')
  processing_str = processing_str.replace('٢', '2')
  processing_str = processing_str.replace('٣', '3')
  processing_str = processing_str.replace('٤', '4')
  processing_str = processing_str.replace('٥', '5')
  processing_str = processing_str.replace('٦', '6')
  processing_str = processing_str.replace('٧', '7')
  processing_str = processing_str.replace('٨', '8')
  processing_str = processing_str.replace('٩', '9')
  processing_str = processing_str.replace('٪', '')
  processing_str = processing_str.replace('٫', '')
  processing_str = processing_str.replace('٬', '')
  processing_str = processing_str.replace('٭', '')
  processing_str = processing_str.replace('ٮ', 'b')
  processing_str = processing_str.replace('ٯ', 'q')
  processing_str = processing_str.replace('ٱ', 'a')
  processing_str = processing_str.replace('ٲ', 'a')
  processing_str = processing_str.replace('ٳ', 'a')
  processing_str = processing_str.replace('ٵ', 'a')
  processing_str = processing_str.replace('ٶ', 'w')
  processing_str = processing_str.replace('ٷ', 'w')
  processing_str = processing_str.replace('ٸ', 'y')
  processing_str = processing_str.replace('ٹ', 'tt')
  processing_str = processing_str.replace('ٺ', 't')
  processing_str = processing_str.replace('ٻ', 'b')
  processing_str = processing_str.replace('ټ', 't')
  processing_str = processing_str.replace('ٽ', 't')
  processing_str = processing_str.replace('پ', 'p')
  processing_str = processing_str.replace('ٿ', 't')
  processing_str = processing_str.replace('ڀ', 'b')
  processing_str = processing_str.replace('ځ', 'h')
  processing_str = processing_str.replace('ڂ', 'h')
  processing_str = processing_str.replace('ڃ', 'ny')
  processing_str = processing_str.replace('ڄ', 'dy')
  processing_str = processing_str.replace('څ', 'h')
  processing_str = processing_str.replace('چ', 'ch')
  processing_str = processing_str.replace('ڇ', 'cj')
  processing_str = processing_str.replace('ڈ', 'dd')
  processing_str = processing_str.replace('ډ', 'd')
  processing_str = processing_str.replace('ڊ', 'd')
  processing_str = processing_str.replace('ڋ', 'd')
  processing_str = processing_str.replace('ڌ', 'd')
  processing_str = processing_str.replace('ڍ', 'dd')
  processing_str = processing_str.replace('ڎ', 'd')
  processing_str = processing_str.replace('ڏ', 'd')
  processing_str = processing_str.replace('ڐ', 'd')
  processing_str = processing_str.replace('ڑ', 'rr')
  processing_str = processing_str.replace('ڒ', 'r')
  processing_str = processing_str.replace('ړ', 'r')
  processing_str = processing_str.replace('ڔ', 'r')
  processing_str = processing_str.replace('ڕ', 'r')
  processing_str = processing_str.replace('ږ', 'r')
  processing_str = processing_str.replace('ڗ', 'r')
  processing_str = processing_str.replace('ژ', 'j')
  processing_str = processing_str.replace('ڙ', 'r')
  processing_str = processing_str.replace('ښ', 's')
  processing_str = processing_str.replace('ڛ', 's')
  processing_str = processing_str.replace('ڜ', 's')
  processing_str = processing_str.replace('ڝ', 's')
  processing_str = processing_str.replace('ڞ', 's')
  processing_str = processing_str.replace('ڟ', 't')
  processing_str = processing_str.replace('ڠ', '')
  processing_str = processing_str.replace('ڡ', 'f')
  processing_str = processing_str.replace('ڢ', 'v')
  processing_str = processing_str.replace('ڣ', 'f')
  processing_str = processing_str.replace('ڤ', 'v')
  processing_str = processing_str.replace('ڥ', 'f')
  processing_str = processing_str.replace('ڦ', 'p')
  processing_str = processing_str.replace('ڧ', 'q')
  processing_str = processing_str.replace('ڨ', 'g')
  processing_str = processing_str.replace('ک', 'k')
  processing_str = processing_str.replace('ڪ', 'k')
  processing_str = processing_str.replace('ګ', 'k')
  processing_str = processing_str.replace('ڬ', 'k')
  processing_str = processing_str.replace('ڭ', 'ng')
  processing_str = processing_str.replace('ڮ', 'k')
  processing_str = processing_str.replace('گ', 'g')
  processing_str = processing_str.replace('ڰ', 'g')
  processing_str = processing_str.replace('ڱ', 'ng')
  processing_str = processing_str.replace('ڲ', 'g')
  processing_str = processing_str.replace('ڳ', 'g')
  processing_str = processing_str.replace('ڴ', 'g')
  processing_str = processing_str.replace('ڵ', 'l')
  processing_str = processing_str.replace('ڶ', 'l')
  processing_str = processing_str.replace('ڷ', 'l')
  processing_str = processing_str.replace('ڸ', 'l')
  processing_str = processing_str.replace('ڹ', 'n')
  processing_str = processing_str.replace('ں', 'n')
  processing_str = processing_str.replace('ڻ', 'rn')
  processing_str = processing_str.replace('ڼ', 'n')
  processing_str = processing_str.replace('ڽ', 'n')
  processing_str = processing_str.replace('ھ', 'h')
  processing_str = processing_str.replace('ڿ', 'ch')
  processing_str = processing_str.replace('ۀ', 'h')
  processing_str = processing_str.replace('ہ', 'h')
  processing_str = processing_str.replace('ۂ', 'h')
  processing_str = processing_str.replace('ۃ', 'h')
  processing_str = processing_str.replace('ۄ', 'w')
  processing_str = processing_str.replace('ۅ', 'oe')
  processing_str = processing_str.replace('ۆ', 'oe')
  processing_str = processing_str.replace('ۇ', 'u')
  processing_str = processing_str.replace('ۈ', 'yu')
  processing_str = processing_str.replace('ۉ', 'yu')
  processing_str = processing_str.replace('ۊ', 'w')
  processing_str = processing_str.replace('ۋ', 'v')
  processing_str = processing_str.replace('ی', 'y')
  processing_str = processing_str.replace('ۍ', 'y')
  processing_str = processing_str.replace('ێ', 'y')
  processing_str = processing_str.replace('ۏ', 'w')
  processing_str = processing_str.replace('ې', 'e')
  processing_str = processing_str.replace('ۑ', 'y')
  processing_str = processing_str.replace('ے', 'y')
  processing_str = processing_str.replace('ۓ', 'y')
  processing_str = processing_str.replace('۔', '')
  processing_str = processing_str.replace('ە', 'ae')
  # processing_str=$(echo "${processing_str}" | sed 's#۝##g')
  # processing_str=$(echo "${processing_str}" | sed 's#۞##g')
  # processing_str=$(echo "${processing_str}" | sed 's#۩##g')
  processing_str = processing_str.replace('ۮ', 'd')
  processing_str = processing_str.replace('ۯ', 'r')
  processing_str = processing_str.replace('۰', '0')
  processing_str = processing_str.replace('۱', '1')
  processing_str = processing_str.replace('۲', '2')
  processing_str = processing_str.replace('۳', '3')
  processing_str = processing_str.replace('۴', '4')
  processing_str = processing_str.replace('۵', '5')
  processing_str = processing_str.replace('۶', '6')
  processing_str = processing_str.replace('۷', '7')
  processing_str = processing_str.replace('۸', '8')
  processing_str = processing_str.replace('۹', '9')
  processing_str = processing_str.replace('ۺ', 'sh')
  processing_str = processing_str.replace('ۻ', 'd')
  processing_str = processing_str.replace('ۼ', 'gh')
  processing_str = processing_str.replace('۽', '_and_')
  processing_str = processing_str.replace('۾', 'm')
  processing_str = processing_str.replace('ۿ', 'h')
  
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  
  if debug_process:
    print("(i) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  
  # Georgian
  
  # processing_str=$(echo "${processing_str}" | \
  # )
  
  #
  
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  
  if debug_process:
    print("(j) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  if dwb_fh_is_found:
    processing_str = dwb_fh_spec.run(processing_str)
  ##endof:  if dwb_fh_is_found
  
  if debug_process:
    print("(k) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  
  # Hangul Jamo
  # Note, no initial vs. final stuff, yet
  #
  
  #"https://codegolf.stackexchange.com/a/155874/61627"
  #      for some better pronunciation rules.
  # Nope, not working. I think it would have to be only hangul by itself.
  #
  
  # get everything in compatibility range (U+31xx), then get separate jamo
  # (character -> jamo)
  processing_str = jamo.j2hcj(jamo.h2j(processing_str))
  
  processing_str = \
    processing_str.translate(str.maketrans(
      'ㄱㄴㄷㄹㅁㅂㅅㅈㅌㅍㅎㅿㆆㅏㅔㅗㅜㅣ', 
      'gndrmbsjtphzjaeoui'))
  

  processing_str = processing_str.replace('ㅇ', '') #ng #modernalph
  processing_str = processing_str.replace('ㅊ', 'ch') #modernalph
  processing_str = processing_str.replace('ㅋ', 'kh') # also see 'k' for both 
                                                     #modernalph
  processing_str = processing_str.replace('ㆁ', 'ng') #modernalph
  
  processing_str = processing_str.replace('ㅐ', 'ae') #modernalph
  processing_str = processing_str.replace('ㅑ', 'ya') #modernalph
  processing_str = processing_str.replace('ㅒ', 'yae') #modernalph
  processing_str = processing_str.replace('ㅓ', 'eo') #modernalph
  processing_str = processing_str.replace('ㅕ', 'yeo') #modernalph
  processing_str = processing_str.replace('ㅖ', 'ye') #modernalph
  processing_str = processing_str.replace('ㅛ', 'yo') #modernalph
  processing_str = processing_str.replace('ㅠ', 'yu') #modernalph
  processing_str = processing_str.replace('ㅡ', 'eu') #modernalph
  
  processing_str = processing_str.replace('ㄲ', 'kk') #k #modernalph
  processing_str = processing_str.replace('ㄳ', 'gs')
  processing_str = processing_str.replace('ㄵ', 'nj')
  processing_str = processing_str.replace('ㄶ', 'nh')
  processing_str = processing_str.replace('ㄸ', 'tt') #<no-final> #modernalph
  processing_str = processing_str.replace('ㄺ', 'rg')
  processing_str = processing_str.replace('ㄻ', 'rm')
  processing_str = processing_str.replace('ㄼ', 'rb')
  processing_str = processing_str.replace('ㄽ', 'rs')
  processing_str = processing_str.replace('ㄾ', 'rt')
  processing_str = processing_str.replace('ㄿ', 'rp')
  processing_str = processing_str.replace('ㅀ', 'rh')
  processing_str = processing_str.replace('ㅃ', 'pp') #<no-final> #modernalph
  processing_str = processing_str.replace('ㅄ', 'bs')
  processing_str = processing_str.replace('ㅆ', 'ss') #t #modernalph
  processing_str = processing_str.replace('ㅉ', 'jj') #<no-final> #modernalph
  
  processing_str = processing_str.replace('ㅘ', 'wa') #modernalph
  processing_str = processing_str.replace('ㅙ', 'wae') #modernalph
  processing_str = processing_str.replace('ㅚ', 'oe') #modernalph
  processing_str = processing_str.replace('ㅝ', 'wo') #modernalph
  processing_str = processing_str.replace('ㅞ', 'we') #modernalph
  processing_str = processing_str.replace('ㅟ', 'wi') #modernalph
  processing_str = processing_str.replace('ㅢ', 'ui') #modernalph
  
  processing_str = processing_str.replace('ㅥ', 'nn')
  processing_str = processing_str.replace('ㅦ', 'nt')
  processing_str = processing_str.replace('ㅧ', 'nt')
  processing_str = processing_str.replace('ㅨ', 'nz')
  processing_str = processing_str.replace('ㅩ', 'rgt')
  processing_str = processing_str.replace('ㅪ', 'rt')
  processing_str = processing_str.replace('ㅫ', 'rbt')
  processing_str = processing_str.replace('ㅬ', 'rz')
  processing_str = processing_str.replace('ㅭ', 'rj')
  processing_str = processing_str.replace('ㅮ', 'mp')
  processing_str = processing_str.replace('ㅯ', 'mt')
  processing_str = processing_str.replace('ㅰ', 'mz')
  processing_str = processing_str.replace('ㅱ', 'mw') #found
  processing_str = processing_str.replace('ㅲ', 'bg')
  processing_str = processing_str.replace('ㅳ', 'bt')
  processing_str = processing_str.replace('ㅴ', 'bsk')
  processing_str = processing_str.replace('ㅵ', 'bst')
  processing_str = processing_str.replace('ㅶ', 'bt')
  processing_str = processing_str.replace('ㅷ', 'bt')
  processing_str = processing_str.replace('ㅸ', 'bw') #found
  processing_str = processing_str.replace('ㅹ', 'bbw')
  processing_str = processing_str.replace('ㅺ', 'sk')
  processing_str = processing_str.replace('ㅻ', 'sn')
  processing_str = processing_str.replace('ㅼ', 'st')
  processing_str = processing_str.replace('ㅽ', 'sp')
  processing_str = processing_str.replace('ㅾ', 'st')
  processing_str = processing_str.replace('ㆀ', 'ngng')
  processing_str = processing_str.replace('ㆂ', 'ngt')
  processing_str = processing_str.replace('ㆃ', 'ngz')
  processing_str = processing_str.replace('ㆄ', 'f') #found
  processing_str = processing_str.replace('ㆅ', 'hh')
  
  processing_str = processing_str.replace('ㆇ', 'yoya')
  processing_str = processing_str.replace('ㆈ', 'yoyae')
  processing_str = processing_str.replace('ㆉ', 'yoi')
  processing_str = processing_str.replace('ㆊ', 'yuyeo')
  processing_str = processing_str.replace('ㆋ', 'yuye')
  processing_str = processing_str.replace('ㆌ', 'yui')
  
  processing_str = processing_str.replace('ㆍ', '') #?
  processing_str = processing_str.replace('ㆎ', '') #?
  
  #------------------------------------------
  #In case, do other range for jamo, U+11xx
  #For not "modernalph", `#fib` is for 
  #  "found in both"
  processing_str = processing_str.replace('ᄀ', 'g') #1charBoth #k #modernalph
  processing_str = processing_str.replace('ᄁ', 'kk') #k #modernalph
  processing_str = processing_str.replace('ᄂ', 'n') #1charBoth #modernalph
  processing_str = processing_str.replace('ᄃ', 'd') #1charBoth #t #modernalph
  processing_str = processing_str.replace('ᄄ', 'tt') #<no-final> #modernalph
  processing_str = processing_str.replace('ᄅ', 'r') #1charBoth #l #modernalph
  processing_str = processing_str.replace('ᄆ', 'm') #1charBoth #modernalph
  processing_str = processing_str.replace('ᄇ', 'b') #1charBoth #p #modernalph
  processing_str = processing_str.replace('ᄈ', 'pp') #<no-final> #modernalph
  processing_str = processing_str.replace('ᄉ', 's') #1charBoth #t #modernalph
  processing_str = processing_str.replace('ᄊ', 'ss') #t #modernalph
  processing_str = processing_str.replace('ᄋ', '') #ng #modernalph
  processing_str = processing_str.replace('ᄌ', 'j') #1charBoth #t #modernalph
  processing_str = processing_str.replace('ᄍ', 'jj') #<no-final> #modernalph
  processing_str = processing_str.replace('ᄎ', 'ch') #modernalph
  processing_str = processing_str.replace('ᄏ', 'kh') #some use k, init&final 
                                                     #modernalph
  processing_str = processing_str.replace('ᄐ', 't') #1charBoth #modernalph
  processing_str = processing_str.replace('ᄑ', 'p') #1charBoth #modernalph
  processing_str = processing_str.replace('ᄒ', 'h') #1charBoth #modernalph
  processing_str = processing_str.replace('ᄓ', 'nk')
  processing_str = processing_str.replace('ᄔ', 'nn') #fib
  processing_str = processing_str.replace('ᄕ', 'nt') #fib
  processing_str = processing_str.replace('ᄖ', 'np')
  processing_str = processing_str.replace('ᄗ', 'dk')
  processing_str = processing_str.replace('ᄘ', 'rn')
  processing_str = processing_str.replace('ᄙ', 'rl')
  processing_str = processing_str.replace('ᄚ', 'rh')
  processing_str = processing_str.replace('ᄛ', 'rng')
  processing_str = processing_str.replace('ᄜ', 'mp') #fib2
  processing_str = processing_str.replace('ᄝ', 'mw') #found #fib2
  processing_str = processing_str.replace('ᄞ', 'bg') #fib
  processing_str = processing_str.replace('ᄟ', 'bn')
  processing_str = processing_str.replace('ᄠ', 'bt') #fib
  processing_str = processing_str.replace('ᄡ', 'bt')
  processing_str = processing_str.replace('ᄢ', 'bsk') #fib
  processing_str = processing_str.replace('ᄣ', 'bst') #fib
  processing_str = processing_str.replace('ᄤ', 'bsp')
  processing_str = processing_str.replace('ᄥ', 'bst')
  processing_str = processing_str.replace('ᄦ', 'bst')
  processing_str = processing_str.replace('ᄧ', 'bt')
  processing_str = processing_str.replace('ᄨ', 'bch')
  processing_str = processing_str.replace('ᄩ', 'bt') #fib
  processing_str = processing_str.replace('ᄪ', 'bp')
  processing_str = processing_str.replace('ᄫ', 'bw') #found #fib2
  processing_str = processing_str.replace('ᄬ', 'bbw') #fib
  processing_str = processing_str.replace('ᄭ', 'sk') #fib2
  processing_str = processing_str.replace('ᄮ', 'sn') #fib
  processing_str = processing_str.replace('ᄯ', 'st') #fib
  processing_str = processing_str.replace('ᄰ', 'sl')
  processing_str = processing_str.replace('ᄱ', 'sm')
  processing_str = processing_str.replace('ᄲ', 'sp') #fib
  processing_str = processing_str.replace('ᄳ', 'sbk')
  processing_str = processing_str.replace('ᄴ', 'sst')
  processing_str = processing_str.replace('ᄵ', 'sng')
  processing_str = processing_str.replace('ᄶ', 'st') #fib
  processing_str = processing_str.replace('ᄷ', 'sch')
  processing_str = processing_str.replace('ᄸ', 'skh')
  processing_str = processing_str.replace('ᄹ', 'st')
  processing_str = processing_str.replace('ᄺ', 'sp')
  processing_str = processing_str.replace('ᄻ', 'sh')
  processing_str = processing_str.replace('ᄼ', '') #?
  processing_str = processing_str.replace('ᄽ', '') #?
  processing_str = processing_str.replace('ᄾ', '') #?
  processing_str = processing_str.replace('ᄿ', '') #?
  processing_str = processing_str.replace('ᅀ', 'z') #1charBoth #modernalph
  processing_str = processing_str.replace('ᅁ', 'k') #?
  processing_str = processing_str.replace('ᅂ', 't') #?
  processing_str = processing_str.replace('ᅃ', 'm') #?
  processing_str = processing_str.replace('ᅄ', 'p') #?
  processing_str = processing_str.replace('ᅅ', 't') #?
  processing_str = processing_str.replace('ᅆ', 'z') #?
  processing_str = processing_str.replace('ᅇ', 'ng') #?
  processing_str = processing_str.replace('ᅈ', 't') #?
  processing_str = processing_str.replace('ᅉ', 'ch') #?
  processing_str = processing_str.replace('ᅊ', 't') #?
  processing_str = processing_str.replace('ᅋ', 'p') #?
  processing_str = processing_str.replace('ᅌ', 'ng') #modernalph
  processing_str = processing_str.replace('ᅍ', 'jng')
  processing_str = processing_str.replace('ᅎ', '') #?
  processing_str = processing_str.replace('ᅏ', '') #?
  processing_str = processing_str.replace('ᅐ', '') #?
  processing_str = processing_str.replace('ᅑ', '') #?
  processing_str = processing_str.replace('ᅒ', 'chkh')
  processing_str = processing_str.replace('ᅓ', 'chh')
  processing_str = processing_str.replace('ᅔ', '') #?
  processing_str = processing_str.replace('ᅕ', '') #?
  processing_str = processing_str.replace('ᅖ', 'pp')
  processing_str = processing_str.replace('ᅗ', 'f') #found #fib2
  processing_str = processing_str.replace('ᅘ', 'hh') #fib
  processing_str = processing_str.replace('ᅙ', 'j') #1charBoth
  processing_str = processing_str.replace('ᅡ', 'a') #1charBoth #modernalph
  processing_str = processing_str.replace('ᅢ', 'ae') #modernalph
  processing_str = processing_str.replace('ᅣ', 'ya') #modernalph
  processing_str = processing_str.replace('ᅤ', 'yae') #modernalph
  processing_str = processing_str.replace('ᅥ', 'eo') #modernalph
  processing_str = processing_str.replace('ᅦ', 'e') #1charBoth #modernalph
  processing_str = processing_str.replace('ᅧ', 'yeo') #modernalph
  processing_str = processing_str.replace('ᅨ', 'ye') #modernalph
  processing_str = processing_str.replace('ᅩ', 'o') #1charBoth #modernalph
  processing_str = processing_str.replace('ᅪ', 'wa') #modernalph
  processing_str = processing_str.replace('ᅫ', 'wae') #modernalph
  processing_str = processing_str.replace('ᅬ', 'oe') #modernalph
  processing_str = processing_str.replace('ᅭ', 'yo') #modernalph
  processing_str = processing_str.replace('ᅮ', 'u') #1charBoth #modernalph
  processing_str = processing_str.replace('ᅯ', 'wo') #modernalph
  processing_str = processing_str.replace('ᅰ', 'we') #modernalph
  processing_str = processing_str.replace('ᅱ', 'wi') #modernalph
  processing_str = processing_str.replace('ᅲ', 'yu') #modernalph
  processing_str = processing_str.replace('ᅳ', 'eu') #modernalph
  processing_str = processing_str.replace('ᅴ', 'ui') #modernalph
  processing_str = processing_str.replace('ᅵ', 'i') #1charBoth #modernalph
  processing_str = processing_str.replace('ᅶ', '')
  processing_str = processing_str.replace('ᅷ', '')
  processing_str = processing_str.replace('ᅸ', '')
  processing_str = processing_str.replace('ᅹ', '')
  processing_str = processing_str.replace('ᅺ', '')
  processing_str = processing_str.replace('ᅻ', '')
  processing_str = processing_str.replace('ᅼ', '')
  processing_str = processing_str.replace('ᅽ', '')
  processing_str = processing_str.replace('ᅾ', '')
  processing_str = processing_str.replace('ᅿ', '')
  processing_str = processing_str.replace('ᆀ', '')
  processing_str = processing_str.replace('ᆁ', '')
  processing_str = processing_str.replace('ᆂ', '')
  processing_str = processing_str.replace('ᆃ', '')
  processing_str = processing_str.replace('ᆄ', '')
  processing_str = processing_str.replace('ᆅ', '')
  processing_str = processing_str.replace('ᆆ', '')
  processing_str = processing_str.replace('ᆇ', '')
  processing_str = processing_str.replace('ᆈ', '')
  processing_str = processing_str.replace('ᆉ', '')
  processing_str = processing_str.replace('ᆊ', '')
  processing_str = processing_str.replace('ᆋ', '')
  processing_str = processing_str.replace('ᆌ', '')
  processing_str = processing_str.replace('ᆍ', '')
  processing_str = processing_str.replace('ᆎ', '')
  processing_str = processing_str.replace('ᆏ', '')
  processing_str = processing_str.replace('ᆐ', '')
  processing_str = processing_str.replace('ᆑ', '')
  processing_str = processing_str.replace('ᆒ', '')
  processing_str = processing_str.replace('ᆓ', '')
  processing_str = processing_str.replace('ᆔ', '')
  processing_str = processing_str.replace('ᆕ', '')
  processing_str = processing_str.replace('ᆖ', '')
  processing_str = processing_str.replace('ᆗ', '')
  processing_str = processing_str.replace('ᆘ', '')
  processing_str = processing_str.replace('ᆙ', '')
  processing_str = processing_str.replace('ᆚ', '')
  processing_str = processing_str.replace('ᆛ', '')
  processing_str = processing_str.replace('ᆜ', '')
  processing_str = processing_str.replace('ᆝ', '') #?
  processing_str = processing_str.replace('ᆞ', '') #?
  processing_str = processing_str.replace('ᆟ', '') #?
  processing_str = processing_str.replace('ᆠ', '') #?
  processing_str = processing_str.replace('ᆡ', '') #?
  processing_str = processing_str.replace('ᆢ', '') #?
  processing_str = processing_str.replace('ᆨ', 'g') #1charBoth #k #modernalph
  processing_str = processing_str.replace('ᆩ', 'kk') #k #modernalph
  processing_str = processing_str.replace('ᆪ', 'gs') #modernalph #fib
  processing_str = processing_str.replace('ᆫ', 'n') #1charBoth #modernalph
  processing_str = processing_str.replace('ᆬ', 'nj') #fib
  processing_str = processing_str.replace('ᆭ', 'nh') #fib
  processing_str = processing_str.replace('ᆮ', 'd') #1charBoth #t #modernalph
  processing_str = processing_str.replace('ᆯ', 'r') #1charBoth #l #modernalph
  processing_str = processing_str.replace('ᆰ', 'rg') #fib
  processing_str = processing_str.replace('ᆱ', 'rm') #fib
  processing_str = processing_str.replace('ᆲ', 'rb') #fib
  processing_str = processing_str.replace('ᆳ', 'rs') #fib
  processing_str = processing_str.replace('ᆴ', 'rt') #fib
  processing_str = processing_str.replace('ᆵ', 'rp') #fib
  processing_str = processing_str.replace('ᆶ', 'rh') #fib
  processing_str = processing_str.replace('ᆷ', 'm') #1charBoth #modernalph
  processing_str = processing_str.replace('ᆸ', 'b') #1charBoth #p #modernalph
  processing_str = processing_str.replace('ᆹ', 'bs') #fib
  processing_str = processing_str.replace('ᆺ', 's') #1charBoth #t #modernalph
  processing_str = processing_str.replace('ᆻ', 'ss') #t #modernalph
  processing_str = processing_str.replace('ᆼ', '') #ng #modernalph
  processing_str = processing_str.replace('ᆽ', 'j') #1charBoth #t #modernalph
  processing_str = processing_str.replace('ᆾ', 'ch') #modernalph
  processing_str = processing_str.replace('ᆿ', 'kh') #modernalph
  processing_str = processing_str.replace('ᇀ', 't') #1charBoth #modernalph
  processing_str = processing_str.replace('ᇁ', 'p') #1charBoth #modernalph
  processing_str = processing_str.replace('ᇂ', 'h') #1charBoth #modernalph
  processing_str = processing_str.replace('ᇃ', 'gl')
  processing_str = processing_str.replace('ᇄ', 'gsk')
  processing_str = processing_str.replace('ᇅ', 'nk')
  processing_str = processing_str.replace('ᇆ', 'nt') #fib2
  processing_str = processing_str.replace('ᇇ', 'nt') #fib
  processing_str = processing_str.replace('ᇈ', 'nz') #fib
  processing_str = processing_str.replace('ᇉ', 'nt')
  processing_str = processing_str.replace('ᇊ', 'dk')
  processing_str = processing_str.replace('ᇋ', 'dl')
  processing_str = processing_str.replace('ᇌ', 'rgt') #fib
  processing_str = processing_str.replace('ᇍ', 'rn')
  processing_str = processing_str.replace('ᇎ', 'rt') #fib
  processing_str = processing_str.replace('ᇏ', 'rdh')
  processing_str = processing_str.replace('ᇐ', 'rl')
  processing_str = processing_str.replace('ᇑ', 'rmk')
  processing_str = processing_str.replace('ᇒ', 'rmt')
  processing_str = processing_str.replace('ᇓ', 'rbt') #fib
  processing_str = processing_str.replace('ᇔ', 'rbh')
  processing_str = processing_str.replace('ᇕ', 'rbng')
  processing_str = processing_str.replace('ᇖ', 'rst')
  processing_str = processing_str.replace('ᇗ', 'rz') #fib
  processing_str = processing_str.replace('ᇘ', 'rkh')
  processing_str = processing_str.replace('ᇙ', 'rj') #fib
  processing_str = processing_str.replace('ᇚ', 'mk')
  processing_str = processing_str.replace('ᇛ', 'ml')
  processing_str = processing_str.replace('ᇜ', 'mp') #fib
  processing_str = processing_str.replace('ᇝ', 'mt') #fib
  processing_str = processing_str.replace('ᇞ', 'mst')
  processing_str = processing_str.replace('ᇟ', 'mz') #fib
  processing_str = processing_str.replace('ᇠ', 'mch')
  processing_str = processing_str.replace('ᇡ', 'mh')
  processing_str = processing_str.replace('ᇢ', 'mw') #found #fib
  processing_str = processing_str.replace('ᇣ', 'bl')
  processing_str = processing_str.replace('ᇤ', 'bp')
  processing_str = processing_str.replace('ᇥ', 'bh')
  processing_str = processing_str.replace('ᇦ', 'bw') #found #fib
  processing_str = processing_str.replace('ᇧ', 'sk') #fib
  processing_str = processing_str.replace('ᇨ', 'st') #fib
  processing_str = processing_str.replace('ᇩ', 'sl')
  processing_str = processing_str.replace('ᇪ', 'sp') #fib
  processing_str = processing_str.replace('ᇫ', 'z') #1charBoth #modernalph?
  processing_str = processing_str.replace('ᇬ', 'k') #?
  processing_str = processing_str.replace('ᇭ', 'kg') #?
  processing_str = processing_str.replace('ᇮ', 'ng') #?
  processing_str = processing_str.replace('ᇯ', 'kh') #?
  processing_str = processing_str.replace('ᇰ', 'ng') #modernalph
  processing_str = processing_str.replace('ᇱ', 'ngt') #fib
  processing_str = processing_str.replace('ᇲ', 'ngz') #fib
  processing_str = processing_str.replace('ᇳ', 'pp')
  processing_str = processing_str.replace('ᇴ', 'f') #found #fib
  processing_str = processing_str.replace('ᇵ', 'hn')
  processing_str = processing_str.replace('ᇶ', 'hl')
  processing_str = processing_str.replace('ᇷ', 'hm')
  processing_str = processing_str.replace('ᇸ', 'hp')
  processing_str = processing_str.replace('ᇹ', 'j') #1charBoth #modernalph
  
  if debug_process:
    print("(l) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  
  # Hiragana
  #@ref https://codegolf.stackexchange.com/a/137339/61627
  # for better pronunciation
  # nope, only for hiragana by itself
  
  # s=re.sub
  # n=unicodedata.normalize
  # k,*r=r'NFKC DZU DU TSU TU \1\1 SM.{6}(.) \1 (CH|J|SH)Y \1 ISMALL.(Y.) CHI TI JI [ZD]I SHI SI FU HU'.split()
  # processing_str=''.join(unicodedata.name(c)[16:]for c in n(k,s(' ','',n(k,input()))))
  # while r:processing_str=s(r.pop(),r.pop(),processing_str)
  
  processing_str = \
    processing_str.translate(str.maketrans(  
      'ぁあぃいぅうぇえぉお',
      'aAiIuUeEoO'))
  
  processing_str = processing_str.replace('か', 'KA')
  processing_str = processing_str.replace('が', 'ga')
  processing_str = processing_str.replace('き', 'ki')
  processing_str = processing_str.replace('ぎ', 'gi')
  processing_str = processing_str.replace('く', 'ku')
  processing_str = processing_str.replace('ぐ', 'gu')
  processing_str = processing_str.replace('け', 'KE')
  processing_str = processing_str.replace('げ', 'ge')
  processing_str = processing_str.replace('こ', 'ko')
  processing_str = processing_str.replace('ご', 'go')
  processing_str = processing_str.replace('さ', 'sa')
  processing_str = processing_str.replace('ざ', 'za')
  processing_str = processing_str.replace('し', 'shi')
  processing_str = processing_str.replace('じ', 'ji')
  processing_str = processing_str.replace('す', 'su')
  processing_str = processing_str.replace('ず', 'zu')
  processing_str = processing_str.replace('せ', 'se')
  processing_str = processing_str.replace('ぜ', 'ze')
  processing_str = processing_str.replace('そ', 'so')
  processing_str = processing_str.replace('ぞ', 'zo')
  processing_str = processing_str.replace('た', 'ta')
  processing_str = processing_str.replace('だ', 'da')
  processing_str = processing_str.replace('ち', 'chi')
  processing_str = processing_str.replace('ぢ', 'ji')
  processing_str = processing_str.replace('っ', 'tsu')
  processing_str = processing_str.replace('つ', 'TSU')
  processing_str = processing_str.replace('づ', 'zu')
  processing_str = processing_str.replace('て', 'te')
  processing_str = processing_str.replace('で', 'de')
  processing_str = processing_str.replace('と', 'to')
  processing_str = processing_str.replace('ど', 'do')
  processing_str = processing_str.replace('な', 'na')
  processing_str = processing_str.replace('に', 'ni')
  processing_str = processing_str.replace('ぬ', 'nu')
  processing_str = processing_str.replace('ね', 'ne')
  processing_str = processing_str.replace('の', 'no')
  processing_str = processing_str.replace('は', 'ha')
  processing_str = processing_str.replace('ば', 'ba')
  processing_str = processing_str.replace('ぱ', 'pa')
  processing_str = processing_str.replace('ひ', 'hi')
  processing_str = processing_str.replace('び', 'bi')
  processing_str = processing_str.replace('ぴ', 'pi')
  processing_str = processing_str.replace('ふ', 'hu')
  processing_str = processing_str.replace('ぶ', 'bu')
  processing_str = processing_str.replace('ぷ', 'pu')
  processing_str = processing_str.replace('へ', 'he')
  processing_str = processing_str.replace('べ', 'be')
  processing_str = processing_str.replace('ぺ', 'pe')
  processing_str = processing_str.replace('ほ', 'ho')
  processing_str = processing_str.replace('ぼ', 'bo')
  processing_str = processing_str.replace('ぽ', 'po')
  processing_str = processing_str.replace('ま', 'ma')
  processing_str = processing_str.replace('み', 'mi')
  processing_str = processing_str.replace('む', 'mu')
  processing_str = processing_str.replace('め', 'me')
  processing_str = processing_str.replace('も', 'mo')
  processing_str = processing_str.replace('ゃ', 'ya')
  processing_str = processing_str.replace('や', 'YA')
  processing_str = processing_str.replace('ゅ', 'yu')
  processing_str = processing_str.replace('ゆ', 'YU')
  processing_str = processing_str.replace('ょ', 'yo')
  processing_str = processing_str.replace('よ', 'YO')
  processing_str = processing_str.replace('ら', 'ra')
  processing_str = processing_str.replace('り', 'ri')
  processing_str = processing_str.replace('る', 'ru')
  processing_str = processing_str.replace('れ', 're')
  processing_str = processing_str.replace('ろ', 'ro')
  processing_str = processing_str.replace('ゎ', 'wa')
  processing_str = processing_str.replace('わ', 'WA')
  processing_str = processing_str.replace('ゐ', 'wi')
  processing_str = processing_str.replace('ゑ', 'we')
  processing_str = processing_str.replace('を', 'wo')
  processing_str = processing_str.replace('ん', 'n')
  processing_str = processing_str.replace('ゔ', 'vu')
  processing_str = processing_str.replace('ゕ', 'ka')
  processing_str = processing_str.replace('ゖ', 'ke')
  processing_str = processing_str.replace('ゝ', '')
  processing_str = processing_str.replace('ゞ', '')
  processing_str = processing_str.replace('ゟ', 'yori')
  
  
  if debug_process:
    print("(m) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  
  # Katakana
  #
  
  # ゠ァアィイゥウェエォオ
  # -aAiIuUeEoO
  #
  #
  # ・ヽヾ
  
  processing_str = \
    processing_str.translate(str.maketrans(
      '゠ァアィイゥウェエォオー', 
      '-aAiIuUeEoO-'))
  
  processing_str = processing_str.replace('カ', 'KA')
  processing_str = processing_str.replace('ガ', 'ga')
  processing_str = processing_str.replace('キ', 'ki')
  processing_str = processing_str.replace('ギ', 'gi')
  processing_str = processing_str.replace('ク', 'ku')
  processing_str = processing_str.replace('グ', 'gu')
  processing_str = processing_str.replace('ケ', 'KE')
  processing_str = processing_str.replace('ゲ', 'ge')
  processing_str = processing_str.replace('コ', 'ko')
  processing_str = processing_str.replace('ゴ', 'go')
  processing_str = processing_str.replace('サ', 'sa')
  processing_str = processing_str.replace('ザ', 'za')
  processing_str = processing_str.replace('シ', 'shi')
  processing_str = processing_str.replace('ジ', 'zi')
  processing_str = processing_str.replace('ス', 'su')
  processing_str = processing_str.replace('ズ', 'zu')
  processing_str = processing_str.replace('セ', 'se')
  processing_str = processing_str.replace('ゼ', 'ze')
  processing_str = processing_str.replace('ソ', 'so')
  processing_str = processing_str.replace('ゾ', 'zo')
  processing_str = processing_str.replace('タ', 'ta')
  processing_str = processing_str.replace('ダ', 'da')
  processing_str = processing_str.replace('チ', 'chi')
  processing_str = processing_str.replace('ヂ', 'di')
  processing_str = processing_str.replace('ッ', 'tsu')
  processing_str = processing_str.replace('ツ', 'TSU')
  processing_str = processing_str.replace('ヅ', 'du')
  processing_str = processing_str.replace('テ', 'te')
  processing_str = processing_str.replace('デ', 'de')
  processing_str = processing_str.replace('ト', 'to')
  processing_str = processing_str.replace('ド', 'do')
  processing_str = processing_str.replace('ナ', 'na')
  processing_str = processing_str.replace('ニ', 'ni')
  processing_str = processing_str.replace('ヌ', 'nu')
  processing_str = processing_str.replace('ネ', 'ne')
  processing_str = processing_str.replace('ノ', 'no')
  processing_str = processing_str.replace('ハ', 'ha')
  processing_str = processing_str.replace('バ', 'ba')
  processing_str = processing_str.replace('パ', 'pa')
  processing_str = processing_str.replace('ヒ', 'hi')
  processing_str = processing_str.replace('ビ', 'bi')
  processing_str = processing_str.replace('ピ', 'pi')
  processing_str = processing_str.replace('フ', 'fu')
  processing_str = processing_str.replace('ブ', 'bu')
  processing_str = processing_str.replace('プ', 'pu')
  processing_str = processing_str.replace('ヘ', 'he')
  processing_str = processing_str.replace('ベ', 'be')
  processing_str = processing_str.replace('ペ', 'pe')
  processing_str = processing_str.replace('ホ', 'ho')
  processing_str = processing_str.replace('ボ', 'bo')
  processing_str = processing_str.replace('ポ', 'po')
  processing_str = processing_str.replace('マ', 'ma')
  processing_str = processing_str.replace('ミ', 'mi')
  processing_str = processing_str.replace('ム', 'mu')
  processing_str = processing_str.replace('メ', 'me')
  processing_str = processing_str.replace('モ', 'mo')
  processing_str = processing_str.replace('ャ', 'ya')
  processing_str = processing_str.replace('ヤ', 'YA')
  processing_str = processing_str.replace('ュ', 'yu')
  processing_str = processing_str.replace('ユ', 'YU')
  processing_str = processing_str.replace('ョ', 'yo')
  processing_str = processing_str.replace('ヨ', 'YO')
  processing_str = processing_str.replace('ラ', 'ra')
  processing_str = processing_str.replace('リ', 'ri')
  processing_str = processing_str.replace('ル', 'ru')
  processing_str = processing_str.replace('レ', 're')
  processing_str = processing_str.replace('ロ', 'ro')
  processing_str = processing_str.replace('ヮ', 'wa')
  processing_str = processing_str.replace('ワ', 'WA')
  processing_str = processing_str.replace('ヰ', 'wi')
  processing_str = processing_str.replace('ヱ', 'we')
  processing_str = processing_str.replace('ヲ', 'wo')
  processing_str = processing_str.replace('ン', 'n')
  processing_str = processing_str.replace('ヴ', 'vu')
  processing_str = processing_str.replace('ヵ', 'ka')
  processing_str = processing_str.replace('ヶ', 'ke')
  processing_str = processing_str.replace('ヷ', 'va')
  processing_str = processing_str.replace('ヸ', 'vi')
  processing_str = processing_str.replace('ヹ', 've')
  processing_str = processing_str.replace('ヺ', 'vo')
  processing_str = processing_str.replace('ヿ', 'koto')
  
  #
  #
  # processing_str=$(echo "${processing_str}" | \
  # )
  
  # #
  
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  
  if debug_process:
    print("(n) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  
  # Bopomofo
  # ㄓㄔㄕㄝㄞㄟㄠㄡㄢㄣㄤ
  #
  # ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄖㄗㄘㄙㄚㄛㄜ
  # bpmfdtnlgkhjqxrzcsaoe
  
  processing_str = \
    processing_str.translate(str.maketrans(
      'ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄖㄗㄘㄙㄚㄛㄜㄧ', 
      'bpmfdtnlgkhjqxrzcsaoei'))
  
  processing_str = processing_str.replace('ㄓ', 'zh')
  processing_str = processing_str.replace('ㄔ', 'ch')
  processing_str = processing_str.replace('ㄕ', 'sh')
  processing_str = processing_str.replace('ㄝ', 'eh')
  processing_str = processing_str.replace('ㄞ', 'ai')
  processing_str = processing_str.replace('ㄟ', 'ei')
  processing_str = processing_str.replace('ㄠ', 'au')
  processing_str = processing_str.replace('ㄡ', 'ou')
  processing_str = processing_str.replace('ㄢ', 'an')
  processing_str = processing_str.replace('ㄣ', 'en')
  processing_str = processing_str.replace('ㄤ', 'ang')
  processing_str = processing_str.replace('ㄥ', 'eng')
  processing_str = processing_str.replace('ㄦ', 'er')
  processing_str = processing_str.replace('ㄨ', 'u')
  processing_str = processing_str.replace('ㄩ', 'iu')
  processing_str = processing_str.replace('\u312A', 'v')
  processing_str = processing_str.replace('\u312B', 'ng')
  processing_str = processing_str.replace('\u312C', 'gn')
  processing_str = processing_str.replace('\u312D', 'ih')
  processing_str = processing_str.replace('\u312E', 'e')
  processing_str = processing_str.replace('\u312F', 'nn')
  
  # processing_str=$(echo "${processing_str}" | \
  # )
  
  # #
  
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  
  if debug_process:
    print("(o) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  
  # Syriac
  #
  
  processing_str = processing_str.replace('ܐ', 'a')
  processing_str = processing_str.replace('ܒ', 'b')
  processing_str = processing_str.replace('ܓ', 'g')
  processing_str = processing_str.replace('ܔ', 'g')
  processing_str = processing_str.replace('ܕ', 'd')
  processing_str = processing_str.replace('ܖ', 'd')
  processing_str = processing_str.replace('ܗ', 'h')
  processing_str = processing_str.replace('ܘ', 'w')
  processing_str = processing_str.replace('ܙ', 'z')
  processing_str = processing_str.replace('ܚ', 'h')
  processing_str = processing_str.replace('ܛ', 't')
  processing_str = processing_str.replace('ܜ', 't')
  processing_str = processing_str.replace('ܝ', 'y')
  processing_str = processing_str.replace('ܞ', 'h')
  processing_str = processing_str.replace('ܟ', 'k')
  processing_str = processing_str.replace('ܠ', 'l')
  processing_str = processing_str.replace('ܡ', 'm')
  processing_str = processing_str.replace('ܢ', 'n')
  processing_str = processing_str.replace('ܣ', 's')
  processing_str = processing_str.replace('ܤ', 's')
  processing_str = processing_str.replace('ܥ', 'e')
  processing_str = processing_str.replace('ܦ', 'p')
  processing_str = processing_str.replace('ܧ', 'p')
  processing_str = processing_str.replace('ܨ', 's')
  processing_str = processing_str.replace('ܩ', 'q')
  processing_str = processing_str.replace('ܪ', 't')
  processing_str = processing_str.replace('ܫ', 's')
  processing_str = processing_str.replace('ܬ', 't')
  processing_str = processing_str.replace('ܭ', 'bh')
  processing_str = processing_str.replace('ܮ', 'gh')
  processing_str = processing_str.replace('ܯ', 'dh')
  processing_str = processing_str.replace('ݍ', 'zh')
  processing_str = processing_str.replace('ݎ', 'kh')
  processing_str = processing_str.replace('ݏ', 'f')
  
  
  """
  wget https://yt-dl.org/downloads/latest/youtube-dl -O \
    /usr/local/bin/youtube-dl
  chmod a+rx /usr/local/bin/youtube-dl
  
  youtube-dl https://www.youtube.com/watch?v=hmXzjqDA4IM
  
  <s>youtube-dl -v jGgmzMKVCYg -f "bestvideo[ext=mp4]+bestaudio[acodec=opus]"\
    --recode-video mp4 --postprocessor-args "-vcodec copy"</s>
  
  youtube-dl -v 9SF5NcELH9E -f "bestvideo[ext=mp4]+bestaudio" \
    --recode-video mp4 --postprocessor-args "-vcodec copy"
  
  """
  #
  # processing_str=$(echo "${processing_str}" | \
  # )
  
  # #
  
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  
  
  # # Another writing system
  # processing_str=$(echo "${processing_str}" | \
  # )
  
  # #
  
  
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  
  
  # # Another writing system
  # processing_str=$(echo "${processing_str}" | \
  # )
  
  # #
  
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  
  
  # # Another writing system
  # processing_str=$(echo "${processing_str}" | \
  # )
  
  # #
  
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  # processing_str=$(echo "${processing_str}" | sed 's###g')
  
  if debug_process:
    print("(p) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  processing_str = processing_str.replace("(", "_")
  processing_str = processing_str.replace(")", "_")
  processing_str = processing_str.replace("'", "_")
  processing_str = processing_str.replace('"', "_")
  
  processing_str = re.sub(r"[^A-Za-z0-9._-]",
                          r"",
                          processing_str,
                          flags=re.IGNORECASE|re.MULTILINE)
  
  if debug_process:
    print("(q) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  
  pre_yt_code_stuff = processing_str
  
  if debug_process:
    print("(r) pre_yt_code_stuff: " + pre_yt_code_stuff, file=sys.stderr)
    print("    yt_code_stuff_etc: " + yt_code_stuff_etc, file=sys.stderr)
  ##endof:  if debug_process
  
  yt_code_stuff_ending_is_there = True
  
  if pre_yt_code_stuff_pre == yt_code_stuff_etc:
    yt_code_stuff_ending_is_there = False
  ##endof:  if/else pre_yt_code_stuff == yt_code_stuff_etc
  
  pre_yt_code_stuff = pre_yt_code_stuff.replace('.', '_')
  
  pre_yt_code_stuff = re.sub(r"[_]+",
                             "_",
                             pre_yt_code_stuff)
  pre_yt_code_stuff = pre_yt_code_stuff.replace("_-_", "-")
  pre_yt_code_stuff = re.sub(r"[_-]{2,}",
                             "_",
                             pre_yt_code_stuff)
  
  pre_yt_code_stuff = re.sub(u"_\u006e\u0067" + \
                             "(_|$)",
                             "_",
                             pre_yt_code_stuff,
                             flags=re.IGNORECASE)
  
  pre_yt_code_stuff = re.sub(r"^[_-]",
                             "",
                             pre_yt_code_stuff)
  pre_yt_code_stuff = re.sub(r"^[_-]+$",
                             "",
                             pre_yt_code_stuff)
  
  #shelnqsoujapl
  #ubcotlbleycwmogovdz
  
  pre_yt_code_stuff = re.sub(r"^ng",
                             "NnGg",
                             pre_yt_code_stuff)
  
  if debug_process:
    print("(s) pre_yt_code_stuff: " + pre_yt_code_stuff, file=sys.stderr)
    print("    yt_code_stuff_etc: " + yt_code_stuff_etc, file=sys.stderr)
  ##endof:  if debug_process
  
  if not yt_code_stuff_ending_is_there:
    processing_str = pre_yt_code_stuff
  else:
    processing_str = pre_yt_code_stuff + yt_code_stuff_etc
  ##endof:  if/else not yt_code_stuff_ending_is_there
  
  if debug_process:
    print("(t) processing_str: " + processing_str, file=sys.stderr)
  ##endof:  if debug_process
  
  return processing_str
  
##endof:  dwb_to_ascii(input_str)


if __name__ == "__main__":
  '''
  Gets run if the script is called from the command line
  
  As of today (2024-04-23), we are assuming that '-u'
  always gets passed in as a parameter. We must have
  not done that before, because we got the renaming
  with resolution and is_best. However, I'm not taking
  the time to do the logic for '-u' optional, right
  now.
  
  Never mind - it doesn't count. 
  '''
  
  is_best = False
  resolution = None
  
  ##  REMEMBER THAT IF ANY DEBUGGING IS GOING FOR THIS PYTHON SCRIPT,
  ##+ IT WILL CAUSE PROBLEMS FOR THE CALLING SCRIPT, WHICH JUST
  ##+ EXPECTS A NORMALIZED FILENAME!
  ##  P.S. Other debug is in the dwb_to_ascii function, near the
  ##+ beginning
  
  do_debug_params = False
  
  if do_debug_params:
    sys.stderr.write("\n\n")
    sys.stderr.write("len(sys.argv): " + str(len(sys.argv)))
    sys.stderr.write("\n")
    sys.stderr.write("sys.argv: " + str(sys.argv))
    sys.stderr.write("\n\n")
  ##endof:  if do_debug_params
  
  retval = " You passed something in wrong.\n" + \
           " Usage is:\n" + \
           ">>>import rus_greek_etc_to_ascii\n" + \
           ">>>dwb_to_ascii(" + \
           "filename_to_normalize, [is_best], [resolution])\n" + \
           " OR\n" + \
           "$ ./rus_greek_etc_to_ascii.py filename_to_normalize " + \
           " [is_best] [resolution]\n" + \
           " OR\n" + \
           "> python rus_greek_etc_to_ascii.py " + \
           "filename_to_normalize [is_best] [resolution]"
  if len(sys.argv) == 2:
    if do_debug_params:
      sys.stderr.write("\n")
      sys.stderr.write("sys.argv[0]: " + str(sys.argv[0]))
      sys.stderr.write("\n")
      sys.stderr.write("sys.argv[1]: " + str(sys.argv[1]))
      sys.stderr.write("\n\n")
    ##endof:  if do_debug_params
    retval = main(sys.argv[1])
  elif len(sys.argv) > 2:
    if do_debug_params:
      sys.stderr.write("\n")
      sys.stderr.write("sys.argv[0]: " + str(sys.argv[0]))
      sys.stderr.write("\n")
      sys.stderr.write("sys.argv[1]: " + str(sys.argv[1]))
      sys.stderr.write("\n")
      sys.stderr.write("sys.argv[2]: " + str(sys.argv[2]))
      sys.stderr.write("\n\n")
    ##endof:  if do_debug_params
    sec_arg = str(sys.argv[2]).lower()
    if sec_arg == 'true' or sec_arg == 't':
      is_best = True
    ##endof:  if sec_arg
  else:
    pass
  ##endof:  if/elif/else
  
  if len(sys.argv) == 3:
    if do_debug_params:
      sys.stderr.write("\n")
      sys.stderr.write("sys.argv[0]: " + str(sys.argv[0]))
      sys.stderr.write("\n")
      sys.stderr.write("sys.argv[1]: " + str(sys.argv[1]))
      sys.stderr.write("\n")
      sys.stderr.write("sys.argv[2]: " + str(sys.argv[2]))
      sys.stderr.write("\n\n")
    ##endof:  if do_debug_params
    retval = main(sys.argv[1], is_best)
  elif len(sys.argv):
    if do_debug_params:
      sys.stderr.write("\n")
      sys.stderr.write("sys.argv[0]: " + str(sys.argv[0]))
      sys.stderr.write("\n")
      sys.stderr.write("sys.argv[1]: " + str(sys.argv[1]))
      sys.stderr.write("\n")
      sys.stderr.write("sys.argv[2]: " + str(sys.argv[2]))
      sys.stderr.write("\n")
      sys.stderr.write("sys.argv[3]: " + str(sys.argv[3]))
      sys.stderr.write("\n\n")
    ##endof:  if do_debug_params
    third_arg = str(sys.argv[3])
    resolution = third_arg
    retval = main(sys.argv[1], is_best, resolution)
  else:
    pass
  ##endof:  the if/else stuff
  
  # We only get here if something went wrong.
  sys.stderr.write(str(retval))
  
##endof:  if __name__ == "__main__"
