To render site, use the script renderSite.R  
It depends on the development code of rmarkdown which can be download from github using devtools

From within in R

```r
if (!require("devtools")) install.packages("devtools")
devtools::install_github("rstudio/rmarkdown")
```


You will likely also need to change what the c++ compiler being used is as the c++ example Rmds assume clang++, currently there is not a great way to change this so the easier way to run a sed on the RMD to change the compiler

```bash
sed -i 's/CXX=clang++/CXX=g++-5/g' *.Rmd
``` 

From within the site directory on the command line, this will download the code for the c++ examples and then render all the .Rmd files  

```bash
./buildSite.sh
```

