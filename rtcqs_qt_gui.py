#!/usr/bin/env python3

import PySimpleGUIQt as sg
import rtcqs
import resources as res

rtcqs.gui_status = True
version = rtcqs.version
element_vars = {}


def run_analysis():
    try:
        rtcqs.main()
    except BaseException as err:
        print(f'rtcqs exited with error {err=}, {type(err)=}')

    for check in rtcqs.output:
        img_key = f'{check}_img'
        output_key = f'{check}_output'
        tab_status = f'{check}_status'

        if rtcqs.status[check]:
            element_vars[img_key] = res.ok_img
            element_vars[tab_status] = '✔'
        else:
            element_vars[img_key] = res.warning_img
            element_vars[tab_status] = '✘'

        element_vars[output_key] = rtcqs.output[check]


def create_tab(tab_name, check):
    tab_layout = [sg.Tab(f"{element_vars[f'{check}_status']}{tab_name}", [[
        sg.Image(data_base64=element_vars[f'{check}_img'],
                 key=f'{check}_img'),
        sg.Multiline(default_text=element_vars[f'{check}_output'],
                     size=(80, 3.5),
                     key=f'{check}_output',
                     disabled=True,
                     background_color='white',
                     text_color='black')]],
            background_color='#FBFBFB', key=f'{check}_tab')]

    return tab_layout


def create_gui():
    sg.theme('SystemDefaultForReal')

    about_window = False

    layout_analysis = [
        [sg.TabGroup([
            create_tab(' Root User', 'root'),
            create_tab(' Audio Group', 'audio_group'),
            create_tab(' Background Processes', 'background_process'),
            create_tab(' CPU Frequency Scaling', 'governor'),
            create_tab(' Kernel Configuration', 'kernel_config'),
            ], key='tab_group1')],
        [sg.TabGroup([
            create_tab(' High Resolution Timers', 'high_res_timers'),
            create_tab(' System Timer', 'system_timer'),
            create_tab(' Tickless Kernel', 'tickless'),
            create_tab(' Real-Time Kernel', 'preempt_rt'),
            create_tab(' Mitigations', 'mitigations'),
            ], key='tab_group2')],
        [sg.TabGroup([
            create_tab(' Real-Time Priorities', 'rt_prio'),
            create_tab(' Swappiness', 'swappiness'),
            create_tab(' Max User Watches', 'max_user_watches'),
            create_tab(' Filesystems', 'filesystems'),
            create_tab(' IRQs', 'irqs'),
            ], key='tab_group3')],
        [sg.TabGroup([
            create_tab(' Power Management', 'power_management'),
            ], key='tab_group4')],
        [sg.Button(button_text='About', size=(25, 1), pad=((0, 0), (0, 0))),
         sg.Stretch(), sg.Cancel(size=(25, 1), pad=((0, 0), (0, 0)))]]

    layout_about = [
        [sg.Column([
            [sg.Stretch(), sg.Image(data_base64=res.logo),
             sg.Stretch()],
            [sg.Stretch(),
             sg.Text(f'rtcqs - version {version}',
                     font=('DejaVu Sans', '12', 'normal')),
             sg.Stretch()],
            [sg.Stretch(),
             sg.Text('rtcqs, pronounced arteeseeks, is a Python '
                     'port of the realtimeconfigquickscan project.'),
             sg.Stretch()]], background_color='white')],
        [sg.Stretch(), sg.OK(size=(13, 1), pad=((0, 0), (3, 0))),
         sg.Stretch()]]

    window_analysis = sg.Window(
        'rtcqs', layout_analysis, icon=res.icon_data)

    window_about = sg.Window(
        'rtcqs', layout_about, icon=res.icon_data, disable_close=True)

    while True:
        event, values = window_analysis.read()

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'About':
            about_window = True
            window_about.un_hide()
            choice, _ = window_about.read(close=True)

            if choice == 'OK':
                window_about.hide()

    if about_window:
        window_about.close()

    window_analysis.close()


def main():
    run_analysis()
    create_gui()


if __name__ == "__main__":
    main()
