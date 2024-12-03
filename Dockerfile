FROM rocker/rstudio

RUN apt update -y && apt install -y python3 python3-pip
RUN pip3 install pandas numpy scipy matplotlib
RUN pip3 install pyreadr scikit-learn seaborn

RUN apt-get update -y && apt-get install -y \
    texlive-base \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    lmodern \
    && apt-get clean
# RUN tlmgr init-usertree
# RUN tlmgr update --self
# RUN tlmgr install pdftexcmd

WORKDIR /workspace

