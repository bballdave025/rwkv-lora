#/bin/bash
#
##############################################################################
# @file : rename_file_to_ascii.sh
# @author : D Black
# @since : 2024-04-23
#
# This one is with a strange, broken python3 in cygwin, so I've hacked
# conda into cygwin
#
# For renaming video files from online servers. yt-dlp, instalooter
#
##############################################################################

outfile_name="renaming_one_file_$(date +'%Y-%m-%dT%H%M%S%z').out"

the_file="problem-if-you-see-this--usage-is-video-filename-in-working-dir"
is_best_1="false" # guilty until proven innocent

do_debug_rename=1

touch "${outfile_name}"

echo | tee -a "${outfile_name}"

## argument number check
if [ $# -eq 0 ]; then
  echo " no filename given; you broke it ... wait and see" | \
                                            tee -a "${outfile_name}"
elif [ $# -eq 1 ]; then
  the_file="$1"
  echo " Using '${the_file}' as the filename to normalize" | \
                                            tee -a "${outfile_name}"
  echo | tee -a "${outfile_name}"
  echo " You didn't specify whether this was the best quality" | \
                                            tee -a "${outfile_name}"
  echo " or not, so we're using the default that" | \
                                            tee -a "${outfile_name}"
  echo " is_best_1='${is_best_1}'" | tee -a "${outfile_name}"
elif [ $# -eq 2 ]; then
  the_file="$1"
  is_best_1="$2"
  echo " Using '${the_file}' as the filename to normalize" | \
                                            tee -a "${outfile_name}"
  echo "and" | tee -a "${outfile_name}"
  echo " Taking the statement, this is the best quality," | \
                                            tee -a "${outfile_name}"
  echo " to be '${is_best_1}'" | tee -a "${outfile_name}"
  
elif [ $# -ge 3 ]; then
  echo " You overspecified ... whatever you were trying to" | \
                                            tee -a "${outfile_name}"
  echo " specify." | tee -a "${outfile_name}"
  echo " Using '${the_file}' as the filename to normalize" | \
                                            tee -a "${outfile_name}"
  echo "and" | tee -a "${outfile_name}"
  echo " Taking the statement, this is the best quality," | \
                                            tee -a "${outfile_name}"
  echo " to be '${is_best_1}'" | tee -a "${outfile_name}"
  echo "and" | tee -a "${outfile_name}"
  echo " Ignoring whatever else you said." | tee -a "${outfile_name}"
fi ##endof:  argument number check

filename_1="${the_file}" # making it fit the get_files_from_list mold

if [ ! -f "${filename_1}" ]; then
  echo | tee -a "${outfile_name}"
  echo " The file, '${filename_1}' does not exist, which will" | \
                                            tee -a "${outfile_name}"
  echo " cause an error, but we'll see what the rename would" | \
                                            tee -a "${outfile_name}"
  echo " have been." | tee -a "${outfile_name}"
  echo | tee -a "${outfile_name}"
fi

dimensions_1=""

# messed up logic, but just experimentally getting it to work
pre_is_best="${is_best_1}"

echo "is_best_1   (a) : '${is_best_1}'"
echo "pre_is_best (a) : '${pre_is_best}'"

if [ "${is_best_1}" = "whocares" ]; then
  is_best_1=""
  pre_is_best="${is_best_1}"
fi ##endof:  if [ ! "${is_best_1}" = "whocares" ]

echo "is_best_1   (b) : '${is_best_1}'"
echo "pre_is_best (b) : '${pre_is_best}'"

if [ ! "${is_best_1}" = "true" -a ! "${is_best_1}" = "t" -a \
     ! "${is_best_1}" = "false" -a ! "${is_best_1}" != "f" -a \
     ! "${is_best_1}" = "whocares" ]; then
  echo "Your is_best_1='${is_best_1}' will break stuff." | \
                                            tee -a "${outfile_name}"
  echo "Very soon, actually." | tee -a "${outfile_name}"
  exit -1
else
  echo "is_best_1   (c) : '${is_best_1}'"
  echo "pre_is_best (c) : '${pre_is_best}'"
  is_best_1="${pre_is_best}"
  echo "Trying for dimensions ... " | tee -a "${outfile_name}"
  touch tmperr01
  dimensions_1=$(ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height -of csv=s=x:p=0 \
      "${filename_1}" 2>tmperr01)
  echo | tee -a "${outfile_name}"
  echo "dimensions_1: ${dimensions_1}" | tee -a "${outfile_name}"
  echo "Any errors: " | tee -a "${outfile_name}"
  cat tmperr01 | tee -a "${outfile_name}"
  echo | tee -a "${outfile_name}"
  rm tmperr01
  echo "is_best_1   (d) : '${is_best_1}'"
  echo "pre_is_best (d) : '${pre_is_best}'"
fi ##endof:  if/else

if [ $do_debug_rename -eq 1 ]; then
  echo | tee -a "${outfile_name}"
  echo "#### DEBUG ####" | tee -a "${outfile_name}"
  echo "#             #" | tee -a "${outfile_name}"
  echo "filename_1: '${filename_1}'" | tee -a "${outfile_name}"
  echo "is_best_1: '${is_best_1}'" | tee -a "${outfile_name}"
  echo "dimensions_1: '${dimensions_1}'" | tee -a "${outfile_name}"
  echo "#             #" | tee -a "${outfile_name}"
  echo "Command should be" | tee -a "${outfile_name}"
  echo "new_fname_1=\$(python -u rus_greek_etc_to_ascii.py "\
"\"${filename_1}\" \"${is_best_1}\" \"${dimensions_1}\" 2>&1)" \
                                               | tee -a "${outfile_name}"
  echo "#             #" | tee -a "${outfile_name}"
  echo "###############" | tee -a "${outfile_name}"
  echo | tee -a "${outfile_name}"
fi ##endof:  if [ $do_debug_rename -eq 1 ]

echo "is_best_1   (e) : '${is_best_1}'"
echo "pre_is_best (e) : '${pre_is_best}'"

touch tmperr02
#new_fname_1=$(python3 -u rus_greek_etc_to_ascii.py "${filename_1}" \
#                "${is_best_1}" "${dimensions_1}" 2>&1)
# with the conda hack
##  REMEMBER THAT IF ANY DEBUGGING IS GOING FOR THE PYTHON SCRIPT,
##+ IT WILL CAUSE PROBLEMS FOR THIS SCRIPT!
new_fname_1=$(python -u rus_greek_etc_to_ascii.py "${filename_1}" \
                "${is_best_1}" "${dimensions_1}" 2>&1) 
#2>tmperr02) ## going to tmperr02 breaks it. so does removing 2>&1
echo | tee -a "${outfile_name}"
echo " [Possibly]" | tee -a "${outfile_name}"
echo "new_fname_1: ${new_fname_1}" | tee -a "${outfile_name}"

echo | tee -a "${outfile_name}"

echo "Any errors: " | tee -a "${outfile_name}"
cat tmperr02 | tee -a "${outfile_name}"
echo | tee -a "${outfile_name}"
rm tmperr02

echo "In case this was a non-patterned file ..." | tee -a "${outfile_name}"

#     -v-     Thinking through this:     -v-
# IN: a.mp4                          OUT: .mp4                         NEQ
# IN: a_mp4                          OUT: _mp4                         NEQ
# IN: This_Person_12345678901_webm   OUT: _webm                        NEQ
# IN: This_Person_12345678901.webm   OUT: .webm                        NEQ
# IN: ThisPerson12345678901webm      OUT: ThisPerson12345678901webm    EQUAL
#(Including the Python for the next line)
# IN: ThisПerson12345678901webm      OUT: ThisPerson12345678901webm    NEQ
# IN: This.Person_12345678901.webm   OUT: .webm                        NEQ
# IN: This.Person_12345678901_webm   OUT: _webm                        NEQ
# IN: This_Person_12345678902.mp4    OUT: .mp4                         NEQ
#(Next one probably shouldn't come as an input)
# IN: This.Person_12345678901webm    OUT: This.Person_12345678901webm  EQUAL
#(Including the Python for the next line
# IN: Этот_Человек_abcdefghijk.mp4   OUT: .mp4                         NEQ
#(Including the Python for the next line
# IN: Этот_Человек_abcdefghijk.webm  OUT: .webm                        NEQ
#(Including the Python for the next line
# IN: Этот_Человек_abcdefghijk       OUT: _webm                        NEQ
#(Including the Python for the next line
# IN: Этот_Человек_abcdefghijk       OUT: Etot_CHelovek_abcdefghijk    NEQ
#(Including the Python for the next line:
# IN: лошадь_ето                     OUT: _eto                         NEQ
#(NOT including the Python for the next line:
# IN: лошадь_ето                     OUT: _ето
# Okay, I could program in normal file extensions, but I won't for now.
touch tmperr03
end_check_orig_f1=$(echo "${filename_1}" | \
                       sed 's#^.*\([_.][^_.]\{2,5\}\)$#\1#g' 2>tmperr03)
end_check_new_f1=$(echo "${new_fname_1}" | \
                      sed 's#^.*\([_.][^_.]\{2,5\}\)$#\1#g' 2>tmperr03)

change_is_likely_needed=0 # innocent until proven guilty
change_is_almost_certainly_needed=0 # guilty until proven innocent (?)

if [ "${end_check_orig_f1}" != "${end_check_new_f1}" ]; then
  change_is_likely_needed=1
fi ##endof:  if [ "${end_check_orig_f1}" != "${end_check_new_f1}" ]

if [ $do_debug_rename -eq 1 ]; then
  echo | tee -a "${outfile_name}"
  echo "#### DEBUG ####" | tee -a "${outfile_name}"
  echo "#             #" | tee -a "${outfile_name}"
  echo "end_check_orig_f1: ${end_check_orig_f1}" | tee -a "${outfile_name}"
  echo "end_check_new_f1: ${end_check_new_f1}" | tee -a "${outfile_name}"
  echo "change_is_likely_needed: ${change_is_likely_needed}" \
                                               | tee -a "${outfile_name}"
fi ##endof:  if [ $do_debug_rename -eq 1 ]

echo "Any errors: " | tee -a "${outfile_name}"
cat tmperr03 | tee -a "${outfile_name}"
echo | tee -a "${outfile_name}"
rm tmperr03

##  Probably possible to do what I want with this, but I'm thinking too
##+ hard for now
#first_orig_f1=$(echo "${filename_1}" | \
#                                sed 's#^\(.*\)[_.][^_.]\{2,5\}$#\1#g')
#first_new_f1=$(echo "${new_fname_1}" | \
#                                sed 's#^\(.*\)[_.][^_.]\{2,5\}$#\1#g')

touch tmperr04
extension_orig_f1=$(echo "${filename_1}" | \
                       sed 's#^.*[_.]\([^_.]\{2,5\}\)$#\1#g' 2>tmperr04)
extension_new_f1=$(echo "${new_fname_1}" | \
                      sed 's#^.*[_.]\([^_.]\{2,5\}\)$#\1#g' 2>tmperr04)

extensions_are_compatible=0 # guilty until proven innocent

if [ "${extension_orig_f1}" = "${extension_new_f1}" -o \
     "${extension_orig_f1}" = "mp4" -o \
     "${extension_orig_f1}" = "mkv" -o \
     "${extension_orig_f1}" = "webm" -o \
     "${extension_orig_f1}" = "mov" -o \
     "${extension_orig_f1}" = "flv" -o \
     "${extension_orig_f1}" = "py" -o \
     "${extension_orig_f1}" = "sh" -o \
     "${extension_orig_f1}" = "txt" -o \
     "${extension_orig_f1}" = "out" -o \
     "${extension_orig_f1}" = "pyc" -o \
     "${extension_orig_f1}" = "lst" -o \
     "${extension_orig_f1}" = "list" -o \
     "${extension_orig_f1}" = "log" -o \
     "${extension_new_f1}"  = "mp4" -o \
     "${extension_new_f1}"  = "webm" -o \
     "${extension_new_f1}"  = "mkv" -o \
     "${extension_new_f1}"  = "mov" -o \
     "${extension_new_f1}"  = "flv" -o \
     "${extension_new_f1}"  = "py" -o \
     "${extension_new_f1}"  = "sh" -o \
     "${extension_new_f1}"  = "txt" -o \
     "${extension_new_f1}"  = "out" -o \
     "${extension_new_f1}"  = "pyc" -o \
     "${extension_new_f1}"  = "lst" -o \
     "${extension_new_f1}"  = "list" -o \
     "${extension_new_f1}"  = "jpg" -o \
     "${extension_new_f1}"  = "jpeg" -o \
     "${extension_new_f1}"  = "gif" -o \
     "${extension_new_f1}"  = "png" -o \
     "${extension_new_f1}"  = "bmp" -o \
     "${extension_new_f1}"  = "log" ]; then
  extensions_are_compatible=1
fi ##endof:  if extension-stuff

echo "Any errors: " | tee -a "${outfile_name}"
cat tmperr04 | tee -a "${outfile_name}"
echo | tee -a "${outfile_name}"
rm tmperr04

if [ $do_debug_rename -eq 1 ]; then
  echo "#             #" | tee -a "${outfile_name}"
  echo "extension_orig_f1: ${extension_orig_f1}" \
                                               | tee -a "${outfile_name}"
  echo "extension_new_f1: ${extension_new_f1}" | tee -a "${outfile_name}"
  echo "extensions_are_compatible: ${extensions_are_compatible}" \
                                               | tee -a "${outfile_name}"
fi ##endof:  if [ $do_debug_rename -eq 1 ]

touch tmperr05

separator_orig_f1=$(printf %.1s "${end_check_orig_f1}" 2>tmperr05)
separator_new_f1=$(printf %.1s "${end_check_new_f1}" 2>tmperr05)

is_likely_changed_extension=0 # innocent? guilty?

if [ $change_is_likely_needed -eq 1 -a \
     "${separator_new_f1}" == "_" ]; then
  is_likely_changed_extension=1
fi ##endof:  if change seems almost certainly needed

if [ $do_debug_rename -eq 1 ]; then
  echo "#             #" | tee -a "${outfile_name}"
  echo "separator_orig_f1: ${separator_orig_f1}" \
                                               | tee -a "${outfile_name}"
  echo "separator_new_f1: ${separator_new_f1}" | tee -a "${outfile_name}"
  echo "is_likely_changed_extension: ${is_likely_changed_extension}" \
                                               | tee -a "${outfile_name}"
fi ##endof:  if [ $do_debug_rename -eq 1 ]

echo "Any errors: " | tee -a "${outfile_name}"
cat tmperr05 | tee -a "${outfile_name}"
echo | tee -a "${outfile_name}"
rm tmperr05

if [ $extensions_are_compatible -eq 1 -a \
     $is_likely_changed_extension -eq 1 ]; then
  change_is_almost_certainly_needed=1
fi ##endof:  if

if [ $do_debug_rename -eq 1 ]; then
  echo "#             #" | tee -a "${outfile_name}"
  echo "change_is_almost_certainly_needed: "\
"${change_is_almost_certainly_needed}" | tee -a "${outfile_name}"
  echo "#             #" | tee -a "${outfile_name}"
  echo "###############" | tee -a "${outfile_name}"
fi ##endof:  if [ $do_debug_rename -eq 1 ]

touch tmperr06

if [ $change_is_almost_certainly_needed -eq 1 ]; then
  new_fname_1=$(echo "${new_fname_1}" | \
                   sed 's#^\(.*\)_\([^_.]\{2,5\}\)$#\1.\2#g' 2>tmperr06)
fi ##endof:  if [ $change_is_almost_certainly_needed -eq 1 ]

echo | tee -a "${outfile_name}"
echo "   ... after the checks:" | tee -a "${outfile_name}"
echo | tee -a "${outfile_name}"
echo "new_fname_1: ${new_fname_1}" | tee -a "${outfile_name}"

echo "Any errors: " | tee -a "${outfile_name}"
cat tmperr06 | tee -a "${outfile_name}"
echo | tee -a "${outfile_name}"
rm tmperr06

try_0_worked=0

echo | tee -a "${outfile_name}"

#touch tmperr07
mv "${filename_1}" "${new_fname_1}" 2>tmperr07 && \
              try_0_worked=1 || \
              echo "  ... rename FAILURE" | tee -a "${outfile_name}"
echo | tee -a "${outfile_name}"
echo "Any errors:" | tee -a "${outfile_name}"
cat tmperr07 | tee -a "${outfile_name}"
echo | tee -a "${outfile_name}"
rm tmperr07

if [ $try_0_worked -eq 1 ]; then
  echo "  ... rename success" | tee -a "${outfile_name}"
  echo | tee -a "${outfile_name}"
  echo "'${filename_1}'"
  echo "  RENAMED TO"
  echo "'${new_fname_1}'"
else
  echo "  ... there was a problem. I might have told you so," | \
                                               tee -a "${outfile_name}"
  echo "      or I might not have done so." | tee -a "${outfile_name}"
fi ##endof:  if [ $try_0_worked -eq 1 ]

echo | tee -a "${outfile_name}"
