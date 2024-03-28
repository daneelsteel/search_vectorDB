FROM semitechnologies/transformers-inference:custom
RUN MODEL_NAME=sentence-transformers/LaBSE ./download.py