#!/usr/bin/env python3

import os
import getpass
import grp
import glob
import re
import gzip

user = getpass.getuser()
wiki_url = "https://wiki.linuxaudio.org/wiki/system_configuration"
status = {}


def version():
    print("rtcqs-python - version 0.0.0")
    print()


def print_status(check):
    if status[check] == 'OK':
        print(f"[ \033[32m{status[check]}\033[00m ] ", end='')
    elif status[check] == 'WARNING':
        print(f"[ \033[31m{status[check]}\033[00m ] ", end='')


def root_check():
    print("Root Check")
    print("==========")

    if user == 'root':
        status['root'] = "WARNING"
        print_status('root')
        print("You are running this script as root. Please run it as a "
              "regular user for the most reliable results.")
    else:
        status['root'] = "OK"
        print_status('root')
        print("Not running as root.")

    print()


def audio_group_check():
    wiki_anchor = '#audio_group'
    gid = os.getgid()
    gids = os.getgrouplist(user, gid)
    groups = [grp.getgrgid(gid)[0] for gid in gids]

    print("Audio Group")
    print("===========")

    if 'audio' not in groups:
        status['audio_group'] = "WARNING"
        print_status('audio_group')
        print(f"User {user} is currently not in the audio group. Add yourself "
              f"to the audio group with 'sudo usermod -a -G audio {user}' and "
              f"log in again. See also: {wiki_url}{wiki_anchor}")
    else:
        status['audio_group'] = "OK"
        print_status('audio_group')
        print(f"User {user} is in the audio group")

    print()


def background_check():
    wiki_anchor = \
        '#disabling_resource-intensive_daemons_services_and_processes'
    procs = ['powersaved', 'kpowersave']
    proc_re = '|'.join(procs)
    proc_compiled_re = re.compile(f'.*({proc_re}).*')
    procs_list = []
    procs_list_dirs = [
        dir for dir in glob.glob(os.path.join('/proc/', '[0-9]*'))]
    procs_bad_list = []

    print("Background Processes")
    print("====================")

    for dir in procs_list_dirs:
        cmdline = f'{dir}/cmdline'
        with open(cmdline, 'r') as f:
            cmd = f.readline().replace('\x00', ' ').rstrip()
        if cmd != '':
            procs_list.append(cmd)

    for proc in procs_list:
        if proc_compiled_re.search(proc):
            procs_bad_list.append(proc)

    if len(procs_bad_list) > 0:
        status['background_process'] = "WARNING"
        print_status('background_process')
        for proc in procs_bad_list:
            print(f"Found resource-intensive process '{proc}'. Please try "
                  "stopping and/or disabling this process.")
        print(f"See also: {wiki_url}{wiki_anchor}")
    else:
        status['background_process'] = "OK"
        print_status('background_process')
        print("No resource intensive background processes found.")

    print()


def governor_check():
    wiki_anchor = '#cpu_frequency_scaling'
    cpu_count = os.cpu_count()
    cpu_dir = '/sys/devices/system/cpu'
    cpu_governor = {}
    bad_governor = 0

    print("CPU Frequency Scaling")
    print("=====================")

    for cpu_nr in range(cpu_count):
        with open(
                f'{cpu_dir}/cpu{cpu_nr}/cpufreq/scaling_governor', 'r') as f:
            cpu_governor[cpu_nr] = f.readline().strip()
            print(f'CPU {cpu_nr}: {cpu_governor[cpu_nr]}')

    print()

    for value in cpu_governor.values():
        if value != 'performance':
            bad_governor += 1

    if bad_governor > 0:
        status['governor'] = "WARNING"
        print_status('governor')
        print(f"The scaling governor of one or more CPU's is not set to "
              "'performance'. You can set the scaling governor to "
              "'performance' with 'cpupower frequency-set -g performance' "
              "or 'cpufreq-set -r -g performance' (Debian/Ubuntu). See "
              f"also: {wiki_url}{wiki_anchor}")
    else:
        status['governor'] = "OK"
        print_status('governor')
        print("The scaling governor of all CPU's is set at performance.")

    print()


def kernel_config_check():
    kernel_release = os.uname().release

    if os.path.exists('/proc/config.gz'):
        with gzip.open('/proc/config.gz', 'r') as f:
            kernel_config = [l.strip() for l in f.readlines()]
    elif os.path.exists(f'/boot/config-{kernel_release}'):
        with open(f'/boot/config-{kernel_release}', 'r') as f:
            kernel_config = [l.strip() for l in f.readlines()]
    else:
        print("Kernel Configuration")
        print("====================")
        status['kernel_config'] = "WARNING"
        print_status('kernel_config')
        print("Could not find kernel configuration.")
        print()

    return kernel_config


def high_res_timers_check(kernel_config):
    wiki_anchor = '#installing_a_real-time_kernel'

    print("High Resolution Timers")
    print("======================")

    if 'CONFIG_HIGH_RES_TIMERS=y' not in kernel_config:
        status['high_res_timers'] = "WARNING"
        print_status('high_res_timers')
        print("High resolution timers are not enabled. Try enabling "
              "high-resolution timers (CONFIG_HIGH_RES_TIMERS "
              "under 'Processor type and features'). See also: "
              f"{wiki_url}{wiki_anchor}")
    else:
        status['high_res_timers'] = "OK"
        print_status('high_res_timers')
        print("High resolution timers are enabled.")

    print()


def system_timer_check(kernel_config):
    wiki_anchor = '#installing_a_real-time_kernel'

    print("System Timer")
    print("============")

    if 'CONFIG_HZ=1000' not in kernel_config and \
            'CONFIG_HIGH_RES_TIMERS=y' not in kernel_config:
        status['system_timer'] = "WARNING"
        print_status('system_timer')
        print("CONFIG_HZ is not set at 1000 Hz. Try setting CONFIG_HZ to 1000 "
              "and/or enabling CONFIG_HIGH_RES_TIMERS. See also: "
              f"{wiki_url}{wiki_anchor}")
    elif 'CONFIG_HZ=1000' not in kernel_config and \
            'CONFIG_HIGH_RES_TIMERS=y' in kernel_config:
        status['system_timer'] = "OK"
        print_status('system_timer')
        print("System timer is not 1000 Hz but high resolution timers are "
              "enabled.")

    print()


def tickless_check(kernel_config):
    wiki_anchor = '#installing_a_real-time_kernel'

    print("Tickless Kernel")
    print("===============")

    if 'CONFIG_NO_HZ=y' not in kernel_config and \
            'CONFIG_NO_HZ_IDLE=y' not in kernel_config:
        status['no_hz'] = "WARNING"
        print_status('no_hz')
        print("Tickless timer support is not not set. Try enabling tickless "
              "timer support (CONFIG_NO_HZ_IDLE, or CONFIG_NO_HZ in older "
              f"kernels). See also: {wiki_url}{wiki_anchor}")
    else:
        status['no_hz'] = "OK"
        print_status('no_hz')
        print("System is using a tickless kernel.")

    print()


def preempt_rt_check(kernel_config):
    wiki_anchor = '#do_i_really_need_a_real-time_kernel'
    threadirqs = preempt = False

    print("Preempt RT")
    print("==========")

    with open('/proc/cmdline', 'r') as f:
        cmd_line = f.readline().strip().split()

    if 'threadirqs' in cmd_line:
        threadirqs = True

    if 'CONFIG_PREEMPT_RT=y' in kernel_config or \
            'CONFIG_PREEMPT_RT_FULL=y' in kernel_config:
        preempt = True

    if not threadirqs or not preempt:
        status['preempt_rt'] = "WARNING"
        print_status('preempt_rt')
        print("Kernel without 'threadirqs' parameter or real-time "
              f"capabilities found. See also: {wiki_url}{wiki_anchor}")
    elif threadirqs:
        status['preempt_rt'] = "OK"
        print_status('preempt_rt')
        print("Kernel is using threaded IRQ's")
    elif preempt:
        status['preempt_rt'] = "OK"
        print_status('preempt_rt')
        print("System is running a real-time kernel.")

    print()


def mitigations_check():
    wiki_anchor = "#disabling_spectre_and_meltdown_mitigations"

    print("Spectre/Meltdown mitigations")
    print("============================")

    with open('/proc/cmdline', 'r') as f:
        cmd_line = f.readline().strip().split()

    if 'mitigations=off' not in cmd_line:
        status['mitigations'] = "WARNING"
        print_status('mitigations')
        print("Kernel with Spectre/Meltdown mitigations found. This could "
              "have a negative impact on the performance of your system. See "
              f"also: {wiki_url}{wiki_anchor}")
    else:
        status['mitigations'] = "OK"
        print_status('mitigations')
        print("Spectre/Meltdown mitigations are disabled. Be warned that "
              "this makes your system more vulnerable for Spectre/Meltdown "
              "attacks.")

    print()


def rt_prio_check():
    wiki_anchor = '#limitsconfaudioconf'
    param = os.sched_param(80)
    sched = os.SCHED_RR

    print("RT priorities")
    print("=============")

    try:
        os.sched_setscheduler(0, sched, param)
    except PermissionError as e:
        status['rt_prio'] = "WARNING"
        print_status('rt_prio')
        print("Could not assign a 80 rtprio SCHED_FIFO value due to the "
              f"following error: {e}. Set up limits.conf. See also "
              f"{wiki_url}{wiki_anchor}")
    else:
        status['rt_prio'] = "OK"
        print_status('rt_prio')
        print("Realtime priorities can be set.")

    print()


def swappiness_check():
    wiki_anchor = '#sysctlconf'

    print("Swappiness")
    print("==========")

    with open('/proc/swaps', 'r') as f:
        lines = f.readlines()

    if len(lines) < 2:
        swap = False
        status['swappiness'] = "OK"
        print_status('swappiness')
        print("Your system is configured without swap, setting swappiness "
              "does not apply.")
    else:
        swap = True

    if swap:
        with open('/proc/sys/vm/swappiness', 'r') as f:
            swappiness = int(f.readline().strip())

        if swappiness > 10:
            status['swappiness'] = "WARNING"
            print_status('swappiness')
            print(f"vm.swappiness is set to {swappiness} which is too high. "
                  "Set swappiness to a lower value by adding "
                  "'vm.swappiness=10' to /etc/sysctl.conf and run "
                  "'sysctl --system'. See also "
                  f"{wiki_url}{wiki_anchor}")
        else:
            status['swappiness'] = "OK"
            print_status('rt_prio')
            print(f"Swappiness is set at {swappiness}.")

    print()


def max_user_watches_check():
    wiki_anchor = "#sysctlconf"

    print("Maximum User Watches")
    print("====================")

    with open('/proc/sys/fs/inotify/max_user_watches', 'r') as f:
        max_user_watches = int(f.readline().strip())

    if max_user_watches < 524288:
        status['max_user_watches'] = "WARNING"
        print_status('max_user_watches')
        print(f"The max_user_watches setting is set to {max_user_watches} "
              "which might be too low when working with a high number of "
              "files that change a lot. Try increasing the setting to at "
              f"least 524288 or higher. See also {wiki_url}{wiki_anchor}")
    else:
        status['max_user_watches'] = "OK"
        print_status('max_user_watches')
        print(f"max_user_watches has been set to {max_user_watches} which is "
              "sufficient")

    print()


def filesystems():
    wiki_anchor = "#filesystems"
    good_fs = ['ext4', 'xfs', 'zfs', 'btrfs']
    bad_fs = ['fuse', 'reiserfs', 'nfs']
    bad_mounts = ['/boot']
    good_mounts_list = []
    bad_mounts_list = []

    print("Filesystems")
    print("===========")

    with open('/proc/mounts', 'r') as f:
        mounts = [l.split() for l in f.readlines()]

    for mount in mounts:
        mount_split = mount[2].split('.')[0]
        if mount_split in good_fs and mount[1] not in bad_mounts:
            good_mounts_list.append(mount[1])
        elif mount_split in bad_fs or mount[1] in bad_mounts:
            bad_mounts_list.append(mount[1])

    if len(good_mounts_list) > 0:
        good_mounts = ', '.join(good_mounts_list)
        status['filesystems'] = "OK"
        print_status('filesystems')
        print("The following mounts can be used for audio purposes: "
              f"{good_mounts}")

    if len(bad_mounts_list) > 0:
        bad_mounts = ', '.join(bad_mounts_list)
        status['filesystems'] = "WARNING"
        print_status('filesystems')
        print("The following mounts should be avoided for audio purposes: "
              f"{bad_mounts}. See also {wiki_url}{wiki_anchor}")

    print()


def main():
    version()
    root_check()
    audio_group_check()
    background_check()
    governor_check()
    kernel_config = kernel_config_check()
    high_res_timers_check(kernel_config)
    system_timer_check(kernel_config)
    tickless_check(kernel_config)
    preempt_rt_check(kernel_config)
    mitigations_check()
    rt_prio_check()
    swappiness_check()
    max_user_watches_check()
    filesystems()


if __name__ == "__main__":
    main()
