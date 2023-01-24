import wx
from main import runApplication

# self.videoPathLb = wx.StaticText(panel, -1, 'Video path')
# my_sizer.Add(self.videoPathLb, 0, wx.ALL | wx.EXPAND, 5) 

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Report Analysis', size=(670, 300))
        panel = wx.Panel(self)

        self.video_path_tc = wx.TextCtrl(panel, size=(500, 20), pos = (10, 10))   
            
        self.list = wx.ListCtrl(panel, -1, style = wx.LC_REPORT, size = (500,200), pos = (10, 40)) 
        self.list.InsertColumn(0, 'Khu vực', wx.LIST_FORMAT_CENTER, width = 80,) 
        self.list.InsertColumn(1, 'Thời gian', wx.LIST_FORMAT_CENTER, 80) 
        self.list.InsertColumn(2, 'Trung bình người', wx.LIST_FORMAT_CENTER, 140)
        self.list.InsertColumn(3, 'Tổng frame', wx.LIST_FORMAT_CENTER, 100)
        self.list.InsertColumn(4, 'Tổng người', wx.LIST_FORMAT_CENTER, 100)


        self.list.InsertItem(0, "0")
        self.list.SetItem(0, 1, "10s")
        self.list.SetItem(0, 2, "10")
        self.list.SetItem(0, 3, "100")
        self.list.SetItem(0, 4, "100")

        browser_btn = wx.Button(panel, label='Browser', pos = (520, 10), size = (120, 25))
        browser_btn.Bind(wx.EVT_BUTTON, self.on_open_browser)

        get_report_btn = wx.Button(panel, label='Get report analysis', pos = (520, 40), size = (120, 25))
        get_report_btn.Bind(wx.EVT_BUTTON, self.on_get_report_analysis)

        get_report_btn = wx.Button(panel, label='Open excel', pos = (520, 70), size = (120, 25))
        get_report_btn.Bind(wx.EVT_BUTTON, self.on_open_excel)

        self.Centre()      
        self.Show()

    def on_open_browser(self, event):
        openFileDialog = wx.FileDialog(frame, "Open", "", "", "Python files (*.mp4)|*.mp4", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()
        self.video_path_tc.SetLabel(path)
        openFileDialog.Destroy()
    
    def on_get_report_analysis(self):
        if(self.video_path_tc.GetLabel != ''):
            runApplication()
    
    def on_open_excel():
        print('open excel')


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()