# Infinite Remixer
Infinite Remixer is a Python application that creates remixes, patching 
together multiple songs.

## Testing
To run unittests, issue the following command from the root of the repo:

`$ pytest`

## Package structure 
The package is divided into 4 sub-packages:
- segmentation
- data
- search
- remix

*segmentation* is responsible to separate in different sources (drums and others)
and segment both into beats and store the beats as separate wav files in different
folders.

*data* can be used to batch extract audio features from a directory containing 
audio files, aggregate the features, and storing the data ready to be 
consumed by *search*.

*search* contains facilities to fit a scikit-learn NearestNeighbour object, 
and a wrapper class around this object to apply nearest neighbour search.

*remix* is responsible for generating new remixes.


## How to generate a remix
To generate a remix, there are two main high-level steps to carry out. 
First, preprocess a group of songs you want to remix. Second, 
generate a remix, which will leverage the preprocessed data.

### Preprocessing
To preprocess data follow these steps:

1- Separate a group of tracks into 2 different sources (drums and other).
2- Segment a group of tracks into beats
3- Extract features and prepare data from the beats
4- Fit a Nearest Neighbour object

To run the steps above, use the entry points below. You can find more info 
on the entry points, in the respective modules.

`$ separate path/to/dir/with/files path/to/save/dir/for/splitted`

`$ segment path/to/save/dir/for/splitted path/to/save/dir/for/beats`

`$ create_dataset path/to/dir/with/audio/files save/dir`

`$ fit_nearest_neighbours dataset/path save/path`


### Remixing
Once you have gone through the preprocessing steps, you're ready to create 
remixes with the command below:

`$ generate_remix 0.1 50 save/path/example.wav`

The first positional argument is the *jump rate*. It's a value between 0 
and 1, which indicates how frequently the system should jump from one song 
to another. The greater the value the higher the chance to jump to a new track.

The second positional argument indicates the number of beats in the remix.

In order to load the necessary artifacts for running the remix, you'll have 
to change the paths to your artifacts directly in the top part of the 
`remix/generateremix.py` script.

## Set-up

### poetry

Install poetry. Poetry is a package management depency tool for Python. Poetry allow you to separate your development dependencies so they are not package inside your production environment.

### pre-commit and git

This project uses pre-commit hooks for code standardization and styling, among other tasks such as checking for heavy files, key pairs, credential files, etc.

To make a new commit, run git inside poetry environment:

```bash
poetry shell
```

Then:

```bash
SKIP=mypy git commit -m "message" 
```

### Docker image

To build a docker image for development testing inside your local machine pass the value __dev__ to building argument named __SOFTWARE_ENV__ to the docker build command with --build-arg flag as follows:

```bash
docker build --build-arg SOFTWARE_ENV=dev -t image_name .
```

To build a docker for prodution environment use __prod__ value instead.

```bash
docker build --build-arg SOFTWARE_ENV=prod -t image_name .
```

To run a docker container on interactive mode based on this image:

```bash
docker run --rm -it -v $(pwd):/app ~/.aws:/root/.aws image_name bash
```

### ECR (Elastic container registry)

In order to push a docker image into an existent ECR registry, follow the next steps.

Login to ECR registry using profile credentials inside your local machine.

```bash
aws --profile mfa ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ecr_registry_uri
```

Then follow this guide from AWS documentation: https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html
