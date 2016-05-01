To render site, use the script renderSite.R  
It depends on the development code of rmarkdown which can be download from github using devtools

From within in R

```r
if (!require("devtools")) install.packages("devtools")
devtools::install_github("rstudio/rmarkdown")
```

```bash
./renderSite.R
```

