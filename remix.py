import json
import os
import subprocess

import boto3
import spotipy
from sklearn.neighbors import NearestNeighbors
from spotipy.oauth2 import SpotifyClientCredentials

from infiniteremixer.data.createdataset import _create_data_pipeline
from infiniteremixer.remix.generateremix import _create_objects
from infiniteremixer.segmentation.segmentextractor import SegmentExtractor
from infiniteremixer.utils.io import load_from_pickle, save_to_pickle, write_wav

# PATHS
AUDIOS_PATH = "results/audios"
SEGMENTS_PATH = "results/segmented"
DATASET_PATH = "results/dataset"
NEAREST_NEIGHBOUR_PATH = "results/model/model.pkl"

REMIX_PATH = "results/remix/remix.wav"
SAMPLE_RATE = 22050
# PARAMETERS FOR GENERATION
JUMP_RATE = 0.005
NUM_BEATS = 60
# SPOTIFY CREDENTIALS (setted based on darko api and db)
os.environ["SPOTIPY_CLIENT_ID"] = "3e97af2ef40f4abdb8804a4cf480dee2"
os.environ["SPOTIPY_CLIENT_SECRET"] = "59ac0311c2cb463bb035c67258aa4ac1"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# AWS CONFIG
boto_session = boto3.session.Session(profile_name="mfa")
sqs = boto_session.client("sqs")
# THIS WILL BE CHANGED BY CLOOUDFORMATION OUTPUT SQS URL
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/315217542954/testQueue"


def parse_spotify_url(url):
    """
    Parse the provided Spotify playlist URL and determine if it is a playlist, track or album.
    :param url: URL to be parsed
    :return tuple indicating the type and id of the item
    """
    parsed_url = url.replace("https://open.spotify.com/", "")
    item_type = parsed_url.split("/")[0]
    item_id = parsed_url.split("/")[1]
    return item_type, item_id


# ****************************************************************
# Simulate sending from api
message = json.dumps(
    {
        "playlist": "https://open.spotify.com/playlist/4ooacn2V0kwAcWkxDosuYr?si=64adb5ad66194816"
    }
)
response = sqs.send_message(
    QueueUrl=QUEUE_URL,
    MessageBody=message,
)
# ****************************************************************

# Retrieve message
response = sqs.receive_message(
    QueueUrl=QUEUE_URL,
    MaxNumberOfMessages=1,
)
# Download songs given the URL
# Delete message after processing
message = response.get("Messages")
print(message)
if message is not None:
    # Get the playlist uri
    playlist_uri = json.loads(message[0].get("Body")).get("playlist")
    print(playlist_uri)
    # Download the songs
    output = subprocess.run(
        ["spotify_dl", "-l", playlist_uri, "-o", AUDIOS_PATH],
        stdout=subprocess.PIPE,
        text=True,
    )
    print(output.returncode)

    _, item_id = parse_spotify_url(playlist_uri)
    playlist_name = sp.playlist(playlist_id=item_id, fields="name").get("name")
    # Clean the files that aren't mp3 files
    PLAYLIST_TRACKS_PATH = f"{AUDIOS_PATH}/{playlist_name}"
    not_audio_files = [
        i for i in os.listdir(PLAYLIST_TRACKS_PATH) if not i.endswith("mp3")
    ]
    for f in not_audio_files:
        output = subprocess.run(
            ["rm", f"{PLAYLIST_TRACKS_PATH}/{f}"], stdout=subprocess.PIPE, text=True
        )

    # Segment
    segment_extractor = SegmentExtractor(SAMPLE_RATE)
    segment_extractor.create_and_save_segments(
        PLAYLIST_TRACKS_PATH,
        SEGMENTS_PATH,
    )
    # Extract and aggreagate features
    data_pipeline = _create_data_pipeline()
    data_pipeline.process(
        SEGMENTS_PATH,
        DATASET_PATH,
    )
    # Fit nearest neighbors
    dataset = load_from_pickle(f"{DATASET_PATH}/dataset.pkl")
    print(f"Loaded dataset from {DATASET_PATH}/dataset.pkl")
    print(f"Dataset array has shape {dataset.shape}")
    nearest_neighbour = NearestNeighbors()
    nearest_neighbour.fit(dataset)
    print("Created nearest neighbour")
    save_to_pickle(NEAREST_NEIGHBOUR_PATH, nearest_neighbour)
    print(f"Saved nearest neighbour model to {NEAREST_NEIGHBOUR_PATH}")
    # Generate remix
    remixer, chunk_merger = _create_objects(JUMP_RATE, NUM_BEATS)
    remix = remixer.generate_remix()
    print(f"Generated remix with {NUM_BEATS} beats")
    audio_remix = chunk_merger.concatenate(remix.file_paths)
    print(f"Merged beats together")
    write_wav(REMIX_PATH, audio_remix, SAMPLE_RATE)
    print(f"Saved new remix to {SAMPLE_RATE}")
