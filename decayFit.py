# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:52:32 2013

@author: bernd
"""

import ROOT
import sys
import math 
import pathfinder

class fidfit:
    result_names = ('amplitude', 'frequency', 'tau', 'phase', 'pi', 'offset')

    def __init__(self):
        ROOT.gSystem.Load(pathfinder.libWaveWaveBase)
	self.rootfile=''
	self.data=None	

    def importfilemanually(self):
	self.rootfile=raw_input("rootfile: ")
	self.file=ROOT.TFile(self.rootfile)
	entry=int(input("channelnum: "))
	self.file.sisDec.GetEntry(entry)
	self.data=self.file.sisDec.wf.GimmeHist()

    def importfile(self):
        self.rootfileshort=raw_input("rootfile: ")
        self.rootfile=pathfinder.ROOTFileFolder+self.rootfileshort
	self.file=ROOT.TFile(self.rootfile)
        entry=int(input("channelnum: "))
        self.file.sisDec.GetEntry(entry)
        self.data=self.file.sisDec.wf.GimmeHist()

    def loadfile(self):
	if self.rootfile:
		print "this rootfile is used: "+self.rootfile
	else:
		return
	self.file=ROOT.TFile(self.rootfile)
        entry=int(input("channelnum: "))
        self.file.sisDec.GetEntry(entry)
        self.data=self.file.sisDec.wf.GimmeHist()

    def load_TWaveform(self, w):
        """Directly load TWaveform from Memory"""
        self.data = w.GimmeHist()

 #   def findparams(self):
 #       self.data.

    def manual_fit(self):
        print("enter starting values for the fit")
        offs=float(input("offset= "))
        ampl=float(input("amplitude= "))
        larmor=float(input("larmor frequency= "))
        T2=float(input("decay lifetime= "))
        fitwinstart=float(input("fitwindow starting pont: "))
        fitwinend=float(input("fitwindow ending point: "))
        raw_input("jump")
        print self.pars[0], self.pars[1], self.pars[2], self.pars[3], self.pars[4], self.pars[5]

    def fit(self, offs, ampl, larmor, T2, fitwinstart, fitwinend):
        #c2=ROOT.TCanvas()
        #self.data.Draw()
        f1=ROOT.TF1("f1", "[5]+[0]*sin(x*[1]*2*[4]+[3])*exp(-x/[2])", fitwinstart, fitwinend)
        f1.SetParNames("Initial amplitude","larmor freq", "T2","Initial Phase","Pi","offset")
        f1.SetParLimits(0,ampl-ampl/2.,ampl+ampl/2.)
        f1.SetParameter(0, ampl)
        f1.SetParLimits(1, larmor-larmor/2., larmor+larmor/2.)
        f1.SetParameter(1, larmor)
        f1.SetParLimits(2, T2-T2/2., T2+T2/2.)
        f1.SetParameter(5, offs)
        f1.SetParLimits(5,offs-offs/2., offs+offs/2.)
        f1.FixParameter(4, math.pi)
        self.data.Fit(f1,"Q,M","SAME", fitwinstart, fitwinend)
        self.pars=f1.GetParameters()
        #self.data.Draw() 
        #c2.Modified() 
        #c2.Update()
        return f1

    def fft(self):
         wf=self.file.sisDec.wf
         #wf=self.data
         fft = ROOT.TWaveformFT()
         new_wf = ROOT.TTemplWaveform('double')()
         new_wf.SetLength(wf.GetLength())
         for i in range(wf.GetLength()): new_wf[i] = wf[i]
         new_wf.SetSamplingFreq(wf.GetSamplingFreq())
 
         sub = new_wf.SubWaveform(10000, wf.GetLength())
         sub=new_wf
 
         ROOT.TFastFourierTransformFFTW.GetFFT(sub.GetLength()).PerformFFT(sub, fft)
         fft.GimmeHist("", "Abs").Draw()
         raw_input("jump")

def main():
    c=fidfit()
    c.importfile()
    c.manual_fit()
    #c.fft()
if __name__ == "__main__":
    main()
