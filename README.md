PythonRamanSpec
===============

Simple script to analyze Raman spectra with Python to find peaks and print the output in LaTeX. 

[![ video](http://img.youtube.com/vi/ffxzzj47Op4/0.jpg)](https://www.youtube.com/watch?v=ffxzzj47Op4)

In this video is shown an example analyzing a cicloexane Raman spectrum with a pre-built filter to extract infos (e.g. integration time, laserwavelength etc. etc.) from the spectrum file and report them directly into the LaTeX caption.
You can make your own filter to analyze quickly the spectra coming from your spectrometer. 

Make sure you put in your latex document these packages, check that you have installed them:

```latex
\usepackage{tikz}
\usepackage{pgfplots}
```

The .csv file must be in the same folder of your LaTeX document. The advantage of these method compared to matplotlib2tikz for example is that you don't have all your data inside your .tex file. 
