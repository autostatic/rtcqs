#!/usr/bin/env python3

import os
import getpass
import re
import gzip
import resource


class Resources:
    def __init__(self):
        self.transparent_img = b'''
        iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9
        kT1Iw0AcxV9Ti6JVByuIKGSoThZERRy1CkWoEGqFVh1MLv2CJg1Jiouj4Fpw8GOx6uDirKuDqyAI
        foC4uTkpukiJ/0sKLWI9OO7Hu3uPu3eAUC0yzWobBzTdNhOxqJhKr4rtr+jCMPoRQI/MLGNOkuJo
        Ob7u4ePrXYRntT735+hWMxYDfCLxLDNMm3iDeHrTNjjvE4dYXlaJz4nHTLog8SPXFY/fOOdcFnhm
        yEwm5olDxGKuiZUmZnlTI54iDquaTvlCymOV8xZnrVhm9XvyFwYz+soy12kOIYZFLEGCCAVlFFCE
        jQitOikWErQfbeEfdP0SuRRyFcDIsYASNMiuH/wPfndrZScnvKRgFAi8OM7HCNC+C9QqjvN97Di1
        E8D/DFzpDX+pCsx8kl5paOEjoHcbuLhuaMoecLkDDDwZsim7kp+mkM0C72f0TWmg7xboXPN6q+/j
        9AFIUlfxG+DgEBjNUfZ6i3d3NPf275l6fz81GnKOR9SOXAAAAAZiS0dEAP8A/wD/oL2nkwAAAAlw
        SFlzAAAuIwAALiMBeKU/dgAAAAd0SU1FB+ULHRUGGu4roaUAAAAZdEVYdENvbW1lbnQAQ3JlYXRl
        ZCB3aXRoIEdJTVBXgQ4XAAAALElEQVRYw+3OMQEAAAgDoGn/zjOGDyRg2ubT5pmAgICAgICAgICA
        gICAgMABQLQDPYU9GZMAAAAASUVORK5CYII='''
        self.ok_img = b'''
        iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAC60lEQVR4AayVA5MkWRSFK2IDa/yE
        Nkpj29aObW+htWPbtu2Z4NhOldq2bd/JM0ZWd2Z0nYiTfPd+z0+lRFputq83Z5ipZs3X1IwxQcOa
        ymE84xv+oYzKldLdnfSb+q1pnI4z3dHx5nydNZD0QgBp+QDScWaC8Yxv+IcyKIsYxDYJ7sMY+mk4
        82u9RUxsC/oG6swog7KIQSxyKAa3fzXqFzVr3KQRAquQTAIky4hFDuRCTlnwf+7P/kvLmq7qbMGy
        WiyvR4IJOZG7QXhLbvavasDtwQh2qZETucFwPstZ0+ZmdrldrtzIDYYkXMP910fPm6uVd7uy4QAD
        rG/pYrfoONMbTBpXwTScyenEBAvMz3w1axiLZeMquB9rpNZ8MPlzRsn/YKnfGMZ+oF8Z9ZM4Lndd
        1Xov9j8aYF1F1qJY2pZwFZWR7AUwwVa5v13gLXZXod4FY+/DGqiHZRk5ihMIshTFUAs+iDTflQML
        TPc3Bi+VWty/ddYgl8C7CItJKIwhKKY0lQbZ1kj2AAwm2Co/xnhdLwQ2eczbCSH0tiCcoKTyTBpu
        X08e7H9OY8AEW4WTTMs3Dd5K7OZneXaC0ityaYxjM7kzzuEwmGCLFTBXNAbwYP6TXFaY5c25AHqQ
        KxCUU1VIk8N2iPCFsioPdgMVANxAox2baG/SrY9A0zdw3O/lch/hRTQ9bKdsOAy20yHAzMUMthXH
        EXQl4yn5s0YCGBWBb2W9JKiguoTmhO8V4Qtkw8EEu8FJCODKuLNUVltJ0LWMZ4QhwVq/lP6YoOKa
        MjJGHpTZcolJqGGNM3RW56sAiZfFnqLy2iqCroo9cTrtHkH4Fhx9TDEcBhNsFTaDxjYidO3K2DNU
        IQIhqKqumtbEnVcIl9iI5G7FAK0ShwPguvo62hx/mfBNIx8svRUrOYw8ROC6uAu0M/EGNhm0Qj5U
        +jBSfBxjy4XlgOQfx+82wA0S+jfJBmmjlP7Ncvp3TIZC14z+ndMB754DANf99mSzjcE0AAAAAElF
        TkSuQmCC'''
        self.warning_img = b'''
        iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACL0lEQVR4AcWXtdYUMRTHcw4Nzktg
        DboNLjPJTHY/qXC3h4EOKeEFsB6eAFrcoaXBZWTl8v3wtWQ+Tc65K8k/93fjiZpM+rxr1+osSs8U
        OrmRG/Om0OY7xm/yKEOjZjK9TdYu+h6Zg7k2t8o0ed+xVloTViaJFL+N3+RRhgYtdag7LXi+K7al
        Nnfa1orU69JMLECnoUFLHeriY9Jg2bx5QWH02VaaFGLrDqDbqIsPfOGzEvx9rbYsN+a60AJvi/2G
        D3zhE9/ulo/VFiKUeqNrjKdr+MInvmEMDeC7Sc9J3U4X7gjCCoyB8DyKkmaaltOHu4OAAasLLrXa
        wtKYu94JZwzf09LAgAXzX9fHyQGWjdOx1lKMjUkRx8M0lKFB6/QFC6YiXVN75+XG3CYyF7x1+Yp0
        Hj6S8sgxKXbv6tOQRxkatK4gYGUTTNjq87Z4ZanNxzK1w7t0bFw6j58Iqf3ihZSHjwLsgpNHGQkt
        dYYNByyY+Q6zQmVRdKbjG/s4pnUA+oPohvON1jlUGEzYKtf6Zss9/thg0IFD2ODAPP5gwlaZMW9K
        t9gRxEts0nAMJmxVaJ35xH1BHDwMEO5fOHl+eLfBDh5A8CGY/CR87piEz6cwCcs4Pt2xttoyBO5b
        hs+rLUOYsBWbgXcjajSk/eBh1Y0ILXUqbUSVt+LmhUvSuX/ftxWjQVt5K57cYdQY8R1GaCofRsGP
        48AXkvBXsvCX0vDX8vAPk/BPs/CP0+DP8x/rq16YWXwOHgAAAABJRU5ErkJggg=='''
        self.icon_data = b'''
        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'''
        self.logo = b'''
        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
        '''


class Rtcqs:
    def __init__(self):
        self.user = getpass.getuser()
        self.wiki_url = "https://wiki.linuxaudio.org/wiki/system_configuration"
        self.gui_status = False
        self.version = "0.6.0"
        self.headline = {}
        self.kernel = {}
        self.output = {}
        self.status = {}

    def print_cli(self, message):
        if not self.gui_status:
            print(message)

    def print_version(self):
        self.print_cli(f"rtcqs - version {self.version}")
        self.print_cli("")

    def print_status(self, check):
        if not self.gui_status:
            if self.status[check]:
                print("[ \033[32mOK\033[00m ] ", end="")
            else:
                print("[ \033[31mWARNING\033[00m ] ", end="")

    def format_output(self, check):
        char_count = int(len(self.headline[check]))
        self.print_cli(self.headline[check])
        self.print_cli(char_count * "=")
        self.print_status(check)
        self.print_cli(self.output[check])
        self.print_cli("")

    def root_check(self):
        check = "root"
        self.headline[check] = "Root User"

        if self.user == "root":
            self.status[check] = False
            self.output[check] = "You are running this script as root. " \
                "Please run it as a regular user for the most reliable "\
                "results."

        else:
            self.status[check] = True
            self.output[check] = "Not running as root."

        self.format_output(check)

    def audio_group_check(self):
        check = "audio_group"
        self.headline[check] = "Group Limits"
        wiki_anchor = "#audio_group"
        limit_rtprio = resource.getrlimit(resource.RLIMIT_RTPRIO)[1]
        limit_memlock = resource.getrlimit(resource.RLIMIT_MEMLOCK)[1]

        if limit_rtprio >= 75 and limit_memlock == -1:
            self.status[check] = True
            self.output[check] = f"User {self.user} is member of a group " \
                                 "that has sufficient rtprio " \
                                 f"({limit_rtprio}) and memlock (unlimited) " \
                                 "limits set."
        else:
            self.status[check] = False
            self.output[check] = f"User {self.user} is currently not member " \
                                 "of a group that has sufficient rtprio " \
                                 f"({limit_rtprio}) and memlock " \
                                 f"({limit_memlock}) set. Add yourself to a " \
                                 "group with sufficent limits set, i.e. " \
                                 "audio or realtime, with 'sudo usermod -a " \
                                 f"-G <group_name> {self.user}. See also " \
                                 f"{self.wiki_url}{wiki_anchor}"

        self.format_output(check)

    def governor_check(self):
        check = "governor"
        self.headline[check] = "CPU Frequency Scaling"
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
            self.status[check] = False
            self.output[check] = "The scaling governor of one or more CPUs " \
                "is not set to 'performance'. You can set the scaling " \
                "governor to 'performance' with 'cpupower frequency-set " \
                "-g performance' or 'cpufreq-set -r -g performance' " \
                f"(Debian/Ubuntu). See also {self.wiki_url}{wiki_anchor}"
        else:
            self.status[check] = True
            self.output[check] = "The scaling governor of all CPUs is set " \
                "to performance."

        self.format_output(check)

    def kernel_config_check(self):
        check = "kernel_config"
        self.headline[check] = "Kernel Configuration"
        self.kernel["release"] = os.uname().release

        with open("/proc/cmdline", "r") as f:
            self.kernel["cmdline"] = f.readline().strip().split()

        if os.path.exists("/proc/config.gz"):
            self.status[check] = True
            self.output[check] = "Valid kernel configuration found."
            with gzip.open("/proc/config.gz", "r") as f:
                self.kernel["config"] = [
                    line.strip().decode() for line in f.readlines()]
        elif os.path.exists(f"/boot/config-{self.kernel['release']}"):
            self.status[check] = True
            self.output[check] = "Valid kernel configuration found."
            with open(f"/boot/config-{self.kernel['release']}", "r") as f:
                self.kernel["config"] = [
                    line.strip() for line in f.readlines()]
        else:
            self.status[check] = False
            self.output[check] = "Could not find kernel configuration."

        self.format_output(check)

    def high_res_timers_check(self):
        check = "high_res_timers"
        self.headline[check] = "High Resolution Timers"
        wiki_anchor = "#installing_a_real-time_kernel"

        if "CONFIG_HIGH_RES_TIMERS=y" not in self.kernel["config"]:
            self.status[check] = False
            self.output[check] = "High resolution timers are not " \
                "enabled. Try enabling high-resolution timers " \
                "(CONFIG_HIGH_RES_TIMERS) under 'Processor type and " \
                f"features'). See also: {self.wiki_url}{wiki_anchor}"
        else:
            self.status[check] = True
            self.output[check] = "High resolution timers are enabled."

        self.format_output(check)

    def tickless_check(self):
        check = "tickless"
        self.headline[check] = "Tickless Kernel"
        wiki_anchor = "#installing_a_real-time_kernel"
        conf_nohz_list = [
            "CONFIG_NO_HZ=y",
            "CONFIG_NO_HZ_IDLE=y",
            "CONFIG_NO_HZ_COMMON=y",
            "CONFIG_NO_HZ_FULL=y"]

        conf_nohz_match = [
            match for match in conf_nohz_list if match in
            self.kernel["config"]]

        if int(len(conf_nohz_match)) > 0 or \
                os.path.exists("/sys/devices/system/cpu/nohz_full"):
            self.status[check] = True
            self.output[check] = "System is using a tickless kernel."
        else:
            self.status[check] = False
            self.output[check] = "Tickless timer support is not set. Try " \
                "enabling tickless timer support (CONFIG_NO_HZ_IDLE, or " \
                "CONFIG_NO_HZ in older kernels). See also " \
                f"{self.wiki_url}{wiki_anchor}"

        self.format_output(check)

    def preempt_rt_check(self):
        check = "preempt_rt"
        self.headline[check] = "Preempt RT"
        wiki_anchor = "#do_i_really_need_a_real-time_kernel"
        threadirqs = preempt = False

        if "threadirqs" in self.kernel["cmdline"]:
            threadirqs = True

        if "CONFIG_PREEMPT_RT=y" in self.kernel["config"] or \
                "CONFIG_PREEMPT_RT_FULL=y" in self.kernel["config"] or \
                "preempt=full" in self.kernel["cmdline"]:
            preempt = True

        if not threadirqs and not preempt:
            self.status[check] = False
            self.output[check] = f"Kernel {self.kernel['release']} without " \
                "'threadirqs' parameter or real-time capabilities found. " \
                f"See also {self.wiki_url}{wiki_anchor}"
        elif threadirqs:
            self.status[check] = True
            self.output[check] = f"Kernel {self.kernel['release']} is using " \
                "threaded IRQs."
        elif preempt:
            self.status[check] = True
            self.output[check] = f"Kernel {self.kernel['release']} is a " \
                "real-time kernel."

        self.format_output(check)

    def mitigations_check(self):
        check = "mitigations"
        self.headline[check] = "Spectre/Meltdown Mitigations"
        wiki_anchor = "#disabling_spectre_and_meltdown_mitigations"

        if "mitigations=off" not in self.kernel["cmdline"]:
            self.status[check] = False
            self.output[check] = "Kernel with Spectre/Meltdown mitigations " \
                "found. This could have a negative impact on the " \
                "performance of your system. See also " \
                f"{self.wiki_url}{wiki_anchor}"
        else:
            self.status[check] = True
            self.output[check] = "Spectre/Meltdown mitigations are " \
                "disabled. Be warned that this makes your system more " \
                "vulnerable to Spectre/Meltdown attacks."

        self.format_output(check)

    def rt_prio_check(self):
        check = "rt_prio"
        self.headline[check] = "RT Priorities"
        wiki_anchor = "#limitsconfaudioconf"
        param = os.sched_param(80)
        sched = os.SCHED_FIFO

        try:
            os.sched_setscheduler(0, sched, param)
        except PermissionError as e:
            self.status[check] = False
            self.output[check] = "Could not assign a 80 rtprio SCHED_FIFO " \
                f"value due to the following error: {e}. Set up " \
                f"imits.conf. See also {self.wiki_url}{wiki_anchor}"
        else:
            self.status[check] = True
            self.output[check] = "Realtime priorities can be set."

        self.format_output(check)

    def swappiness_check(self):
        check = "swappiness"
        self.headline[check] = "Swappiness"
        wiki_anchor = "#sysctlconf"

        with open("/proc/swaps", "r") as f:
            lines = f.readlines()

        if len(lines) < 2:
            swap = False
            self.status[check] = True
            self.output[check] = "Your system is configured without swap, " \
                "setting swappiness does not apply."
        else:
            swap = True

        if swap:
            with open("/proc/sys/vm/swappiness", "r") as f:
                swappiness = int(f.readline().strip())

            if swappiness > 10:
                self.status[check] = False
                self.output[check] = f"vm.swappiness is set to {swappiness} " \
                    "which is too high. Set swappiness to a lower value by " \
                    "adding 'vm.swappiness=10' to /etc/sysctl.conf and run " \
                    f"'sysctl --system'. See also {self.wiki_url}{wiki_anchor}"
            else:
                self.status[check] = True
                self.output[check] = f"Swappiness is set at {swappiness}."

        self.format_output(check)

    def filesystems_check(self):
        check = "filesystems"
        self.headline[check] = "Filesystems"
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

        self.print_cli(self.headline[check])
        self.print_cli("===========")

        if len(good_mounts_list) > 0:
            good_mounts = ", ".join(good_mounts_list)
            self.status[check] = True
            self.output[check] = "The following mounts can be used for " \
                f"audio purposes: {good_mounts}"
            self.print_status('filesystems')
            self.print_cli(self.output['filesystems'])

        if len(bad_mounts_list) > 0:
            bad_mounts = ', '.join(bad_mounts_list)
            self.status[check] = False
            self.output[check] = "The following mounts should be avoided " \
                f"for audio purposes: {bad_mounts}. See also " \
                f"{self.wiki_url}{wiki_anchor}"
            self.print_status(check)
            self.print_cli(self.output[check])

        self.print_cli("")

    def irq_check(self):
        check = "irqs"
        self.headline[check] = "IRQs"
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
                    self.status["snd_irqs"] = False
                    output_irq[irq] = f"Soundcard {device_list[0]} with IRQ " \
                        f"{irq} shares its IRQ with the following other " \
                        f"devices {devices}"
                else:
                    good_irq_list.append(irq)
                    self.status["snd_irqs"] = True
                    output_irq[irq] = f"Soundcard {device_list[0]} with IRQ " \
                        f"{irq} does not share its IRQ."
            if usb_compiled_re.search(devices):
                if len(device_list) > 1:
                    bad_irq_list.append(irq)
                    self.status["usb_irqs"] = False
                    output_irq[irq] = f"Found USB port {device_list[0]} " \
                        f"with IRQ {irq} that shares its IRQ with the " \
                        f"following other devices: {devices}"
                else:
                    good_irq_list.append(irq)
                    self.status["usb_irqs"] = True
                    output_irq[irq] = f"USB port {device_list[0]} with IRQ " \
                        f"{irq} does not share its IRQ."

        self.print_cli(self.headline[check])
        self.print_cli("====")

        if len(good_irq_list) > 0:
            self.status[check] = True
            self.output[check] = "\n".join(
                [output_irq[good_irq] for good_irq in good_irq_list])

            for good_irq in good_irq_list:
                self.print_status(check)
                self.print_cli(output_irq[good_irq])

        if len(bad_irq_list) > 0:
            self.status[check] = False
            self.output[check] = "\n".join(
                [output_irq[bad_irq] for bad_irq in bad_irq_list])

            for bad_irq in bad_irq_list:
                self.print_status(check)
                self.print_cli(output_irq[bad_irq])

        self.print_cli("")

    def power_management_check(self):
        check = "power_management"
        self.headline[check] = "Power Management"
        wiki_anchor = "#quality_of_service_interface"

        if os.access("/dev/cpu_dma_latency", os.W_OK):
            self.status[check] = True
            self.output[check] = "Power management can be controlled from " \
                "user space. This enables DAWs like Ardour and Reaper to " \
                "set CPU DMA latency which could help prevent xruns."
        else:
            self.status[check] = False
            self.output[check] = "Power management can't be controlled from " \
                "user space, the device node /dev/cpu_dma_latency can't be " \
                "accessed by your user. This prohibits DAWs like Ardour and " \
                "Reaper to set CPU DMA latency which could help prevent " \
                "xruns. For enabling access see " \
                f"{self.wiki_url}{wiki_anchor}"

        self.format_output(check)

    def main(self):
        self.print_version()
        self.root_check()
        self.audio_group_check()
        self.governor_check()
        self.kernel_config_check()
        self.high_res_timers_check()
        self.tickless_check()
        self.preempt_rt_check()
        self.mitigations_check()
        self.rt_prio_check()
        self.swappiness_check()
        self.filesystems_check()
        self.irq_check()
        self.power_management_check()


def main():
    app = Rtcqs()
    app.main()


if __name__ == "__main__":
    main()
