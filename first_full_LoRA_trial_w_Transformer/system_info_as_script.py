#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#########################################################################
'''
@file: win_system_info_as_script.py
@editor:  David Wallace BLACK (GitHub @bballdave025)
@authors: Main one: Stack Overflow @24_saurabh_sharma
Other StackOverflow Users from
@archived_ref = "https://web.archive.org/web/20240529202404/" + \
                "https://stackoverflow.com/questions/3103178/" + \
                "how-to-get-the-system-info-with-python"

Further edits, info, thoughts to come from David BLACK
@since 2024-05-29 (for @bballdave025)

Other possible references
         ref02 = "https://docs.python.org/3/library/" + \
                 "os.html#miscellaneous-system-information"
archived_ref02 = "https://web.archive.org/web/20240529212940/" + \
                 "https://docs.python.org/3/library/os.html"
archived_ref03 = "https://web.archive.org/web/20240529212142/" + \
                 "https://stackoverflow.com/questions/276052/" + \
                 "how-to-get-current-cpu-and-ram-usage-in-python"
archived_ref04 = "https://web.archive.org/web/20240529220012/" + \
                 "https://stackoverflow.com/questions/64996339/" + \
                 "get-cpu-and-gpu-temp-using-python-without-admin-access-windows"
archived_ref05 = "https://web.archive.org/web/20240529222504/" + \
                 "https://superuser.com/questions/723506/" + \
                 "get-the-video-card-model-via-command-line-in-windows"

@todo : make this a class, 
        get certain parts of the info, 
        get info as done from several Linux/Windows/Mac commands
           (CMD) >systeminfo | findstr "OS"
           (CMD) >systeminfo
          (*NIX) $ uname -a
          ...
        get info about useful and/or problem-specific software
          (*NIX) $ bash --version # | head -n 1
          (*NIX) $ gcc --version # | head -n 1
          (*NIX) $ g++ --version # | head -n 1
          (*NIX) $ make --version # | head -n 2
          (*NIX) $ cmake --version # head -n 1
        get stuff from my standard Windows System query
        
        @result : Prints out a bunch of system info



        
'''
#########################################################################


##----------------
## IMPORTS
##----------------

import psutil
import platform
from datetime import datetime
import cpuinfo  # needs `pip install py-cpuinfo`
import socket
import uuid
import getpass
import pprint
import re
import subprocess
import sys
import os

import qwqfetch 
  # needs `pip install git+https://github.com/nexplorer-3e/qwqfetch`

can_do_wmi = True     # innocent until proven guilty
can_do_pylspci = True # ditto
can_do_torch = True
can_do_tf = True
can_do_tfdl = True


try:
  import torch
except Exception as e_torch:
  can_do_torch = False
finally:
  pass
##endof:  try/except/finally torch

try:
  import tensorflow as tf
except Exception as e_tf:
  can_do_tf = False
finally:
  pass
##endof:  try/except/finally tf

try:
  from tensorflow.python.client import device_lib
except Exception as e_tfdl:
  can_do_tf = False
finally:
  pass
##endof:  try/except/finally device_lib

try:
  from pylspci.parsers import SimpleParser
    # needs `pip install pylspci`
except Exception as e_pci:
  can_do_pylspci = False
finally:
  pass
##endof:  try/except/finally pci

# For windows
try:
  import wmi  # needs `pip install wmi`
except Exception as e_wmi:
  can_do_wmi = False
finally:
  pass
##endof:  try/except/finally wmi



first_replace_prime = "bballdave025"
second_replace_prime = "MYMACHINE"
vanilla_replace = "NOT-FOR-NOW"
first_replace = "potAtoYOUnItdi0de"
second_replace = "2indiViduAlsWokIntoABaRdiFf"


##-----------------
##  METHODS, ETC.
##-----------------

def main():
  '''
  An easy-to-remember entrance from the command-line
  '''
  
  print_system_information()
  
##endof:  main()


def run():
  '''
  An easy-to-remember entrance from the module name.
  '''
  
  print_system_information()
  
##endof:  run()


def print_system_information():
  '''
  Takes care of printing the system information. Right now, I know just Windows.
  
  Will take care of it for *NIX, too
  
  Later, this should have options as in the todo stuff above, as well
  as returning parts of the information. It should also give the option
  to show or not show some of the things commented out here.
  
  Also refer to my global_parameters functions
    
  Also later, this should be put into a SystemInformationProvider class.
  
  @result : prints system information to stdout
  '''
  
  print()
  print_main_sys_info()
  print()
  print_boot_time()
  global first_replace
  first_replace = str(getpass.getuser())
  print()
  print_cpu_info()
  print()
  print_gpu_graphics_card_info()
  print()
  print_memory_info()
  print()
  print_disk_info()
  print()
  print("### No network info for now ###")
  # print_network_info()
  print()
  print("##### The last attempts for any useful system info #####")
  print("These might give lots of info, or new info.")
  print("Then again, they might fail miserably.")
  print()
  print("Try to access lscpi (through python).")
  print_all_pci_devices_from_lspci(
                           do_only_likely_graphics=False,
                           do_output_short_info=False,
                           do_output_if_likely_graphics=False,
                           do_output_long_info=True
  )
  print()
  print("Should be a good recap, but might not be complete.")
  print(" ...")
  print_qwqfetch_screenfetch_sysinfo()
  print()
  
##endof:  print_system_information()


def print_main_sys_info():
  '''
  High-level stuff
  '''
  
  print("#"*25, " System Information ", "#"*25)
  uname = platform.uname()
  print(f"System: {uname.system}")
  global second_replace
  second_replace = uname.node
  node_str = str(uname.node).replace(second_replace,
                                     second_replace_prime)
  print(f"Node Name: {node_str}")
  print(f"Release: {uname.release}")
  print(f"Version: {uname.version}")
  print(f"Machine: {uname.machine}")
  print(f"Processor: {uname.processor}")
  print(f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}")
  print("Ip-Address: NOT-FOR-NOW")
  #print(f"Ip-Address: {socket.gethostbyname(socket.gethostname())}")
  print("Mac-Address: NOT-FOR-NOW")
  #print(f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}")
##endof:  print_main_sys_info()


def print_boot_time():
  '''
  Gives a timestamp before when this module was run, hopefully
  close to the time when the work is being done.
  '''
  
  print("#"*29, " Boot Time ", "#"*30)
  boot_time_timestamp = psutil.boot_time()
  bt = datetime.fromtimestamp(boot_time_timestamp)
  print("Boot Time (date and time of last boot) was")
  print(f"Boot Time: {bt.year}-{bt.month}-{bt.day}T" + \
        f"{bt.hour}:{bt.minute}:{bt.second}")
##endof:  print_boot_time()


def print_cpu_info():
  '''
  
  '''
  
  print("#"*30, " CPU Info ", "#"*30)
  
  print("Physical cores:", psutil.cpu_count(logical=False))
  print("Total cores:", psutil.cpu_count(logical=True))
  print("CPU Usage Per Core:")
  for core_num, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
      print(f"Core {core_num}: {percentage}%")
  ##endof:  for core_num, percentage ...
  print(f"Total CPU Usage: {psutil.cpu_percent()}%")
  
  cpufreq = psutil.cpu_freq()
  print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
  print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
  print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
  
##endof:  print_cpu_info()


def print_gpu_graphics_card_info():
  '''
  
  '''
  
  print("#"*30, " GPU Info ", "#"*30)
  
  print("Information on GPU(s)/Graphics Card(s)")
  print(" (if any such information is to be found)")
  print()
  
  if can_do_wmi:
    try:
      print("Using `wmi`, we get the following `win32_VideoController` names.")
      this_computer = wmi.WMI()
      for so_called_gpu in this_computer.Win32_VideoController():
        print("  ", so_called_gpu.name)
      ##endof:  for so_called_gpu in this_computer.Win32_VideoController()
    except Exception as e_gr_wmi:
      print("   ... There was a problem with using the PyPI `wml` module")
      print("  Details:")
      print(str(e_gr_wmi))
      print("      ... Not a big surprise, since we're trying lots of ways")
      print("          to get the info, especially since this module")
      print("          wraps a Windows command. Not a big deal.")
    finally:
      pass
    ##endof:  try/except/finally
  else:
    print("Can't use  wmi  to test for GPU/Graphics Card.")
  ##endof:  if/else can_do_wmi
  
  if can_do_torch:
    print("Using  PyTorch  and the `torch.cuda.is_available()` method.")
    torch_cuda_is_available = torch.cuda.is_available()
    print("The statement, 'There is CUDA and an appropriate GPU',")
    print("  is ... ", str(torch_cuda_is_available))
    
    #  Possible future reference:
    #+ pf_ref_1 = "https://web.archive.org/web/20240529231349/" + \
    #+            "https://stackoverflow.com/questions/71188895/" + \
    #+            "how-to-get-pytorchs-memory-stats-on-cpu-main-memory"
    #+ pf_ref_2 = 
  else:
    print("Can't use  PyTorch  to test for (NVidia, CUDA-enabled) GPU.")
  ##endof:  if can_do_torch
  
  if can_do_tf:
    print("Using  TensorFlow  with several of its methods.")
    print("  Attempting to get GPU Device List")
    gpu_device_list = tf.config.list_physical_devices('GPU')
    if gpu_device_list:
      pprint.pp(gpu_device_list)
      for this_device in gpu_device_list:
        #  GDD_ref = "https://web.archive.org/web/20240529230520/" + \
        #+           "https://www.tensorflow.org/api_docs/python/" + \
        #+           "tf/config/experimental/get_device_details"
        details = tf.config.experimental.get_device_details(this_device)
        print(str(details))
      ##endof:  for this_device in gpu_device_list
    else:
      print("No GPU devices found by TensorFlow.")
    ##endof:  if gpu_device_list
  else:
    print("Can't use  TensorFlow  to test for GPU.")
  ##endof:  if can_do_tf
  
  if can_do_tfdl:
    print("Tensorflow can give us CPU (and/or GPU) info.")
    print("The info here might help you know if we're running on a CPU.")
    device_lib.list_local_devices()
    print("# -- (i) -- #")
    print("Sometimes, this doesn't show up when run on Windows")
    print("through this script, but it does show up when run")
    print("from the command line.")
    print("(Where \"this\" refers to")
    print("   tensorflow.python.client.device_lib.list_local_devices()")
    print("If the other info tells you that this is probably")
    print("Dave's PC in the corner of the room (3 screens),")
    print("then the inbput/output on the command line would likely")
    print("be as follows:")
    print("""
          (conda-env) >pip install tensorflow-cpu
          (conda-env) >python
          Python 3.10.14 | packaged by Anaconda, Inc. | \\
            (main, May  6 2024, 19:44:50) \\
            [MSC v.1916 64 bit (AMD64)] on win32
          Type "help", "copyright", "credits" or "license" for more information.
          >>>
          >>> from tensorflow.python.client import device_lib
          2024-06-02 09:50:02.208877: I tensorflow/core/util/port.cc:113] \\
            oneDNN custom operations are on. \\
            You may see slightly different numerical results due to \\
            floating-point round-off errors from different computation \\
            orders. To turn them off, set the environment variable \\
            `TF_ENABLE_ONEDNN_OPTS=0`.
          2024-06-02 09:50:04.867132: I tensorflow/core/util/port.cc:113] \\
            oneDNN custom operations are on. \\
            You may see slightly different numerical results due to \\
            floating-point round-off errors from different computation \\
            orders. To turn them off, set the environment variable \\
            `TF_ENABLE_ONEDNN_OPTS=0`.
          >>> device_lib.list_local_devices
          <function list_local_devices at 0x000001E69CF6E200>
          >>> device_lib.list_local_devices()
          2024-06-02 09:50:25.325804: \\
            I tensorflow/core/platform/cpu_feature_guard.cc:210] \\
            This TensorFlow binary is optimized to use available CPU \\
            instructions in performance-critical operations.
          To enable the following instructions: AVX2 FMA, in other \\
            operations, rebuild TensorFlow with the appropriate compiler \\
            flags.
          [name: "/device:CPU:0"
          device_type: "CPU"
          memory_limit: 268435456
          locality {
          }
          incarnation: 4538066893645489801
          xla_global_id: -1
          ]
          >>>
"""
    )
    ##endof:  heredoc-ed string print
  ##endof:  if can_do_tfdl
  
  dash_str_len = 15
  print()
  print("Trying to use some nvidia code ( nvidia-smi ) to find information")
  try:
    nvidia_cmd_out, nvidia_cmd_err = \
               subprocess.Popen(['nvidia-smi', '-q'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE
    )
    print("-"*dash_str_len)
    print("No exception thrown from using the `subprocess` module")
    print("to run `nvidia-smi -q`")
    out_str = nvidia_cmd_out.communicate()
    err_str = nvidia_cmd_err.communicate()
    print("   ### Output:", "\n", str(out_str))
    print("   ###  Error:", "\n", str(err_str))
  except Exception as e_nvidia:
    print("  That nvidia stuff didn't work") #, file=sys.stderr)
    print("  The error information is:") #, file=sys.stderr)
    print(str(e_nvidia)) # , file=sys.stderr)
    print("  Neither a big surprise nor a big deal")
  finally:
    print("  That's the end of the nvidia try.")
  ##endof:  try/except/finally
  print()
  
  if can_do_pylspci:
    print("Trying to use  [py]lspci   to find information")
    print_all_pci_devices_from_lspci(
                           do_only_likely_graphics=True,
                           do_output_short_info=True,
                           do_output_if_likely_graphics=True,
                           do_output_long_info=True
    )
  ##endof:  if can_do_pylspci
  print()
  
  do_debug_qwq = False
  
  print("There might be graphics card/GPU information in")
  print("the output from a python-only screenfetch copycat.")
  print("Getting the 'GPU' line from the qwqfetch output")
  qwq_str = get_qwqfetch_screenfetch_sysinfo()
  if do_debug_qwq:
    print("# DEBUG # qwq_str:")
    print(qwq_str)
  ##endof:  if do_debug_qwq
  gpu_entries = re.findall(r"\n([^\n]*GPU[^\n]+)\n", qwq_str)
  if do_debug_qwq:
    print("# DEBUG # gpu_entries:")
    pprint.pp(gpu_entries)
  ##endof:  if do_debug_qwq
  for this_entry in gpu_entries:
    print(this_entry)
 ##endof:  for this_entry in gpu_entries
  print()
  
  print("Those are all our chances to find out about any GPU/Graphics Cards")
  
##endof:  print_gpu_graphics_card_info()


def print_memory_info():
  '''
   
  '''
  
  print("#"*22, " Memory (RAM) Information ", "#"*22)
  
  svmem = psutil.virtual_memory()
  print(f"Total: {get_size(svmem.total)}")
  print(f"Available: {get_size(svmem.available)}")
  print(f"Used: {get_size(svmem.used)}")
  print(f"Percentage: {svmem.percent}%")
  
  print(" "*5, "="*15, "SWAP Memory", "="*15, " "*5)
  swap = psutil.swap_memory()
  print(f"Total: {get_size(swap.total)}")
  print(f"Free: {get_size(swap.free)}")
  print(f"Used: {get_size(swap.used)}")
  print(f"Percentage: {swap.percent}%")
##endof:  get_memory_info()


def print_disk_info():
  '''
   
  '''
  
  print("#"*29, " Disk Info ", "#"*30)
  print("Partitions and Usage:")
  partitions = psutil.disk_partitions()
  for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File system type: {partition.fstype}")
    try:
      partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError as e_perm:
      print("  PermissionDrror while trying to get partition.",
            file=sys.stdout
      )
      print("  Details are:") #, file=sys.stdout)
      print("  This can be thrown when the disk is not ready." #,
      #      file=sys.stdout
      )
      print("It's not a big deal.")
      continue
    print(f"  Total Size: {get_size(partition_usage.total)}")
    print(f"  Used: {get_size(partition_usage.used)}")
    print(f"  Free: {get_size(partition_usage.free)}")
    print(f"  Percentage: {partition_usage.percent}%")
  ##endof:  for partition in partitions
  
  print("  Since last boot,")
  disk_io = psutil.disk_io_counters()
  print(f"Total read: {get_size(disk_io.read_bytes)}")
  print(f"Total write: {get_size(disk_io.write_bytes)}")
##endof:  print_disk_info()


def print_network_info():
  '''
  
  '''
  
  print("#"*24, " Network Information ", "#"*25)
  ## get all network interfaces (virtual and physical)
  if_addrs = psutil.net_if_addrs()
  for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
      print(f"=== Interface: {interface_name} ===")
      if str(address.family) == 'AddressFamily.AF_INET':
        print(f"  IP Address: {address.address}")
        print(f"  Netmask: {address.netmask}")
        print(f"  Broadcast IP: {address.broadcast}")
      elif str(address.family) == 'AddressFamily.AF_PACKET':
        print(f"  MAC Address: {address.address}")
        print(f"  Netmask: {address.netmask}")
        print(f"  Broadcast MAC: {address.broadcast}")
      ##endof:  if/elif
  print("Stats since boot")
  net_io = psutil.net_io_counters()
  print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
  print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
  
##endof:  print_network_info()


def get_size(n_bytes, suffix="iB"):
  '''
  Scale bytes to a nice-looking format, so we don't get any factors
  of 10^5 or of 10^-8, etc. Well, actually just the big positive ones.
  examples:
    @todo : examples of n_bytes to the proper context
  
  @param  int n_bytes  :  The number of bytes, which should be converted
                          to something more easily handled.
  @param  string suffix  :  The suffix for the units (the second character(s)
                            I make the default 'iB' instead of 'B' - bballdave025
  
  @return  string  : the well-formatted string representing the amount of memory
  '''
  cs_standard_pow2_factor = 1024
  
  for prefix in ["", "K", "M", "G", "T", "P"]:
    if n_bytes < cs_standard_pow2_factor:
      return f"{n_bytes:.2f}{prefix}{suffix}"
    ##endof:  if n_bytes < cs_standard_pow2_factor
    
    n_bytes /= cs_standard_pow2_factor
    
  ##endof:  for prefix in ...
##endof:  get_size(n_bytes, suffix="iB")


##---------------------------------------
##  Some bulldozer solutions (just try
##+ outputting everything)
##---------------------------------------

def print_all_pci_devices_from_lspci(
                           do_only_likely_graphics=True,
                           do_output_short_info=False,
                           do_output_if_likely_graphics=True,
                           do_output_long_info=True
):
  '''
  @todo : this documentation
  '''
  
  big_plus_width = 70
  little_hyphen_width = 25
  
  had_lspci_problem = False # We haven't had one, yet
  
  try:
    device_list = SimpleParser().run()
    print("   ... we have a device_list")
  except Exception as e_lspci:
    print("   ... problem with pylspci.parsers.SimpleParser")
    print("      ... not especially surprising, nor a big deal")
    print(str(e_lspci))
    print("#  Note, if it says something about the file not being")
    print("#+ found, 'the file' is `lscpi`")
    print("         ... continuing with other ways to get information")
    # raise e_lspci
    had_lspci_problem = True
  finally:
    if had_lspci_problem:
      return
    ##endof:  if had_lspci_problem
  ##endof:  try/except/finally
  
  num_devices = len(device_list)
  
  if num_devices == 0:
    print("      ... we have an empty device_list")
    print("         ... problems during trying many methods are not")
    print("             surprising, nor are they a big deal")
    raise Exception("Problem with pylspci; " + \
                    "on to the next info-collection attempt")
  ##endof:  if num_devices == 0
  
  for i in range(num_devices):
    print()
    this_device = device_list[i]
    this_cls = this_device.cls
    
    is_likely_graphics = find_if_is_likely_graphics(this_device)
    
    if ( (not is_likely_graphics) and (do_only_likely_graphics) ):
      continue
    ##endof:  if ( (not is_likely_graphics) and (do_only_likely_graphics) )
    
    print("\n", "+"*big_plus_width, "\n", "device at index:", str(i))
    
    if do_output_short_info:
      print("\n", "Type of my_device: ", str(type(my_device)), "\n", 
            "my_cls as a string:", str(my_cls), "\n", 
            "Type of my_cls", str(type(my_cls))
      )
    ##endof:  if do_output_short_info
    
    if do_output_if_likely_graphics:
      is_likely_graphics = find_if_is_likely_graphics(this_device)
      print("\n", "-"*little_hyphen_width)
      print(f" is_likely_graphics: , {is_likely_graphics}")
      print("", "-"*little_hyphen_width, "\n")
    ##endof:  if do_output_if_likely_graphics
    
    if do_output_long_info:
      output_long_info(this_device)
    ##endof:  if do_output_long_info
    
    print("+"*big_plus_width, "\n\n")
    
  ##endof:  for i in range(len(device_list))
##endof:  print_all_pci_devices_from_lspci(<params>)


def find_if_is_likely_graphics(the_device):
  '''
  
  '''
  
  return ( "VGA" in str(the_device.cls) )
##endof:  find_if_is_likely_graphics(the_device)


def output_long_info(the_device):
  '''
  Info from pylspci, which wraps lspci
  '''
  
  all_device_info_str = str(the_device)
  all_device_info_str = re.sub(r"([(,][ ]?)([0-9A-Za-z_]+[=])",
                                "\g<1>\n     \g<2>",
                                all_device_info_str,
                                flags=re.I|re.M
                        )
  all_device_info_str = re.sub(r"(.)([)])$",
                                "\g<1>\n\g<2>",
                                all_device_info_str
                        )
  print("\n", "All device information:", "\n",
        all_device_info_str, "\n", 
  )
##endof:  output_long_info(the_device)


def print_qwqfetch_screenfetch_sysinfo():
  '''
  
  '''
  
  print(get_qwqfetch_screenfetch_sysinfo())
  
##endof:  print_qwqfetch_screenfetch_sysinfo()


def get_qwqfetch_screenfetch_sysinfo():
  '''
  
  '''
  
  global first_replace
  global second_replace
  
  ret_str = qwqfetch.get_result(False).split(
               "\n\n"
             )[0].replace(
                     first_replace, 
                     first_replace_prime
                ).replace(
                  second_replace, 
                  second_replace_prime
                )
  return ret_str
##endof:  print_qwqfetch_screenfetch_sysinfo()


if __name__ == "__main__":
  #''' The script is called from the command-line '''
  main()
##endof:  if __name__ == "__main__"