#!/usr/bin/env python3

import PySimpleGUI as sg
from rtcqs import Rtcqs, Resources


class RtcqsGUI:
    def __init__(self):
        self.rtcqs = Rtcqs()
        self.res = Resources()
        self.rtcqs.gui_status = True
        self.version = self.rtcqs.version
        self.element_vars = {}
        self.element_vars["check_keys"] = []
        self.tab_group_list = []

    def run_analysis(self):
        try:
            self.rtcqs.main()
        except BaseException as err:
            print(f"rtcqs exited with error {err=}, {type(err)=}")

        for check in self.rtcqs.output:
            headline_key = f"{check}_headline"
            img_key = f"{check}_img"
            output_key = f"{check}_output"
            tab_status = f"{check}_status"

            if self.rtcqs.status[check]:
                self.element_vars[img_key] = self.res.ok_img
                self.element_vars[tab_status] = "✔"
            else:
                self.element_vars[img_key] = self.res.warning_img
                self.element_vars[tab_status] = "✘"

            self.element_vars[headline_key] = self.rtcqs.headline[check]
            self.element_vars[output_key] = self.rtcqs.output[check]

            self.element_vars["check_keys"].append(check)

    def create_tab(self, tab_name, check):
        tab_layout = [
            sg.Tab(f"{self.element_vars[f'{check}_status']}{tab_name}", [[
                sg.Image(source=self.element_vars[f"{check}_img"],
                         key=f"{check}_img"),
                sg.Multiline(default_text=self.element_vars[f"{check}_output"],
                             size=(90, 4),
                             key=f"{check}_output",
                             disabled=True,
                             background_color="white",
                             text_color="black",
                             no_scrollbar=True)]],
                   background_color="#D9D9D9",
                   key=f"{check}_tab")]

        return tab_layout

    def create_tab_group(self):
        tab_count = len(self.element_vars["check_keys"])
        tab_group_count = 0
        tab_row_count = 0
        tab_group_layout = []

        for tab in range(tab_count):
            if tab % 5 == 0:
                tab_group_count += 1
                tab_row_count += 5
                tab_group_layout.append(
                    [sg.TabGroup([
                     self.create_tab(
                        f"{self.element_vars[f'{check}_headline']}",
                        check) for check in self.element_vars["check_keys"]
                     ][tab:tab_row_count],
                        key=f"tab_group{tab_group_count}",
                        pad=(None, (0, 10)))]
                )

        return tab_group_layout

    def make_analysis(self):
        layout_analysis = [
            self.create_tab_group(),
            [sg.Button(
                button_text="About", size=(25, 1), pad=((5, 0), (0, 0))),
             sg.Stretch(), sg.Cancel(size=(25, 1), pad=((0, 5), (0, 0)))]]

        window_analysis = sg.Window(
            "rtcqs", layout_analysis, icon=self.res.icon_data, finalize=True)

        return window_analysis

    def make_about(self):
        layout_about = [
            [sg.Column([
                [sg.Stretch(), sg.Image(source=self.res.logo),
                 sg.Stretch()],
                [sg.Stretch(),
                 sg.Text(f"rtcqs - version {self.version}",
                         font=("DejaVu Sans", "12", "normal")),
                 sg.Stretch()],
                [sg.Stretch(),
                 sg.Text("rtcqs, pronounced arteeseeks, is a Python "
                         "port of the realtimeconfigquickscan project."),
                 sg.Stretch()]])],
            [sg.Stretch(), sg.OK(size=(13, 1), pad=((0, 0), (3, 0))),
             sg.Stretch()]]

        window_about = sg.Window(
            "rtcqs", layout_about,
            icon=self.res.icon_data,
            finalize=True,
            disable_close=True)

        return window_about

    def create_gui(self):
        sg.theme("SystemDefaultForReal")

        self.make_analysis()

        while True:
            window, event, values = sg.read_all_windows()

            if event in (sg.WIN_CLOSED, "Cancel"):
                break

            if event == "About":
                window_about = self.make_about()

            if event == "OK":
                window_about.close()

    def main(self):
        self.run_analysis()
        self.create_gui()


def main():
    app = RtcqsGUI()
    app.main()


if __name__ == "__main__":
    main()
