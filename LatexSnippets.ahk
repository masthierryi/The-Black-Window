; LATEX ----------------------
; iff you write "item]]" the AHK will substitute this for the send, "...", so you can change the name between ":*:"..."::" to change the command, or the one between "::Send,"..."return" to change the print

:*:item]]::
Send, \begin{{}itemize{}}`n{TAB}\item ...`n\item ...`n+{TAB}\end{{}itemize{}}`n
return

:*:item]]::
Send, {Raw}\begin{{}itemize{}}`n{Tab}\item ...`n\item ...`n+{Tab}\end{{}itemize{}}`n
return

:*:code]]::
Send, \lstinputlisting[language = ]{{}file{}}`n
return

:*:img]]::
Send, \begin{{}figure{}}[H]`n{TAB}\centering`n\includegraphics[scale= ... ]{{}file.extension{}}`n\caption{{} ... {}}`n\label{{} ... {}}`n+{TAB}\end{{}figure{}}`n
return

:*:2img]]::
Send, \begin{{}figure{}}[H] `%two images aside`n{TAB}\centering\noindent`n\subcaptionbox{{}\label{{} ... {}}{}}`n{TAB}{{}\includegraphics[scale= ... ]{{} ... {}}{}}`n+{TAB}\subcaptionbox{{}\label{{} ... {}}{}}`n{TAB}{{}\includegraphics[scale= ... ]{{} ... {}}{}}`n+{TAB}\caption{{}Two animals{}}\label{{} ... {}}`n\label{{} ... {}}`n+{TAB}\end{{}figure{}}`n
return

:*:mpimg]]::
Send, \begin{{}figure{}}[H] `%minipage`n{TAB}\begin{{}minipage{}}[b]{{}0.49\textwidth{}}`n\centering`n{TAB}\includegraphics[width= ... ]{{} ... {}}`n+{TAB}\end{{}minipage{}}`n+{TAB}\hfill`n{TAB}\begin{{}minipage{}}[b]{{}0.49\textwidth{}}`n\centering`n{TAB}\includegraphics[width= ... ]{{} ... {}}`n+{TAB}\end{{}minipage{}}`n+{TAB}\caption{{}\textbf{{} ... {}}{}}`n\label{{} ... {}}`n\end{{}figure{}}`n
return

:*:table]]::
Send, \begin{{}table{}}[H]`n\centering`n\caption{{} ... {}}\vspace{{}1pt{}}`n{TAB}\begin{{}tabular{}}{{}ccc{}}`n\hline`n{TAB}... & ... & ... \\`n... & ... & ...`n+{TAB}\end{{}tabular{}}`n+{TAB}{{}\\ \normalfont \autores{{} ... {}}{}}`n\label{{}{}}`n\end{{}table{}}`n
return

:*:minip]]::
Send, \begin{{}minipage{}}[b]{{}0.49{}}`n{TAB}...`n+{TAB}\end{{}minipage{}}`n{TAB}\hfill`n+{TAB}\begin{{}minipage{}}[b]{{}0.49{}}`n{TAB}...`n+{TAB}\end{{}minipage{}}`n
return

:*:eq]]::
Send, \begin{{}equation{}}`n{TAB}...`n\label{{}{}}`n+{TAB}\end{{}equation{}}`n
return

:*:align]]::
Send, \begin{{}align{}}`n{TAB}... & ... \nonumber \\`n... & ... \\ `%this equation has number`n... & ... \nonumber`n\label{{}{}}`n+{TAB}\end{{}align{}}`n
return

:*:book]]::
Send, @book{{}author_code,{}`n{TAB}title={{} *...{}},`nauthor={{} *... {}},`npublisher={{} *... {}},`nyear={{} *... {}},`naddress={{} *... {}},`nsubtitle={{} ... {}},`nedition={{} ... {}},`npages={{}...{}},`nnumber={{} ... {}},`nseries={{} ... {}},`nisbn={{} ... {}},`nvolume={{} ... {}},`norg-short={{} ... {}},`nurl={{} ... {}},`nurlaccessdate={{} ... {}},`nnote={{} ... {}}`n+{TAB}{}}`n
return

:*:article]]::
Send, @article{{}author_code,{}`n{TAB}title={{} *... {}},`nauthor={{} *... {}},`njournal={{} *... {}},`nyear={{} *... {}},`nvolume={{} *... {}},`nnumber={{} *... {}},`npages={{} *... {}},`nmonth={{} ... {}},`npart={{} ... {}},`nsection={{} ... {}},`nurl={{} ... {}},`nurlaccessdate={{} ... {}},`nnote={{} ... {}}`n+{TAB}{}}`n
return

:*:proceeding]]::
Send, @inproceedings{{}author_code,{}`n{TAB}title={{} *... {}},`nauthor={{} *... {}},`norganization={{} *... {}},`nconference-number={{} *... {}},`nyear={{} *... {}},`naddress={{} *... {}},`npublisher={{} ... {}},`nbooktitle={{} ... {}},`npages={{} ... {}},`nmonth={{} ... {}},`nconference-location={{} ... {}},`nconference-year={{} ... {}},`nurl={{} ... {}},`nurlaccessdate={{} ... {}},`nnote={{} ... {}}`n+{TAB}{}}`n
return

:*:date]]::
Send, {{dd-mm-yyyy}}`n
return
; ----------------------------
