#!/usr/bin/env python3

import os
import getpass
import grp
import glob
import re
import gzip

user = getpass.getuser()
wiki_url = "https://wiki.linuxaudio.org/wiki/system_configuration"


def audio_group_check():
    wiki_anchor = '#audio_group'
    gid = os.getgid()
    gids = os.getgrouplist(user, gid)
    groups = [grp.getgrgid(gid)[0] for gid in gids]
    if 'audio' not in groups:
        print(f"User {user} is currently not in the audio group. Add yourself "
              f"to the audio group with 'sudo usermod -a -G audio {user}' and "
              f"log in again. See also: {wiki_url}{wiki_anchor}")


def background_check():
    wiki_anchor = \
        '#disabling_resource-intensive_daemons_services_and_processes'
    procs = ['powersaved', 'kpowersave']
    proc_re = '|'.join(procs)
    proc_compiled_re = re.compile(f'.*({proc_re}).*')
    procs_list = []
    procs_list_dirs = [
        dir for dir in glob.glob(os.path.join('/proc/', '[0-9]*'))]

    for dir in procs_list_dirs:
        cmdline = f'{dir}/cmdline'
        with open(cmdline, 'r') as f:
            cmd = f.readline().replace('\x00', ' ').rstrip()
        if cmd != '':
            procs_list.append(cmd)

    for proc in procs_list:
        if proc_compiled_re.search(proc):
            print(f"Found resource-intensive process '{proc}'. Please try "
                  "stopping and/or disabling this process. See also: "
                  f"{wiki_url}{wiki_anchor}")


def governor_check():
    wiki_anchor = '#cpu_frequency_scaling'
    cpu_count = os.cpu_count()
    cpu_dir = '/sys/devices/system/cpu'
    cpu_governor = {}
    bad_governor = 0

    for cpu_nr in range(cpu_count):
        with open(
                f'{cpu_dir}/cpu{cpu_nr}/cpufreq/scaling_governor', 'r') as f:
            cpu_governor[cpu_nr] = f.readline().strip()
            print(f'CPU {cpu_nr}: {cpu_governor[cpu_nr]}')

    for value in cpu_governor.values():
        if value != 'performance':
            bad_governor += 1

    if bad_governor > 0:
        print(f"The scaling governor of one or more CPU's is not set to "
              "'performance'. You can set the scaling governor to "
              "'performance' with 'cpupower frequency-set -g performance' "
              "or 'cpufreq-set -r -g performance' (Debian/Ubuntu). See "
              f"also: {wiki_url}{wiki_anchor}")


def kernel_config_check():
    kernel_release = os.uname().release

    if os.path.exists('/proc/config.gz'):
        with gzip.open('/proc/config.gz', 'r') as f:
            kernel_config = [l.strip() for l in f.readlines()]
    elif os.path.exists(f'/boot/config-{kernel_release}'):
        with open(f'/boot/config-{kernel_release}', 'r') as f:
            kernel_config = [l.strip() for l in f.readlines()]

    else:
        print('Could not find kernel configuration')

    return kernel_config


def high_res_timers_check(kernel_config):
    wiki_anchor = '#installing_a_real-time_kernel'

    if 'CONFIG_HIGH_RES_TIMERS=y' not in kernel_config:
        print("High resolution timers are not enabled. Try enabling "
              "high-resolution timers (CONFIG_HIGH_RES_TIMERS "
              "under 'Processor type and features'). See also: "
              f"{wiki_url}{wiki_anchor}")


def hz_1000_check(kernel_config):
    wiki_anchor = '#installing_a_real-time_kernel'

    if 'CONFIG_HZ=1000' not in kernel_config and \
            'CONFIG_HIGH_RES_TIMERS=y' not in kernel_config:
        print("CONFIG_HZ is not set at 1000 Hz. Try setting CONFIG_HZ to 1000 "
              "and/or enabling CONFIG_HIGH_RES_TIMERS. See also: "
              f"{wiki_url}{wiki_anchor}")


def no_hz_check(kernel_config):
    wiki_anchor = '#installing_a_real-time_kernel'

    if 'CONFIG_NO_HZ=y' not in kernel_config and \
            'CONFIG_NO_HZ_IDLE=y' not in kernel_config:
        print("Tickless timer support is not not set. Try enabling tickless "
              "timer support (CONFIG_NO_HZ_IDLE, or CONFIG_NO_HZ in older "
              f"kernels). See also: {wiki_url}{wiki_anchor}")


def preempt_rt_check(kernel_config):
    wiki_anchor = '#do_i_really_need_a_real-time_kernel'
    threadirqs = preempt = False

    with open('/proc/cmdline', 'r') as f:
        cmd_line = f.readline().strip().split()

    if 'threadirqs' in cmd_line:
        threadirqs = True

    if 'CONFIG_PREEMPT_RT=y' not in kernel_config or \
            'CONFIG_PREEMPT_RT_FULL=y' not in kernel_config:
        preempt = True

    if not threadirqs or preempt:
        print("Kernel without 'threadirqs' parameter or real-time "
              f"capabilities found. See also: {wiki_url}{wiki_anchor}")


def root_check():
    if user == 'root':
        print("You are running this script as root. Please run it as a "
              "regular user for the most reliable results.")


def rt_prio_check():
    wiki_anchor = '#limitsconfaudioconf'
    param = os.sched_param(80)
    sched = os.SCHED_RR

    try:
        os.sched_setscheduler(0, sched, param)
    except PermissionError as e:
        print("Could not assign a 80 rtprio SCHED_FIFO value due to the "
              f"following error: {e}. Set up limits.conf. See also "
              f"{wiki_url}{wiki_anchor}")


def swappiness_check():
    wiki_anchor = '#sysctlconf'

    with open('/proc/swaps', 'r') as f:
        lines = f.readlines()

    if len(lines) < 2:
        swap = False
        print("Your system is configured without swap, setting swappiness "
              "does not apply.")
    else:
        swap = True

    if swap:
        with open('/proc/sys/vm/swappiness', 'r') as f:
            swappiness = int(f.readline().strip())

        if swappiness > 10:
            print(f"vm.swappiness is set to {swappiness} which is too high. "
                  "Set swappiness to a lower value by adding "
                  "'vm.swappiness=10' to /etc/sysctl.conf and run "
                  "'sysctl --system'. See also "
                  f"{wiki_url}{wiki_anchor}")


def main():
    root_check()
    audio_group_check()
    background_check()
    governor_check()
    kernel_config = kernel_config_check()
    high_res_timers_check(kernel_config)
    hz_1000_check(kernel_config)
    no_hz_check(kernel_config)
    preempt_rt_check(kernel_config)
    rt_prio_check()
    swappiness_check()


if __name__ == "__main__":
    main()
