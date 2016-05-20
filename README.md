<h1>Internship project</h1>
<p><strong>Supervision : </strong>Maaike de Boer</h1>
<p><strong>Location : </strong>The Machine learning department of Radboud University in Nijmegen, the Netherlands</p>
<p><strong>Author : </strong>Camille Escher</p>

<p><strong>Start date : </strong>   15/02/16</br></p>

<p><strong>Main goal : </strong>Build a model and implement a prototype to better recognize events in videos by using the temporal relations of the sub-events sequence of events. </br>
<p><strong>Progress : </strong>The graph and the inference process has been tested on the simulation data (see simulate.py for further details). The method is now able to classify events which are defined as simulated sequences of sub-events (x keyframes, y possible sub-events, one sub-event of interest per keyframe). The graph can classify n classes. Need to evaluate the complexity and to test the method on the VIRAT 2.0 dataset.</br></p>

<p><strong>Files : </strong>
<ul>
<li>The entry point of the program is 'main.py'</li>
<li>The simulation of the data is processed by 'simulateMultiClasses.py' ('simulate.py' only generate particular sequences (2 seq) of 3 keyframes and an alphabet of 5 sub-events.</li>
<li>The graph structure is implemented in 'Graph.py'.</li>
<li>The building of the graph is coded in 'graphBuilder.py'</li>
<li>The method is compared to a basic linear SVM method see 'SVM.py' : the implementation has been checked for 2 classes : update needed for multi-classes</li>
<li>The calculation of the confusion matrix and the MAP - Mean Average Precision are implemented in 'evaluation.py'</li>
</ul>

<strong>Tools and language : </strong>
<ul>
<li>Ubuntu 15.04 (OS) </li>
<li>Python 2.7.9 (Language)</li>
<li>Pdb (Debugger)</li>
<li>VIM (Editor)</li>
<li>Scikit-learn (Library)</li>
<li>NumPy 1.8.2 (Package)</li>
<li>dot - Graphviz version 2.38.0 (Package)</li>
</ul>
