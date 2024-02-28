#!/usr/bin/env python3

import os
import getpass
import re
import gzip
import resource

user = getpass.getuser()
wiki_url = "https://wiki.linuxaudio.org/wiki/system_configuration"
gui_status = False
version = "0.5.5"
headline = {}
kernel = {}
output = {}
status = {}


def print_version():
    print_cli(f"rtcqs - version {version}")
    print_cli("")


def print_cli(message):
    if not gui_status:
        print(message)


def print_status(check):
    if not gui_status:
        if status[check]:
            print("[ \033[32mOK\033[00m ] ", end="")
        else:
            print("[ \033[31mWARNING\033[00m ] ", end="")


def format_output(check):
    char_count = int(len(headline[check]))
    print_cli(headline[check])
    print_cli(char_count * "=")
    print_status(check)
    print_cli(output[check])
    print_cli("")


def root_check():
    check = "root"
    headline[check] = "Root User"

    if user == "root":
        status[check] = False
        output[check] = "You are running this script as root. Please run " \
            "it as a regular user for the most reliable results."

    else:
        status[check] = True
        output[check] = "Not running as root."

    format_output(check)


def audio_group_check():
    check = "audio_group"
    headline[check] = "Group Limits"
    wiki_anchor = "#audio_group"
    limit_rtprio = resource.getrlimit(resource.RLIMIT_RTPRIO)[1]
    limit_memlock = resource.getrlimit(resource.RLIMIT_MEMLOCK)[1]

    if limit_rtprio >= 75 and limit_memlock == -1:
        status[check] = True
        output[check] = f"User {user} is member of a group that has " \
                        f"sufficient rtprio ({limit_rtprio}) and " \
                        " memlock (unlimited) limits set."
    else:
        status[check] = False
        output[check] = f"User {user} is currently not member of a group " \
                        f"that has sufficient rtprio ({limit_rtprio}) and " \
                        f"memlock ({limit_memlock}) set. Add yourself to a " \
                        "group with sufficent limits set, i.e. audio or " \
                        "realtime, with 'sudo usermod -a -G <group_name> " \
                        f"{user}. See also {wiki_url}{wiki_anchor}"

    format_output(check)


def governor_check():
    check = "governor"
    headline[check] = "CPU Frequency Scaling"
    wiki_anchor = "#cpu_frequency_scaling"
    cpu_count = os.cpu_count()
    cpu_dir = "/sys/devices/system/cpu"
    cpu_list = []
    cpu_governor = {}
    bad_governor = 0

    with open("/sys/devices/system/cpu/smt/active", "r") as f:
        cpu_smt = f.readline().strip()

    for cpu_nr in range(cpu_count):
        governor_path = f"{cpu_dir}/cpu{cpu_nr}/cpufreq/scaling_governor"

        try:
            with open(governor_path, "r") as f:
                cpu_governor[cpu_nr] = f.readline().strip()
                cpu_list.append(f"CPU {cpu_nr}: {cpu_governor[cpu_nr]}")
        except OSError as e:
            if e.errno == 16 and not cpu_smt:
                pass

    for value in cpu_governor.values():
        if value != "performance":
            bad_governor += 1

    if bad_governor > 0:
        status[check] = False
        output[check] = "The scaling governor of one or more CPUs is " \
            "not set to 'performance'. You can set the scaling governor to " \
            "'performance' with 'cpupower frequency-set -g performance' " \
            "or 'cpufreq-set -r -g performance' (Debian/Ubuntu). See " \
            f"also {wiki_url}{wiki_anchor}"
    else:
        status[check] = True
        output[check] = "The scaling governor of all CPUs is set to " \
            "performance."

    format_output(check)


def kernel_config_check():
    check = "kernel_config"
    headline[check] = "Kernel Configuration"
    kernel["release"] = os.uname().release

    with open("/proc/cmdline", "r") as f:
        kernel["cmdline"] = f.readline().strip().split()

    if os.path.exists("/proc/config.gz"):
        status[check] = True
        output[check] = "Valid kernel configuration found."
        with gzip.open("/proc/config.gz", "r") as f:
            kernel["config"] = [
                line.strip().decode() for line in f.readlines()]
    elif os.path.exists(f"/boot/config-{kernel['release']}"):
        status[check] = True
        output[check] = "Valid kernel configuration found."
        with open(f"/boot/config-{kernel['release']}", "r") as f:
            kernel["config"] = [
                line.strip() for line in f.readlines()]
    else:
        status[check] = False
        output[check] = "Could not find kernel configuration."

    format_output(check)


def high_res_timers_check():
    check = "high_res_timers"
    headline[check] = "High Resolution Timers"
    wiki_anchor = "#installing_a_real-time_kernel"

    if "CONFIG_HIGH_RES_TIMERS=y" not in kernel["config"]:
        status[check] = False
        output[check] = "High resolution timers are not " \
            "enabled. Try enabling high-resolution timers " \
            "(CONFIG_HIGH_RES_TIMERS) under 'Processor type and features'). " \
            f"See also: {wiki_url}{wiki_anchor}"
    else:
        status[check] = True
        output[check] = "High resolution timers are enabled."

    format_output(check)


def tickless_check():
    check = "tickless"
    headline[check] = "Tickless Kernel"
    wiki_anchor = "#installing_a_real-time_kernel"
    conf_nohz_list = [
        "CONFIG_NO_HZ=y",
        "CONFIG_NO_HZ_IDLE=y",
        "CONFIG_NO_HZ_COMMON=y",
        "CONFIG_NO_HZ_FULL=y"]

    conf_nohz_match = [
        match for match in conf_nohz_list if match in kernel["config"]]

    if int(len(conf_nohz_match)) > 0 or \
            os.path.exists("/sys/devices/system/cpu/nohz_full"):
        status[check] = True
        output[check] = "System is using a tickless kernel."
    else:
        status[check] = False
        output[check] = "Tickless timer support is not set. Try " \
            "enabling tickless timer support (CONFIG_NO_HZ_IDLE, or " \
            "CONFIG_NO_HZ in older kernels). See also " \
            f"{wiki_url}{wiki_anchor}"

    format_output(check)


def preempt_rt_check():
    check = "preempt_rt"
    headline[check] = "Preempt RT"
    wiki_anchor = "#do_i_really_need_a_real-time_kernel"
    threadirqs = preempt = False

    if "threadirqs" in kernel["cmdline"]:
        threadirqs = True

    if "CONFIG_PREEMPT_RT=y" in kernel["config"] or \
            "CONFIG_PREEMPT_RT_FULL=y" in kernel["config"] or \
            "preempt=full" in kernel["cmdline"]:
        preempt = True

    if not threadirqs and not preempt:
        status[check] = False
        output[check] = f"Kernel {kernel['release']} without " \
            "'threadirqs' parameter or real-time capabilities found. See " \
            f"also {wiki_url}{wiki_anchor}"
    elif threadirqs:
        status[check] = True
        output[check] = f"Kernel {kernel['release']} is using " \
            "threaded IRQs."
    elif preempt:
        status[check] = True
        output[check] = f"Kernel {kernel['release']} is a real-time " \
            "kernel."

    format_output(check)


def mitigations_check():
    check = "mitigations"
    headline[check] = "Spectre/Meltdown Mitigations"
    wiki_anchor = "#disabling_spectre_and_meltdown_mitigations"

    if "mitigations=off" not in kernel["cmdline"]:
        status[check] = False
        output[check] = "Kernel with Spectre/Meltdown mitigations " \
            "found. This could have a negative impact on the performance of " \
            f"your system. See also {wiki_url}{wiki_anchor}"
    else:
        status[check] = True
        output[check] = "Spectre/Meltdown mitigations are disabled. " \
            "Be warned that this makes your system more vulnerable to " \
            "Spectre/Meltdown attacks."

    format_output(check)


def rt_prio_check():
    check = "rt_prio"
    headline[check] = "RT Priorities"
    wiki_anchor = "#limitsconfaudioconf"
    param = os.sched_param(80)
    sched = os.SCHED_FIFO

    try:
        os.sched_setscheduler(0, sched, param)
    except PermissionError as e:
        status[check] = False
        output[check] = "Could not assign a 80 rtprio SCHED_FIFO value " \
            f"due to the following error: {e}. Set up limits.conf. See also " \
            f"{wiki_url}{wiki_anchor}"
    else:
        status[check] = True
        output[check] = "Realtime priorities can be set."

    format_output(check)


def swappiness_check():
    check = "swappiness"
    headline[check] = "Swappiness"
    wiki_anchor = "#sysctlconf"

    with open("/proc/swaps", "r") as f:
        lines = f.readlines()

    if len(lines) < 2:
        swap = False
        status[check] = True
        output[check] = "Your system is configured without swap, " \
            "setting swappiness does not apply."
    else:
        swap = True

    if swap:
        with open("/proc/sys/vm/swappiness", "r") as f:
            swappiness = int(f.readline().strip())

        if swappiness > 10:
            status[check] = False
            output[check] = f"vm.swappiness is set to {swappiness} " \
                "which is too high. Set swappiness to a lower value by " \
                "adding 'vm.swappiness=10' to /etc/sysctl.conf and run " \
                f"'sysctl --system'. See also {wiki_url}{wiki_anchor}"
        else:
            status[check] = True
            output[check] = f"Swappiness is set at {swappiness}."

    format_output(check)


def filesystems_check():
    check = "filesystems"
    headline[check] = "Filesystems"
    wiki_anchor = "#filesystems"
    good_fs = ["ext4", "xfs", "zfs", "btrfs"]
    bad_fs = ["fuse", "reiserfs", "nfs", "cifs"]
    bad_mounts = ["/boot"]
    ignore_mounts = ["/run"]
    good_mounts_list = []
    bad_mounts_list = []

    with open("/proc/mounts", "r") as f:
        mounts = [line.split() for line in f.readlines()]

    for mount in mounts:
        mount_split = mount[2].split(".")[0]
        mount_point = mount[1]
        mount_top_dir = f"/{mount_point.split('/')[1]}"
        if mount_split in good_fs and mount_point not in bad_mounts:
            good_mounts_list.append(mount_point)
        elif (mount_split in bad_fs or mount_point in bad_mounts) and \
                mount_top_dir not in ignore_mounts:
            bad_mounts_list.append(mount_point)

    print_cli(headline[check])
    print_cli("===========")

    if len(good_mounts_list) > 0:
        good_mounts = ", ".join(good_mounts_list)
        status[check] = True
        output[check] = "The following mounts can be used for audio " \
            f"purposes: {good_mounts}"
        print_status('filesystems')
        print_cli(output['filesystems'])

    if len(bad_mounts_list) > 0:
        bad_mounts = ', '.join(bad_mounts_list)
        status[check] = False
        output[check] = "The following mounts should be avoided for " \
            f"audio purposes: {bad_mounts}. See also {wiki_url}{wiki_anchor}"
        print_status(check)
        print_cli(output[check])

    print_cli("")


def irq_check():
    check = "irqs"
    headline[check] = "IRQs"
    bad_irq_list = []
    good_irq_list = []
    snd_list = ["audiodsp", "snd_.*"]
    snd_re = "|".join(snd_list)
    usb_re = "[e,u,x]hci_hcd"
    snd_compiled_re = re.compile(snd_re)
    usb_compiled_re = re.compile(usb_re)
    output_irq = {}
    irq_path = "/sys/kernel/irq"
    irq_path_list = os.listdir(irq_path)

    for irq in irq_path_list:
        with open(f"{irq_path}/{irq}/actions", "r") as f:
            devices = f.readline().strip()

        device_list = devices.split(", ")

        if snd_compiled_re.search(devices):
            if len(device_list) > 1:
                bad_irq_list.append(irq)
                status["snd_irqs"] = False
                output_irq[irq] = f"Soundcard {device_list[0]} with IRQ " \
                    f"{irq} shares its IRQ with the following other devices " \
                    f"{devices}"
            else:
                good_irq_list.append(irq)
                status["snd_irqs"] = True
                output_irq[irq] = f"Soundcard {device_list[0]} with IRQ " \
                    f"{irq} does not share its IRQ."
        if usb_compiled_re.search(devices):
            if len(device_list) > 1:
                bad_irq_list.append(irq)
                status["usb_irqs"] = False
                output_irq[irq] = f"Found USB port {device_list[0]} with " \
                    f"IRQ {irq} that shares its IRQ with the following " \
                    f"other devices: {devices}"
            else:
                good_irq_list.append(irq)
                status["usb_irqs"] = True
                output_irq[irq] = f"USB port {device_list[0]} with IRQ " \
                    f"{irq} does not share its IRQ."

    print_cli(headline[check])
    print_cli("====")

    if len(good_irq_list) > 0:
        status[check] = True
        output[check] = "\n".join(
            [output_irq[good_irq] for good_irq in good_irq_list])

        for good_irq in good_irq_list:
            print_status(check)
            print_cli(output_irq[good_irq])

    if len(bad_irq_list) > 0:
        status[check] = False
        output[check] = "\n".join(
            [output_irq[bad_irq] for bad_irq in bad_irq_list])

        for bad_irq in bad_irq_list:
            print_status(check)
            print_cli(output_irq[bad_irq])

    print_cli("")


def power_management_check():
    check = "power_management"
    headline[check] = "Power Management"
    wiki_anchor = "#quality_of_service_interface"

    if os.access("/dev/cpu_dma_latency", os.W_OK):
        status[check] = True
        output[check] = "Power management can be controlled from user " \
                        "space. This enables DAWs like Ardour and Reaper " \
                        "to set CPU DMA latency which could help prevent " \
                        "xruns."
    else:
        status[check] = False
        output[check] = "Power management can't be controlled from user " \
                        "space, the device node /dev/cpu_dma_latency can't " \
                        "be accessed by your user. This prohibits DAWs " \
                        "like Ardour and Reaper to set CPU DMA latency " \
                        "which could help prevent xruns. For enabling " \
                        f"access see {wiki_url}{wiki_anchor}"

    format_output(check)


def main():
    print_version()
    root_check()
    audio_group_check()
    governor_check()
    kernel_config_check()
    high_res_timers_check()
    tickless_check()
    preempt_rt_check()
    mitigations_check()
    rt_prio_check()
    swappiness_check()
    filesystems_check()
    irq_check()
    power_management_check()


if __name__ == "__main__":
    main()
