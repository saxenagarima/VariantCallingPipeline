#!/usr/bin/env python
from multiprocessing import Process
from Tkinter import *
from datetime import datetime
from functools import partial
from collections import defaultdict
from tkFileDialog import askopenfilename
from PIL import ImageTk, Image
import Tkinter as tk
import ttk as ttk
import tkFileDialog, tkMessageBox
import tkFileDialog as filedialog
import os,sys
from Tkinter import Frame, Tk, BOTH, Text, Menu, END
import tkFont, re, fileinput, json, ntpath, time, webbrowser, Queue
import os.path

class Intf:
	def __init__(self, root):
		self.master=root
		self.master.title("Variant Calling Pipeline")
		self.parfold=os.getcwd()
		self.x0, self.y0 = 10, 95
		x0, y0, ry, rx =10,65,0.15,0.01 
		self.inwin=self.master
		self.mybuttons=[0]*5
		buttonlab=["Upload reads","Upload Reference"]
		version_info=Text(root)
		version_info.place(x=400, y=5,height=50, width=210)
		version_info.insert(END, "Variant Calling Pipeline"+"\n"+"\n"+"Developed by:Garima Saxena")
		version_info.configure(state='disabled', bg=root["bg"])
		mybgcolor=[""]
		mycomms=[self.load_file,self.ref_file,self.tri,self.view]

		for i in range (len(buttonlab)):
			self.mybuttons[i]= Button(self.inwin, text=buttonlab[i], command=mycomms[i])
			self.mybuttons[i].place(x=x0, y=y0, height=25, width=125)
			y0+=35

		self.trimview()
		self.multi()
		self.vcparam()
		self.varcaller()

		self.mybuttons[3]=Button(self.inwin, text="Start", bg="yellow green", command=self.tri, width=10)
		self.mybuttons[3].place(x=10,y=500,height=40, width=100)
		#self.mybuttons[4]=Button(self.inwin, text="View", bg="peachpuff", command=self.view, width=10)
		#self.mybuttons[4].place(x=120,y=500,height=40, width=100)
		x0, y0 =70, 65
		self.filename=Entry(self.inwin)
		self.filename.place(x=x0+75,y=y0,height=25, width=470)
		self.reffilename=Entry(self.inwin)
		self.reffilename.place(x=x0+75,y=y0+35,height=25, width=470)
	
	def trimview(self):
		lf = ttk.Labelframe(self.inwin, text='Trimmomatic')
		lf.place(x=self.x0,y=self.y0+40,height=125, width=200)
		self.intvar=IntVar(value=1)
		self.trimcheckbox=Checkbutton(lf, text="Trim", variable = self.intvar)
		self.trimcheckbox.place(x=1, y=3, height=20, width=50 )
		trimlabels=["Min. read length", "Leading", "Trailing"]
		yte,ytl=20,25
		self.trimentry=[0]*3
		trimparam=[40,10,10]
		for i in range(len(trimparam)):
			tlabel=Label(lf, text=trimlabels[i])
			tlabel.place(x=5, y=ytl)
			self.trimentry[i]=Entry(lf)
			self.trimentry[i].place(x=140, y=yte, height=25, width=50)
			self.trimentry[i].insert(END, trimparam[i])
			yte+=30
			ytl+=30	
	
	def multi(self):
		multi = ttk.Labelframe(self.inwin, text='Multiprocess')
		multi.place(x=self.x0+200, y=self.y0+40,height=125, width=200)
		self.Threadlabel=Label(multi, text="Num. of Threads ")
		self.Threadlabel.place(x=15, y=40)
		self.T_entry=Entry(multi)
		self.T_entry.place(x=135, y=40, height=25, width=50)
		self.T_entry.insert(END, '8')	
	
	def vcparam(self):
		self.variant = ttk.Labelframe(self.inwin, text='VariantCaller Parameters')
		self.variant.place(x=self.x0+400, y=self.y0+40,height=125, width=200)
		varlabels=["Sensitivity", "Min. coverage", "Min. base quality", "Min. map. quality"]
		yte,ytl=5,10
		self.varentry=[0]*4
		self.varparam=[5,100,10,10]
		for i in range(len(self.varparam)):
			vlabel=Label(self.variant, text=varlabels[i])
			vlabel.place(x=5, y=ytl)
			self.varentry[i]=Entry(self.variant)
			self.varentry[i].place(x=140, y=yte, height=25, width=50)
			self.varentry[i].insert(END, self.varparam[i])
			yte+=25
			ytl+=25
	
	def varcaller(self):
		self.vc = ttk.Labelframe(self.inwin, text='Variant Caller')
		self.vc.place(x=self.x0, y=self.y0+215,height=150, width=600)
		vlabel=["Aligner"]
		valv=["bwa mem"]
		aligner,self.vstr,vref=[0]*2,[0]*2,[0]*2
		xvl,xrl=5,70
		for i in range(len(valv)):
			aligner[i]=Label(self.vc, text=vlabel[i])
			aligner[i].place(x=xvl, y=10)
			self.vstr[i] = StringVar(self.vc)
			self.vstr[i].set(valv[i]) # default value
			vref[i] = OptionMenu(self.vc, self.vstr[i], valv[i])
			vref[i].place(x=xrl,y=5)
			xvl+=190
			xrl+=195

		self.sam=Label(self.vc, text="Samtools")
		self.sam.place(x=5, y=70)
		
		self.sam_entry=Text(self.vc)
		self.sam_entry.place(x=70, y=55, height=50, width=450)
		self.sam_entry.insert(END,'samtools mpileup -uBg --max-depth 100000 --min-MQ minMappingQuality --min-BQ minBaseQuality -f RefGenome $1.sorted.bam|bcftools call --ploidy 1 --skip-variants indels --multiallelic-caller > $1_caller.vcf')
		self.sam_entry.configure(state='disabled', wrap='word')
	
	
	def view(self):
		self.viewfold=self.folder_selected
		self.login()
	
	def load_file(self):
		self.fileselected = filedialog.askopenfilename(filetypes =(("Fastq", "*.fastq"),("All Files","*.*")))
		self.filename.delete(0,END)
		self.filename.insert(0,self.fileselected)
		if self.fileselected:
			print "Input File:",self.fileselected
			self.folder_selected = "/".join(self.fileselected.split('/')[:-1])
			self.outfolname=self.folder_selected.split('/')[-1]
			self.dirpath=self.folder_selected
		else:
			print "Please select a folder containing fastq files"

	def ref_file(self):
		self.reference = filedialog.askopenfilename(filetypes =(("Fasta", "*.fasta"),("All Files","*.*")))
		self.reffilename.delete(0,END)
		self.reffilename.insert(0,self.reference)
		if self.reference:
			print "Reference File:",self.reference
		else:
			print "Please select a folder containing fasta files"

	def tri(self):
		start_time_all = time.time()
		self.dat=datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
		dat=datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
		self.trim(self.fileselected,self.fileselected.split("/")[-1])
		print("---Completed %s seconds ---" % (int(time.time() - start_time_all)))	

	def trim(self, name, fastqname):
		self.fname=name
		if (self.intvar.get()==1):
			newfilename=self.fname+".trimmo"
			cmd = "trimmomatic SE -quiet %s %s LEADING:%s TRAILING:%s MINLEN:%s" %(self.fname, newfilename,self.trimentry[1].get(),self.trimentry[2].get(),self.trimentry[0].get())
			os.system(cmd)	
	
		else:
			newfilename=self.fname

		cmd = "bash mysam.sh %s %s %s %s %s %s %s" %(newfilename,self.reference,self.T_entry,self.varparam[0],self.varparam[1],self.varparam[2],self.varparam[3])
		os.system(cmd)
		self.newfilename = newfilename
			
		print "\n\nAnalysis Complete\n\n"
		self.output()
		
	def output(self):
		self.win = tk.Toplevel()
		self.win.wm_title("Results")
		self.win.geometry("580x580")
		self.finout=self.win	
		self.outfile=Label(self.finout, text="Sample")
		self.outfile.place(relx=0.01, rely=0.075)
		self.outshow(self.fileselected)

	def outshow(self, outfile):
		def treeview_sort_column(tv, col, reverse):	##tv=self.tree, col="Select", reverse=True
			l =[(float(tv.set(k, col)), k) for k in tv.get_children('')]				
			l.sort(reverse=reverse)
			for index, (val, k) in enumerate(l):
				tv.move(k, '', index)
			tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

		def makevartree (ext,xvar,yvar,nam):
			ssvarcol=("Ref","Alt","Ref. Freq.", "Alt Freq.", "%Variant")
			f1=open(ext, 'r')
			self.vartree = ttk.Treeview(self.finout, columns=ssvarcol)
			self.vartree.heading("#0", text="Pos")
			self.vartree.column("#0", width=50)
			for col in ["Ref","Alt","Ref. Freq.", "Alt Freq.", "%Variant"]:
				self.vartree.heading(col, text="Percent", command=lambda: treeview_sort_column(self.vartree, col, False))

			for col in ssvarcol:
				self.vartree.column(col, width=45, anchor=tk.CENTER)
				self.vartree.heading(col, text=col)
			f1=open(ext, 'r')
			j=0
			for line in f1:
				line=line.strip()
				varposssvar=line.split('\t')
				try:
					varposssvar[-1]=("%.2f" %float(varposssvar[-1]))
				except:
					pass
				try:
					varpc=("%.2f" %float(varposssvar[6]))
				except:
					varpc=varposssvar[6]
				self.vartree.insert("", str(j), "vardir"+str(j), text=varposssvar[1], values=(varposssvar[2],varposssvar[3],varposssvar[4], varposssvar[5],varpc))
				j+=1

			self.vartree.place(relx=xvar,rely=yvar, relheight=0.9, relwidth=0.9)
	    		ext = ttk.Scrollbar(self.finout,orient="vertical",command=self.vartree.yview)
			ext.place(relx=xvar+0.9, rely=yvar, relheight=0.9)


		makevartree(self.newfilename+".variants.vcf.tsv", 0.01, 0.01, "16s Variants")
		myfont = tkFont.Font(font='TkDefaultFont')
		helv36 = tkFont.Font(family=myfont, size=12)
		igvbutton=Button(self.finout, text="IGV", bg="DodgerBlue3", command=self.igv, width=10,font=helv36)
		igvbutton.place(relx=0.01,rely=0.92,relheight=0.05, relwidth=0.2)

	def igv(self):
		os.system("igv %s -g %s" %(self.newfilename+".sorted.bam", self.reference))

		
def main():
	os.system('cls' if os.name == 'nt' else 'clear')
	root=Tk()
	Intf(root)
	root.geometry("640x600")
	root.resizable(0,0)
	root.mainloop()

if __name__ == '__main__':
	main()  
