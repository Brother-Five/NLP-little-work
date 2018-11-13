# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 622,342 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer1.SetMinSize( wx.Size( 23,23 ) ) 
        self.Question = wx.StaticText( self, wx.ID_ANY, u"请输入您的问题：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Question.Wrap( -1 )
        self.Question.SetFont( wx.Font( 18, 75, 90, 90, False, "楷体" ) )
        
        bSizer1.Add( self.Question, 0, wx.ALL, 5 )
        
        self.InPut = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.Point( 5,5 ), wx.DefaultSize, 0 )
        self.InPut.SetFont( wx.Font( 14, 70, 90, 90, False, "宋体" ) )
        
        bSizer1.Add( self.InPut, 20, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        
        gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
        
        self.ConFirm = wx.Button( self, wx.ID_ANY, u"确认", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ConFirm.SetFont( wx.Font( 14, 75, 90, 90, False, "楷体" ) )
        
        gSizer1.Add( self.ConFirm, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
        
        self.Clear_All = wx.Button( self, wx.ID_ANY, u"清除", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Clear_All.SetFont( wx.Font( 14, 75, 90, 90, False, "楷体" ) )
        
        gSizer1.Add( self.Clear_All, 0, wx.ALL, 5 )
        
        
        bSizer1.Add( gSizer1, 1, wx.EXPAND, 5 )
        
        self.Title2 = wx.StaticText( self, wx.ID_ANY, u"回答：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Title2.Wrap( -1 )
        self.Title2.SetFont( wx.Font( 18, 75, 90, 90, False, "楷体" ) )
        
        bSizer1.Add( self.Title2, 0, wx.ALL, 5 )
        
        self.OutPut = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
        self.OutPut.SetFont( wx.Font( 14, 70, 90, 90, False, "宋体" ) )
        
        bSizer1.Add( self.OutPut, 20, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.ConFirm.Bind( wx.EVT_BUTTON, self.Main_button_click )
        self.Clear_All.Bind( wx.EVT_BUTTON, self.ClearAll )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def Main_button_click( self, event ):
        event.Skip()
    
    def ClearAll( self, event ):
        event.Skip()
    

