#!/usr/bin/env python3

import PySimpleGUIQt as sg
import rtcqs

transparent_img = b'''iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9
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
ok_img = b'''iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAC60lEQVR4AayVA5MkWRSFK2IDa/yE
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
warning_img = b'''iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACY0lEQVR4Ac2XNfDUQBjFM0OD0/dY
g16DcyS7SQ53d6fBrUEa3F36BuuhL6Av/u2fCne7ZHOXj/sxuGYXy868mTdvd7+3Lp5NelGt9q37
0fJUhVcTrdtTpd8AOBp5lPH+ZLoX9u/yxtdzEqWvmyh8ksexNFowYSjpe8DRyKMMZalD3d8yT6pB
bJS+2WwFllpNsjDG8KegDGWpQ11iWBvL0KGdUq32N6IwlbhGYCdQlxjEImYh8yeVSo9E6ytCDz71
2BnEIBYxif1Tc5lQ6fzOvDb2izn+XRCLmMTG44cNeKOjA1KLbc0tGhELHt9fcL4fZlFkCptH8Zco
2Ag88PrCXCqVzkbrW4UX3KiRkp04JfnduwCOVnhh4oXnp6EPwtnN2GLBjWw14NxF+ZDgaEXr44Wn
R7rszeiQaH3DarsxAkePf/CHo1ltz3rLE2/vxYigt1H6mYksRmD0KMn2HvjgD0crXB8vPJNRupdX
9/3lue1hUx0t2c7dH/zhaFYx8MTbS5S6xjlu14CqZFu3izSbAI5mFQNPvL261u3W+36ML2bdBpGs
AeBo1ucC3l6qVB3BCoEvZuUakTQFcDSxjYO3YwOUmAWLJTcpgKO5NcBpCpQSM32m5PfvAzia0xS4
LcIPmDARwIHbIjRBsCx3aUAQiJk2A8Ct6+OJt8dhYH0Q+b40Dh+V/NFjAEdzOojsj2KtJZ0woTX3
D+RDgqORZ3sU219GmIwdJ3n77Q/+cDTyrC4j9+vYD8Rs3ip5WxuAo7lfx04PEuZcawC3fpCU4ElW
gkdpCZ7lZfyYlOJrVprP6b/4nr8Fda5BEkkNcp8AAAAASUVORK5CYII='''


def create_gui():
    sg.theme('SystemDefaultForReal')

    layout = [
        [sg.Text('Root User', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='root_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='root_output')],
        [sg.Text('Audio Group', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='audio_group_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='audio_group_output')],
        [sg.Text('Background Processes', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='background_process_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='background_process_output')],
        [sg.Text('CPU Frequency Scaling', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='governor_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='governor_output')],
        [sg.Text('Kernel Configuration', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='kernel_config_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='kernel_config_output')],
        [sg.Text('High Resolution Timers', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='high_res_timers_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='high_res_timers_output')],
        [sg.Text('System Timer', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='system_timer_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='system_timer_output')],
        [sg.Text('Tickless Kernel', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='tickless_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='tickless_output')],
        [sg.Text('Real-Time Kernel', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='preempt_rt_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='preempt_rt_output')],
        [sg.Text('Mitigations', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='mitigations_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='mitigations_output')],
        [sg.Text('Real-Time Priorities', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='rt_prio_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='rt_prio_output')],
        [sg.Text('Swappiness', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='swappiness_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='swappiness_output')],
        [sg.Text('Max User Watches', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='max_user_watches_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='max_user_watches_output')],
        [sg.Text('Filesystems', size=(15, 1)),
         sg.Image(data_base64=transparent_img, key='filesystems_img'),
         sg.Multiline(size=(75, 3.2), pad=((0, 15), (0, 0)),
                      key='filesystems_output')],
        [sg.OK(size=(32, 1), pad=((0, 0), (0, 0))),
         sg.Button(size=(32, 1), pad=((0, 0), (0, 0)),
                   button_text='Clear'),
         sg.Cancel(size=(32, 1), pad=((0, 5), (0, 0)))]]

    icon_data = b''''''

    window = sg.Window(
        'rtcqs', layout, icon=icon_data)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Clear':
            for check in rtcqs.output:
                window_name = f"{check}_img"
                output_name = f"{check}_output"
                window[window_name].update(data_base64=transparent_img)
                window[output_name].update('')
        elif event == 'OK':
            try:
                rtcqs.gui()
            except BaseException as err:
                print(f'rtcqs exited with error {err=}, {type(err)=}')

            for check in rtcqs.output:
                window_name = f"{check}_img"
                output_name = f"{check}_output"
                if rtcqs.status[check]:
                    window[window_name].update(data_base64=ok_img)
                else:
                    window[window_name].update(data_base64=warning_img)

                window[output_name].print(rtcqs.output[check], end='')

    window.close()


def main():
    create_gui()


if __name__ == "__main__":
    main()
