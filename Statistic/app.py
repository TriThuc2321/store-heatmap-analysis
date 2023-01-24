import wx
from main import runApplication


class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Report Analysis')
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)        
        self.videoPathLb = wx.StaticText(panel, -1, 'Video path')
        my_sizer.Add(self.videoPathLb, 0, wx.ALL | wx.EXPAND, 5)        
        my_btn = wx.Button(panel, label='Press Me')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)        
        panel.SetSizer(my_sizer)        
        self.Show()

    def on_press(self, event):
        openFileDialog = wx.FileDialog(frame, "Open", "", "", "Python files (*.mp4)|*.mp4", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()
        self.videoPathLb.SetLabel(path)
        openFileDialog.Destroy()
        runApplication()
       

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()