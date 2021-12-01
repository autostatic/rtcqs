#!/usr/bin/env python3

import os
import getpass
import grp
import glob
import re
import gzip

user = getpass.getuser()
wiki_url = "https://wiki.linuxaudio.org/wiki/system_configuration"
gui_status = False
status = {}
kernel = {}
output = {}


def version():
    print_cli("rtcqs-python - version 0.1.0")
    print_cli("")


def print_cli(message):
    if not gui_status:
        print(message)


def print_status(check):
    if not gui_status:
        if status[check]:
            print('[ \033[32mOK\033[00m ] ', end='')
        else:
            print('[ \033[31mWARNING\033[00m ] ', end='')


def root_check():
    if user == 'root':
        status['root'] = False
        output['root'] = "You are running this script as root. Please run " \
            "it as a regular user for the most reliable results."

    else:
        status['root'] = True
        output['root'] = "Not running as root."

    print_cli("Root Check")
    print_cli("==========")
    print_status('root')
    print_cli(output['root'])
    print_cli("")


def audio_group_check():
    wiki_anchor = '#audio_group'
    gid = os.getgid()
    gids = os.getgrouplist(user, gid)
    groups = [grp.getgrgid(gid)[0] for gid in gids]

    if 'audio' not in groups:
        status['audio_group'] = False
        output['audio_group'] = f"User {user} is currently not in the audio " \
            "group. Add yourself to the audio group with 'sudo usermod -a " \
            f"-G audio {user}' and log in again. See also: " \
            f"{wiki_url}{wiki_anchor}"
    else:
        status['audio_group'] = True
        output['audio_group'] = f"User {user} is in the audio group."

    print_cli("Audio Group")
    print_cli("===========")
    print_status('audio_group')
    print_cli(output['audio_group'])
    print_cli("")


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
        status['background_process'] = False
        for proc in procs_bad_list:
            output['background_process'] = "Found resource-intensive " \
                f"process '{proc}'. Please try stopping and/or disabling " \
                "this process."
        print_cli(f"See also: {wiki_url}{wiki_anchor}")
    else:
        status['background_process'] = True
        output['background_process'] = "No resource intensive background " \
            "processes found."

    print_cli("Background Processes")
    print_cli("====================")
    print_status('background_process')
    print_cli(output['background_process'])
    print_cli("")


def governor_check():
    wiki_anchor = '#cpu_frequency_scaling'
    cpu_count = os.cpu_count()
    cpu_dir = '/sys/devices/system/cpu'
    cpu_list = []
    cpu_governor = {}
    bad_governor = 0

    for cpu_nr in range(cpu_count):
        with open(
                f'{cpu_dir}/cpu{cpu_nr}/cpufreq/scaling_governor', 'r') as f:
            cpu_governor[cpu_nr] = f.readline().strip()
            cpu_list.append(f'CPU {cpu_nr}: {cpu_governor[cpu_nr]}')

    for value in cpu_governor.values():
        if value != 'performance':
            bad_governor += 1

    if bad_governor > 0:
        status['governor'] = False
        output['governor'] = "The scaling governor of one or more CPU's is " \
            " not set to 'performance'. You can set the scaling governor to " \
            "'performance' with 'cpupower frequency-set -g performance' " \
            "or 'cpufreq-set -r -g performance' (Debian/Ubuntu). See " \
            f"also: {wiki_url}{wiki_anchor}"
    else:
        status['governor'] = True
        output['governor'] = "The scaling governor of all CPU's is set at " \
            "performance."

    print_cli("CPU Frequency Scaling")
    print_cli("=====================")

    for cpu in cpu_list:
        print_cli(cpu)

    print_cli("")
    print_status('governor')
    print_cli(output['governor'])
    print_cli("")


def kernel_config_check():
    kernel['release'] = os.uname().release

    with open('/proc/cmdline', 'r') as f:
        kernel['cmdline'] = f.readline().strip().split()

    if os.path.exists('/proc/config.gz'):
        status['kernel_config'] = True
        output['kernel_config'] = "Valid kernel configuration found."
        with gzip.open('/proc/config.gz', 'r') as f:
            kernel['config'] = [l.strip() for l in f.readlines()]
    elif os.path.exists(f'/boot/config-{kernel["release"]}'):
        status['kernel_config'] = True
        output['kernel_config'] = "Valid kernel configuration found."
        with open(f'/boot/config-{kernel["release"]}', 'r') as f:
            kernel['config'] = [l.strip() for l in f.readlines()]
    else:
        status['kernel_config'] = False
        output['kernel_config'] = "Could not find kernel configuration."

    print_cli("Kernel Configuration")
    print_cli("====================")
    print_status('kernel_config')
    print_cli(output['kernel_config'])
    print_cli("")


def high_res_timers_check():
    wiki_anchor = '#installing_a_real-time_kernel'

    if 'CONFIG_HIGH_RES_TIMERS=y' not in kernel['config']:
        status['high_res_timers'] = False
        output['high_res_timers'] = "High resolution timers are not " \
            "enabled. Try enabling high-resolution timers " \
            "(CONFIG_HIGH_RES_TIMERS) under 'Processor type and features'). " \
            f"See also: {wiki_url}{wiki_anchor}"
    else:
        status['high_res_timers'] = True
        output['high_res_timers'] = "High resolution timers are enabled."

    print_cli("High Resolution Timers")
    print_cli("======================")
    print_status('high_res_timers')
    print_cli(output['high_res_timers'])
    print_cli("")


def system_timer_check():
    wiki_anchor = '#installing_a_real-time_kernel'

    if 'CONFIG_HZ=1000' not in kernel['config'] and \
            'CONFIG_HIGH_RES_TIMERS=y' not in kernel['config']:
        status['system_timer'] = False
        output['system_timer'] = "CONFIG_HZ is not set at 1000 Hz. Try " \
            "setting CONFIG_HZ to 1000 and/or enabling " \
            f"CONFIG_HIGH_RES_TIMERS. See also: {wiki_url}{wiki_anchor}"
    elif 'CONFIG_HZ=1000' not in kernel['config'] and \
            'CONFIG_HIGH_RES_TIMERS=y' in kernel['config']:
        status['system_timer'] = True
        output['system_timer'] = "System timer is not 1000 Hz but high " \
            "resolution timers are enabled."
    elif 'CONFIG_HZ=1000' in kernel['config'] and \
            'CONFIG_HIGH_RES_TIMERS=y' in kernel['config']:
        status['system_timer'] = True
        output['system_timer'] = "System timer is set at 1000 Hz and high " \
            "resolution timers are enabled."

    print_cli("System Timer")
    print_cli("============")
    print_status('system_timer')
    print_cli(output['system_timer'])
    print_cli("")


def tickless_check():
    wiki_anchor = '#installing_a_real-time_kernel'

    if 'CONFIG_NO_HZ=y' not in kernel['config'] and \
            'CONFIG_NO_HZ_IDLE=y' not in kernel['config']:
        status['tickless'] = False
        output['tickless'] = "Tickless timer support is not not set. Try " \
            "enabling tickless timer support (CONFIG_NO_HZ_IDLE, or " \
            "CONFIG_NO_HZ in older kernels). See also: " \
            f"{wiki_url}{wiki_anchor}"
    else:
        status['tickless'] = True
        output['tickless'] = "System is using a tickless kernel."

    print_cli("Tickless Kernel")
    print_cli("===============")
    print_status('tickless')
    print_cli(output['tickless'])
    print_cli("")


def preempt_rt_check():
    wiki_anchor = '#do_i_really_need_a_real-time_kernel'
    threadirqs = preempt = False

    if 'threadirqs' in kernel['cmdline']:
        threadirqs = True

    if 'CONFIG_PREEMPT_RT=y' in kernel['config'] or \
            'CONFIG_PREEMPT_RT_FULL=y' in kernel['config']:
        preempt = True

    if not threadirqs and not preempt:
        status['preempt_rt'] = False
        output['preempt_rt'] = f"Kernel {kernel['release']} without " \
            "'threadirqs' parameter or real-time capabilities found. See " \
            f"also: {wiki_url}{wiki_anchor}"
    elif threadirqs:
        status['preempt_rt'] = True
        output['preempt_rt'] = f"Kernel {kernel['release']} is using " \
            "threaded IRQ's."
    elif preempt:
        status['preempt_rt'] = True
        output['preempt_rt'] = f"Kernel {kernel['release']} is a real-time " \
            "kernel."

    print_cli("Preempt RT")
    print_cli("==========")
    print_status('preempt_rt')
    print_cli(output['preempt_rt'])
    print_cli("")


def mitigations_check():
    wiki_anchor = "#disabling_spectre_and_meltdown_mitigations"

    if 'mitigations=off' not in kernel['cmdline']:
        status['mitigations'] = False
        output['mitigations'] = "Kernel with Spectre/Meltdown mitigations " \
            "found. This could have a negative impact on the performance of " \
            f"your system. See also: {wiki_url}{wiki_anchor}"
    else:
        status['mitigations'] = True
        output['mitigations'] = "Spectre/Meltdown mitigations are disabled. " \
            "Be warned that this makes your system more vulnerable to " \
            "Spectre/Meltdown attacks."

    print_cli("Spectre/Meltdown Mitigations")
    print_cli("============================")
    print_status('mitigations')
    print_cli(output['mitigations'])
    print_cli("")


def rt_prio_check():
    wiki_anchor = '#limitsconfaudioconf'
    param = os.sched_param(80)
    sched = os.SCHED_RR

    try:
        os.sched_setscheduler(0, sched, param)
    except PermissionError as e:
        status['rt_prio'] = False
        output['rt_prio'] = "Could not assign a 80 rtprio SCHED_FIFO value " \
            f"due to the following error: {e}. Set up limits.conf. See also " \
            f"{wiki_url}{wiki_anchor}"
    else:
        status['rt_prio'] = True
        output['rt_prio'] = "Realtime priorities can be set."

    print_cli("RT Priorities")
    print_cli("=============")
    print_status('rt_prio')
    print_cli(output['rt_prio'])
    print_cli("")


def swappiness_check():
    wiki_anchor = '#sysctlconf'

    with open('/proc/swaps', 'r') as f:
        lines = f.readlines()

    if len(lines) < 2:
        swap = False
        status['swappiness'] = True
        output['swappiness'] = "Your system is configured without swap, " \
            "setting swappiness does not apply."
    else:
        swap = True

    if swap:
        with open('/proc/sys/vm/swappiness', 'r') as f:
            swappiness = int(f.readline().strip())

        if swappiness > 10:
            status['swappiness'] = False
            output['swappiness'] = f"vm.swappiness is set to {swappiness} " \
                "which is too high. Set swappiness to a lower value by " \
                "adding 'vm.swappiness=10' to /etc/sysctl.conf and run " \
                f"'sysctl --system'. See also {wiki_url}{wiki_anchor}"
        else:
            status['swappiness'] = True
            output['swappiness'] = f"Swappiness is set at {swappiness}."

    print_cli("Swappiness")
    print_cli("==========")
    print_status('swappiness')
    print_cli(output['swappiness'])
    print_cli("")


def max_user_watches_check():
    wiki_anchor = "#sysctlconf"

    with open('/proc/sys/fs/inotify/max_user_watches', 'r') as f:
        max_user_watches = int(f.readline().strip())

    if max_user_watches < 524288:
        status['max_user_watches'] = False
        output['max_user_watches'] = f"The max_user_watches setting is set " \
            f"to {max_user_watches} which might be too low when working " \
            "with a high number of files that change a lot. Try increasing " \
            "the setting to at least 524288 or higher. See also " \
            f"{wiki_url}{wiki_anchor}"
    else:
        status['max_user_watches'] = True
        output['max_user_watches'] = f"max_user_watches has been set to " \
            f"{max_user_watches} which is sufficient."

    print_cli("Maximum User Watches")
    print_cli("====================")
    print_status('max_user_watches')
    print_cli(output['max_user_watches'])
    print_cli("")


def filesystems_check():
    wiki_anchor = "#filesystems"
    good_fs = ['ext4', 'xfs', 'zfs', 'btrfs']
    bad_fs = ['fuse', 'reiserfs', 'nfs']
    bad_mounts = ['/boot']
    good_mounts_list = []
    bad_mounts_list = []

    with open('/proc/mounts', 'r') as f:
        mounts = [l.split() for l in f.readlines()]

    for mount in mounts:
        mount_split = mount[2].split('.')[0]
        if mount_split in good_fs and mount[1] not in bad_mounts:
            good_mounts_list.append(mount[1])
        elif mount_split in bad_fs or mount[1] in bad_mounts:
            bad_mounts_list.append(mount[1])

    print_cli("Filesystems")
    print_cli("===========")

    if len(good_mounts_list) > 0:
        good_mounts = ', '.join(good_mounts_list)
        status['filesystems'] = True
        output['filesystems'] = "The following mounts can be used for audio " \
            f"purposes: {good_mounts}"
        print_status('filesystems')
        print_cli(output['filesystems'])

    if len(bad_mounts_list) > 0:
        bad_mounts = ', '.join(bad_mounts_list)
        status['filesystems'] = False
        output['filesystems'] = "The following mounts should be avoided for " \
            f"audio purposes: {bad_mounts}. See also {wiki_url}{wiki_anchor}"
        print_status('filesystems')
        print_cli(output['filesystems'])

    print_cli("")


def gui():
    global gui_status
    gui_status = True
    main()


def main():
    version()
    root_check()
    audio_group_check()
    background_check()
    governor_check()
    kernel_config_check()
    high_res_timers_check()
    system_timer_check()
    tickless_check()
    preempt_rt_check()
    mitigations_check()
    rt_prio_check()
    swappiness_check()
    max_user_watches_check()
    filesystems_check()


if __name__ == "__main__":
    main()
