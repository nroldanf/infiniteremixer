#!/bin/bash
segment results/audios results/segmented
create_dataset results/segmented results/dataset
fit_nearest_neighbours results/dataset/dataset.pkl results/model/model.pkl
