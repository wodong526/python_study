#coding=utf-8
import os
import subprocess
from PySide2 import QtWidgets

from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class TranscodeWindow(QtWidgets.QDialog):
    FFMPEG_PATH = 'F:/ffmpeg_6_1/ffmpeg.exe'

    QUALITY_OPTIONS = [(u'����', '18'), (u'��', '20'), (u'�е�', '23'), (u'��', '26')]#����ѡ��
    QUALITY_DEFAULT = u'�е�'#Ĭ������
    PRESETS = [(u'�ǳ���', 'veryslow'), (u'�Ƚ���', 'slower'), (u'��', 'slow'), (u'�е�', 'medium'), (u'��', 'fast'),
               (u'�Ͽ�', 'faster'), (u'�ǳ���', 'veryfast'), (u'����', 'ultrafast')]#�ٶ�

    def __init__(self, parent = maya_main_window()):
        super(TranscodeWindow, self).__init__(parent)

        self.setWindowTitle(u'��Ƶ������')
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.lin_input_path = QtWidgets.QLineEdit()
        self.but_input_path = QtWidgets.QPushButton('...')
        self.but_input_path.setFixedWidth(30)

        self.lin_output_path = QtWidgets.QLineEdit()
        self.but_output_path = QtWidgets.QPushButton('...')
        self.but_output_path.setFixedWidth(30)

        self.combox_video_codec = QtWidgets.QComboBox()
        self.combox_video_codec.addItem('h264', 'libx264')

        self.combox_quality = QtWidgets.QComboBox()
        for title, cmd in self.QUALITY_OPTIONS:
            self.combox_quality.addItem(title, cmd)
        self.combox_quality.setCurrentText(self.QUALITY_DEFAULT)

        self.combox_preset = QtWidgets.QComboBox()
        for title, cmd in self.PRESETS:
            self.combox_preset.addItem(title, cmd)
        self.combox_preset.setCurrentText(self.QUALITY_DEFAULT)

        self.combox_audio_codec = QtWidgets.QComboBox()
        self.combox_audio_codec.addItem('acc', 'acc')

        self.but_transcode = QtWidgets.QPushButton(u'��ʼ����')
        self.but_cancel = QtWidgets.QPushButton(u'ȡ��')

    def create_layout(self):
        grp_input = QtWidgets.QGroupBox(u'����·��')
        layout_grp_input = QtWidgets.QHBoxLayout()
        layout_grp_input.addWidget(self.lin_input_path)
        layout_grp_input.addWidget(self.but_input_path)
        grp_input.setLayout(layout_grp_input)

        grp_output = QtWidgets.QGroupBox(u'����·��')
        layout_grp_output = QtWidgets.QHBoxLayout()
        layout_grp_output.addWidget(self.lin_output_path)
        layout_grp_output.addWidget(self.but_output_path)
        grp_output.setLayout(layout_grp_output)

        grp_setVideo = QtWidgets.QGroupBox(u'��Ƶ����')
        layout_grp_video = QtWidgets.QFormLayout()
        layout_grp_video.addRow(u'��Ƶ����', self.combox_video_codec)
        layout_grp_video.addRow(u'����', self.combox_quality)
        layout_grp_video.addRow(u'�ٶ�', self.combox_preset)
        grp_setVideo.setLayout(layout_grp_video)

        grp_setAudio = QtWidgets.QGroupBox(u'��Ƶ����')
        layout_grp_audio = QtWidgets.QFormLayout()
        layout_grp_audio.addRow(u'��Ƶ����', self.combox_audio_codec)
        grp_setAudio.setLayout(layout_grp_audio)

        layout_options = QtWidgets.QHBoxLayout()
        layout_options.addWidget(grp_setVideo)
        layout_options.addWidget(grp_setAudio)

        layout_but = QtWidgets.QHBoxLayout()
        layout_but.addStretch()
        layout_but.addWidget(self.but_transcode)
        layout_but.addWidget(self.but_cancel)

        layout_main = QtWidgets.QVBoxLayout(self)
        layout_main.setSpacing(3)
        layout_main.addWidget(grp_input)
        layout_main.addWidget(grp_output)
        layout_main.addLayout(layout_options)
        layout_main.addLayout(layout_but)

    def create_connections(self):
        self.but_input_path.clicked.connect(self.set_input_path)
        self.but_output_path.clicked.connect(self.set_output_path)

        self.but_transcode.clicked.connect(self.transcode)
        self.but_cancel.clicked.connect(self.close)

    def set_input_path(self):
        filters = ''
        selected_filter = ''
        input_path, selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, u'ѡ�����ļ�', '', filters,
                                                                            selected_filter)
        if input_path:
            self.lin_input_path.setText(input_path)

    def set_output_path(self):
        filters = '*.mp4'
        selected_filter = '*.mp4'
        ouput_path, selected_filter = QtWidgets.QFileDialog.getSaveFileName(self, u'���浽', '', filters,
                                                                             selected_filter)
        if ouput_path:
            self.lin_output_path.setText(ouput_path)

    def transcode(self):
        input_path = self.lin_input_path.text()
        if not input_path:
            QtWidgets.QMessageBox.critical(self, u'ת�����', u'����·��Ϊ��')
            return
        if not os.path.exists(input_path):
            QtWidgets.QMessageBox.critical(self, u'ת�����', u'�����ļ�������')
            return

        output_path = self.lin_output_path.text()
        if not output_path:
            QtWidgets.QMessageBox.critical(self, u'�������', u'����·��Ϊ��')
            return

        video_codec = self.combox_video_codec.currentData()
        crf = self.combox_quality.currentData()
        preset = self.combox_preset.currentData()

        audio_codec = self.combox_audio_codec.currentData()

        args = [self.FFMPEG_PATH]
        args.extend(['-hide_banner', '-y'])
        args.extend(['-i', input_path])
        args.extend(['-c:v', video_codec, '-crf', crf, '-preset', preset])
        args.extend(['-c:a', audio_codec])
        args.append(output_path)

        subprocess.call(args)
        QtWidgets.QMessageBox.information(self, u'�������', u'�ļ��������')






if __name__ == '__main__':
    try:
        my_window.close()
        my_window.deleteLater()
    except:
        pass
    finally:
        my_window = TranscodeWindow()
        my_window.show()
