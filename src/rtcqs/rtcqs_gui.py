#!/usr/bin/env python3

import PySimpleGUI as sg
import rtcqs.rtcqs as rtcqs
import rtcqs.resources as res

rtcqs.gui_status = True
version = rtcqs.version
element_vars = {}
element_vars['check_keys'] = []
tab_group_list = []


def run_analysis():
    try:
        rtcqs.main()
    except BaseException as err:
        print(f'rtcqs exited with error {err=}, {type(err)=}')

    for check in rtcqs.output:
        headline_key = f'{check}_headline'
        img_key = f'{check}_img'
        output_key = f'{check}_output'
        tab_status = f'{check}_status'

        if rtcqs.status[check]:
            element_vars[img_key] = res.ok_img
            element_vars[tab_status] = '✔'
        else:
            element_vars[img_key] = res.warning_img
            element_vars[tab_status] = '✘'

        element_vars[headline_key] = rtcqs.headline[check]
        element_vars[output_key] = rtcqs.output[check]

        element_vars['check_keys'].append(check)


def create_tab(tab_name, check):
    tab_layout = [sg.Tab(f"{element_vars[f'{check}_status']}{tab_name}", [[
        sg.Image(source=element_vars[f'{check}_img'],
                 key=f'{check}_img'),
        sg.Multiline(default_text=element_vars[f'{check}_output'],
                     size=(90, 4),
                     key=f'{check}_output',
                     disabled=True,
                     background_color='white',
                     text_color='black',
                     no_scrollbar=True)]],
            background_color='#D9D9D9',
            key=f'{check}_tab')]

    return tab_layout


def create_tab_group():
    tab_count = len(element_vars['check_keys'])
    tab_group_count = 0
    tab_row_count = 0
    tab_group_layout = []

    for tab in range(tab_count):
        if tab % 5 == 0:
            tab_group_count += 1
            tab_row_count += 5
            tab_group_layout.append(
                [sg.TabGroup([
                 create_tab(
                    f"{element_vars[f'{check}_headline']}",
                    check) for check in element_vars['check_keys']
                 ][tab:tab_row_count],
                    key=f'tab_group{tab_group_count}',
                    pad=(None, (0, 10)))]
            )

    return tab_group_layout


def make_analysis():
    layout_analysis = [
        create_tab_group(),
        [sg.Button(button_text='About', size=(25, 1), pad=((5, 0), (0, 0))),
         sg.Stretch(), sg.Cancel(size=(25, 1), pad=((0, 5), (0, 0)))]]

    window_analysis = sg.Window(
        'rtcqs', layout_analysis, icon=res.icon_data, finalize=True)

    return window_analysis


def make_about():
    layout_about = [
        [sg.Column([
            [sg.Stretch(), sg.Image(source=res.logo),
             sg.Stretch()],
            [sg.Stretch(),
             sg.Text(f'rtcqs - version {version}',
                     font=('DejaVu Sans', '12', 'normal')),
             sg.Stretch()],
            [sg.Stretch(),
             sg.Text('rtcqs, pronounced arteeseeks, is a Python '
                     'port of the realtimeconfigquickscan project.'),
             sg.Stretch()]])],
        [sg.Stretch(), sg.OK(size=(13, 1), pad=((0, 0), (3, 0))),
         sg.Stretch()]]

    window_about = sg.Window(
        'rtcqs', layout_about,
        icon=res.icon_data,
        finalize=True,
        disable_close=True)

    return window_about


def create_gui():
    sg.theme('SystemDefaultForReal')

    make_analysis()

    while True:
        window, event, values = sg.read_all_windows()

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break

        if event == 'About':
            window_about = make_about()

        if event == 'OK':
            window_about.close()


def main():
    run_analysis()
    create_gui()


if __name__ == "__main__":
    main()
