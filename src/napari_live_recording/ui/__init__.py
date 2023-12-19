from napari.viewer import Viewer
from qtpy.QtCore import QTimer, Qt
from qtpy.QtWidgets import (
    QTabWidget,
    QWidget,
    QScrollArea,
    QVBoxLayout,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
)
from typing import Dict
from superqt import QCollapsible
from napari_live_recording.common import (
    THIRTY_FPS,
    WriterInfo,
    Settings,
)
from napari_live_recording.control.devices import devicesDict, ICamera
from napari_live_recording.control.devices.interface import NumberParameter
from napari_live_recording.control import MainController
from napari_live_recording.ui.widgets import (
    QFormLayout,
    QGroupBox,
    QComboBox,
    QPushButton,
    LabeledSlider,
    ComboBox,
    CameraTab,
    RecordHandling,
    CameraSelection,
    ROIHandling,
)
import numpy as np


class ViewerAnchor:
    """Class which handles the UI elements of the plugin."""

    def __init__(
        self,
        napari_viewer: Viewer,
        mainController: MainController,
    ) -> None:
        self.viewer = napari_viewer
        self.mainController = mainController
        self.settings = Settings()
        self.filterGroupsDict = self.settings.getFilterGroupsDict()
        self.mainLayout = QVBoxLayout()
        self.selectionWidget = CameraSelection()
        self.selectionWidget.setDeviceSelectionWidget(list(devicesDict.keys()))
        self.selectionWidget.setAvailableCameras(list(devicesDict.keys()))
        self.recordingWidget = RecordHandling()
        verticalSpacer = QSpacerItem(0, 1, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.mainLayout.addWidget(self.selectionWidget.group)
        self.mainLayout.addWidget(self.recordingWidget.group)
        self.mainLayout.setAlignment(
            self.selectionWidget.group, Qt.AlignmentFlag.AlignTop
        )
        self.cameraWidgetGroups: Dict[str, CameraTab] = {}
        self.selectionWidget.newCameraRequested.connect(self.addCameraUI)
        self.recordingWidget.signals["snapRequested"].connect(self.snap)
        self.recordingWidget.signals["liveRequested"].connect(self.live)
        self.recordingWidget.signals["recordRequested"].connect(self.record)

        self.mainController.newMaxTimePoint.connect(
            self.recordingWidget.recordProgress.setMaximum
        )
        self.mainController.newTimePoint.connect(
            self.recordingWidget.recordProgress.setValue
        )
        self.recordingWidget.filterCreated.connect(self.refreshAvailableFilters)
        self.mainController.recordFinished.connect(
            lambda: self.recordingWidget.record.setChecked(False)
        )
        self.mainController.cameraDeleted.connect(self.recordingWidget.live.setChecked)
        self.liveTimer = QTimer()
        self.liveTimer.timeout.connect(self._updateLiveLayers)
        self.liveTimer.setInterval(THIRTY_FPS)
        self.isFirstTab = True
        self.mainLayout.addItem(verticalSpacer)

    def addTabWidget(self, isFirstTab: bool):
        if isFirstTab:
            self.tabs = QTabWidget()
            self.mainLayout.insertWidget(self.mainLayout.count() - 1, self.tabs)
            self.isFirstTab = False
        else:
            pass

    def addCameraUI(self, interface: str, name: str, idx: int):
        self.addTabWidget(self.isFirstTab)
        camera: ICamera = devicesDict[interface](name, idx)
        cameraKey = f"{camera.name}:{camera.__class__.__name__}:{str(idx)}"
        self.filterGroupsDict = self.settings.getFilterGroupsDict()
        tab = CameraTab(camera, self.filterGroupsDict, interface)

        self.mainController.addCamera(cameraKey, camera)
        tab.deleteButton.clicked.connect(lambda: self.deleteCameraUI(cameraKey))
        self.cameraWidgetGroups[cameraKey] = tab
        self.tabs.addTab(tab.widget, cameraKey)

    def deleteCameraUI(self, cameraKey: str) -> None:
        self.mainController.deleteCamera(cameraKey)
        self.mainController.deviceControllers.pop(cameraKey)
        self.tabs.removeTab(self.tabs.currentIndex())
        if self.tabs.count() == 0:
            self.mainLayout.removeWidget(self.tabs)
            self.tabs.setParent(None)
            self.isFirstTab = True
        del self.cameraWidgetGroups[cameraKey]

    def refreshAvailableFilters(self):
        for key in self.cameraWidgetGroups.keys():
            tab = self.cameraWidgetGroups[key]
            previousIndex = tab.getFiltersComboCurrentIndex()
            self.filterGroupsDict = self.settings.getFilterGroupsDict()
            tab.setFiltersCombo(self.filterGroupsDict)
            # filterDescription = ""
            # for key in list(self.filterGroupsDict.values())[-1].keys():
            #     filterDescription += str(key)
            #     filterDescription += " "
            # indexOfLast = widget.count() - 1
            # widget.setItemData(indexOfLast, filterDescription, Qt.ToolTipRole)
            tab.setFiltersComboCurrentIndex(previousIndex)


    def record(self, status: bool) -> None:
        self.mainController.recordToBuffer(status)
        if status:
            # todo: add dynamic control
            filtersList = {}
            cameraKeys = list(self.cameraWidgetGroups.keys())

            writerInfo = WriterInfo(
                folder=self.recordingWidget.folderTextEdit.text(),
                filename=self.recordingWidget.filenameTextEdit.text(),
                fileFormat=self.recordingWidget.formatComboBox.currentEnum(),
                recordType=self.recordingWidget.recordComboBox.currentEnum(),
                stackSize=self.recordingWidget.recordSize,
                acquisitionTime=self.recordingWidget.recordSize,
            )
            writerInfoProcessed = WriterInfo(
                folder=self.recordingWidget.folderTextEdit.text(),
                filename=self.recordingWidget.filenameTextEdit.text() + "processed",
                fileFormat=self.recordingWidget.formatComboBox.currentEnum(),
                recordType=self.recordingWidget.recordComboBox.currentEnum(),
                stackSize=self.recordingWidget.recordSize,
                acquisitionTime=self.recordingWidget.recordSize,
            )

            for key in cameraKeys:
                cameraTab = self.cameraWidgetGroups[key]
                selectedFilter = cameraTab.getFiltersComboCurrentText()
                filtersList[key] = self.filterGroupsDict[selectedFilter]
            self.mainController.process(filtersList, writerInfoProcessed)
            self.mainController.record(cameraKeys, writerInfo)
            self.liveTimer.start()
        else:
            self.mainController.stopRecord()
            self.liveTimer.stop()

    def snap(self) -> None:
        for key in self.mainController.deviceControllers.keys():
            cameraTab = self.cameraWidgetGroups[key]
            selectedFilter = cameraTab.getFiltersComboCurrentText()
            functionsDict = self.filterGroupsDict[selectedFilter]
            self._updateLayer(f"Snap {key}", self.mainController.snap(key, functionsDict))

    def live(self, status: bool) -> None:
        cameraKeys = list(self.cameraWidgetGroups.keys())
        self.mainController.recordToBuffer(status)
        for key in cameraKeys:
            cameraTab = self.cameraWidgetGroups[key]
            selectedFilter = cameraTab.getFiltersComboCurrentText()
            selectedFilterGroup = self.filterGroupsDict[selectedFilter]
            self.mainController.processFrames(status,key, selectedFilterGroup)
        if status:
            self.liveTimer.start()
        else:
            self.liveTimer.stop()

    def cleanup(self) -> None:
        if (
            len(self.mainController.deviceControllers.keys()) == 0
            and len(self.cameraWidgetGroups.keys()) == 0
        ):
            # no cleanup required
            return

        # first delete the controllers...
        # if self.mainController.isLive:
        #     self.mainController.live(False)
        for key in self.mainController.deviceControllers.keys():
            self.mainController.deleteCamera(key)
        self.mainController.deviceControllers.clear()

        # ... then delete the UI tabs
        self.tabs.clear()
        self.mainLayout.removeWidget(self.tabs)
        self.tabs.setParent(None)
        self.isFirstTab = True

        self.cameraWidgetGroups.clear()

    def _updateLiveLayers(self):
        try:
            # for key, buffer in self.mainController.deviceLiveBuffer.items():
            for key in self.mainController.deviceControllers.keys():
                # this copy may not be truly necessary
                # but it does not impact performance too much
                # so we keep it to avoid possible data corruption
                self._updateLayer(
                    f"Live {key}", np.copy(self.mainController.returnNewestFrame(key))
                )
        except Exception as e:
            pass

    def _updateLayer(self, layerKey: str, data: np.ndarray) -> None:
        try:
            # layer is recreated in case the image changes type (i.e. grayscale -> RGB and viceversa)
            if data.ndim != self.viewer.layers[layerKey].data.ndim:
                self.viewer.layers.remove(layerKey)
                self.viewer.add_image(data, name=layerKey)
            else:
                self.viewer.layers[layerKey].data = data
        except KeyError:
            # needed in case the layer of that live recording does not exist
            self.viewer.add_image(data, name=layerKey)
